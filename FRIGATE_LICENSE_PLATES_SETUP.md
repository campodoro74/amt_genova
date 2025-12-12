# Adding Last 5 License Plates to Frigate Dashboard

This guide will help you add a card to your Frigate dashboard that displays the last 5 recognized license plates.

## Step 1: Restart Home Assistant

The template sensor `sensor.frigate_last_5_license_plates` needs Home Assistant to restart to be loaded. After restart, the sensor will be available.

1. Go to **Settings → System → Restart**
2. Wait for Home Assistant to restart (30-60 seconds)

## Step 2: Add Card to Frigate Dashboard

Since your dashboard is in storage mode, you need to add the card manually:

### Option A: Using the Card Configuration File (Recommended)

1. Go to your **Frigate dashboard** in Home Assistant
2. Click the **three dots menu (⋮)** in the top right → **"Edit Dashboard"**
3. Click **"+ ADD CARD"** button
4. Scroll down and click **"Manual"** (or select "Entities" card)
5. Click the **three dots** on the new card → **"Edit Card"**
6. Click the **three dots again** → **"Raw configuration editor"**
7. Open the file `frigate-license-plates-card.yaml` and copy the **OPTION 1** configuration
8. Paste it into the editor
9. Click **Save**

### Option B: Using the UI (Simpler but less features)

1. Go to your **Frigate dashboard** in Home Assistant
2. Click the **three dots menu (⋮)** in the top right → **"Edit Dashboard"**
3. Click **"+ ADD CARD"** button
4. Select **"Vertical Stack"** card
5. Add two cards:
   - **Card 1:** Entities card with:
     - `sensor.window_last_recognized_plate` (name: "Window Camera")
     - `sensor.eufy_last_recognized_plate` (name: "Eufy Camera")
   - **Card 2:** History Graph card with:
     - `sensor.window_last_recognized_plate`
     - `sensor.eufy_last_recognized_plate`
     - Hours to show: 168 (7 days)
6. Click **Save**

## What the Card Shows

The card displays:
- **Current last recognized plate** from each camera (Window and Eufy)
- **History graph** showing license plate detections over the last 7 days
- The graph will show the last 5 unique detections visually

## Viewing Detailed History

To see the actual last 5 plates with timestamps:

1. Go to **Developer Tools → Logbook**
2. Filter by:
   - `sensor.window_last_recognized_plate`
   - `sensor.eufy_last_recognized_plate`
3. You'll see the last detections with timestamps

## Alternative: View Last 5 Plates in Logbook

To see the actual last 5 plates with timestamps directly:

1. Go to **Developer Tools → Logbook**
2. Filter by entities:
   - `sensor.window_last_recognized_plate`
   - `sensor.eufy_last_recognized_plate`
3. Set the time range to "Last 7 days"
4. You'll see the last detections with timestamps, sorted by most recent first
5. The first 5 entries (excluding "None" or "Unknown") are your last 5 recognized plates

## Troubleshooting

**Card doesn't appear:**
- Make sure Home Assistant has been restarted after adding `sensors.yaml`
- Check that the sensor `sensor.frigate_last_5_license_plates` exists in **Developer Tools → States**

**No plates showing:**
- Check that Frigate is detecting license plates (check the Frigate UI)
- Verify that `sensor.window_last_recognized_plate` and `sensor.eufy_last_recognized_plate` are updating
- Check the logbook to see if there are any recent detections

**History graph is empty:**
- Make sure there have been license plate detections in the last 7 days
- Check that the sensors are updating correctly

