"""
Example usage of the DriveBC to KML converter.

This file demonstrates different ways to use the converter programmatically.
"""

from drivebc_to_kml import DriveBCToKMLConverter

def basic_conversion():
    """Basic conversion example."""
    print("=== Basic Conversion Example ===")
    
    # Create converter
    converter = DriveBCToKMLConverter()
    
    # Fetch and convert
    if converter.fetch_events():
        kml_content = converter.convert_to_kml()
        output_file = converter.save_kml(kml_content)
        print(f"Conversion complete! Output: {output_file}")
    else:
        print("Failed to fetch events")

def custom_filename_example():
    """Example with custom filename."""
    print("\n=== Custom Filename Example ===")
    
    converter = DriveBCToKMLConverter()
    
    if converter.fetch_events():
        kml_content = converter.convert_to_kml()
        
        # Save with custom filename
        custom_filename = "my_traffic_map.kml"
        output_file = converter.save_kml(kml_content, custom_filename)
        print(f"Saved as: {output_file}")

def filtering_example():
    """Example of filtering events by type."""
    print("\n=== Filtering Example ===")
    
    converter = DriveBCToKMLConverter()
    
    if converter.fetch_events():
        # Filter for construction events only
        construction_events = [
            event for event in converter.events_data 
            if event.get('event_type') == 'CONSTRUCTION'
        ]
        
        print(f"Total events: {len(converter.events_data)}")
        print(f"Construction events: {len(construction_events)}")
        
        # Temporarily replace events data with filtered data
        original_data = converter.events_data
        converter.events_data = construction_events
        
        # Convert filtered data
        kml_content = converter.convert_to_kml()
        output_file = converter.save_kml(kml_content, "construction_only.kml")
        
        # Restore original data
        converter.events_data = original_data
        
        print(f"Construction-only KML saved as: {output_file}")

def inspect_data_example():
    """Example of inspecting the raw data."""
    print("\n=== Data Inspection Example ===")
    
    converter = DriveBCToKMLConverter()
    
    if converter.fetch_events():
        print(f"Total events: {len(converter.events_data)}")
        
        # Count events by type
        event_types = {}
        for event in converter.events_data:
            event_type = event.get('event_type', 'UNKNOWN')
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        print("\nEvent types breakdown:")
        for event_type, count in sorted(event_types.items()):
            print(f"  {event_type}: {count}")
        
        # Show sample event
        if converter.events_data:
            print("\nSample event:")
            sample = converter.events_data[0]
            print(f"  ID: {sample.get('id', 'N/A')}")
            print(f"  Type: {sample.get('event_type', 'N/A')}")
            print(f"  Description: {sample.get('description', 'N/A')[:100]}...")
            print(f"  Status: {sample.get('status', 'N/A')}")
            print(f"  Route: {sample.get('route_at', 'N/A')}")

if __name__ == "__main__":
    print("DriveBC to KML Converter - Usage Examples")
    print("=" * 50)
    
    try:
        # Run examples
        basic_conversion()
        custom_filename_example()
        filtering_example()
        inspect_data_example()
        
        print("\n=== All Examples Complete ===")
        print("Check the generated KML files in this directory.")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have internet connectivity and the requests library installed.")
