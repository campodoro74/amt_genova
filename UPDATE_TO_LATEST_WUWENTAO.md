# Update to Latest wuwentao/midea_ac_lan

## Current Situation

You have an **old version** of wuwentao's integration:
- Current version: `1.0.0` (very old)
- Latest version: `v0.6.10` (Sep 30, 2025)
- Your manifest already points to: `https://github.com/wuwentao/midea_ac_lan` ✅

## Why Update?

1. **Bug fixes**: Many fixes since v1.0.0
2. **New features**: Extra sensors, switches, better device support
3. **Midea API changes**: Handles recent Midea API closures
4. **Python 3.13 compatibility**: Works with newer Python versions
5. **Better error handling**: Improved stability

## Quick Update Steps

### Option 1: Via HACS (Easiest)

1. **Go to HACS → Integrations**
2. **Search for "Midea AC LAN"**
3. If it shows an **Update** button, click it
4. If not found, add as custom repository:
   - Repository URL: `https://github.com/wuwentao/midea_ac_lan`
   - Category: **Integration**
   - Then install/update
5. **Restart Home Assistant**

### Option 2: Install Script (Fast)

Run in HA Terminal or SSH add-on:
```bash
wget -O - https://github.com/wuwentao/midea_ac_lan/raw/master/scripts/install.sh | ARCHIVE_TAG=latest bash -
```

Then **restart Home Assistant**.

### Option 3: Manual Update

1. **Backup current integration** (optional but recommended):
   ```bash
   cp -r /config/custom_components/midea_ac_lan /config/custom_components/midea_ac_lan_backup
   ```

2. **Download latest release**:
   - Go to: https://github.com/wuwentao/midea_ac_lan/releases
   - Download `midea_ac_lan.zip` from latest release (v0.6.10)

3. **Replace files**:
   - Extract the ZIP
   - Copy `custom_components/midea_ac_lan/` to `/config/custom_components/`
   - Overwrite existing files

4. **Restart Home Assistant**

## After Update

1. **Check your devices still work**:
   - Go to **Settings → Devices & Services → Midea AC LAN**
   - Verify all 3 AC units are still there
   - Check entity IDs haven't changed

2. **If devices are missing**:
   - Go to **Settings → Devices & Services → Midea AC LAN → Devices**
   - Click **CONFIGURE** on each device
   - Enable the device if it's disabled

3. **Update dashboard** (if entity IDs changed):
   - Check **Developer Tools → States** for new entity IDs
   - Update `air-conditioner-dashboard.yaml` if needed

## Important Notes

⚠️ **Midea API Changes**: 
- Midea is closing token APIs gradually
- For v3 devices, **backup your device `.json` config files** (see integration docs)
- Your existing devices should continue working even after API closures

⚠️ **HA Version Requirement**: 
- Requires Home Assistant **2023.8 or higher**
- Check your HA version before updating

## Your Current Devices

These should continue working after update:
- **AC Bedroom** (Entry ID: `01KC6PK6RDZ7E3GW17F0CS7N1Z`)
- **AC Liam** (Entry ID: `01KC6PKXZENJJG8D7CPKF1H8B1`)
- **AC Living Room** (Entry ID: `01KC6PJ0C34408GW7MDY65T0VX`)

## Troubleshooting

- **Devices not showing**: Go to device configuration and enable them
- **Entity IDs changed**: Check Developer Tools → States for new IDs
- **Integration errors**: Check Home Assistant logs for specific errors
- **Can't add new devices**: Midea token APIs may be closed; use manual config with `msmart-ng discover` output
