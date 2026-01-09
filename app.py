from flask import Flask, jsonify, request
import serial_comm

app = Flask(__name__)

# Store active serial connections
active_connections = {}

@app.route("/")
def home():
    return "Hello, Flask on Cloud Run! USB as UART API is available."

@app.route("/serial/ports", methods=["GET"])
def get_serial_ports():
    """List all available serial ports."""
    try:
        ports = serial_comm.list_serial_ports()
        return jsonify({
            "status": "success",
            "ports": ports,
            "count": len(ports)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/serial/open", methods=["POST"])
def open_serial_port():
    """Open a serial port connection."""
    data = request.get_json()
    
    if not data or "port" not in data:
        return jsonify({
            "status": "error",
            "message": "Port parameter is required"
        }), 400
    
    port = data["port"]
    baudrate = data.get("baudrate", 9600)
    timeout = data.get("timeout", 1)
    
    try:
        if port in active_connections:
            return jsonify({
                "status": "error",
                "message": f"Port {port} is already open"
            }), 400
        
        ser = serial_comm.open_serial_connection(port, baudrate, timeout)
        active_connections[port] = ser
        
        return jsonify({
            "status": "success",
            "message": f"Serial port {port} opened successfully",
            "port": port,
            "baudrate": baudrate
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/serial/write", methods=["POST"])
def write_serial():
    """Write data to a serial port."""
    data = request.get_json()
    
    if not data or "port" not in data or "data" not in data:
        return jsonify({
            "status": "error",
            "message": "Port and data parameters are required"
        }), 400
    
    port = data["port"]
    write_data = data["data"]
    
    try:
        if port not in active_connections:
            return jsonify({
                "status": "error",
                "message": f"Port {port} is not open. Please open it first."
            }), 400
        
        ser = active_connections[port]
        bytes_written = serial_comm.write_to_serial(ser, write_data)
        
        return jsonify({
            "status": "success",
            "message": "Data written successfully",
            "bytes_written": bytes_written
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/serial/read", methods=["POST"])
def read_serial():
    """Read data from a serial port."""
    data = request.get_json()
    
    if not data or "port" not in data:
        return jsonify({
            "status": "error",
            "message": "Port parameter is required"
        }), 400
    
    port = data["port"]
    size = data.get("size", 1024)
    
    try:
        if port not in active_connections:
            return jsonify({
                "status": "error",
                "message": f"Port {port} is not open. Please open it first."
            }), 400
        
        ser = active_connections[port]
        read_data, bytes_read = serial_comm.read_from_serial(ser, size)
        
        return jsonify({
            "status": "success",
            "data": read_data,
            "bytes_read": bytes_read
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/serial/close", methods=["POST"])
def close_serial_port():
    """Close a serial port connection."""
    data = request.get_json()
    
    if not data or "port" not in data:
        return jsonify({
            "status": "error",
            "message": "Port parameter is required"
        }), 400
    
    port = data["port"]
    
    try:
        if port not in active_connections:
            return jsonify({
                "status": "error",
                "message": f"Port {port} is not open"
            }), 400
        
        ser = active_connections[port]
        serial_comm.close_serial_connection(ser)
        del active_connections[port]
        
        return jsonify({
            "status": "success",
            "message": f"Serial port {port} closed successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)