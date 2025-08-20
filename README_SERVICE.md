# DriveBC Enhanced KML Service

A comprehensive web service that automatically converts DriveBC traffic events AND ferry information to KML format every 30 minutes.

## 🚀 Live Service

The service is automatically deployed and running at:
- **KML File**: `https://rogene-bcgov.github.io/drivebc-kml/drivebc_events.kml`
- **Web Interface**: `https://rogene-bcgov.github.io/drivebc-kml/`

## 📋 Features

- 🔄 **Auto-updates every 30 minutes** via GitHub Actions
- 📍 **Fixed filename** (`drivebc_events.kml`) for Google Maps auto-refresh
- 🌐 **Public access** via GitHub Pages
- 🚗 **Traffic events** with color-coded styling (construction, incidents, weather, etc.)
- ⛴️ **Ferry information** with schedules, capacities, and contact details
- 📱 **Simple web interface** with usage instructions
- 📹 **Live webcam links** for ferry terminals
- 📊 **Organized data structure** with folders for easy navigation
- 🎨 **Rich styling** with icons and colors for different event types
- 🔧 **Multiple service options** for different use cases
- ✅ **Comprehensive testing** with unit test suite
- 🐳 **Docker support** for containerized deployment
- 🖥️ **Cross-platform** compatibility (Windows, Linux, macOS)

## 🛠️ Setup Instructions

### 1. Fork/Clone Repository
```bash
git clone https://github.com/yourusername/drivebc-kml-service.git
cd drivebc-kml-service
```

### 2. Enable GitHub Pages
1. Go to your repository settings
2. Navigate to "Pages" section
3. Set source to "Deploy from a branch"
4. Select "main" branch and "/ (root)" folder
5. Save

### 3. Enable GitHub Actions
1. Go to "Actions" tab in your repository
2. Enable workflows if prompted
3. The service will automatically start running every 30 minutes

### 4. Test Manual Run
- Go to "Actions" tab
- Click on "Update DriveBC KML" workflow
- Click "Run workflow" button

## 📁 File Structure

```
├── drivebc_service.py          # Enhanced service script (main)
├── drivebc_enhanced_service.py # Alternative enhanced service  
├── drivebc_to_kml.py          # Original basic converter
├── drivebc_events.kml          # Generated KML file (auto-updated)
├── index.html                  # Web interface
├── requirements.txt            # Python dependencies
├── run_converter.bat           # Windows runner script
├── setup.bat                   # Windows setup script
├── setup.sh                    # Linux/macOS setup script
├── run_tests.py               # Test runner
├── test_drivebc_to_kml.py     # Unit tests
├── examples.py                # Usage examples
├── Dockerfile                 # Container support
├── .github/workflows/
│   └── update-kml.yml          # GitHub Actions workflow
└── README.md                   # Main documentation
```

## 🔧 How It Works

1. **GitHub Actions** runs every 30 minutes (cron: `*/30 * * * *`)
2. **Python script** fetches latest events from DriveBC API
3. **Converts data** to KML format with proper styling
4. **Commits updated file** back to repository
5. **GitHub Pages** serves the file publicly

## 🗺️ Using in Google Maps

### Method 1: Direct Link (Recommended)
1. Copy the KML URL: `https://rogene-bcgov.github.io/drivebc-kml/drivebc_events.kml`
2. Go to [Google My Maps](https://mymaps.google.com)
3. Create/open a map
4. Click "Import" → Paste the URL
5. Data will auto-refresh when you reload the map

### Method 2: Download File
1. Visit the web interface
2. Download the KML file
3. Upload to Google My Maps
4. Re-download for updates

## 🎨 Event Types & Colors

### 🚗 Traffic Events
- 🔴 **Construction** - Road construction and maintenance
- 🟡 **Incidents** - Accidents and traffic disruptions  
- 🟢 **Road Conditions** - Weather-related road conditions
- 🔵 **Weather** - Weather-related traffic impacts
- ⚪ **Other** - Miscellaneous events

### ⛴️ Ferry Routes
- 🟣 **Cable Ferries** - Cable-operated crossings
- 🔷 **Scheduled Ferries** - Regular scheduled services
- 🔹 **On-Demand Ferries** - On-demand services
- 🟣 **Other Ferries** - Miscellaneous ferry services

## 📊 Data Sources

**Traffic Events:**
- **Endpoint**: `https://www.drivebc.ca/api/events/`
- **Coverage**: All traffic events in British Columbia

**Ferry Information:**
- **Endpoint**: `https://www.drivebc.ca/api/ferries/`
- **Coverage**: All inland ferry routes in British Columbia
- **Details**: Schedules, capacities, contact info, webcams

Both APIs are provided by the Government of British Columbia.

## 🆓 Cost

This service is completely free using:
- GitHub Actions (2000 minutes/month free)
- GitHub Pages (unlimited for public repositories)
- DriveBC API (free public API)

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the enhanced service (recommended)
python drivebc_service.py

# Run the alternative enhanced service
python drivebc_enhanced_service.py

# Run the original basic converter (traffic only)
python drivebc_to_kml.py

# Run tests
python run_tests.py

# Quick setup (Windows)
setup.bat

# Quick setup (Linux/macOS)
chmod +x setup.sh && ./setup.sh
```

### Development Options

**Enhanced Service (`drivebc_service.py`)**:
- Combines traffic events and ferry information
- Generates organized folder structure
- Fixed output filename: `drivebc_events.kml`
- Recommended for production use

**Basic Converter (`drivebc_to_kml.py`)**:
- Traffic events only
- Timestamped output filenames
- Good for testing and development

**Alternative Enhanced Service (`drivebc_enhanced_service.py`)**:
- Similar to main enhanced service
- May have different implementation details
- Available for comparison/backup

## 📝 License

MIT License - feel free to use and modify for your own projects.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues or questions:
- Create an issue in this repository
- Check DriveBC API status: https://www.drivebc.ca

---

*This service provides real-time traffic data for British Columbia. Data accuracy and availability depend on the DriveBC API.*
