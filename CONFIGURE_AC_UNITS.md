# Configure Midea AC Units

The custom integration has been installed. After Home Assistant restarts, follow these steps to configure your 3 AC units:

## Step 1: Wait for Home Assistant to Restart

The restart may take 30-60 seconds. Wait until Home Assistant is fully back online.

## Step 2: Install msmart Library (if needed)

If you see errors about the msmart library, you may need to install it:
- If using Home Assistant OS: The integration should handle this automatically
- If using Docker or manual install: You may need to install `msmart` in your Python environment

## Step 3: Configure Each AC Unit

1. **Go to Settings → Devices & Services**
2. **Click "Add Integration"** (bottom right)
3. **Search for "Midea AC LAN"**
4. **Click on it to start configuration**

### For AC B64E (192.168.68.37):
- **Host:** `192.168.68.37`
- **Device ID:** `152832116922715`
- **Token:** `0e86b416c7d1928a9e6bca125d56f046d88e152191acb80ff44c9dce3c8749048d1754d99c7d693ecbf206f9381b6229cfb88d4044dbb20602a18556efe51a4f`
- **Key:** `2007fc6f36d24f81aa8aae70e3717446a9b43b0253314fedb0c379ebce4f905c`
- **Name (optional):** `AC B64E`
- **Port:** `6444` (default)

### For AC C400 (192.168.68.19):
- **Host:** `192.168.68.19`
- **Device ID:** `153931628549890`
- **Token:** `6c0245bc8bbe24511a321c999bd657990999a6562ff3ab14cc80e14e623e33fa283e6c6b3cb4618701ab8f2b59c24597edea499da7b9f76f077753f0b6e7a6e0`
- **Key:** `aaee6a8cc2024716ba34ffb5cd2b3619a5dd1aebe4c54b3d9be42ed49fb5743a`
- **Name (optional):** `AC C400`
- **Port:** `6444` (default)

### For AC 2332 (192.168.68.165):
- **Host:** `192.168.68.165`
- **Device ID:** `153931628549884`
- **Token:** `f0d0b4a06a9481a0ec300f4a5b265862592e4b78d674d7320a96d481f2736871cf54f1f57744f16365f6997ec50f53624e51bcc7d57794c1d20c878ece6f7a04`
- **Key:** `11ba77e17e244ce8b4b112d72ebfcf31cbf32db6a53f44959f6e96c2f1f5fb41`
- **Name (optional):** `AC 2332`
- **Port:** `6444` (default)

## Step 4: Verify Entity IDs

After configuration, check the created entity IDs:
- Go to **Developer Tools → States**
- Search for entities starting with `climate.`
- Look for entities like:
  - `climate.midea_ac_lan_152832116922715` (or similar)
  - `climate.midea_ac_lan_153931628549890` (or similar)
  - `climate.midea_ac_lan_153931628549884` (or similar)

## Step 5: Update Dashboard

Once you have the entity IDs, let me know and I'll update the dashboard configuration to match them.

## Troubleshooting

- **Integration not appearing:** Make sure Home Assistant has fully restarted
- **msmart library error:** The library should install automatically, but if not, you may need to install it manually
- **Connection errors:** Verify IP addresses are correct and devices are online
- **Invalid token/key:** Tokens may expire; you may need to re-extract them

