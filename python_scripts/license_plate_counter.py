"""Count license plate occurrences from Frigate sensors."""
from collections import Counter
from datetime import datetime, timedelta

# Get Home Assistant instance
hass = data.get('hass')

# Sensor entities
sensors = ['sensor.window_last_recognized_plate', 'sensor.eufy_last_recognized_plate']

# Get history for last 30 days
end_time = datetime.now()
start_time = end_time - timedelta(days=30)

# Collect all plates
all_plates = []

for sensor_id in sensors:
    try:
        history = hass.states.async_history(
            sensor_id,
            start_time,
            end_time,
            include_start_time_state=False
        )
        
        for state in history:
            plate = state.state
            if plate and plate not in ['None', 'Unknown', 'unknown', '', 'unavailable']:
                all_plates.append(plate)
    except Exception as e:
        logger.warning(f"Error getting history for {sensor_id}: {e}")

# Count occurrences
plate_counts = Counter(all_plates)

# Get top 10
top_10 = plate_counts.most_common(10)

# Format result
result_list = [{'plate': plate, 'count': count} for plate, count in top_10]

# Update sensor
state_value = ', '.join([plate for plate, _ in top_10]) if top_10 else 'No plates detected'

hass.states.async_set(
    'sensor.frigate_license_plate_counts',
    state_value,
    {
        'plates': result_list,
        'friendly_name': 'Frigate License Plate Counts',
        'icon': 'mdi:car-multiple'
    }
)

logger.info(f"Updated license plate counts: {len(top_10)} unique plates found")

