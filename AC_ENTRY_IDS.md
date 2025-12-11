# AC Unit Entry ID Mapping

This document maps the Home Assistant config entry IDs to the AC unit names.

## AC Units

1. **AC Bedroom**
   - Config Entry ID: `01KC6PK6RDZ7E3GW17F0CS7N1Z`
   - Entity ID: (To be determined - check Developer Tools → States)

2. **AC Liam**
   - Config Entry ID: `01KC6PKXZENJJG8D7CPKF1H8B1`
   - Entity ID: (To be determined - check Developer Tools → States)

3. **AC Living Room**
   - Config Entry ID: `01KC6PJ0C34408GW7MDY65T0VX`
   - Entity ID: (To be determined - check Developer Tools → States)

## Finding Entity IDs

To find the actual entity IDs for these AC units:

1. Go to **Settings → Devices & Services**
2. Find each Midea AC LAN integration entry
3. Click on the entry to see the device details
4. The entity IDs will be listed under the device (typically `climate.*` entities)

Alternatively:
1. Go to **Developer Tools → States**
2. Search for entities starting with `climate.`
3. Look for entities related to Midea AC units

## Previous Device Information

The original device information (for reference):
- AC B64E: IP 192.168.68.37, Device ID 152832116922715
- AC C400: IP 192.168.68.19, Device ID 153931628549890
- AC 2332: IP 192.168.68.165, Device ID 153931628549884
