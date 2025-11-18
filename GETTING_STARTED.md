# Getting Started with Ingenic OSD

This guide will help you quickly get started with the Ingenic OSD API.

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python app.py
```

The server will start on `http://0.0.0.0:8080`

### 3. Test the API

Open your browser and visit:
- `http://localhost:8080/` - Welcome page
- `http://localhost:8080/health` - Health check
- `http://localhost:8080/osd/test` - View a test image with OSD overlays

## Running the Test Suite

```bash
python test_osd.py
```

This will generate 7 test images in `/tmp/` demonstrating all OSD features.

## Example Usage

### Python Client Example

```python
import cv2
import base64
import requests

# Read your image
image = cv2.imread('your_image.jpg')

# Encode to base64
_, buffer = cv2.imencode('.png', image)
image_base64 = base64.b64encode(buffer).decode('utf-8')

# Add timestamp
response = requests.post('http://localhost:8080/osd/add_timestamp', json={
    'image': image_base64,
    'x': 10,
    'y': 30
})

# Save result
if response.status_code == 200:
    result = response.json()
    result_data = base64.b64decode(result['image'])
    with open('output.png', 'wb') as f:
        f.write(result_data)
    print("✓ Image saved!")
```

### Using cURL

```bash
# Download test image
curl http://localhost:8080/osd/test -o test.png

# Check health
curl http://localhost:8080/health
```

### Direct Python Usage (Without API)

```python
from osd_utils import IngenicOSD, create_test_image
import cv2

# Create OSD instance
osd = IngenicOSD()

# Load or create an image
image = cv2.imread('input.jpg')
# or create test image
# image = create_test_image(640, 480)

# Add timestamp
image = osd.add_timestamp(image)

# Add text
image = osd.add_text(image, "Camera 01", position=(10, 70))

# Add bounding box
image = osd.add_box(image, (100, 100), (300, 300), label="Detection")

# Save result
cv2.imwrite('output.jpg', image)
```

## Common Use Cases

### 1. IP Camera Overlay

```python
from osd_utils import IngenicOSD
import cv2

osd = IngenicOSD()
frame = cv2.imread('camera_frame.jpg')

# Add camera info
frame = osd.add_timestamp(frame, position=(10, 30))
frame = osd.add_text(frame, "CAM-01 | Front Door", position=(10, 70))

cv2.imwrite('camera_with_osd.jpg', frame)
```

### 2. Object Detection Visualization

```python
from osd_utils import IngenicOSD
import cv2

osd = IngenicOSD()
image = cv2.imread('detection_frame.jpg')

# Add detection boxes
detections = [
    {"bbox": (100, 100, 200, 300), "label": "Person (98%)"},
    {"bbox": (300, 150, 450, 350), "label": "Car (95%)"}
]

for det in detections:
    x1, y1, x2, y2 = det["bbox"]
    image = osd.add_box(image, (x1, y1), (x2, y2), 
                        label=det["label"], color=(0, 255, 0))

cv2.imwrite('detections.jpg', image)
```

### 3. Status Information Display

```python
from osd_utils import IngenicOSD
import cv2

osd = IngenicOSD()
frame = cv2.imread('video_frame.jpg')

# Add status info
status_lines = [
    "Recording: Active",
    "FPS: 30",
    "Resolution: 1920x1080",
    "Storage: 45% free"
]

frame = osd.add_multiline_text(frame, status_lines, start_position=(10, 50))

cv2.imwrite('status_overlay.jpg', frame)
```

## Customizing OSD Appearance

```python
from osd_utils import IngenicOSD, OSDConfig

# Create custom configuration
config = OSDConfig()
config.font_scale = 1.5
config.font_thickness = 3
config.text_color = (0, 255, 255)  # Yellow
config.bg_opacity = 0.7

# Use custom config
osd = IngenicOSD(config)
```

## Production Deployment

### Using Gunicorn (Recommended)

```bash
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

### Using Docker

```bash
docker build -t ingenic-osd .
docker run -p 8080:8080 ingenic-osd
```

### Deploy to Google Cloud Run

```bash
gcloud run deploy ingenic-osd \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Troubleshooting

### Issue: Server won't start
**Solution:** Make sure port 8080 is not already in use:
```bash
lsof -i :8080
# Kill the process if needed
```

### Issue: OpenCV not found
**Solution:** Reinstall opencv-python-headless:
```bash
pip install --force-reinstall opencv-python-headless
```

### Issue: Image quality is poor
**Solution:** Use PNG format for lossless quality:
```python
_, buffer = cv2.imencode('.png', image)  # Use .png instead of .jpg
```

## API Reference

For complete API documentation, see [OSD_API.md](OSD_API.md)

## Examples

See [test_osd.py](test_osd.py) for comprehensive examples of all features.

## Support

For issues and questions, please check:
1. [OSD_API.md](OSD_API.md) - Complete API reference
2. [test_osd.py](test_osd.py) - Working examples
3. [README.md](README.md) - Project overview
