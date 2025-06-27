"""
Simple test script to verify Python and dependencies are working.
"""

def test_basic_functionality():
    """Test basic Python functionality."""
    print("Testing Python basic functionality...")
    
    # Test basic Python operations
    result = 2 + 2
    assert result == 4, "Basic math failed"
    print("✓ Basic math operations working")
    
    # Test string operations
    text = "Hello, World!"
    assert len(text) == 13, "String operations failed"
    print("✓ String operations working")
    
    # Test list operations
    data = [1, 2, 3, 4, 5]
    assert sum(data) == 15, "List operations failed"
    print("✓ List operations working")
    
    print("All basic tests passed!")

def test_imports():
    """Test required imports."""
    print("\nTesting required imports...")
    
    try:
        import json
        print("✓ json module available")
    except ImportError:
        print("✗ json module not available")
        return False
    
    try:
        import xml.etree.ElementTree as ET
        print("✓ xml.etree.ElementTree module available")
    except ImportError:
        print("✗ xml.etree.ElementTree module not available")
        return False
    
    try:
        from xml.dom import minidom
        print("✓ xml.dom.minidom module available")
    except ImportError:
        print("✗ xml.dom.minidom module not available")
        return False
    
    try:
        from datetime import datetime
        print("✓ datetime module available")
    except ImportError:
        print("✗ datetime module not available")
        return False
    
    try:
        import requests
        print("✓ requests module available")
        return True
    except ImportError:
        print("✗ requests module not available")
        print("  Run: pip install requests")
        return False

if __name__ == "__main__":
    print("DriveBC to KML Converter - Test Script")
    print("=" * 40)
    
    test_basic_functionality()
    
    if test_imports():
        print("\n✓ All required modules are available!")
        print("Ready to run drivebc_to_kml.py")
    else:
        print("\n✗ Some required modules are missing.")
        print("Please install missing dependencies.")
