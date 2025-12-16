import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import datetime as dt
import logging
from .const import AMT_XML_URL

_LOGGER = logging.getLogger(__name__)

def fetch_stop(stop_id: str) -> dict:
    """Fetch bus arrival data for a specific stop from AMT Genova API."""
    url = f"{AMT_XML_URL}?CodiceFermata={stop_id}"
    now = dt.datetime.now()

    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            xml = r.read()
    except urllib.error.URLError as err:
        _LOGGER.warning("Failed to fetch data for stop %s: %s", stop_id, err)
        return {"next": [], "stop": stop_id, "updated": now.isoformat()}
    except Exception as err:
        _LOGGER.error("Unexpected error fetching stop %s: %s", stop_id, err)
        return {"next": [], "stop": stop_id, "updated": now.isoformat()}

    try:
        root = ET.fromstring(xml)
    except ET.ParseError as err:
        _LOGGER.error("Failed to parse XML for stop %s: %s", stop_id, err)
        return {"next": [], "stop": stop_id, "updated": now.isoformat()}

    ns = {"ns": "http://cities-avm/WebServicePrevisioni"}

    items = []
    for p in root.findall("ns:Previsione", ns):
        try:
            wait = p.findtext("ns:PrevisioneArrivo", "", ns)
            if not wait:
                continue
            wait_min = int(wait.replace("'", ""))
        except (ValueError, AttributeError) as err:
            _LOGGER.debug("Skipping invalid wait time for stop %s: %s", stop_id, err)
            continue

        items.append({
            "route": p.findtext("ns:Linea", "", ns),
            "headsign": p.findtext("ns:Destinazione", "", ns),
            "wait": wait_min,
            "time": p.findtext("ns:OraArrivo", "", ns),
            "crowded": p.findtext("ns:AutobusPieno", "false", ns) == "true",
            "source": "realtime",
            "stop": stop_id,
            "vehicle": p.findtext("ns:NumeroSociale", "", ns),
        })

    leave_warning = any(b["wait"] <= 3 for b in items)

    return {
        "stop": stop_id,
        "updated": now.strftime("%Y-%m-%d %H:%M:%S"),
        "leave_warning": leave_warning,
        "next": items,
    }

