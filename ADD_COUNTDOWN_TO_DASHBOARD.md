# Adding Toilet Heater Countdown to Default Overview Dashboard

## Step 1: Restart Home Assistant
The template sensor `sensor.toilet_heater_countdown` needs Home Assistant to restart to be loaded. After restart, the sensor will be available.

## Step 2: Add to Default Overview Dashboard

Since the Default overview is in storage mode (not YAML), you need to add it manually:

### Option A: Add to Existing Toilet Heater Card
1. Go to your **Default overview** dashboard
2. Find the card showing the Toilet heater information
3. Click the **three dots (⋮)** in the top right of that card
4. Select **Edit Card**
5. In the entities list, add:
   ```
   sensor.toilet_heater_countdown
   ```
6. Optionally set a custom name: `Countdown` and icon: `mdi:timer`
7. Click **Save**

### Option B: Create a New Card Next to Existing One
1. Go to your **Default overview** dashboard
2. Click the **three dots (⋮)** in the top right → **Edit Dashboard**
3. Click **+ ADD CARD**
4. Select **Entities** card
5. Add these entities:
   - `switch.standing_lamp_socket_1` (name: "Toilet Heater")
   - `sensor.standing_lamp_power` (name: "Power")
   - `sensor.toilet_heater_countdown` (name: "Countdown", icon: `mdi:timer`)
6. Set title: "Toilet Heater"
7. Click **Save**

### Option C: Use Horizontal Stack
1. Go to your **Default overview** dashboard
2. Click the **three dots (⋮)** in the top right → **Edit Dashboard**
3. Click **+ ADD CARD**
4. Select **Horizontal Stack**
5. Add three **Entity** cards:
   - Card 1: `switch.standing_lamp_socket_1`
   - Card 2: `sensor.standing_lamp_power`
   - Card 3: `sensor.toilet_heater_countdown` (with icon `mdi:timer`)
6. Click **Save**

## What the Countdown Shows
- **MM:SS format** (e.g., "04:32") when the heater is on or power > 1W
- **"Off"** when the heater is off and power ≤ 1W
- Updates every second automatically
- Counts down from 5:00 (5 minutes) to 00:00

## Troubleshooting
If the sensor doesn't appear:
1. Check that Home Assistant has been restarted after adding `sensors.yaml`
2. Go to **Developer Tools** → **States** and search for `toilet_heater_countdown`
3. If it's not there, check **Developer Tools** → **YAML** for configuration errors

