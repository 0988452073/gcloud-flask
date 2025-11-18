#!/usr/bin/env python3
"""
Test script for Ingenic OSD functionality.
Run this script to test the OSD module without starting the Flask server.
"""

import cv2
import numpy as np
from osd_utils import IngenicOSD, OSDConfig, create_test_image


def test_basic_text():
    """Test basic text overlay."""
    print("Test 1: Basic text overlay")
    osd = IngenicOSD()
    image = create_test_image(640, 480)
    result = osd.add_text(image, "Hello Ingenic OSD!", position=(50, 50))
    cv2.imwrite('/tmp/test1_text.png', result)
    print("  ✓ Saved to /tmp/test1_text.png")


def test_timestamp():
    """Test timestamp overlay."""
    print("Test 2: Timestamp overlay")
    osd = IngenicOSD()
    image = create_test_image(640, 480)
    result = osd.add_timestamp(image, position=(10, 30))
    cv2.imwrite('/tmp/test2_timestamp.png', result)
    print("  ✓ Saved to /tmp/test2_timestamp.png")


def test_multiline():
    """Test multiline text overlay."""
    print("Test 3: Multiline text overlay")
    osd = IngenicOSD()
    image = create_test_image(640, 480)
    lines = [
        "Camera: Front Door",
        "Location: Entrance",
        "Status: Active",
        "FPS: 30"
    ]
    result = osd.add_multiline_text(image, lines, start_position=(10, 50))
    cv2.imwrite('/tmp/test3_multiline.png', result)
    print("  ✓ Saved to /tmp/test3_multiline.png")


def test_bounding_box():
    """Test bounding box overlay."""
    print("Test 4: Bounding box overlay")
    osd = IngenicOSD()
    image = create_test_image(640, 480)
    result = osd.add_box(image, (100, 100), (300, 300), 
                         color=(0, 255, 0), label="Person Detected")
    cv2.imwrite('/tmp/test4_box.png', result)
    print("  ✓ Saved to /tmp/test4_box.png")


def test_combined():
    """Test combined OSD elements."""
    print("Test 5: Combined OSD elements")
    osd = IngenicOSD()
    image = create_test_image(800, 600)
    
    # Add timestamp
    image = osd.add_timestamp(image, position=(10, 30))
    
    # Add camera info
    image = osd.add_text(image, "Camera: Main Entrance", position=(10, 70))
    
    # Add status info
    lines = ["Status: Recording", "Motion: Detected", "FPS: 30"]
    image = osd.add_multiline_text(image, lines, start_position=(10, 110))
    
    # Add multiple detection boxes
    image = osd.add_box(image, (200, 200), (400, 400), 
                       color=(0, 255, 0), label="Person")
    image = osd.add_box(image, (450, 150), (600, 300), 
                       color=(255, 0, 0), label="Vehicle")
    
    cv2.imwrite('/tmp/test5_combined.png', image)
    print("  ✓ Saved to /tmp/test5_combined.png")


def test_custom_config():
    """Test with custom OSD configuration."""
    print("Test 6: Custom OSD configuration")
    
    # Create custom config
    config = OSDConfig()
    config.font_scale = 1.5
    config.font_thickness = 3
    config.text_color = (0, 255, 255)  # Yellow
    config.bg_opacity = 0.7
    
    osd = IngenicOSD(config)
    image = create_test_image(640, 480)
    result = osd.add_text(image, "Large Yellow Text", position=(100, 250))
    cv2.imwrite('/tmp/test6_custom.png', result)
    print("  ✓ Saved to /tmp/test6_custom.png")


def test_real_image():
    """Test with a real camera-like image."""
    print("Test 7: Real-world scenario")
    
    # Create a more realistic test image
    image = np.zeros((720, 1280, 3), dtype=np.uint8)
    
    # Simulate a scene with gradient
    for i in range(720):
        for j in range(1280):
            image[i, j] = [30 + i//10, 50 + j//20, 70 + (i+j)//30]
    
    # Add some noise to simulate real camera
    noise = np.random.randint(-20, 20, image.shape, dtype=np.int16)
    image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    osd = IngenicOSD()
    
    # Add typical IP camera OSD elements
    image = osd.add_timestamp(image, position=(10, 35), 
                             format_str="%Y-%m-%d %H:%M:%S")
    image = osd.add_text(image, "CAM-01 | Front Gate", position=(10, 75))
    
    # Add detection info
    lines = [
        "Motion Detection: ON",
        "Recording: Active",
        "Objects: 2"
    ]
    image = osd.add_multiline_text(image, lines, start_position=(10, 650))
    
    # Add detection boxes
    image = osd.add_box(image, (300, 200), (500, 450), 
                       color=(0, 255, 0), thickness=2, label="Person")
    image = osd.add_box(image, (700, 300), (950, 500), 
                       color=(0, 255, 0), thickness=2, label="Person")
    
    cv2.imwrite('/tmp/test7_realistic.png', image)
    print("  ✓ Saved to /tmp/test7_realistic.png")


if __name__ == "__main__":
    print("=" * 50)
    print("Ingenic OSD Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_basic_text()
        test_timestamp()
        test_multiline()
        test_bounding_box()
        test_combined()
        test_custom_config()
        test_real_image()
        
        print()
        print("=" * 50)
        print("All tests completed successfully! ✓")
        print("Check /tmp/test*.png for results")
        print("=" * 50)
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
