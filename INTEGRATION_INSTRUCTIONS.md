# Midea AC Integration Instructions

## Quick Setup (Recommended)

Since HACS API installation isn't available, please follow these manual steps:

### Step 1: Install Midea AC LAN Integration via HACS UI

1. **Open Home Assistant UI**
2. **Go to HACS** (in the sidebar)
3. **Click "Integrations"** tab
4. **Click the three dots menu (⋮)** in the top right
5. **Select "Custom repositories"**
6. **Add Repository:**
   - Repository URL: `https://github.com/wuwentao/midea_ac_lan`
   - Category: **Integration**
   - Click **Add**
7. **Install the Integration:**
   - Search for "Midea AC LAN" in HACS
   - Click on it and select **Download**
8. **Restart Home Assistant**

### Step 2: Configure Each AC Unit

After restart, configure each device:

1. **Go to Settings → Devices & Services**
2. **Click "Add Integration"** (bottom right)
3. **Search for "Midea AC LAN"**
4. **For each AC unit, enter:**
   - **AC B64E:**
     - Host: `192.168.68.37`
     - Device ID: `152832116922715`
     - Token: `0e86b416c7d1928a9e6bca125d56f046d88e152191acb80ff44c9dce3c8749048d1754d99c7d693ecbf206f9381b6229cfb88d4044dbb20602a18556efe51a4f`
     - Key: `2007fc6f36d24f81aa8aae70e3717446a9b43b0253314fedb0c379ebce4f905c`
   
   - **AC C400:**
     - Host: `192.168.68.19`
     - Device ID: `153931628549890`
     - Token: `6c0245bc8bbe24511a321c999bd657990999a6562ff3ab14cc80e14e623e33fa283e6c6b3cb4618701ab8f2b59c24597edea499da7b9f76f077753f0b6e7a6e0`
     - Key: `aaee6a8cc2024716ba34ffb5cd2b3619a5dd1aebe4c54b3d9be42ed49fb5743a`
   
   - **AC 2332:**
     - Host: `192.168.68.165`
     - Device ID: `153931628549884`
     - Token: `f0d0b4a06a9481a0ec300f4a5b265862592e4b78d674d7320a96d481f2736871cf54f1f57744f16365f6997ec50f53624e51bcc7d57794c1d20c878ece6f7a04`
     - Key: `11ba77e17e244ce8b4b112d72ebfcf31cbf32db6a53f44959f6e96c2f1f5fb41`

### Step 3: Verify Entity IDs

After configuration, check the created entity IDs:
- Go to **Developer Tools → States**
- Search for entities starting with `climate.`
- Note the exact entity IDs for your AC units
- They might be named like:
  - `climate.midea_ac_b64e` or `climate.midea_ac_lan_b64e`
  - `climate.midea_ac_c400` or `climate.midea_ac_lan_c400`
  - `climate.midea_ac_2332` or `climate.midea_ac_lan_2332`

### Step 4: Update Dashboard

Once you have the entity IDs, I can update the dashboard configuration to match them.

## Alternative: Manual Installation via File System

If you prefer to install manually:

1. **SSH into your Home Assistant instance**
2. **Navigate to `/config/custom_components/`**
3. **Clone the repository:**
   ```bash
   git clone https://github.com/wuwentao/midea_ac_lan.git
   ```
4. **Restart Home Assistant**
5. **Follow Step 2 above to configure devices**

## Troubleshooting

- **Integration not appearing:** Make sure you restarted Home Assistant after installation
- **Devices not connecting:** Verify IP addresses are correct and devices are online
- **Invalid token/key:** Tokens may expire; you may need to re-extract them from NetHome Plus
- **Port issues:** Ensure port 6444 is not blocked by firewall

