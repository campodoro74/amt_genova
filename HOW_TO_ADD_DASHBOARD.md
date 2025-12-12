# How to Add the Ariel AC Dashboard to Home Assistant

The dashboard file is ready, but you need to **import it into Home Assistant**. Here are the steps:

## Method 1: Add as New Dashboard (Recommended)

1. **Go to Settings → Dashboards**
2. **Click "Add Dashboard"** (bottom right)
3. **Select "New Dashboard"**
4. **Choose "Start with an empty dashboard"**
5. **Click the three dots menu (⋮)** in the top right of the new dashboard
6. **Select "Edit Dashboard"**
7. **Click the three dots menu again (⋮)**
8. **Select "Raw configuration editor"**
9. **Delete any existing content**
10. **Copy the entire content from `air-conditioner-dashboard.yaml`**
11. **Paste it into the editor**
12. **Click "Save"** (top right)
13. **Click "Done"** (top right)

The dashboard should now appear in your dashboard list as "Ariel AC".

## Method 2: Add to Existing Dashboard

If you want to add it as a view to an existing dashboard:

1. **Go to your dashboard**
2. **Click the three dots menu (⋮)** → **"Edit Dashboard"**
3. **Click the three dots menu again (⋮)** → **"Manage views"**
4. **Click "Add view"**
5. **Click the three dots next to the new view** → **"Edit view"**
6. **Click the three dots again** → **"Raw configuration editor"**
7. **Copy just the view content** (the part starting with `- title: Ariel AC`)
8. **Paste and save**

## Method 3: Import via File (Advanced)

If you have file system access:

1. Copy `air-conditioner-dashboard.yaml` to your Home Assistant config directory
2. The file should be at: `/config/air-conditioner-dashboard.yaml`
3. In Home Assistant, go to **Settings → Dashboards**
4. Click **"Add Dashboard"** → **"Import from file"**
5. Select the file

## Troubleshooting

**Dashboard doesn't appear:**
- Make sure you saved the configuration
- Check for YAML syntax errors (red indicators in the editor)
- Try refreshing the browser

**Cards don't show:**
- Verify the entity IDs exist: Go to **Developer Tools → States** and search for `climate.153931628549890_climate`
- Check Home Assistant logs for errors

**Buttons don't work:**
- Verify the service calls are correct
- Check that the entities are actually controllable
- Look for errors in the browser console (F12)

## Quick Test

After adding the dashboard:
1. Navigate to the "Ariel AC" dashboard
2. You should see 3 AC units
3. Try clicking a button to test if controls work
4. Check the thermostat cards show current temperatures
