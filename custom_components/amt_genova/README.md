# AMT Genova Home Assistant Integration

A Home Assistant custom integration to display real-time bus arrival times from AMT Genova (Azienda Mobilità e Trasporti di Genova).

## Features

- **Real-time bus arrival information** - Get live bus tracking data from AMT Genova
- **Scheduled bus information** - Fallback to scheduled times when real-time data is unavailable
- **Vehicle position tracking** - Track specific buses and see how many stops away they are
- **Multiple bus stop support** - Monitor multiple stops simultaneously
- **Automatic updates** - Updates every 30 seconds automatically
- **Detailed bus information** including:
  - Route number and destination
  - Wait time in minutes
  - Scheduled arrival time
  - Crowded status
  - Vehicle number
  - Real-time vs scheduled data source
  - Current position (stops away from your stop)
  - Departure status (if bus hasn't left yet)
- **Stop name mapping** - Human-readable stop names instead of just IDs
- **Leave warnings** - Automatic alerts when buses are arriving within 3 minutes
- **YAML-based configuration** - Simple and flexible configuration

## Installation

1. Copy the `amt_genova` folder to your Home Assistant `custom_components` directory:
   ```
   /config/custom_components/amt_genova/
   ```

2. Restart Home Assistant

3. Add the following to your `configuration.yaml`:

```yaml
amt_genova:
  stops:
    - "0731"  # Stop ID 1
    - "0732"  # Stop ID 2
```

Replace `"0731"` and `"0732"` with your desired bus stop IDs. You can find stop IDs on the [AMT Genova website](https://www.amt.genova.it/).

4. Restart Home Assistant again

## Configuration

The integration supports two configuration formats:

### Simple Format (List)

For basic usage, you can use a simple list of stop IDs:

```yaml
amt_genova:
  - "0731"
  - "0732"
```

### Advanced Format (Dictionary)

For vehicle tracking and position information, use the dictionary format:

```yaml
amt_genova:
  stops:
    - "0731"
    - "0732"
  tracking_stops:
    # Stops to monitor before your target stops (for vehicle tracking)
    "0731": ["0730", "0729"]  # Stops before 0731
    "0732": ["0731", "0730"]   # Stops before 0732
  routes:
    # Full route information for accurate position calculation
    "512":
      departure: "2386"  # Starting stop for line 512
      stops: ["2386", "2385", "2384", "0732"]  # Full route sequence
    "513":
      departure: "2395"  # Starting stop for line 513
      stops: ["2395", "2396", "2397", "0731"]  # Full route sequence
```

### Configuration Parameters

- **`stops`** (required): List of bus stop codes (as strings) to monitor. These are the stops where you want to see arrival times.

- **`tracking_stops`** (optional): Dictionary mapping target stop IDs to lists of stop IDs that come before them. Used for vehicle position tracking. For example, if you want to track buses approaching stop "0731", you would list all stops that come before "0731" on the route.

- **`routes`** (optional): Dictionary with complete route information. Each route should have:
  - `departure`: The stop ID where the route starts
  - `stops`: Complete list of stop IDs in order from departure to destination

## Entities

For each configured stop, a sensor entity is created:

- **Entity ID**: `sensor.amt_{STOP_ID}` (e.g., `sensor.amt_0731`)
- **State**: Minutes until **next bus** arrival (for the primary line at that stop)
- **Attributes**:
  - `stop`: The stop ID
  - `updated`: Last update timestamp (format: "YYYY-MM-DD HH:MM:SS")
  - `leave_warning`: Boolean indicating if a bus is arriving within 3 minutes
  - `next`: List of upcoming buses with detailed information:
    - `route`: Bus line number (e.g., "512", "513")
    - `headsign`: Destination (e.g., "VIA ISONZO")
    - `wait`: Minutes until arrival
    - `time`: Scheduled arrival time (format: "HH:MM")
    - `crowded`: Boolean indicating if the bus is crowded
    - `source`: Data source - `"realtime"` for live tracking or `"scheduled"` for timetable data
    - `vehicle`: Vehicle number (e.g., "0E181") - only present for real-time buses
    - `stop`: The stop ID this bus is arriving at
    - `position`: Vehicle position information (only for real-time buses with tracking configured):
      - `found`: Boolean - whether the vehicle was found at a tracking stop
      - `stops_away`: Integer - number of stops away from your target stop (null if at departure)
      - `current_stop`: Stop ID where the bus is currently located
      - `current_stop_name`: Human-readable name of current stop
      - `target_stop_name`: Human-readable name of your target stop
      - `at_departure`: Boolean - true if bus hasn't left the starting point yet
      - `scheduled_time`: Scheduled departure time (only when `at_departure` is true)

## Examples

### Basic Configuration

After basic configuration, you'll have entities like:
- `sensor.amt_0731` - Shows wait time for stop 0731
- `sensor.amt_0732` - Shows wait time for stop 0732

### Advanced Configuration with Vehicle Tracking

With tracking stops and routes configured, you can track specific buses and see their position:

```yaml
amt_genova:
  stops:
    - "0731"
    - "0732"
  tracking_stops:
    "0731": ["2395", "2396", "2397", "0418", "2398", "2399", "0399", "0400", "0401", "0402", "0730"]
    "0732": ["2386", "2385", "2384", "2563", "2564", "2565", "2383", "2381", "2387", "2388", "2395", "2396", "2397", "0418", "2398", "2399", "0399", "0400", "0401", "0402", "0730", "0731"]
  routes:
    "512":
      departure: "2386"
      stops: ["2386", "2385", "2384", "2563", "2564", "2565", "2383", "2381", "2387", "2388", "0732", "0733"]
    "513":
      departure: "2395"
      stops: ["2395", "2396", "2397", "0418", "2398", "2399", "0399", "0400", "0401", "0402", "0730", "0731", "0732", "0733"]
```

This configuration allows the integration to:
- Track buses by vehicle number
- Calculate how many stops away a bus is from your stop
- Show if a bus is still at the departure point
- Display human-readable stop names

## Usage in Dashboards

### Simple Entity Card

You can use these sensors in your Lovelace dashboards:

```yaml
type: entities
title: AMT Genova Bus Times
entities:
  - entity: sensor.amt_0731
    name: Stop **Prasca / Chiesa**
    icon: mdi:bus-clock
  - entity: sensor.amt_0732
    name: Stop **Carrara 1 / Prasca**
    icon: mdi:bus-clock
```

### Advanced Dashboard with Position Information

For detailed information including vehicle positions, use a markdown card with Jinja2 templates:

```yaml
type: markdown
content: |
  ## 🚏 Stop **Prasca / Chiesa**
  {% set data = state_attr('sensor.amt_0731', 'next') or [] %}
  {% for bus in data %}
    {% if bus.source == 'realtime' %}
      **Line {{ bus.route }}** → {{ bus.headsign }}
      - Wait: {{ bus.wait }} minutes
      - Vehicle: {{ bus.vehicle }}
      {% if bus.position and bus.position.found %}
        - Position: {{ bus.position.stops_away }} stops away
        - Current stop: {{ bus.position.current_stop_name }}
      {% endif %}
      {% if bus.crowded %}🚨 Crowded{% endif %}
    {% endif %}
  {% endfor %}
```

## Stop Names

The integration includes a built-in mapping of stop IDs to human-readable names. Common stops include:

- `0731`: **Prasca / Chiesa**
- `0732`: **Carrara 1 / Prasca**
- `0730`: **Prasca / Rosata**
- `2386`: **Via Bobbio / Ponte** (Line 512 departure)
- `2395`: **Staglieno** (Line 513 departure)

See `const.py` for the complete list of mapped stop names. If a stop ID is not in the mapping, the ID itself will be displayed.

## Troubleshooting

### Sensors not appearing

1. Check that the integration files are in `/config/custom_components/amt_genova/`
2. Verify your `configuration.yaml` syntax is correct
3. Check Home Assistant logs for errors
4. Ensure you've restarted Home Assistant after adding the configuration

### No data

1. Verify the stop IDs are correct
2. Check your internet connection
3. The AMT API may be temporarily unavailable
4. Some stops may not have buses scheduled at certain times

### Position tracking not working

1. Ensure `tracking_stops` is configured for your target stops
2. Verify that the tracking stops are correct (they should be stops that come before your target stop)
3. Check that `routes` configuration includes the route you're tracking
4. Position tracking only works for real-time buses (those with a vehicle number)

### ConfigEntryError

This integration is YAML-only. If you see a ConfigEntryError, it means there's a config entry in Home Assistant that needs to be removed:

1. Go to **Settings → Devices & Services → Integrations**
2. Find "AMT Genova" (if present)
3. Remove it
4. Configure via `configuration.yaml` instead

## Technical Details

- **Update Interval**: 30 seconds (configurable via `DEFAULT_SCAN_INTERVAL` in `const.py`)
- **API**: AMT Genova XML API (`https://www.amt.genova.it/amt/servizi/passaggi_xml.php`)
- **Data Source**: Real-time bus tracking with scheduled fallback
- **Platform**: Sensor
- **Vehicle Tracking**: Uses vehicle numbers to track buses across multiple stops
- **Position Calculation**: Calculates stops away using route data when available, falls back to tracking stop index

## How Vehicle Tracking Works

The integration can track specific buses by their vehicle number (e.g., "0E181") across multiple stops:

1. When a bus appears at a tracking stop with a vehicle number, the integration records its position
2. The integration checks all tracking stops in reverse order (closest to target first)
3. It calculates how many stops away the bus is using route data if available
4. If route data is not available, it uses the index in the tracking stops list
5. The bus is only considered "at" a stop if its wait time at that stop is less than 5 minutes
6. If a bus is at its departure stop, it's marked as "has not left yet" with the scheduled departure time

## License

This integration is provided as-is for use with Home Assistant.

## Support

For issues or questions, please visit: https://github.com/campodoro74/amt_genova
