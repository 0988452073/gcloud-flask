# Ingenic OSD API Documentation

This Flask application provides On-Screen Display (OSD) functionality for Ingenic SoC-based devices, allowing you to overlay text, timestamps, and bounding boxes on images.

## Features

- Text overlay with customizable position and color
- Timestamp overlay with custom formatting
- Bounding box overlay with optional labels
- Multi-line text support
- Semi-transparent background for better text visibility

## API Endpoints

### Health Check

**GET** `/health`

Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "service": "Ingenic OSD API"
}
```

### Test OSD

**GET** `/osd/test`

Generates a test image with various OSD elements for demonstration.

**Response:** PNG image with timestamp, text, multi-line text, and bounding box overlays.

### Add Text Overlay

**POST** `/osd/add_text`

Adds text overlay to an uploaded image.

**Request Body:**
```json
{
  "image": "base64_encoded_image_data",
  "text": "Text to overlay",
  "x": 10,
  "y": 30,
  "color": [255, 255, 255]
}
```

**Parameters:**
- `image` (required): Base64-encoded image data
- `text` (required): Text string to overlay
- `x` (optional): X coordinate for text position (default: 10)
- `y` (optional): Y coordinate for text position (default: 30)
- `color` (optional): Text color as [B, G, R] array (default: [255, 255, 255] - white)

**Response:**
```json
{
  "success": true,
  "image": "base64_encoded_result_image"
}
```

### Add Timestamp Overlay

**POST** `/osd/add_timestamp`

Adds current timestamp overlay to an uploaded image.

**Request Body:**
```json
{
  "image": "base64_encoded_image_data",
  "x": 10,
  "y": 30,
  "format": "%Y-%m-%d %H:%M:%S"
}
```

**Parameters:**
- `image` (required): Base64-encoded image data
- `x` (optional): X coordinate for timestamp position (default: 10)
- `y` (optional): Y coordinate for timestamp position (default: 30)
- `format` (optional): Datetime format string (default: "%Y-%m-%d %H:%M:%S")

**Response:**
```json
{
  "success": true,
  "image": "base64_encoded_result_image"
}
```

### Add Bounding Box

**POST** `/osd/add_box`

Adds a bounding box with optional label to an uploaded image.

**Request Body:**
```json
{
  "image": "base64_encoded_image_data",
  "x1": 100,
  "y1": 100,
  "x2": 300,
  "y2": 300,
  "color": [0, 255, 0],
  "thickness": 2,
  "label": "Detection Zone"
}
```

**Parameters:**
- `image` (required): Base64-encoded image data
- `x1`, `y1` (required): Top-left corner coordinates
- `x2`, `y2` (required): Bottom-right corner coordinates
- `color` (optional): Box color as [B, G, R] array (default: [0, 255, 0] - green)
- `thickness` (optional): Line thickness (default: 2)
- `label` (optional): Label text to display above the box

**Response:**
```json
{
  "success": true,
  "image": "base64_encoded_result_image"
}
```

## Usage Examples

### Python Example

```python
import cv2
import base64
import requests

# Read image
image = cv2.imread('input.jpg')

# Encode to base64
_, buffer = cv2.imencode('.png', image)
image_base64 = base64.b64encode(buffer).decode('utf-8')

# Add timestamp
response = requests.post('http://localhost:8080/osd/add_timestamp', json={
    'image': image_base64,
    'x': 10,
    'y': 30
})

# Decode result
if response.status_code == 200:
    result = response.json()
    result_image_data = base64.b64decode(result['image'])
    with open('output.png', 'wb') as f:
        f.write(result_image_data)
```

### cURL Example

```bash
# Test health endpoint
curl http://localhost:8080/health

# Download test image
curl http://localhost:8080/osd/test -o test_osd.png
```

## OSD Configuration

The OSD module uses the following default settings:

- **Font:** OpenCV FONT_HERSHEY_SIMPLEX
- **Font Scale:** 1.0
- **Font Thickness:** 2
- **Text Color:** White (255, 255, 255)
- **Background Color:** Black (0, 0, 0)
- **Background Opacity:** 0.5 (50% transparent)
- **Default Position:** (10, 30)

## Running the Application

### Local Development

```bash
python app.py
```

The server will start on `http://0.0.0.0:8080`

### Docker

```bash
docker build -t ingenic-osd .
docker run -p 8080:8080 ingenic-osd
```

### Production with Gunicorn

```bash
gunicorn -b 0.0.0.0:8080 app:app
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request (missing required parameters or invalid image data)
- `500`: Internal server error

Error responses include a JSON object with an `error` field describing the issue:

```json
{
  "error": "Error message description"
}
```

## Dependencies

- Flask: Web framework
- OpenCV (opencv-python-headless): Image processing
- NumPy: Array operations
- Gunicorn: WSGI HTTP server (production)

## Common Use Cases

1. **IP Camera Overlays**: Add camera name, location, and timestamp to video frames
2. **Object Detection**: Draw bounding boxes and labels around detected objects
3. **Status Information**: Display system status, FPS, or other metrics on video feeds
4. **Watermarking**: Add text watermarks to images for identification
