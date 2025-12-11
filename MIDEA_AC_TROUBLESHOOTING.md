# Midea AC Integration Troubleshooting

## The Problem

You previously used **"Midea Smart AC" by mill1000** (which uses `msmart-ng`) and it worked. Now you have the **"Midea AC LAN" by wuwentao** integration (which uses old `msmart`) and it's not working.

## Recommended Solution

**Switch to [georgezhao2010/midea_ac_lan](https://github.com/georgezhao2010/midea_ac_lan)** - This is the most popular and well-maintained Midea integration with:
- Auto-discovery
- Better features
- Active maintenance
- See `SWITCH_TO_GEORGEZHAO_INTEGRATION.md` for detailed steps

## Why It Stopped Working

1. **Python 3.13 Compatibility**: The old `msmart` library has recursion errors with Python 3.13
2. **Token Expiration**: Midea tokens can expire after a few months
3. **Library Issues**: The old `msmart` library is no longer maintained

## Solution: Switch Back to mill1000's Fork

The mill1000 fork uses `msmart-ng` which:
- ✅ Works with Python 3.13
- ✅ Has better error handling
- ✅ Supports region selection for V3 auth
- ✅ Is actively maintained

## Steps to Fix

### Option 1: Use mill1000's "Midea Smart AC" (Recommended)

1. **Remove the current integration:**
   - Go to **Settings → Devices & Services**
   - Find all "Midea AC LAN" entries
   - Click on each → **Delete** (this removes the config entries)

2. **Remove the old custom component:**
   - SSH into Home Assistant or access the file system
   - Delete `/config/custom_components/midea_ac_lan/`

3. **Install mill1000's integration via HACS:**
   - Go to **HACS → Integrations**
   - Search for **"Midea Smart AC"** by **mill1000**
   - Install it
   - Restart Home Assistant

4. **Re-discover devices:**
   - Go to **Settings → Devices & Services → Add Integration**
   - Search for **"Midea Smart AC"**
   - Click **"Discover devices"**
   - If V3 auth fails, select **"Italy"** or a nearby country in the region dialog

5. **If discovery doesn't work, add manually:**
   - Use the output from `msmart-ng discover` (see below)
   - Enter: IP, Device ID, Port (6444)
   - The integration will handle token/key automatically

### Option 2: Update Current Integration to Use msmart-ng

If you want to keep the current integration structure, you need to:
1. Update `manifest.json` to require `msmart-ng` instead of `msmart`
2. Update the code to use `msmart-ng` imports
3. This is more complex and not recommended

## Getting Fresh Device Info

Run this to get current device information:

```bash
python3 -m venv ~/.venvs/midea && source ~/.venvs/midea/bin/activate && pip uninstall -y msmart && pip install --upgrade pip && pip install msmart-ng
msmart-ng discover
```

This will output the current IP, Device ID, token, and key for each device.

## Security Note

⚠️ **IMPORTANT**: The tokens/keys in your config files are real credentials. If you've shared these files or they're in a public repository, you should:
1. Rotate your Midea app password
2. Generate new tokens using `msmart-ng discover`
3. Update all integrations with new credentials

## Current Device Info (from your discovery)

Based on your previous discovery:

1. **AC Bedroom** (was B64E)
   - IP: `192.168.68.37`
   - Device ID: `152832116922715`
   - Port: `6444`
   - Entry ID: `01KC6PK6RDZ7E3GW17F0CS7N1Z`

2. **AC Liam** (was C400)
   - IP: `192.168.68.19`
   - Device ID: `153931628549890`
   - Port: `6444`
   - Entry ID: `01KC6PKXZENJJG8D7CPKF1H8B1`

3. **AC Living Room** (was 2332)
   - IP: `192.168.68.165`
   - Device ID: `153931628549884`
   - Port: `6444`
   - Entry ID: `01KC6PJ0C34408GW7MDY65T0VX`

**Note**: Tokens and keys may have expired. Re-run `msmart-ng discover` to get fresh credentials.

## Network Troubleshooting

If discovery fails:
- Ensure UDP broadcast is allowed on your network
- Temporarily disable VLAN rules if using Proxmox/OPNsense
- Port 6444 TCP must be open for device communication
- Ensure devices are online and reachable

## After Re-installation

Once the mill1000 integration is working:
1. Check the entity IDs created (they'll be different from the old ones)
2. Update the dashboard (`air-conditioner-dashboard.yaml`) with the new entity IDs
3. The entity IDs will likely be something like:
   - `climate.midea_smart_ac_152832116922715` (or similar)
   - Check in **Developer Tools → States** for the exact names
