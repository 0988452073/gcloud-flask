from flask import Flask, request, send_file, jsonify
import cv2
import numpy as np
import io
import base64
from osd_utils import IngenicOSD, OSDConfig, create_test_image

app = Flask(__name__)

# Initialize OSD
osd = IngenicOSD()

@app.route("/")
def home():
    return "Hello, Flask on Cloud Run! OSD API Ready."

@app.route("/osd/test", methods=["GET"])
def test_osd():
    """Generate a test image with OSD overlay."""
    # Create test image
    image = create_test_image()
    
    # Add timestamp
    image = osd.add_timestamp(image, position=(10, 30))
    
    # Add sample text
    image = osd.add_text(image, "Ingenic OSD Demo", position=(10, 70))
    
    # Add multiline text
    lines = ["Line 1: Camera Info", "Line 2: Status OK", "Line 3: FPS: 30"]
    image = osd.add_multiline_text(image, lines, start_position=(10, 110))
    
    # Add bounding box
    image = osd.add_box(image, (200, 200), (400, 350), label="Detection")
    
    # Encode image to send as response
    _, buffer = cv2.imencode('.png', image)
    
    return send_file(
        io.BytesIO(buffer),
        mimetype='image/png',
        as_attachment=False,
        download_name='osd_test.png'
    )

@app.route("/osd/add_text", methods=["POST"])
def add_text_to_image():
    """
    Add text overlay to an uploaded image.
    
    Expected JSON:
    {
        "image": "base64_encoded_image",
        "text": "Text to overlay",
        "x": 10,  // optional
        "y": 30,  // optional
        "color": [255, 255, 255]  // optional [B, G, R]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data or 'text' not in data:
            return jsonify({"error": "Missing 'image' or 'text' in request"}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400
        
        # Get parameters
        text = data['text']
        position = (data.get('x', 10), data.get('y', 30))
        color = tuple(data.get('color', [255, 255, 255]))
        
        # Add text overlay
        result = osd.add_text(image, text, position=position, color=color)
        
        # Encode result
        _, buffer = cv2.imencode('.png', result)
        result_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            "success": True,
            "image": result_base64
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/osd/add_timestamp", methods=["POST"])
def add_timestamp_to_image():
    """
    Add timestamp overlay to an uploaded image.
    
    Expected JSON:
    {
        "image": "base64_encoded_image",
        "x": 10,  // optional
        "y": 30,  // optional
        "format": "%Y-%m-%d %H:%M:%S"  // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({"error": "Missing 'image' in request"}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400
        
        # Get parameters
        position = (data.get('x', 10), data.get('y', 30))
        format_str = data.get('format', "%Y-%m-%d %H:%M:%S")
        
        # Add timestamp overlay
        result = osd.add_timestamp(image, position=position, format_str=format_str)
        
        # Encode result
        _, buffer = cv2.imencode('.png', result)
        result_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            "success": True,
            "image": result_base64
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/osd/add_box", methods=["POST"])
def add_box_to_image():
    """
    Add bounding box to an uploaded image.
    
    Expected JSON:
    {
        "image": "base64_encoded_image",
        "x1": 100,
        "y1": 100,
        "x2": 300,
        "y2": 300,
        "color": [0, 255, 0],  // optional [B, G, R]
        "thickness": 2,  // optional
        "label": "Object"  // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({"error": "Missing 'image' in request"}), 400
        
        if not all(k in data for k in ['x1', 'y1', 'x2', 'y2']):
            return jsonify({"error": "Missing box coordinates (x1, y1, x2, y2)"}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400
        
        # Get parameters
        top_left = (data['x1'], data['y1'])
        bottom_right = (data['x2'], data['y2'])
        color = tuple(data.get('color', [0, 255, 0]))
        thickness = data.get('thickness', 2)
        label = data.get('label')
        
        # Add box overlay
        result = osd.add_box(image, top_left, bottom_right, color=color, 
                            thickness=thickness, label=label)
        
        # Encode result
        _, buffer = cv2.imencode('.png', result)
        result_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            "success": True,
            "image": result_base64
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "Ingenic OSD API"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)