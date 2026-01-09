# gcloud-flask

Flask application with USB as UART (serial communication) support for Google Cloud Run.

## Features

- Flask web application
- USB as UART serial communication API
- Computer vision support (OpenCV, Ultralytics)
- Production-ready with Gunicorn

## USB as UART API Endpoints

### 1. List Serial Ports
Get a list of all available serial ports on the system.

**Endpoint:** `GET /serial/ports`

**Response:**
```json
{
  "status": "success",
  "ports": [
    {
      "device": "/dev/ttyUSB0",
      "description": "USB Serial Port",
      "hwid": "USB VID:PID=1234:5678"
    }
  ],
  "count": 1
}
```

### 2. Open Serial Port
Open a connection to a serial port.

**Endpoint:** `POST /serial/open`

**Request Body:**
```json
{
  "port": "/dev/ttyUSB0",
  "baudrate": 9600,
  "timeout": 1
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Serial port /dev/ttyUSB0 opened successfully",
  "port": "/dev/ttyUSB0",
  "baudrate": 9600
}
```

### 3. Write to Serial Port
Write data to an opened serial port.

**Endpoint:** `POST /serial/write`

**Request Body:**
```json
{
  "port": "/dev/ttyUSB0",
  "data": "Hello UART"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Data written successfully",
  "bytes_written": 10
}
```

### 4. Read from Serial Port
Read data from an opened serial port.

**Endpoint:** `POST /serial/read`

**Request Body:**
```json
{
  "port": "/dev/ttyUSB0",
  "size": 1024
}
```

**Response:**
```json
{
  "status": "success",
  "data": "Response from device",
  "bytes_read": 20
}
```

### 5. Close Serial Port
Close a serial port connection.

**Endpoint:** `POST /serial/close`

**Request Body:**
```json
{
  "port": "/dev/ttyUSB0"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Serial port /dev/ttyUSB0 closed successfully"
}
```

## Installation

```bash
pip install -r requirements.txt
```

## Running Locally

```bash
python app.py
```

The application will start on `http://0.0.0.0:8080`

## Docker Deployment

```bash
docker build -t gcloud-flask .
docker run -p 8080:8080 --device=/dev/ttyUSB0 gcloud-flask
```

Note: Use `--device` flag to pass USB devices to the container.

## Google Cloud Run Deployment

```bash
gcloud run deploy gcloud-flask --source .
```
