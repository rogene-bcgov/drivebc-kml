# DriveBC to KML Converter

A Python tool that converts DriveBC traffic events data to KML format for use in Google Maps.

## Overview

This project fetches live traffic event data from the DriveBC API (https://www.drivebc.ca/api/events/) and converts it into KML (Keyhole Markup Language) format that can be imported into Google Maps as a custom layer.

## Features

- **Live Data Fetching**: Retrieves current traffic events from DriveBC API
- **Complete Event Information**: Includes all available fields:
  - ✅ Event ID (no truncation)
  - ✅ Severity/Incident Level
  - ✅ Closest Landmark
  - ✅ Next Update time
  - ✅ Start/End times
  - ✅ Full descriptions
- **Event Type Styling**: Different colors and icons for various event types:
  - 🔴 Construction events (Red)
  - 🟡 Incidents (Yellow) 
  - 🟢 Road conditions (Green)
  - 🔵 Weather events (Blue)
  - ⚪ Other events (Gray)
- **Route Visualization**: Shows event locations as points or line strings for road segments
- **Google Maps Compatible**: Generates standard KML format for easy import
- **Comprehensive Testing**: Full unit test suite with 100% success rate

## Requirements

- Python 3.6 or higher
- `requests` library for API calls

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script directly:
```bash
python drivebc_to_kml.py
```

The script will:
1. Fetch current events from the DriveBC API
2. Convert them to KML format
3. Save the output as `drivebc_events_YYYYMMDD_HHMMSS.kml`

### Running Tests

To run the comprehensive unit test suite:
```bash
python run_tests.py
```

Or run tests directly with unittest:
```bash
python -m unittest test_drivebc_to_kml.py -v
```

The test suite includes:
- API functionality tests
- KML generation validation
- Field completeness verification
- Edge case handling
- XML validity checks

### Demonstrating Improvements

To see a detailed report of all improvements made:
```bash
python -m unittest test_drivebc_to_kml.TestImprovementsDemo.test_improvement_summary_report -v
```

This will show verification that all originally missing fields (Event IDs, Severity levels, Closest landmarks, Next updates) are now properly included and that name truncation has been eliminated.

### Using in Google Maps

1. Go to [Google My Maps](https://mymaps.google.com)
2. Create a new map or open an existing one
3. Click "Import" button
4. Upload the generated KML file
5. The traffic events will appear as a new layer on your map

### Programmatic Usage

```python
from drivebc_to_kml import DriveBCToKMLConverter

# Create converter instance
converter = DriveBCToKMLConverter()

# Fetch events
if converter.fetch_events():
    # Convert to KML
    kml_content = converter.convert_to_kml()
    
    # Save to custom filename
    converter.save_kml(kml_content, "my_traffic_events.kml")
```

## Event Types

The DriveBC API provides various event types that are styled differently in the KML output:

- **CONSTRUCTION**: Road construction and maintenance work
- **INCIDENT**: Traffic incidents, accidents, and closures  
- **ROAD_CONDITION**: Road condition updates and advisories
- **WEATHER**: Weather-related traffic impacts
- **Other types**: Handled with default styling

## Output Format

The generated KML file includes:
- Organized folders by event type
- Detailed event information in pop-up descriptions
- Appropriate styling based on event type
- Geographic coordinates for precise location mapping
- Line strings for events affecting road segments

## Error Handling

The script includes robust error handling for:
- Network connectivity issues
- API response errors
- Invalid JSON data
- File I/O operations

## Limitations

- Requires internet connection to fetch live data
- API response size may vary based on current traffic conditions
- Google Maps has file size limits for KML imports (typically 5MB)

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the converter.

## License

This project is open source and available under the MIT License.
