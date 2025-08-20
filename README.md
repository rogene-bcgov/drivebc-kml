# DriveBC to KML Converter

A comprehensive Python toolset that converts DriveBC traffic events and ferry information to KML format for use in Google Maps and other mapping applications.

## Overview

This project provides multiple tools to fetch live data from the DriveBC APIs and convert it into KML (Keyhole Markup Language) format that can be imported into Google Maps as custom layers. The project includes both basic conversion tools and enhanced services that combine traffic events with ferry information.

## Features

### Core Features
- **Live Data Fetching**: Retrieves current traffic events and ferry information from DriveBC APIs
- **Dual Data Sources**: 
  - 🚗 Traffic events from https://www.drivebc.ca/api/events/
  - ⛴️ Ferry information from https://www.drivebc.ca/api/ferries/
- **Complete Event Information**: Includes all available fields:
  - ✅ Event ID (no truncation)
  - ✅ Severity/Incident Level
  - ✅ Closest Landmark
  - ✅ Next Update time
  - ✅ Start/End times
  - ✅ Full descriptions
  - ✅ Ferry schedules, capacities, and contact details

### Styling & Visualization
- **Event Type Styling**: Different colors and icons for various event types:
  - 🔴 Construction events (Red)
  - 🟡 Incidents (Yellow) 
  - 🟢 Road conditions (Green)
  - 🔵 Weather events (Blue)
  - ⚪ Other events (Gray)
- **Ferry Type Styling**: Different colors for ferry types:
  - 🟣 Cable ferries (Purple)
  - 🔷 Scheduled ferries (Teal)
  - 🔹 On-demand ferries (Indigo)
  - 🟣 Other ferries (Purple)
- **Route Visualization**: Shows event locations as points or line strings for road segments
- **Organized Folders**: Events and ferries grouped by type for easy navigation
- **Google Maps Compatible**: Generates standard KML format for easy import

### Technical Features
- **Comprehensive Testing**: Full unit test suite with robust error handling
- **Multiple Service Options**: Choose between basic converter or enhanced service
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Web Interface**: Simple HTML interface for easy access

## Requirements

- Python 3.6 or higher
- `requests` library for API calls

## Installation

### Quick Start (Windows)
```bash
# Run the setup script
setup.bat
```

### Quick Start (Linux/macOS)
```bash
# Run the setup script
chmod +x setup.sh
./setup.sh
```

### Manual Installation
1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
├── drivebc_to_kml.py           # Original basic converter
├── drivebc_service.py          # Enhanced service (traffic + ferries)
├── drivebc_enhanced_service.py # Alternative enhanced service
├── drivebc_events.kml          # Generated KML output
├── index.html                  # Web interface
├── requirements.txt            # Python dependencies
├── run_converter.bat           # Windows runner script
├── setup.bat                   # Windows setup script
├── setup.sh                    # Linux/macOS setup script
├── run_tests.py               # Test runner
├── test_drivebc_to_kml.py     # Unit tests
├── examples.py                # Usage examples
├── example_input.txt          # Sample data
├── Dockerfile                 # Container support
└── README_SERVICE.md          # Service-specific documentation
```

## Usage

### Option 1: Enhanced Service (Recommended)
The enhanced service combines both traffic events and ferry information:

```bash
python drivebc_service.py
```

This will:
1. Fetch current traffic events from the DriveBC API
2. Fetch current ferry information from the DriveBC API
3. Convert both to KML format with organized folders
4. Save the output as `drivebc_events.kml`

### Option 2: Basic Converter (Traffic Only)
Run the original basic script for traffic events only:

```bash
python drivebc_to_kml.py
```

This will:
1. Fetch current events from the DriveBC API
2. Convert them to KML format
3. Save the output as `drivebc_events_YYYYMMDD_HHMMSS.kml`

### Option 3: Windows Batch Script
```bash
# Double-click or run from command line
run_converter.bat
```

### Option 4: Using Tasks (VS Code)
If using VS Code, you can run predefined tasks:
- **Install Dependencies**: Installs required packages
- **Run DriveBC to KML Converter**: Runs the enhanced service

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

## Recent Updates

### Latest Enhancements
- ✅ **Enhanced Service**: Combined traffic events with ferry information
- ✅ **Multiple Service Options**: Choose between basic converter and enhanced service
- ✅ **Improved File Organization**: Organized folder structure by data type and category
- ✅ **Ferry Integration**: Complete ferry route information with schedules and contact details
- ✅ **Web Interface**: Simple HTML interface for easy access
- ✅ **Cross-Platform Support**: Setup scripts for Windows, Linux, and macOS
- ✅ **Container Support**: Docker configuration for deployment
- ✅ **Rich Metadata**: Comprehensive event details including webcam links for ferries

### Current Status
- **Traffic Events**: ✅ Fully implemented with all event types and styling
- **Ferry Information**: ✅ Complete integration with schedules, capacity, and contact info
- **Testing**: ✅ Comprehensive unit test suite with 100% success rate
- **Documentation**: ✅ Updated with current features and file structure
- **Cross-Platform**: ✅ Works on Windows, Linux, and macOS

### Using in Google Maps

1. Go to [Google My Maps](https://mymaps.google.com)
2. Create a new map or open an existing one
3. Click "Import" button
4. Upload the generated KML file
5. The traffic events will appear as a new layer on your map

### Programmatic Usage

```python
# Using the Enhanced Service
from drivebc_service import EnhancedDriveBCService

