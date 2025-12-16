# AMT Genova Home Assistant Integration

A Home Assistant custom integration to display real-time bus arrival times from AMT Genova (Azienda Mobilità e Trasporti di Genova).

## Features

- Real-time bus arrival information
- Multiple bus stop support
- Automatic updates every 30 seconds
- Detailed bus information including route, destination, and wait time
- YAML-based configuration

## Installation

1. Copy the `amt_genova` folder to your Home Assistant `custom_components` directory:
   ```
   /config/custom_components/amt_genova/
   ```

2. Restart Home Assistant

3. Add the following to your `configuration.yaml`:

```yaml
amt_genova:
  - "0731"  # Stop ID 1
  - "0732"  # Stop ID 2
```

Replace `"0731"` and `"0732"` with your desired bus stop IDs. You can find stop IDs on the [AMT Genova website](https://www.amt.genova.it/).

4. Restart Home Assistant again

## Configuration

The integration is configured via YAML in `configuration.yaml`:

```yaml
amt_genova:
  - "STOP_ID_1"
  - "STOP_ID_2"
  # Add more stop IDs as needed
```

### Parameters

- **Stop IDs**: List of bus stop codes (as strings) to monitor

## Entities

For each configured stop, a sensor entity is created:

- **Entity ID**: `sensor.amt_{STOP_ID}`
- **State**: Minutes until next bus arrival
- **Attributes**:
  - `stop`: The stop ID
  - `updated`: Last update timestamp
  - `leave_warning`: Boolean indicating if a bus is arriving within 3 minutes
  - `next`: List of upcoming buses with:
    - `route`: Bus line number
    - `headsign`: Destination
    - `wait`: Minutes until arrival
    - `time`: Scheduled arrival time
    - `crowded`: Whether the bus is crowded
    - `source`: Data source (usually "realtime")
    - `vehicle`: Vehicle number

## Example

After configuration, you'll have entities like:
- `sensor.amt_0731` - Shows wait time for stop 0731
- `sensor.amt_0732` - Shows wait time for stop 0732

## Usage in Dashboards

You can use these sensors in your Lovelace dashboards:

```yaml
type: entities
title: AMT Genova Bus Times
entities:
  - entity: sensor.amt_0731
    name: Stop 0731
    icon: mdi:bus-clock
  - entity: sensor.amt_0732
    name: Stop 0732
    icon: mdi:bus-clock
```

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

### ConfigEntryError

This integration is YAML-only. If you see a ConfigEntryError, it means there's a config entry in Home Assistant that needs to be removed:

1. Go to **Settings → Devices & Services → Integrations**
2. Find "AMT Genova" (if present)
3. Remove it
4. Configure via `configuration.yaml` instead

## Technical Details

- **Update Interval**: 30 seconds (configurable via `DEFAULT_SCAN_INTERVAL` in `const.py`)
- **API**: AMT Genova XML API
- **Data Source**: Real-time bus tracking
- **Platform**: Sensor

## License

This integration is provided as-is for use with Home Assistant.

## Support

For issues or questions, please visit: https://github.com/campodoro74/amt_genova

