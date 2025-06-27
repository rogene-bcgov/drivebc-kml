"""
DriveBC to KML Service - Simplified version for automated updates

This script is optimized for running as a service that generates a fixed-name KML file
for automatic updates in Google Maps.
"""

import requests
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os
import sys
from typing import Dict, List, Any


class DriveBCService:
    """Simplified DriveBC to KML converter for service use."""
    
    API_URL = "https://www.drivebc.ca/api/events/"
    OUTPUT_FILENAME = "drivebc_events.kml"  # Fixed filename for automatic updates
    
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
    
    def fetch_events(self) -> List[Dict[str, Any]]:
        """Fetch events from DriveBC API."""
        try:
            print(f"[{datetime.now()}] Fetching events from DriveBC API...")
            response = requests.get(self.API_URL, timeout=30)
            response.raise_for_status()
            
            events = response.json()
            print(f"[{datetime.now()}] Successfully fetched {len(events)} events")
            return events
            
        except Exception as e:
            print(f"[{datetime.now()}] Error fetching data: {e}")
            raise
    
    def extract_coordinates(self, location_data: Dict[str, Any]) -> List[List[float]]:
        """Extract coordinates from location data."""
        coordinates = []
        
        if location_data and location_data.get('type') == 'LineString':
            coordinates = location_data.get('coordinates', [])
        elif location_data and location_data.get('type') == 'Point':
            coords = location_data.get('coordinates', [])
            if len(coords) >= 2:
                coordinates = [coords]
                
        return coordinates
    
    def create_kml_document(self) -> tuple:
        """Create the root KML document structure."""
        kml = ET.Element('kml')
        kml.set('xmlns', 'http://www.opengis.net/kml/2.2')
        
        document = ET.SubElement(kml, 'Document')
        
        # Add document metadata
        name = ET.SubElement(document, 'name')
        name.text = 'DriveBC Traffic Events (Live)'
        
        description = ET.SubElement(document, 'description')
        description.text = f'Live traffic events from DriveBC API - Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}'
        
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
        """Create a KML placemark for an event."""
        placemark = ET.SubElement(parent, 'Placemark')
        
        # Add name
        name = ET.SubElement(placemark, 'name')
        name.text = event.get('description', 'Traffic Event')[:100]
        
        # Add description with event details
        description = ET.SubElement(placemark, 'description')
        desc_text = f"""
        <![CDATA[
        <b>Event Type:</b> {event.get('event_type', 'Unknown')}<br/>
        <b>Sub Type:</b> {event.get('event_sub_type', 'Unknown')}<br/>
        <b>Status:</b> {event.get('status', 'Unknown')}<br/>
        <b>Direction:</b> {event.get('direction', 'Unknown')}<br/>
        <b>Route:</b> {event.get('route_at', 'Unknown')}<br/>
        <b>Location:</b> {event.get('location_description', 'No description')}<br/>
        <b>Last Updated:</b> {event.get('last_updated', 'Unknown')}<br/>
        <b>Closed:</b> {'Yes' if event.get('closed') else 'No'}
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
                lon, lat = coordinates[0][:2]
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
    
    def generate_kml(self, output_path: str = None) -> str:
        """Generate KML file from current events."""
        if output_path is None:
            output_path = self.OUTPUT_FILENAME
        
        # Fetch events
        events = self.fetch_events()
        
        print(f"[{datetime.now()}] Converting {len(events)} events to KML...")
        
        kml_root, document = self.create_kml_document()
        
        # Group events by type
        event_folders = {}
        
        for event in events:
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
        kml_content = reparsed.toprettyxml(indent="  ")
        
        # Save to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(kml_content)
            
            print(f"[{datetime.now()}] KML file saved as: {output_path}")
            return output_path
            
        except IOError as e:
            print(f"[{datetime.now()}] Error saving file: {e}")
            raise


def main():
    """Main function for service execution."""
    print(f"[{datetime.now()}] DriveBC KML Service Starting...")
    
    try:
        service = DriveBCService()
        output_file = service.generate_kml()
        print(f"[{datetime.now()}] Service completed successfully. Output: {output_file}")
        
    except Exception as e:
        print(f"[{datetime.now()}] Service failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
