"""
OSD (On-Screen Display) utility module for Ingenic devices.
Provides functions to overlay text, timestamps, and graphics on images.
"""

import cv2
import numpy as np
from datetime import datetime
from typing import Tuple, Optional


class OSDConfig:
    """Configuration for OSD rendering."""
    
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1.0
        self.font_thickness = 2
        self.text_color = (255, 255, 255)  # White
        self.bg_color = (0, 0, 0)  # Black background
        self.bg_opacity = 0.5
        self.position = (10, 30)  # Default position (x, y)
        self.line_spacing = 10


class IngenicOSD:
    """Main OSD class for rendering text and graphics on images."""
    
    def __init__(self, config: Optional[OSDConfig] = None):
        """
        Initialize OSD with configuration.
        
        Args:
            config: OSD configuration object. If None, uses default config.
        """
        self.config = config or OSDConfig()
    
    def add_text(self, image: np.ndarray, text: str, 
                 position: Optional[Tuple[int, int]] = None,
                 color: Optional[Tuple[int, int, int]] = None) -> np.ndarray:
        """
        Add text overlay to image.
        
        Args:
            image: Input image as numpy array (BGR format)
            text: Text to overlay
            position: Position (x, y) for text. If None, uses config default
            color: Text color (B, G, R). If None, uses config default
            
        Returns:
            Image with text overlay
        """
        if image is None or len(image.shape) < 2:
            raise ValueError("Invalid image")
        
        # Make a copy to avoid modifying original
        output = image.copy()
        
        # Use provided values or defaults from config
        pos = position or self.config.position
        text_color = color or self.config.text_color
        
        # Get text size for background rectangle
        (text_width, text_height), baseline = cv2.getTextSize(
            text, 
            self.config.font, 
            self.config.font_scale, 
            self.config.font_thickness
        )
        
        # Draw semi-transparent background
        x, y = pos
        padding = 5
        overlay = output.copy()
        cv2.rectangle(
            overlay,
            (x - padding, y - text_height - padding),
            (x + text_width + padding, y + baseline + padding),
            self.config.bg_color,
            -1
        )
        
        # Blend background with original image
        cv2.addWeighted(
            overlay, 
            self.config.bg_opacity, 
            output, 
            1 - self.config.bg_opacity, 
            0, 
            output
        )
        
        # Draw text
        cv2.putText(
            output,
            text,
            pos,
            self.config.font,
            self.config.font_scale,
            text_color,
            self.config.font_thickness,
            cv2.LINE_AA
        )
        
        return output
    
    def add_timestamp(self, image: np.ndarray, 
                     position: Optional[Tuple[int, int]] = None,
                     format_str: str = "%Y-%m-%d %H:%M:%S") -> np.ndarray:
        """
        Add current timestamp to image.
        
        Args:
            image: Input image as numpy array
            position: Position for timestamp. If None, uses config default
            format_str: Datetime format string
            
        Returns:
            Image with timestamp overlay
        """
        timestamp = datetime.now().strftime(format_str)
        return self.add_text(image, timestamp, position)
    
    def add_multiline_text(self, image: np.ndarray, 
                          lines: list,
                          start_position: Optional[Tuple[int, int]] = None) -> np.ndarray:
        """
        Add multiple lines of text to image.
        
        Args:
            image: Input image as numpy array
            lines: List of text lines to display
            start_position: Starting position (x, y). If None, uses config default
            
        Returns:
            Image with multiline text overlay
        """
        output = image.copy()
        start_pos = start_position or self.config.position
        x, y = start_pos
        
        # Calculate line height
        (_, text_height), baseline = cv2.getTextSize(
            "Ay",  # Sample text with ascender and descender
            self.config.font,
            self.config.font_scale,
            self.config.font_thickness
        )
        line_height = text_height + baseline + self.config.line_spacing
        
        # Add each line
        for i, line in enumerate(lines):
            current_y = y + (i * line_height)
            output = self.add_text(output, line, position=(x, current_y))
        
        return output
    
    def add_box(self, image: np.ndarray, 
                top_left: Tuple[int, int],
                bottom_right: Tuple[int, int],
                color: Tuple[int, int, int] = (0, 255, 0),
                thickness: int = 2,
                label: Optional[str] = None) -> np.ndarray:
        """
        Add bounding box to image, optionally with label.
        
        Args:
            image: Input image as numpy array
            top_left: Top-left corner (x, y)
            bottom_right: Bottom-right corner (x, y)
            color: Box color (B, G, R)
            thickness: Line thickness
            label: Optional label text above box
            
        Returns:
            Image with bounding box
        """
        output = image.copy()
        
        # Draw rectangle
        cv2.rectangle(output, top_left, bottom_right, color, thickness)
        
        # Add label if provided
        if label:
            label_pos = (top_left[0], top_left[1] - 10)
            if label_pos[1] < 20:  # Ensure label is visible
                label_pos = (top_left[0], top_left[1] + 20)
            output = self.add_text(output, label, position=label_pos, color=color)
        
        return output


def create_test_image(width: int = 640, height: int = 480) -> np.ndarray:
    """
    Create a test image for OSD demonstration.
    
    Args:
        width: Image width
        height: Image height
        
    Returns:
        Test image as numpy array
    """
    # Create a gradient image
    image = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(height):
        color_value = int(255 * i / height)
        image[i, :] = [color_value // 2, color_value, color_value // 3]
    
    return image
