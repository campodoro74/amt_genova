# AMT Genova Home Assistant Integration

A custom Home Assistant integration that provides real-time bus arrival information for AMT (Azienda Mobilità e Trasporti) Genova public transportation system.

## Overview

This integration fetches real-time bus departure information from AMT Genova's XML API and creates sensor entities in Home Assistant. Each configured bus stop becomes a sensor that displays the wait time (in minutes) until the next bus arrival, along with detailed information about upcoming departures.

## Features

- **Real-time Updates**: Automatically fetches bus arrival data every 30 seconds
- **Multiple Stops**: Configure as many bus stops as needed
- **Detailed Information**: Each sensor provides:
  - Wait time until next bus (in minutes)
  - Route number
  - Destination
  - Arrival time
  - Vehicle number
  - Crowding status
  - Leave warning (when bus arrives in ≤3 minutes)
- **Efficient Polling**: Uses Home Assistant's DataUpdateCoordinator to manage updates efficiently
- **Error Handling**: Gracefully handles API failures and network issues

## Installation

### Manual Installation

1. Copy the `amt_genova` folder to your Home Assistant `custom_components` directory:
   ```
   <config>/custom_components/amt_genova/
   ```

2. Restart Home Assistant

3. Add configuration to your `configuration.yaml`:

```yaml
amt_genova:
  - "0731"  # Stop ID 1
  - "0732"  # Stop ID 2
```

## Configuration

### Finding Your Stop ID

The stop ID is a 4-digit code that identifies your bus stop. You can find it:
- On the physical bus stop sign
- By inspecting the AMT Genova website URL when viewing a stop
- By checking the XML API directly: `https://www.amt.genova.it/amt/servizi/passaggi_xml.php?CodiceFermata=YOUR_STOP_ID`

### Configuration Format

```yaml
amt_genova:
  - "0731"
  - "0732"
  - "1234"
```

Simply list your stop IDs as strings in a YAML list.

## How It Works

### Architecture

The integration consists of four main components:

1. **`__init__.py`**: Entry point that reads YAML configuration and initializes the integration
2. **`sensor.py`**: Creates sensor entities using Home Assistant's platform system and DataUpdateCoordinator
3. **`amt_api.py`**: Fetches and parses XML data from AMT Genova's API
4. **`const.py`**: Contains constants (domain name, scan interval, API URL)

### Data Flow

1. **Configuration**: Home Assistant reads the `amt_genova` section from `configuration.yaml`
2. **Initialization**: `__init__.py` stores the stop IDs and loads the sensor platform
3. **Sensor Creation**: `sensor.py` creates one `AMTStopSensor` entity for each configured stop
4. **Data Updates**: `DataUpdateCoordinator` calls `amt_api.py` every 30 seconds to fetch fresh data
5. **XML Parsing**: The API response (XML) is parsed to extract departure information
6. **State Updates**: Sensor entities update their state and attributes with the latest data

### API Details

The integration queries AMT Genova's XML endpoint:
```
https://www.amt.genova.it/amt/servizi/passaggi_xml.php?CodiceFermata={stop_id}
```

The XML response contains:
- `PrevisioneArrivo`: Wait time (e.g., "5'" for 5 minutes)
- `Linea`: Bus route number
- `Destinazione`: Final destination
- `OraArrivo`: Scheduled arrival time
- `AutobusPieno`: Whether the bus is crowded ("true"/"false")
- `NumeroSociale`: Vehicle identification number

## Sensor Attributes

Each sensor (`sensor.amt_0731`, etc.) provides:

- **State**: Wait time in minutes until next bus (or `None` if no data)
- **Attributes**:
  - `stop`: Stop ID
  - `updated`: Last update timestamp
  - `leave_warning`: Boolean indicating if a bus arrives in ≤3 minutes
  - `next`: Array of upcoming departures, each containing:
    - `route`: Bus line number
    - `headsign`: Destination
    - `wait`: Minutes until arrival
    - `time`: Scheduled arrival time
    - `crowded`: Whether bus is full
    - `vehicle`: Vehicle number
    - `source`: Always "realtime"
    - `stop`: Stop ID

## Usage Examples

### Basic Sensor Display

The sensor state shows the wait time:
```
sensor.amt_0731: 5
```

### Automation Example

Notify when bus is arriving soon:

```yaml
automation:
  - alias: "Bus arriving soon"
    trigger:
      - platform: numeric_state
        entity_id: sensor.amt_0731
        below: 3
    action:
      - service: notify.mobile_app
        data:
          message: "Bus arriving in {{ states('sensor.amt_0731') }} minutes!"
```

### Template Example

Display next bus information:

```yaml
template:
  - sensor:
      - name: "Next Bus Info"
        state: >
          {% set data = state_attr('sensor.amt_0731', 'next') %}
          {% if data %}
            Line {{ data[0].route }} to {{ data[0].headsign }} in {{ data[0].wait }} min
          {% else %}
            No buses scheduled
          {% endif %}
```

### Dashboard Card

Create a card showing bus times:

```yaml
type: entities
title: Bus Times
entities:
  - entity: sensor.amt_0731
    name: Stop 0731
  - entity: sensor.amt_0732
    name: Stop 0732
```

## File Structure

```
custom_components/amt_genova/
├── __init__.py          # Integration entry point
├── manifest.json         # Integration metadata
├── const.py             # Constants (domain, URLs, intervals)
├── sensor.py            # Sensor platform and entities
└── amt_api.py           # API client and XML parser
```

## Technical Details

- **Update Interval**: 30 seconds (configurable in `const.py`)
- **API Timeout**: 10 seconds
- **Error Handling**: Returns empty data structure on API failures
- **XML Namespace**: `http://cities-avm/WebServicePrevisioni`
- **IoT Class**: `cloud_polling` (requires internet connection)

## Troubleshooting

### Sensors Not Appearing

1. Check that the integration files are in `custom_components/amt_genova/`
2. Verify your `configuration.yaml` syntax is correct
3. Restart Home Assistant
4. Check Home Assistant logs for errors

### No Data / Unknown State

1. Verify your stop ID is correct
2. Check if the stop has active bus service
3. Test the API directly in a browser with the stop ID
4. Check Home Assistant logs for API errors

### Updates Not Happening

1. Verify internet connectivity
2. Check if AMT Genova's API is accessible
3. Review logs for timeout or connection errors

## License

This integration is provided as-is for use with Home Assistant.

## Author

Created by [@campodoro74](https://github.com/campodoro74)

## Links

- [GitHub Repository](https://github.com/campodoro74/amt_genova)
- [AMT Genova Official Website](https://www.amt.genova.it/)
