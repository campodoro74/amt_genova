# Entity ID Mapping - VERIFIED AND FIXED

## Correct Mapping (Now Fixed in Dashboard)

Based on device information and entry IDs:

1. **AC Bedroom**
   - Config Entry ID: `01KC6PK6RDZ7E3GW17F0CS7N1Z`
   - Device ID: `152832116922715` (originally AC B64E)
   - Entity ID: `climate.152832116922715_climate` ✅

2. **AC Liam**
   - Config Entry ID: `01KC6PKXZENJJG8D7CPKF1H8B1`
   - Device ID: `153931628549890` (originally AC C400)
   - Entity ID: `climate.153931628549890_climate` ✅

3. **AC Living Room**
   - Config Entry ID: `01KC6PJ0C34408GW7MDY65T0VX`
   - Device ID: `153931628549884` (originally AC 2332)
   - Entity ID: `climate.153931628549884_climate` ✅

## What Was Fixed

**Bug 1 - Entity ID Mapping (FIXED):**
- ✅ AC Bedroom section now uses: `climate.152832116922715_climate`
- ✅ AC Liam section now uses: `climate.153931628549890_climate`
- ✅ AC Living Room section now uses: `climate.153931628549884_climate`
- ✅ Master Controls now include all three entity IDs correctly

## Verification

All sections in the dashboard have been updated:
- Quick Status Row: ✅ Correct entity IDs
- AC Bedroom section: ✅ All controls use `climate.152832116922715_climate`
- AC Liam section: ✅ All controls use `climate.153931628549890_climate`
- AC Living Room section: ✅ All controls use `climate.153931628549884_climate`
- Master Controls: ✅ All buttons include all three entity IDs

## Original Device Reference

For historical reference:
- AC B64E (IP 192.168.68.37) → Device ID 152832116922715 → **AC Bedroom**
- AC C400 (IP 192.168.68.19) → Device ID 153931628549890 → **AC Liam**
- AC 2332 (IP 192.168.68.165) → Device ID 153931628549884 → **AC Living Room**
