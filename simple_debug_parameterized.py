#!/usr/bin/env python3
"""
Parameterized UE4SS Debug Test - Based on the WORKING simple version
Usage: python simple_debug_parameterized.py [host] [port] [command]
"""

import socket
import json
import time
import sys

def connect_to_debugger(host="localhost", port=8172):
    """Connect to UE4SS debugger - returns socket or None"""
    print(f"🔌 Connecting to UE4SS debugger at {host}:{port}...")
    
    # Try IPv6 first (Windows default), then IPv4
    connection_attempts = []
    if host == "localhost":
        connection_attempts = [("::1", socket.AF_INET6), ("127.0.0.1", socket.AF_INET)]
    elif host == "::1":
        connection_attempts = [("::1", socket.AF_INET6)]
    elif ":" in host:  # IPv6 address
        connection_attempts = [(host, socket.AF_INET6)]
    else:  # IPv4 address
        connection_attempts = [(host, socket.AF_INET)]
    
    for attempt_host, family in connection_attempts:
        try:
            sock = socket.socket(family, socket.SOCK_STREAM)
            sock.connect((attempt_host, port))
            print(f"✅ Connected to {attempt_host}:{port}")
            sock.settimeout(5.0)  # Set timeout after connection
            return sock
        except Exception as e:
            print(f"❌ Failed to connect to {attempt_host}: {e}")
            if 'sock' in locals():
                sock.close()
    
    print("💥 Could not connect to debugger!")
    return None

def get_welcome_message(sock):
    """Get welcome message from debugger - exactly like working version"""
    try:
        print("⏳ Waiting a moment for debugger to prepare...")
        time.sleep(0.5)  # Critical timing from working version
        
        print("📡 Waiting for initial message...")
        response = sock.recv(1024).decode()
        print(f"📨 Initial message: {response.strip()}")
        return response.strip()
    except socket.timeout:
        print("❌ No initial message received (timeout)")
        return None
    except Exception as e:
        print(f"⚠️ Welcome message error: {e}")
        return None

def send_command(sock, command):
    """Send command to debugger - exactly like working version"""
    print(f"📤 Sending: {command}")
    
    # Format exactly like working version
    json_command = f'{{"type":"evaluate","expression":"{command}"}}\n'
    sock.send(json_command.encode())
    print(f"✅ Sent: {json_command.strip()}")
    
    # Wait for response
    print("📡 Waiting for response...")
    try:
        response = sock.recv(1024).decode()
        print(f"📨 Response: {response.strip()}")
        return response.strip()
    except socket.timeout:
        print("⏰ Timeout waiting for response")
        return None

def parse_response(response):
    """Parse and display response"""
    if not response:
        return None
        
    try:
        data = json.loads(response)
        if data.get('success'):
            result = data.get('result', '')
            # Send full result - let UI handle display formatting
            print(f"🎉 SUCCESS: {result}")
            return result
        else:
            error = data.get('error', 'Unknown error')
            print(f"❌ ERROR: {error}")
            return None
    except json.JSONDecodeError:
        print(f"📦 Raw response (not JSON): {response}")
        return response

def main():
    # Show usage
    print("🎮 UE4SS Parameterized Debug Test")
    print("Usage: python simple_debug_parameterized.py [host] [port] [command]")
    print("Examples:")
    print("  python simple_debug_parameterized.py")
    print("  python simple_debug_parameterized.py localhost 8172")
    print("  python simple_debug_parameterized.py ::1 8172 'math.sqrt(16)'")
    print("=" * 60)
    
    # Parse command line arguments
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8172
    command = sys.argv[3] if len(sys.argv) > 3 else "UEHelpers.GetPlayer():GetFullName()"
    
    print(f"📍 Target: {host}:{port}")
    print(f"📝 Command: {command}")
    print()
    
    sock = None
    try:
        # Connect using exact working method
        sock = connect_to_debugger(host, port)
        if not sock:
            return 1
            
        # Get welcome message using exact working method
        get_welcome_message(sock)
        
        # Send command using exact working method
        response = send_command(sock, command)
        
        # Parse response
        result = parse_response(response)
        
        if result is not None:
            print("✅ Test completed successfully!")
            return 0
        else:
            print("❌ Test failed - no valid response")
            return 1
        
    except Exception as e:
        print(f"💥 Error: {e}")
        return 1
    finally:
        if sock:
            sock.close()
            print("🔌 Connection closed")

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 