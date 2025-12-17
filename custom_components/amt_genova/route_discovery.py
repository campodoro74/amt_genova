"""Helper script to discover stops along a route by tracking vehicles."""
import xml.etree.ElementTree as ET
import urllib.request
from .const import AMT_XML_URL


def find_stops_with_vehicle(stop_ids, target_vehicle, target_route, target_headsign):
    """Find which stops have a specific vehicle.
    
    Args:
        stop_ids: List of stop IDs to check
        target_vehicle: Vehicle number to find (e.g., "0E181")
        target_route: Route number (e.g., "513")
        target_headsign: Destination (e.g., "VIA ISONZO")
    
    Returns:
        List of stop IDs where the vehicle was found
    """
    found_stops = []
    
    for stop_id in stop_ids:
        try:
            url = f"{AMT_XML_URL}?CodiceFermata={stop_id}"
            with urllib.request.urlopen(url, timeout=5) as r:
                xml = r.read()
            
            root = ET.fromstring(xml)
            ns = {"ns": "http://cities-avm/WebServicePrevisioni"}
            
            for p in root.findall("ns:Previsione", ns):
                vehicle = p.findtext("ns:NumeroSociale", "", ns)
                route = p.findtext("ns:Linea", "", ns).rstrip("/")
                headsign = p.findtext("ns:Destinazione", "", ns)
                
                if (vehicle == target_vehicle and 
                    route == target_route and 
                    headsign == target_headsign):
                    found_stops.append(stop_id)
                    break
        except Exception:
            continue
    
    return found_stops


def discover_route_stops(target_stop, target_route, target_headsign, search_range=10):
    """Discover stops along a route by checking nearby stop IDs.
    
    Args:
        target_stop: The target stop ID (e.g., "0731")
        target_route: Route number (e.g., "513")
        target_headsign: Destination (e.g., "VIA ISONZO")
        search_range: How many stops before/after to check
    
    Returns:
        List of stop IDs in order (stops before target_stop)
    """
    # Get current vehicle at target stop
    try:
        url = f"{AMT_XML_URL}?CodiceFermata={target_stop}"
        with urllib.request.urlopen(url, timeout=5) as r:
            xml = r.read()
        
        root = ET.fromstring(xml)
        ns = {"ns": "http://cities-avm/WebServicePrevisioni"}
        
        vehicles = []
        for p in root.findall("ns:Previsione", ns):
            route = p.findtext("ns:Linea", "", ns).rstrip("/")
            headsign = p.findtext("ns:Destinazione", "", ns)
            if route == target_route and headsign == target_headsign:
                vehicles.append(p.findtext("ns:NumeroSociale", "", ns))
        
        if not vehicles:
            return []
        
        # Check nearby stops for the same vehicles
        base_num = int(target_stop)
        stop_ids_to_check = [f"{base_num - i:04d}" for i in range(1, search_range + 1)]
        
        # Find which stops have our vehicles
        all_found = {}
        for vehicle in vehicles[:3]:  # Check first 3 vehicles
            found = find_stops_with_vehicle(stop_ids_to_check, vehicle, target_route, target_headsign)
            for stop in found:
                if stop not in all_found:
                    all_found[stop] = base_num - int(stop)
        
        # Sort by distance from target (closest first)
        sorted_stops = sorted(all_found.items(), key=lambda x: x[1])
        return [stop for stop, _ in sorted_stops]
        
    except Exception as e:
        print(f"Error discovering route: {e}")
        return []

