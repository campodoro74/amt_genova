import xml.etree.ElementTree as ET
import urllib.request
import datetime as dt
from .const import AMT_XML_URL

def fetch_stop(stop_id: str) -> dict:
    url = f"{AMT_XML_URL}?CodiceFermata={stop_id}"
    now = dt.datetime.now()

    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            xml = r.read()
    except Exception:
        return {"next": [], "stop": stop_id, "updated": now.isoformat()}

    root = ET.fromstring(xml)
    ns = {"ns": "http://cities-avm/WebServicePrevisioni"}

    items = []
    for p in root.findall("ns:Previsione", ns):
        try:
            wait = p.findtext("ns:PrevisioneArrivo", "", ns)
            wait_min = int(wait.replace("'", ""))
        except Exception:
            continue

        vehicle = p.findtext("ns:NumeroSociale", "", ns)
        # If vehicle number exists and is not empty, it's real-time; otherwise scheduled
        source = "realtime" if vehicle and vehicle.strip() else "scheduled"

        items.append({
            "route": p.findtext("ns:Linea", "", ns),
            "headsign": p.findtext("ns:Destinazione", "", ns),
            "wait": wait_min,
            "time": p.findtext("ns:OraArrivo", "", ns),
            "crowded": p.findtext("ns:AutobusPieno", "false", ns) == "true",
            "source": source,
            "stop": stop_id,
            "vehicle": vehicle,
        })

    leave_warning = any(b["wait"] <= 3 for b in items)

    return {
        "stop": stop_id,
        "updated": now.strftime("%Y-%m-%d %H:%M:%S"),
        "leave_warning": leave_warning,
        "next": items,
    }

