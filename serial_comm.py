"""
USB as UART Serial Communication Module

This module provides functionality to communicate with USB devices using UART protocol.
"""

import serial
import serial.tools.list_ports


def list_serial_ports():
    """
    List all available serial ports on the system.
    
    Returns:
        list: List of dictionaries containing port information (device, description, hwid)
    """
    ports = serial.tools.list_ports.comports()
    port_list = []
    for port in ports:
        port_list.append({
            'device': port.device,
            'description': port.description,
            'hwid': port.hwid
        })
    return port_list


def open_serial_connection(port, baudrate=9600, timeout=1):
    """
    Open a serial connection to a USB device.
    
    Args:
        port (str): Serial port device name (e.g., '/dev/ttyUSB0', 'COM3')
        baudrate (int): Baud rate for communication (default: 9600)
        timeout (int): Read timeout in seconds (default: 1)
    
    Returns:
        serial.Serial: Serial connection object
    
    Raises:
        serial.SerialException: If unable to open the port
    """
    return serial.Serial(port, baudrate=baudrate, timeout=timeout)


def write_to_serial(ser, data):
    """
    Write data to the serial port.
    
    Args:
        ser (serial.Serial): Serial connection object
        data (str or bytes): Data to write
    
    Returns:
        int: Number of bytes written
    
    Raises:
        serial.SerialException: If write operation fails
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    bytes_written = ser.write(data)
    ser.flush()
    return bytes_written


def read_from_serial(ser, size=1024):
    """
    Read data from the serial port.
    
    Args:
        ser (serial.Serial): Serial connection object
        size (int): Maximum number of bytes to read (default: 1024)
    
    Returns:
        tuple: (decoded_str, bytes_read) - Data read as UTF-8 string and actual bytes read
    
    Raises:
        serial.SerialException: If read operation fails
    """
    data = ser.read(size)
    bytes_read = len(data)
    decoded_str = data.decode('utf-8', errors='ignore')
    return decoded_str, bytes_read


def close_serial_connection(ser):
    """
    Close the serial connection.
    
    Args:
        ser (serial.Serial): Serial connection object
    """
    if ser and ser.is_open:
        ser.close()