# Create service instance
service = EnhancedDriveBCService()

# Generate comprehensive KML with both traffic and ferry data
output_file = service.generate_kml("my_custom_output.kml")

# Or using the basic converter
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

## Data Types & Styling

### 🚗 Traffic Event Types

The DriveBC API provides various event types that are styled differently in the KML output:

- **CONSTRUCTION**: Road construction and maintenance work
- **INCIDENT**: Traffic incidents, accidents, and closures  
- **ROAD_CONDITION**: Road condition updates and advisories
- **WEATHER**: Weather-related traffic impacts
- **Other types**: Handled with default styling

### ⛴️ Ferry Types

Ferry routes are categorized and styled as follows:

- **Cable Ferries**: Cable-operated ferry crossings
- **Scheduled Ferries**: Regular scheduled ferry services  
- **On-Demand Ferries**: On-demand ferry services
- **Other Ferries**: Miscellaneous ferry services

Ferry information includes:
- Vehicle and passenger capacity
- Crossing times and schedules
- Contact information (phone, email)
- Live webcam links where available
- Current operational status

## Output Format

The generated KML file includes:
- **Organized folder structure** by data type (Traffic Events vs Ferry Routes)
- **Sub-folders by category** (Construction, Incidents, etc. for traffic; Cable, Scheduled, etc. for ferries)
- **Detailed information** in pop-up descriptions for each item
- **Appropriate styling** based on event/ferry type with color-coded icons
- **Geographic coordinates** for precise location mapping
- **Line strings** for events affecting road segments
- **Rich metadata** including schedules, contact info, and webcam links for ferries

### Sample Output Structure
```
📁 DriveBC Traffic Events & Ferry Information
├── 🚗 Traffic Events (285)
│   ├── 📁 Construction Events
│   ├── 📁 Incident Events  
│   ├── 📁 Road Condition Events
│   └── 📁 Weather Events
└── ⛴️ Ferry Routes (14)
    ├── 📁 Cable Ferries
    ├── 📁 Scheduled Ferries
    ├── 📁 On-Demand Ferries
    └── 📁 Other Ferries
```

## Error Handling

The script includes robust error handling for:
- Network connectivity issues
- API response errors
- Invalid JSON data
- File I/O operations

## Limitations

- Requires internet connection to fetch live data
- API response size may vary based on current traffic conditions and ferry operations
- Google Maps has file size limits for KML imports (typically 5MB)
- Ferry data availability depends on DriveBC API coverage

## Alternative Services

For automated updates and web hosting, see [`README_SERVICE.md`](README_SERVICE.md) which describes:
- Auto-updating service that runs every 30 minutes
- GitHub Pages hosting for public access
- Direct URL access for Google Maps integration
- Web interface for easy downloading

## Development & Testing

### Running Tests
```bash
# Run all tests
python run_tests.py

# Run tests with verbose output
python -m unittest test_drivebc_to_kml.py -v

# Run specific test demonstrating improvements
python -m unittest test_drivebc_to_kml.TestImprovementsDemo.test_improvement_summary_report -v
```

### Docker Support
```bash
# Build container
docker build -t drivebc-kml .

# Run container
docker run drivebc-kml
```

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the converter.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests as needed
5. Submit a pull request

## License

This project is open source and available under the MIT License.
