# DriveBC KML Service

A simple web service that automatically converts DriveBC traffic events to KML format every 30 minutes.

## 🚀 Live Service

The service is automatically deployed and running at:
- **KML File**: `https://rogene-bcgov.github.io/drivebc-kml/drivebc_events.kml`
- **Web Interface**: `https://rogene-bcgov.github.io/drivebc-kml/`

## 📋 Features

- 🔄 **Auto-updates every 30 minutes** via GitHub Actions
- 📍 **Fixed filename** (`drivebc_events.kml`) for Google Maps auto-refresh
- 🌐 **Public access** via GitHub Pages
- 🎨 **Color-coded events** by type (construction, incidents, weather, etc.)
- 📱 **Simple web interface** with usage instructions

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
├── drivebc_service.py          # Simplified service script
├── drivebc_events.kml          # Generated KML file (auto-updated)
├── index.html                  # Web interface
├── .github/workflows/
│   └── update-kml.yml          # GitHub Actions workflow
└── README.md                   # This file
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

- 🔴 **Construction** - Road construction and maintenance
- 🟡 **Incidents** - Accidents and traffic disruptions  
- 🟢 **Road Conditions** - Weather-related road conditions
- 🔵 **Weather** - Weather-related traffic impacts
- ⚪ **Other** - Miscellaneous events

## 🔄 Update Frequency

The service updates every 30 minutes. You can also trigger manual updates:
- Via GitHub Actions web interface
- By pushing commits to the repository

## 📊 API Source

Data is sourced from the official DriveBC API:
- **Endpoint**: `https://www.drivebc.ca/api/events/`
- **Provider**: Government of British Columbia
- **Coverage**: British Columbia, Canada

## 🆓 Cost

This service is completely free using:
- GitHub Actions (2000 minutes/month free)
- GitHub Pages (unlimited for public repositories)
- DriveBC API (free public API)

## 🔧 Local Development

```bash
# Install dependencies
pip install requests

# Run locally
python drivebc_service.py

# Test the original converter
python drivebc_to_kml.py
```

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
