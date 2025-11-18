# gcloud-flask

Flask application with Ingenic OSD (On-Screen Display) support for adding text overlays, timestamps, and bounding boxes to images.

## Features

- **OSD Text Overlay**: Add custom text with positioning and color options
- **Timestamp Overlay**: Automatically add current timestamp to images
- **Bounding Box**: Draw detection boxes with labels
- **REST API**: Easy-to-use HTTP endpoints for all OSD operations
- **Cloud Run Ready**: Configured for deployment on Google Cloud Run

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The server will start on `http://0.0.0.0:8080`

## API Documentation

See [OSD_API.md](OSD_API.md) for detailed API documentation and usage examples.

## Quick Test

```bash
# View test image with OSD overlays
curl http://localhost:8080/osd/test -o test.png
```

## Docker Deployment

```bash
docker build -t gcloud-flask .
docker run -p 8080:8080 gcloud-flask
```

## Dependencies

- Flask
- OpenCV (opencv-python-headless)
- Ultralytics (YOLO)
- Gunicorn