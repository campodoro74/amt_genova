# Air Conditioner Setup Guide

## Device Information

You have 3 Midea/M-Smart air conditioning units:

1. **AC B64E**
   - IP: 192.168.68.37
   - Port: 6444
   - ID: 152832116922715
   - Serial: 000000P0000000Q1B07839CEB64E0000
   - Key: `2007fc6f36d24f81aa8aae70e3717446a9b43b0253314fedb0c379ebce4f905c`
   - Token: `0e86b416c7d1928a9e6bca125d56f046d88e152191acb80ff44c9dce3c8749048d1754d99c7d693ecbf206f9381b6229cfb88d4044dbb20602a18556efe51a4f`

2. **AC C400**
   - IP: 192.168.68.19
   - Port: 6444
   - ID: 153931628549890
   - Serial: 000000P0000000Q1B07839D2C4000000
   - Key: `aaee6a8cc2024716ba34ffb5cd2b3619a5dd1aebe4c54b3d9be42ed49fb5743a`
   - Token: `6c0245bc8bbe24511a321c999bd657990999a6562ff3ab14cc80e14e623e33fa283e6c6b3cb4618701ab8f2b59c24597edea499da7b9f76f077753f0b6e7a6e0`

3. **AC 2332**
   - IP: 192.168.68.165
   - Port: 6444
   - ID: 153931628549884
   - Serial: 000000P0000000Q1B07839CF23320000
   - Key: `11ba77e17e244ce8b4b112d72ebfcf31cbf32db6a53f44959f6e96c2f1f5fb41`
   - Token: `f0d0b4a06a9481a0ec300f4a5b265862592e4b78d674d7320a96d481f2736871cf54f1f57744f16365f6997ec50f53624e51bcc7d57794c1d20c878ece6f7a04`

## Integration Options

### Option 1: Midea AC Integration (Recommended)

1. **Install via HACS:**
   - Go to HACS → Integrations
   - Search for "Midea AC" or "midea_ac"
   - Install the integration
   - Restart Home Assistant

2. **Configure via UI:**
   - Go to Settings → Devices & Services → Add Integration
   - Search for "Midea AC"
   - Enter device information for each unit

3. **Or configure via YAML** (if supported):
   ```yaml
   midea_ac:
     - host: 192.168.68.37
       id: 152832116922715
       token: 0e86b416c7d1928a9e6bca125d56f046d88e152191acb80ff44c9dce3c8749048d1754d99c7d693ecbf206f9381b6229cfb88d4044dbb20602a18556efe51a4f
       key: 2007fc6f36d24f81aa8aae70e3717446a9b43b0253314fedb0c379ebce4f905c
     - host: 192.168.68.19
       id: 153931628549890
       token: 6c0245bc8bbe24511a321c999bd657990999a6562ff3ab14cc80e14e623e33fa283e6c6b3cb4618701ab8f2b59c24597edea499da7b9f76f077753f0b6e7a6e0
       key: aaee6a8cc2024716ba34ffb5cd2b3619a5dd1aebe4c54b3d9be42ed49fb5743a
     - host: 192.168.68.165
       id: 153931628549884
       token: f0d0b4a06a9481a0ec300f4a5b265862592e4b78d674d7320a96d481f2736871cf54f1f57744f16365f6997ec50f53624e51bcc7d57794c1d20c878ece6f7a04
       key: 11ba77e17e244ce8b4b112d72ebfcf31cbf32db6a53f44959f6e96c2f1f5fb41
   ```

### Option 2: M-Smart Integration

If there's a specific M-Smart integration:
1. Check HACS for "M-Smart" or "msmart" integration
2. Follow the integration's setup instructions
3. Use the provided tokens and keys

### Option 3: Generic Climate Integration

If no specific integration exists, you might need to:
1. Use a generic climate integration that supports local control
2. Or create a custom integration using the msmart library

## Dashboard Setup

1. **After integration is complete:**
   - Check the entity IDs created in Home Assistant
   - They might be named like:
     - `climate.net_ac_b64e` or `climate.net_ac_B64E`
     - `climate.net_ac_c400` or `climate.net_ac_C400`
     - `climate.net_ac_2332` or `climate.net_ac_2332`

2. **Update the dashboard:**
   - Open `air-conditioner-dashboard.yaml`
   - Replace entity IDs if they differ from expected names
   - Search and replace all instances of the entity IDs

3. **Add dashboard to Home Assistant:**
   - Go to Settings → Dashboards
   - Click "Add Dashboard" → "New Dashboard"
   - Choose "YAML" mode
   - Copy the contents of `air-conditioner-dashboard.yaml`
   - Or use the MCP server to apply it directly

## Dashboard Features

The dashboard includes:

✅ **Individual Controls for Each Unit:**
   - Thermostat card with temperature control
   - Current status display (mode, temperature, fan speed)
   - Quick mode buttons (Off, Cool, Heat, Auto)
   - Quick temperature buttons (18°C, 20°C, 22°C, 24°C, 26°C)

✅ **Master Controls:**
   - Control all 3 units simultaneously
   - Set all to same mode (Off, Cool, Heat, Auto)
   - Set all to same temperature (20°C, 22°C, 24°C, 26°C)

✅ **Status Overview:**
   - Quick status card showing all 3 units at a glance

## Troubleshooting

1. **Entities not found:**
   - Check that the integration is properly installed
   - Verify entity IDs in Developer Tools → States
   - Update dashboard YAML with correct entity IDs

2. **Devices not responding:**
   - Verify IP addresses are correct and devices are online
   - Check network connectivity
   - Ensure tokens and keys are still valid

3. **Dashboard not loading:**
   - Check YAML syntax for errors
   - Verify all entity IDs exist
   - Check Home Assistant logs for errors

## Next Steps

1. Install the appropriate integration for your AC units
2. Verify the entity IDs created
3. Update `air-conditioner-dashboard.yaml` with correct entity IDs
4. Apply the dashboard to Home Assistant
5. Test all controls to ensure they work properly

