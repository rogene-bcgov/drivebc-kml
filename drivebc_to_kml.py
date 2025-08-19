"""
DriveBC to KML Converter

This script fetches traffic event data from the DriveBC API and converts it to KML format
for use in Google Maps as a custom layer.

Features:
- Fetches live traffic events from DriveBC API
- Converts different event types (construction, incidents, etc.) to KML
- Applies appropriate styling based on event type
- Outputs KML file compatible with Google Maps
"""

import requests
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import sys
import os
from typing import Dict, List, Any


class DriveBCToKMLConverter:
    """Converts DriveBC events data to KML format."""
    
    # DriveBC API endpoint
    API_URL = "https://www.drivebc.ca/api/events/"
    
    # Event type styling
    EVENT_STYLES = {
        'CONSTRUCTION': {
            'color': 'ff0000ff',  # Red
            'icon': 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png'
        },
        'INCIDENT': {
            'color': 'ff00ffff',  # Yellow
            'icon': 'http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png'
        },
        'ROAD_CONDITION': {
            'color': 'ff00ff00',  # Green
            'icon': 'http://maps.google.com/mapfiles/kml/paddle/grn-circle.png'
        },
        'WEATHER': {
            'color': 'ffff0000',  # Blue
            'icon': 'http://maps.google.com/mapfiles/kml/paddle/blu-circle.png'
        },
        'DEFAULT': {
            'color': 'ff888888',  # Gray
            'icon': 'http://maps.google.com/mapfiles/kml/paddle/wht-circle.png'
        }
    }
    
    def __init__(self):
        """Initialize the converter."""
        self.events_data = None
        
    def fetch_events(self) -> bool:
        """
        Fetch events data from DriveBC API.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("Fetching events from DriveBC API...")
            response = requests.get(self.API_URL, timeout=30)
            response.raise_for_status()
            
            self.events_data = response.json()
            print(f"Successfully fetched {len(self.events_data)} events")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return False
            
    def extract_coordinates(self, location_data: Dict[str, Any]) -> List[List[float]]:
        """
        Extract coordinates from location data.
        
        Args:
            location_data: Location information from event
            
        Returns:
            List of [longitude, latitude] pairs
        """
        coordinates = []
        
        if location_data and location_data.get('type') == 'LineString':
            coords = location_data.get('coordinates', [])
            # LineString coordinates are [longitude, latitude] pairs
            coordinates = coords
        elif location_data and location_data.get('type') == 'Point':
            coords = location_data.get('coordinates', [])
            if len(coords) >= 2:
                coordinates = [coords]
                
        return coordinates
    
    def get_event_style(self, event_type: str) -> Dict[str, str]:
        """
        Get styling information for an event type.
        
        Args:
            event_type: Type of event
            
        Returns:
            Dictionary with color and icon information
        """
        return self.EVENT_STYLES.get(event_type, self.EVENT_STYLES['DEFAULT'])
    
    def create_kml_document(self) -> ET.Element:
        """
        Create the root KML document structure.
        
        Returns:
            Root KML element
        """
        kml = ET.Element('kml')
        kml.set('xmlns', 'http://www.opengis.net/kml/2.2')
        
        document = ET.SubElement(kml, 'Document')
        
        # Add document metadata
        name = ET.SubElement(document, 'name')
        name.text = 'DriveBC Traffic Events'
        
        description = ET.SubElement(document, 'description')
        description.text = f'Traffic events from DriveBC API - Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        
        # Add styles for different event types
        for event_type, style_info in self.EVENT_STYLES.items():
            style = ET.SubElement(document, 'Style')
            style.set('id', f'style_{event_type}')
            
            icon_style = ET.SubElement(style, 'IconStyle')
            color = ET.SubElement(icon_style, 'color')
            color.text = style_info['color']
            
            icon = ET.SubElement(icon_style, 'Icon')
            href = ET.SubElement(icon, 'href')
            href.text = style_info['icon']
            
            # Line style for routes
            line_style = ET.SubElement(style, 'LineStyle')
            line_color = ET.SubElement(line_style, 'color')
            line_color.text = style_info['color']
            line_width = ET.SubElement(line_style, 'width')
            line_width.text = '3'
        
        return kml, document
    
    def create_placemark(self, event: Dict[str, Any], parent: ET.Element) -> None:
        """
        Create a KML placemark for an event.
        
        Args:
            event: Event data
            parent: Parent XML element to add placemark to
        """
        placemark = ET.SubElement(parent, 'Placemark')
        
        # Add name - use route and location info instead of truncated description
        name = ET.SubElement(placemark, 'name')
        route_info = event.get('route_at', '')
        location_info = event.get('location_description', '')
        event_id = event.get('id', '')
        
        # Create a more informative, shorter name
        if route_info and location_info:
            name_text = f"{route_info} - {location_info}"
        elif route_info:
            name_text = route_info
        elif location_info:
            name_text = location_info
        else:
            name_text = event.get('description', 'Traffic Event')
        
        # Add event ID to name for uniqueness
        if event_id:
            name_text = f"[{event_id}] {name_text}"
        
        name.text = name_text
        
        # Add description with event details
        description = ET.SubElement(placemark, 'description')
        
        # Format next update
        next_update = event.get('next_update')
        next_update_text = next_update if next_update else 'No scheduled update'
        
        # Format severity/incident level
        severity = event.get('severity', 'Unknown')
        
        # Format closest landmark
        closest_landmark = event.get('closest_landmark', 'Not specified')
        
        # Format start and end times
        start_time = event.get('start', 'Unknown')
        end_time = event.get('end', 'Unknown')
        
        desc_text = f"""
        <![CDATA[
        <h3>Traffic Event Details</h3>
        <b>Event ID:</b> {event.get('id', 'Unknown')}<br/>
        <b>Event Type:</b> {event.get('event_type', 'Unknown')}<br/>
        <b>Sub Type:</b> {event.get('event_sub_type', 'Unknown')}<br/>
        <b>Severity/Incident Level:</b> {severity}<br/>
        <b>Status:</b> {event.get('status', 'Unknown')}<br/>
        <b>Direction:</b> {event.get('direction', 'Unknown')}<br/>
        <b>Route:</b> {event.get('route_at', 'Unknown')}<br/>
        <b>Location:</b> {event.get('location_description', 'No description')}<br/>
        <b>Closest Landmark:</b> {closest_landmark}<br/>
        <b>Start Time:</b> {start_time}<br/>
        <b>End Time:</b> {end_time}<br/>
        <b>Last Updated:</b> {event.get('last_updated', 'Unknown')}<br/>
        <b>Next Update:</b> {next_update_text}<br/>
        <b>Closed:</b> {'Yes' if event.get('closed') else 'No'}<br/>
        <hr/>
        <b>Full Description:</b><br/>
        {event.get('description', 'No description available')}
        ]]>
        """
        description.text = desc_text
        
        # Add style reference
        event_type = event.get('event_type', 'DEFAULT')
        style_url = ET.SubElement(placemark, 'styleUrl')
        style_url.text = f'#style_{event_type}'
        
        # Add geometry
        location_data = event.get('location', {})
        coordinates = self.extract_coordinates(location_data)
        
        if coordinates:
            if len(coordinates) == 1:
                # Single point
                point = ET.SubElement(placemark, 'Point')
                coord_text = ET.SubElement(point, 'coordinates')
                lon, lat = coordinates[0][:2]  # Take only lon, lat (ignore elevation if present)
                coord_text.text = f'{lon},{lat},0'
            else:
                # Line string for routes
                linestring = ET.SubElement(placemark, 'LineString')
                tessellate = ET.SubElement(linestring, 'tessellate')
                tessellate.text = '1'
                
                coord_text = ET.SubElement(linestring, 'coordinates')
                coord_pairs = []
                for coord in coordinates:
                    if len(coord) >= 2:
                        lon, lat = coord[:2]
                        coord_pairs.append(f'{lon},{lat},0')
                coord_text.text = ' '.join(coord_pairs)
    
    def convert_to_kml(self) -> str:
        """
        Convert the events data to KML format.
        
        Returns:
            KML content as string
        """
        if not self.events_data:
            raise ValueError("No events data available. Call fetch_events() first.")
        
        print("Converting events to KML format...")
        
        kml_root, document = self.create_kml_document()
        
        # Group events by type for organization
        event_folders = {}
        
        for event in self.events_data:
            event_type = event.get('event_type', 'OTHER')
            
            if event_type not in event_folders:
                folder = ET.SubElement(document, 'Folder')
                folder_name = ET.SubElement(folder, 'name')
                folder_name.text = f'{event_type.replace("_", " ").title()} Events'
                event_folders[event_type] = folder
            
            self.create_placemark(event, event_folders[event_type])
        
        # Convert to string with pretty printing
        rough_string = ET.tostring(kml_root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        
        print(f"Successfully converted {len(self.events_data)} events to KML")
        return reparsed.toprettyxml(indent="  ")
    
    def save_kml(self, kml_content: str, filename: str = None, output_dir: str = None) -> str:
        """
        Save KML content to file.
        
        Args:
            kml_content: KML content string
            filename: Output filename (optional)
            output_dir: Output directory (optional, defaults to 'exports' folder)
            
        Returns:
            Path to saved file
        """
        # Set default output directory to 'exports'
        if output_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(script_dir, 'exports')
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"drivebc_events_{timestamp}.kml"
        
        # Construct full file path
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(kml_content)
            
            print(f"KML file saved as: {filepath}")
            return filepath
            
        except IOError as e:
            print(f"Error saving file: {e}")
            raise


def main():
    """Main function to run the converter."""
    print("DriveBC to KML Converter")
    print("=" * 30)
    
    converter = DriveBCToKMLConverter()
    
    # Fetch events data
    if not converter.fetch_events():
        print("Failed to fetch events data. Exiting.")
        sys.exit(1)
    
    try:
        # Convert to KML
        kml_content = converter.convert_to_kml()
        
        # Save to file
        output_file = converter.save_kml(kml_content)
        
        print("\nConversion completed successfully!")
        print(f"Output file: {output_file}")
        print("\nTo use in Google Maps:")
        print("1. Go to https://mymaps.google.com")
        print("2. Create a new map or open an existing one")
        print("3. Click 'Import' and upload the KML file")
        print("4. The traffic events will appear as a new layer")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
