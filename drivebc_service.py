"""
Enhanced DriveBC Service - Traffic Events + Ferry Information
Combines traffic events and ferry data into a comprehensive KML file
"""

import requests
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os
import sys
from typing import Dict, List, Any
import re


class EnhancedDriveBCService:
    """Enhanced DriveBC service combining traffic events and ferry information."""
    
    EVENTS_API_URL = "https://www.drivebc.ca/api/events/"
    FERRIES_API_URL = "https://www.drivebc.ca/api/ferries/"
    OUTPUT_FILENAME = "drivebc_events.kml"
    
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
        },
        # Ferry styles
        'FERRY_CABLE': {
            'color': 'ff800080',  # Purple
            'icon': 'http://maps.google.com/mapfiles/kml/shapes/ferry.png'
        },
        'FERRY_SCHEDULED': {
            'color': 'ff008080',  # Teal
            'icon': 'http://maps.google.com/mapfiles/kml/shapes/ferry.png'
        },
        'FERRY_ON_DEMAND': {
            'color': 'ff4B0082',  # Indigo
            'icon': 'http://maps.google.com/mapfiles/kml/shapes/ferry.png'
        },
        'FERRY_DEFAULT': {
            'color': 'ff800080',  # Purple
            'icon': 'http://maps.google.com/mapfiles/kml/shapes/ferry.png'
        }
    }
    
    def fetch_events(self) -> List[Dict[str, Any]]:
        """Fetch traffic events from DriveBC API."""
        try:
            print(f"[{datetime.now()}] Fetching traffic events from DriveBC API...")
            response = requests.get(self.EVENTS_API_URL, timeout=30)
            response.raise_for_status()
            
            events = response.json()
            print(f"[{datetime.now()}] Successfully fetched {len(events)} traffic events")
            return events
            
        except Exception as e:
            print(f"[{datetime.now()}] Error fetching traffic events: {e}")
            return []
    
    def fetch_ferries(self) -> List[Dict[str, Any]]:
        """Fetch ferry information from DriveBC API."""
        try:
            print(f"[{datetime.now()}] Fetching ferry information from DriveBC API...")
            response = requests.get(self.FERRIES_API_URL, timeout=30)
            response.raise_for_status()
            
            ferries = response.json()
            print(f"[{datetime.now()}] Successfully fetched {len(ferries)} ferry routes")
            return ferries
            
        except Exception as e:
            print(f"[{datetime.now()}] Error fetching ferry data: {e}")
            return []
    
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
    
    def clean_html(self, text: str) -> str:
        """Clean HTML tags from text."""
        if not text:
            return ""
        # Remove HTML tags
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()
    
    def get_ferry_style_key(self, ferry: Dict[str, Any]) -> str:
        """Determine ferry style based on ferry characteristics."""
        route_name = ferry.get('route_name', '').lower()
        
        if 'cable' in route_name:
            return 'FERRY_CABLE'
        
        vessels = ferry.get('vessels', [])
        if vessels:
            schedule_type = vessels[0].get('schedule_type', '').lower()
            if 'scheduled' in schedule_type:
                return 'FERRY_SCHEDULED'
            elif 'demand' in schedule_type:
                return 'FERRY_ON_DEMAND'
        
        return 'FERRY_DEFAULT'
    
    def create_kml_document(self) -> tuple:
        """Create the root KML document structure."""
        kml = ET.Element('kml')
        kml.set('xmlns', 'http://www.opengis.net/kml/2.2')
        
        document = ET.SubElement(kml, 'Document')
        
        # Add document metadata
        name = ET.SubElement(document, 'name')
        name.text = 'DriveBC Traffic Events & Ferry Information (Live)'
        
        description = ET.SubElement(document, 'description')
        description.text = f'''
        Live traffic events and ferry information from DriveBC API
        Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
        
        Includes:
        • Traffic events (construction, incidents, road conditions, weather)
        • Ferry routes and schedules
        • Contact information and webcam links
        '''
        
        # Add styles for different event types and ferries
        for style_type, style_info in self.EVENT_STYLES.items():
            style = ET.SubElement(document, 'Style')
            style.set('id', f'style_{style_type}')
            
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
    
    def create_traffic_placemark(self, event: Dict[str, Any], parent: ET.Element) -> None:
        """Create a KML placemark for a traffic event."""
        placemark = ET.SubElement(parent, 'Placemark')
        
        # Add name
        name = ET.SubElement(placemark, 'name')
    name.text = event.get('description', 'Traffic Event')
        
        # Add description with event details
        description = ET.SubElement(placemark, 'description')
    desc_text = f"""
    <![CDATA[
    <h3>Traffic Event Details</h3>
    <b>Event Type:</b> {event.get('event_type', 'Unknown')}<br/>
    <b>Sub Type:</b> {event.get('event_sub_type', 'Unknown')}<br/>
    <b>Status:</b> {event.get('status', 'Unknown')}<br/>
    <b>Direction:</b> {event.get('direction', 'Unknown')}<br/>
    <b>Route:</b> {event.get('route_at', 'Unknown')}<br/>
    <b>Location:</b> {event.get('location_description', 'No description')}<br/>
    <b>Closest Landmark:</b> {event.get('closest_landmark', 'Unknown')}<br/>
    <b>Incident Level:</b> {event.get('incident_level', 'Unknown')}<br/>
    <b>Last Updated:</b> {event.get('last_updated', 'Unknown')}<br/>
    <b>Next Update:</b> {event.get('next_update', 'Unknown')}<br/>
    <b>Closed:</b> {'Yes' if event.get('closed') else 'No'}<br/>
    <hr/>
    <b>ID:</b> {event.get('id', 'Unknown')}
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
    
    def create_ferry_placemark(self, ferry: Dict[str, Any], parent: ET.Element) -> None:
        """Create a KML placemark for a ferry route."""
        placemark = ET.SubElement(parent, 'Placemark')
        
        # Add name
        name = ET.SubElement(placemark, 'name')
        name.text = ferry.get('route_name', 'Ferry Route')
        
        # Extract vessel information
        vessels = ferry.get('vessels', [])
        vessel_info = ""
        if vessels:
            vessel = vessels[0]  # Use first vessel for main info
            vessel_info = f"""
            <h4>Vessel Information</h4>
            <b>Name:</b> {vessel.get('name') or 'Unnamed'}<br/>
            <b>Vehicle Capacity:</b> {vessel.get('vehicle_capacity') or 'N/A'}<br/>
            <b>Passenger Capacity:</b> {vessel.get('passenger_capacity') or 'N/A'}<br/>
            <b>Crossing Time:</b> {vessel.get('crossing_time_min') or 'N/A'} minutes<br/>
            <b>Weight Capacity:</b> {vessel.get('weight_capacity_kg') or 'N/A'} kg<br/>
            <b>Schedule Type:</b> {vessel.get('schedule_type', 'Unknown')}<br/>
            """
            
            if vessel.get('special_restriction'):
                vessel_info += f"<b>Special Restrictions:</b> {vessel.get('special_restriction')}<br/>"
        
        # Build contact information
        contact_info = ""
        if ferry.get('contact_org'):
            contact_info = f"""
            <h4>Contact Information</h4>
            <b>Organization:</b> {ferry.get('contact_org')}<br/>
            """
            if ferry.get('contact_phone'):
                contact_info += f"<b>Phone:</b> {ferry.get('contact_phone')}<br/>"
            if ferry.get('contact_alt_phone'):
                contact_info += f"<b>Alt Phone:</b> {ferry.get('contact_alt_phone')}<br/>"
            if ferry.get('contact_email'):
                contact_info += f"<b>Email:</b> <a href='mailto:{ferry.get('contact_email')}'>{ferry.get('contact_email')}</a><br/>"
        
        # Build webcam links
        webcam_info = ""
        webcam_urls = [ferry.get(f'webcam_url_{i}') for i in range(1, 6) if ferry.get(f'webcam_url_{i}')]
        if webcam_urls:
            webcam_info = "<h4>Live Webcams</h4>"
            for i, url in enumerate(webcam_urls, 1):
                webcam_info += f"<a href='{url}' target='_blank'>Webcam {i}</a><br/>"
        
        # Add description with ferry details
        description = ET.SubElement(placemark, 'description')
        schedule_detail = self.clean_html(vessels[0].get('schedule_detail', '')) if vessels else ''
        
        desc_text = f"""
        <![CDATA[
        <h3>🚢 {ferry.get('route_name', 'Ferry Route')}</h3>
        <p>{ferry.get('route_description', 'No description available')}</p>
        
        {vessel_info}
        
        <h4>Schedule Information</h4>
        {schedule_detail}
        
        {contact_info}
        
        {webcam_info}
        
        <p><b>Last Updated:</b> {ferry.get('feed_modified_at', 'Unknown')}</p>
        
        <p><a href="{ferry.get('url', '#')}" target="_blank">More Information</a></p>
        ]]>
        """
        description.text = desc_text
        
        # Add style reference
        style_key = self.get_ferry_style_key(ferry)
        style_url = ET.SubElement(placemark, 'styleUrl')
        style_url.text = f'#style_{style_key}'
        
        # Add geometry (ferry location)
        location_data = ferry.get('location', {})
        coordinates = self.extract_coordinates(location_data)
        
        if coordinates:
            point = ET.SubElement(placemark, 'Point')
            coord_text = ET.SubElement(point, 'coordinates')
            lon, lat = coordinates[0][:2]
            coord_text.text = f'{lon},{lat},0'
    
    def generate_kml(self, output_path: str = None) -> str:
        """Generate comprehensive KML file from current events and ferry data."""
        if output_path is None:
            output_path = self.OUTPUT_FILENAME
        
        # Fetch both data sources
        events = self.fetch_events()
        ferries = self.fetch_ferries()
        
        total_items = len(events) + len(ferries)
        print(f"[{datetime.now()}] Converting {total_items} items to KML ({len(events)} events, {len(ferries)} ferries)...")
        
        kml_root, document = self.create_kml_document()
        
        # Create folder for traffic events
        if events:
            events_folder = ET.SubElement(document, 'Folder')
            events_folder_name = ET.SubElement(events_folder, 'name')
            events_folder_name.text = f'🚗 Traffic Events ({len(events)})'
            
            # Group events by type
            event_folders = {}
            for event in events:
                event_type = event.get('event_type', 'OTHER')
                
                if event_type not in event_folders:
                    folder = ET.SubElement(events_folder, 'Folder')
                    folder_name = ET.SubElement(folder, 'name')
                    folder_name.text = f'{event_type.replace("_", " ").title()} Events'
                    event_folders[event_type] = folder
                
                self.create_traffic_placemark(event, event_folders[event_type])
        
        # Create folder for ferry information
        if ferries:
            ferries_folder = ET.SubElement(document, 'Folder')
            ferries_folder_name = ET.SubElement(ferries_folder, 'name')
            ferries_folder_name.text = f'⛴️ Ferry Routes ({len(ferries)})'
            
            # Group ferries by type
            ferry_folders = {}
            for ferry in ferries:
                style_key = self.get_ferry_style_key(ferry)
                folder_name_map = {
                    'FERRY_CABLE': 'Cable Ferries',
                    'FERRY_SCHEDULED': 'Scheduled Ferries',
                    'FERRY_ON_DEMAND': 'On-Demand Ferries',
                    'FERRY_DEFAULT': 'Other Ferries'
                }
                folder_name = folder_name_map.get(style_key, 'Other Ferries')
                
                if folder_name not in ferry_folders:
                    folder = ET.SubElement(ferries_folder, 'Folder')
                    folder_name_element = ET.SubElement(folder, 'name')
                    folder_name_element.text = folder_name
                    ferry_folders[folder_name] = folder
                
                self.create_ferry_placemark(ferry, ferry_folders[folder_name])
        
        # Convert to string with pretty printing
        rough_string = ET.tostring(kml_root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        kml_content = reparsed.toprettyxml(indent="  ")
        
        # Save to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(kml_content)
            
            print(f"[{datetime.now()}] Enhanced KML file saved as: {output_path}")
            print(f"[{datetime.now()}] Contains {len(events)} traffic events and {len(ferries)} ferry routes")
            return output_path
            
        except IOError as e:
            print(f"[{datetime.now()}] Error saving file: {e}")
            raise


def main():
    """Main function for enhanced service execution."""
    print(f"[{datetime.now()}] Enhanced DriveBC Service Starting...")
    print("Fetching traffic events AND ferry information...")
    
    try:
        service = EnhancedDriveBCService()
        output_file = service.generate_kml()
        print(f"[{datetime.now()}] Enhanced service completed successfully!")
        print(f"Output: {output_file}")
        
    except Exception as e:
        print(f"[{datetime.now()}] Enhanced service failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
