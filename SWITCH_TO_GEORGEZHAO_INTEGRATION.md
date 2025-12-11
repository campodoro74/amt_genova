# Switch/Update to wuwentao/midea_ac_lan Integration (RECOMMENDED)

**This is the most up-to-date and actively maintained Midea integration!**

**Note**: You already have wuwentao's integration installed, but it's an old version (v1.0.0). 
See `UPDATE_TO_LATEST_WUWENTAO.md` for updating your existing installation, or follow this guide for a fresh install.

## Why Switch?

The [wuwentao/midea_ac_lan](https://github.com/wuwentao/midea_ac_lan) integration is:
- ✅ **Most recent**: Latest release Sep 30, 2025 (actively maintained)
- ✅ **Successor to georgezhao2010**: Includes upgrade path from older version
- ✅ **Auto-discovery**: Automatically finds devices on your network
- ✅ **Better features**: Extra sensors, switches, long TCP connection for real-time status
- ✅ **Actively maintained**: 869 commits, 27 releases, regular updates
- ✅ **Comprehensive**: Supports many device types (AC, Fan, Water Heater, Washer, etc.)
- ✅ **User-friendly**: Config flow UI with automatic device discovery
- ✅ **Modern requirements**: Requires HA 2023.8+ (more up-to-date)
- ⚠️ **Important**: Documents Midea API changes and token API closures

## Current Situation

You currently have:
- **Integration**: `midea_ac_lan` by wuwentao (in `/custom_components/midea_ac_lan/`)
- **Entry IDs**: 
  - AC Bedroom: `01KC6PK6RDZ7E3GW17F0CS7N1Z`
  - AC Liam: `01KC6PKXZENJJG8D7CPKF1H8B1`
  - AC Living Room: `01KC6PJ0C34408GW7MDY65T0VX`

## Steps to Switch

### Step 1: Remove Current Integration

1. **Delete integration entries in Home Assistant:**
   - Go to **Settings → Devices & Services**
   - Find all "Midea AC LAN" entries
   - Click on each → **Delete** (removes config entries but keeps devices)

2. **Remove old custom component:**
   - SSH into Home Assistant or use file editor
   - Delete `/config/custom_components/midea_ac_lan/` directory
   - Or rename it to `/config/custom_components/midea_ac_lan_backup/` for safety

### Step 2: Install georgezhao2010 Integration

**Option A: Via HACS (Recommended)**
1. Go to **HACS → Integrations**
2. Search for **"Midea AC LAN"** in HACS (it should already be available)
3. Click on it and select **Download** (or **Update** if already installed)
4. **Restart Home Assistant**

**Note**: If not found in HACS, add as custom repository:
- Repository URL: `https://github.com/wuwentao/midea_ac_lan`
- Category: **Integration**

**Option B: Install with Script**
Run this in HA Terminal or SSH add-on:
```bash
wget -O - https://github.com/wuwentao/midea_ac_lan/raw/master/scripts/install.sh | ARCHIVE_TAG=latest bash -
```

**Option C: Manual Installation**
1. Go to the [latest release](https://github.com/wuwentao/midea_ac_lan/releases)
2. Download the latest release ZIP
3. Extract and copy `custom_components/midea_ac_lan/` to your `/config/custom_components/` directory
4. **Restart Home Assistant**

### Step 3: Configure Midea Account (First Time Only)

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **"Midea AC LAN"**
3. Enter your **Midea account** (email) and **password**
   - This is needed once to retrieve tokens/keys from Midea cloud
   - After devices are configured, you can remove the account config
   - Devices will continue working locally

### Step 4: Add Your AC Devices

After account configuration, click **"ADD DEVICE"** again.

**Option A: Auto-Discovery (Recommended)**
1. Select **"Discover automatically"**
2. The integration will scan your network and list all Midea devices
3. Select your 3 AC units:
   - AC Bedroom (IP: 192.168.68.37, ID: 152832116922715)
   - AC Liam (IP: 192.168.68.19, ID: 153931628549890)
   - AC Living Room (IP: 192.168.68.165, ID: 153931628549884)
4. Click to add each one

**Option B: Manual Configuration**
If auto-discovery doesn't work, you can add manually:
1. Select **"Configure manually"**
2. Enter for each device:
   - **Appliance code**: (Device ID, e.g., `152832116922715`)
   - **Appliance type**: `AC` (Air Conditioner)
   - **IP address**: (e.g., `192.168.68.37`)
   - **Port**: `6444` (default)
   - **Protocol version**: (usually auto-detected)
   - **Token**: (from `msmart-ng discover` or auto-filled if account configured)
   - **Key**: (from `msmart-ng discover` or auto-filled if account configured)

### Step 5: Verify Entity IDs

After configuration:
1. Go to **Developer Tools → States**
2. Search for `climate.` entities
3. Look for entities like:
   - `climate.midea_ac_lan_152832116922715` (or similar)
   - The exact naming depends on how the integration creates them

### Step 6: Update Dashboard

Once you have the new entity IDs:
1. Open `air-conditioner-dashboard.yaml`
2. Replace the placeholder entity IDs with the actual ones
3. The dashboard is already configured with the correct names (Bedroom, Liam, Living Room)

## Device Information Reference

Your 3 AC units:
1. **AC Bedroom** (was B64E)
   - IP: `192.168.68.37`
   - Device ID: `152832116922715`
   - Port: `6444`

2. **AC Liam** (was C400)
   - IP: `192.168.68.19`
   - Device ID: `153931628549890`
   - Port: `6444`

3. **AC Living Room** (was 2332)
   - IP: `192.168.68.165`
   - Device ID: `153931628549884`
   - Port: `6444`

## Important Notes

1. **Static IP Addresses**: Set static IPs for your AC units in your router to prevent IP changes
2. **Network Requirements**: Auto-discovery requires devices and Home Assistant to be on the same subnet
3. **Account Security**: After devices are configured, you can remove the Midea account from the integration settings
4. **Refresh Interval**: Default is 30 seconds. You can adjust this in device configuration
5. **Extra Entities**: This integration can create additional sensor and switch entities for more control
6. **⚠️ Midea API Changes**: Midea is closing token APIs. Backup your device `.json` config files (for v3 devices) - see integration docs for details
7. **HA Version**: Requires Home Assistant 2023.8 or higher

## Troubleshooting

- **Discovery fails**: Ensure devices are on the same network/subnet as Home Assistant
- **Can't find devices**: Try manual configuration with device info from `msmart-ng discover`
- **Token errors**: Re-run `msmart-ng discover` to get fresh tokens if needed
- **Entity IDs different**: Check Developer Tools → States after configuration

## After Installation

Once everything is working:
1. Note the new entity IDs
2. Update the dashboard with correct entity IDs
3. Enjoy better integration with auto-discovery and extra features!
