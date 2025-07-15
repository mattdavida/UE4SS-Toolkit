#!/usr/bin/env python3
"""
UE4SS Lua Playground Server
Serves the HTML interface and provides API for UE4SS communication
"""

from flask import Flask, render_template_string, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import json
import tempfile
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Connection state (simplified)
last_host = "localhost"
last_port = 8172
connected = False

def test_connection(host="localhost", port=8172):
    """Test connection using our proven script"""
    global last_host, last_port, connected
    
    print(f"🔌 Testing connection to {host}:{port}...")
    
    try:
        # Use our proven script to test connection with a simple command
        cmd = ["python", "simple_debug_parameterized.py", host, str(port), "math.sqrt(16)"]
        
        # Set UTF-8 encoding to handle emojis
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, 
                              encoding='utf-8', env=env)
        
        if result.returncode == 0 and "SUCCESS" in result.stdout:
            print("✅ Connection test successful!")
            last_host = host
            last_port = port  
            connected = True
            return True
        else:
            print(f"❌ Connection test failed: {result.stderr}")
            connected = False
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Connection test timed out")
        connected = False
        return False
    except Exception as e:
        print(f"❌ Connection test error: {e}")
        connected = False
        return False

def disconnect_from_debugger():
    """Mark as disconnected"""
    global connected
    connected = False
    print("⛔ Marked as disconnected")

def clean_lua_code(code):
    """Clean Lua code by removing comments and empty lines"""
    lines = code.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove leading/trailing whitespace
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Skip comment-only lines (starting with --)
        if line.startswith('--'):
            continue
            
        # Remove inline comments but preserve strings
        in_string = False
        quote_char = None
        clean_line = ""
        i = 0
        
        while i < len(line):
            char = line[i]
            
            # Handle string boundaries
            if char in ['"', "'"] and (i == 0 or line[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    quote_char = char
                elif char == quote_char:
                    in_string = False
                    quote_char = None
            
            # Handle comment start
            elif char == '-' and i + 1 < len(line) and line[i+1] == '-' and not in_string:
                # Found comment start, truncate here
                break
                
            clean_line += char
            i += 1
        
        # Add cleaned line if not empty
        clean_line = clean_line.strip()
        if clean_line:
            cleaned_lines.append(clean_line)
    
    return '\n'.join(cleaned_lines)

def auto_unpack_table(original_command, table_result, max_items=10):
    """Auto-unpack table results by programmatically querying elements"""
    global last_host, last_port, connected
    
    if not connected:
        return None
        
    try:
        print(f"🔍 Auto-unpacking table from: {original_command[:50]}...")
        
        # Step 1: Get table size
        size_command = f"#{original_command}"
        print(f"🔍 Size command: {size_command}")
        size_result = execute_single_command(size_command)
        
        if not size_result or not size_result.get('success'):
            print("❌ Failed to get table size")
            return None
            
        try:
            table_size = int(size_result['result'])
            print(f"📊 Table has {table_size} elements")
        except (ValueError, TypeError):
            print(f"❌ Invalid table size: {size_result['result']}")
            return None
            
        if table_size == 0:
            return f"table[0]: (empty table)"
            
        # Step 2: Build formatted result
        result_lines = [f"table[{table_size}]: (auto-expanded)"]
        
        # Limit items to prevent spam
        items_to_show = min(table_size, max_items)
        
        for i in range(1, items_to_show + 1):
            # Try getting full name first, fall back to string representation
            element_commands = [
                f"{original_command}[{i}]:GetFullName()",
                f"tostring({original_command}[{i}])"
            ]
            
            element_result = None
            for cmd in element_commands:
                element_result = execute_single_command(cmd)
                if element_result and element_result.get('success') and element_result['result'] != 'nil':
                    break
                    
            if element_result and element_result.get('success'):
                result_text = element_result['result']
                # Send full result to UI - let frontend handle truncation/display
                result_lines.append(f"  [{i}] {result_text}")
            else:
                result_lines.append(f"  [{i}] (failed to get element)")
                
        # Add truncation notice if needed
        if table_size > max_items:
            result_lines.append(f"  ... ({table_size - max_items} more items)")
            
        return '\n'.join(result_lines)
        
    except Exception as e:
        print(f"❌ Auto-unpack error: {e}")
        return None

def auto_unpack_tarray(original_command, tarray_result, max_items=10):
    """Auto-unpack TArray results by programmatically querying elements"""
    global last_host, last_port, connected
    
    if not connected:
        return None
        
    try:
        print(f"📋 Auto-unpacking TArray from: {original_command[:50]}...")
        
        # Step 1: Get TArray size using :GetArrayNum()
        size_command = f"{original_command}:GetArrayNum()"
        print(f"📊 Size command: {size_command}")
        size_result = execute_single_command(size_command)
        
        if not size_result or not size_result.get('success'):
            print("❌ Failed to get TArray size")
            return None
            
        try:
            array_size = int(size_result['result'])
            print(f"📋 TArray has {array_size} elements")
        except (ValueError, TypeError):
            print(f"❌ Invalid TArray size: {size_result['result']}")
            return None
            
        if array_size == 0:
            return f"TArray[0]: (empty array)"
            
        # Step 2: Build formatted result
        result_lines = [f"TArray[{array_size}]: (auto-expanded)"]
        
        # Limit items to prevent spam
        items_to_show = min(array_size, max_items)
        
        for i in range(1, items_to_show + 1):
            # Try getting full name first, fall back to string representation
            element_commands = [
                f"{original_command}[{i}]:GetFullName()",
                f"tostring({original_command}[{i}])"
            ]
            
            element_result = None
            for cmd in element_commands:
                element_result = execute_single_command(cmd)
                if element_result and element_result.get('success') and element_result['result'] != 'nil':
                    break
                    
            if element_result and element_result.get('success'):
                result_text = element_result['result']
                # Send full result to UI - let frontend handle truncation/display
                result_lines.append(f"  [{i}] {result_text}")
            else:
                result_lines.append(f"  [{i}] (failed to get element)")
                
        # Add truncation notice if needed
        if array_size > max_items:
            result_lines.append(f"  ... ({array_size - max_items} more items)")
            
        return '\n'.join(result_lines)
        
    except Exception as e:
        print(f"❌ TArray auto-unpack error: {e}")
        return None

def execute_single_command(command):
    """Execute a single Lua command and return parsed result"""
    global last_host, last_port
    
    try:
        cmd = ["python", "simple_debug_parameterized.py", last_host, str(last_port), command]
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10,
                              encoding='utf-8', env=env)
        
        if result.returncode == 0:
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if "🎉 SUCCESS:" in line:
                    result_text = line.split("🎉 SUCCESS: ", 1)[1] if "🎉 SUCCESS: " in line else line
                    return {"success": True, "result": result_text}
        
        return {"success": False, "error": "Command failed"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}



def execute_lua_code(code):
    """Execute Lua code using our proven script"""
    global last_host, last_port, connected
    
    if not connected:
        return {
            "success": False,
            "error": "Not connected to UE4SS debugger"
        }
    
    # Clean the code first
    cleaned_code = clean_lua_code(code)
    if not cleaned_code.strip():
        return {
            "success": False,
            "error": "No executable code found (only comments and empty lines)"
        }
    
    try:
        print(f"📤 Executing cleaned code: {cleaned_code[:50]}...")
        print(f"📤 Original had {len(code.split(chr(10)))} lines, cleaned has {len(cleaned_code.split(chr(10)))} lines")
        
                # Convert multi-line code to single-line  
        if '\n' in cleaned_code:
            print("🔄 Converting multi-line to single-line...")
            # Join lines with spaces for Lua (Lua treats newlines as whitespace)
            single_line_code = ' '.join(line.strip() for line in cleaned_code.split('\n') if line.strip())
            print(f"📝 Converted to: {single_line_code[:100]}...")
        else:
            single_line_code = cleaned_code
        
        # Fix quote issue: Replace double quotes with single quotes for Lua compatibility
        # This helps with FindAllOf("ClassName") -> FindAllOf('ClassName')
        lua_fixed_code = single_line_code.replace('"', "'")
        if lua_fixed_code != single_line_code:
            print(f"🔧 Fixed quotes: {lua_fixed_code[:100]}...")
        
        # Use our proven single-line approach
        cmd = ["python", "simple_debug_parameterized.py", last_host, str(last_port), lua_fixed_code]
        
        # Set UTF-8 encoding to handle emojis
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                              encoding='utf-8', env=env)
        
        print(f"📨 Script output: {result.stdout[:100]}...")
        print(f"📨 Script errors: {result.stderr}")
        
        if result.returncode == 0:
            # Parse the output for the actual result
            output_lines = result.stdout.split('\n')
            
            # Look for SUCCESS line to extract result
            for line in output_lines:
                if "🎉 SUCCESS:" in line:
                    # Extract the result after "🎉 SUCCESS: "
                    result_text = line.split("🎉 SUCCESS: ", 1)[1] if "🎉 SUCCESS: " in line else line
                    print(f"🔍 Result: {result_text}")
                    print('fixed code: ' + lua_fixed_code)
                    # Check if result is a table or TArray and auto-unpack it
                    if "table:" in result_text:
                        expanded_result = auto_unpack_table(lua_fixed_code, result_text)
                        if expanded_result:
                            return {
                                "success": True,
                                "result": expanded_result,
                                "raw_output": result.stdout
                            }
                    elif "TArray:" in result_text:
                        expanded_result = auto_unpack_tarray(lua_fixed_code, result_text)
                        if expanded_result:
                            return {
                                "success": True,
                                "result": expanded_result,
                                "raw_output": result.stdout
                            }
                    
                    return {
                        "success": True,
                        "result": result_text,
                        "raw_output": result.stdout
                    }
            
            # If no SUCCESS line found, return full output
            return {
                "success": True,
                "result": "Command executed (see raw output)",
                "raw_output": result.stdout
            }
        else:
            # Script failed
            connected = False  # Mark as disconnected on error
            return {
                "success": False,
                "error": f"Script failed: {result.stderr or 'Unknown error'}",
                "raw_output": result.stdout
            }
                
    except subprocess.TimeoutExpired:
        print("💥 Execution timeout")
        return {
            "success": False,
            "error": "Execution timed out (30s limit)"
        }
    except Exception as e:
        print(f"💥 Execution error: {e}")
        connected = False
        return {
            "success": False,
            "error": f"Execution failed: {str(e)}"
        }

# Static file serving
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve static assets from React build"""
    return send_from_directory('dist/assets', filename)

# API Routes
@app.route('/')
@app.route('/<path:path>')
def index(path=''):
    """Serve React app for all routes"""
    # Don't serve index.html for API routes or asset routes
    if path.startswith('api/') or path.startswith('assets/'):
        return "Not found", 404
        
    try:
        with open('dist/index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "React app not built yet! Run: npm run build", 404

@app.route('/api/connect', methods=['POST'])
def api_connect():
    """Test connection to UE4SS debugger"""
    data = request.get_json()
    host = data.get('host', 'localhost')
    port = int(data.get('port', 8172))
    
    success = test_connection(host, port)
    
    return jsonify({
        "success": success,
        "message": "Connected to UE4SS debugger!" if success else "Failed to connect to UE4SS debugger"
    })

@app.route('/api/disconnect', methods=['POST'])
def api_disconnect():
    """Disconnect from UE4SS debugger"""
    disconnect_from_debugger()
    
    return jsonify({
        "success": True,
        "message": "Disconnected from UE4SS debugger"
    })

@app.route('/api/status', methods=['GET'])
def api_status():
    """Get connection status"""
    return jsonify({
        "connected": connected
    })

@app.route('/api/execute', methods=['POST'])
def api_execute():
    """Execute Lua code"""
    data = request.get_json()
    code = data.get('command', '')
    print(f"🔍 Executing command: {code}")
    
    if not code.strip():
        return jsonify({
            "success": False,
            "error": "No code provided"
        })
    
    result = execute_lua_code(code)
    return jsonify(result)

def create_display_name(spot_name, category_name="", subcategory_name=""):
    """Create a user-friendly display name from internal location name"""
    display = spot_name
    
    # Handle boss challenges specifically
    if 'DLC_BC_CH' in spot_name and 'Boss' in spot_name:
        import re
        ch_match = re.search(r'CH(\d+)', spot_name)
        if ch_match:
            ch_num = ch_match.group(1)
            if 'Clear' in spot_name:
                return f"Chapter {ch_num} Boss (Victory)"
            elif 'Portal' in spot_name:
                return f"Chapter {ch_num} Boss (Portal)"
            else:
                return f"Chapter {ch_num} Boss Arena"
    
    # Remove common prefixes
    prefixes_to_remove = ['LD_', 'DLC_LD_', 'DLC_BC_CH', 'DLC_BC_']
    for prefix in prefixes_to_remove:
        if display.startswith(prefix):
            display = display[len(prefix):]
            break
    
    # Replace underscores with spaces and title case
    display = display.replace('_', ' ').title()
    
    # Special cases for better readability
    replacements = {
        'Cathrdal': 'Cathedral',
        'Townhall': 'Town Hall', 
        'Culturestreet': 'Culture Street',
        'Exhibitionhall': 'Exhibition Hall',
        'Puppet Grave': 'Puppet Graveyard',
        'Underdark': 'Underground Areas',
        'Bossroom': 'Boss Arena',
        'Enterance': 'Entrance',
        'S Enter': 'South Entrance',
        'S Exit': 'South Exit',
        'N Enter': 'North Entrance', 
        'N Exit': 'North Exit',
        'E Enter': 'East Entrance',
        'E Exit': 'East Exit',
        'NW Enter': 'Northwest Entrance',
        'NW Exit': 'Northwest Exit'
    }
    
    for old, new in replacements.items():
        if old.lower() in display.lower():
            display = display.replace(old, new)
    
    return display

def get_teleport_locations_data():
    """Get teleport locations from the structured Python data file"""
    try:
        # Import the structured data
        from teleport_locations import get_all_locations_flat, get_location_count
        
        print("📊 Loading teleport locations from Python data structure...")
        locations = get_all_locations_flat()
        counts = get_location_count()
        
        print(f"✅ Loaded {counts['total']} total locations:")
        print(f"   📁 Base Game: {counts['base_game']}")
        print(f"   📁 DLC Content: {counts['dlc_content']}")
        print(f"   📁 Boss Challenges: {counts['boss_challenges']}")
        
        return locations
        
    except ImportError as e:
        print(f"❌ Could not import teleport_locations.py: {str(e)}")
        return []
    except Exception as e:
        print(f"❌ Error loading teleport locations data: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def get_fallback_locations():
    """Return fallback locations if file parsing fails"""
    return [
        {
            "id": "DLC_BC_CH12_Boss",
            "name": "DLC_BC_CH12_Boss",
            "displayName": "Chapter 12 Boss Arena",
            "description": "DLC Boss encounter area",
            "chapter": "DLC Boss Challenges"
        },
        {
            "id": "DLC_BC_CH10_Boss", 
            "name": "DLC_BC_CH10_Boss",
            "displayName": "Chapter 10 Boss Arena",
            "description": "DLC Boss encounter area", 
            "chapter": "DLC Boss Challenges"
        },
        {
            "id": "LD_Hotel_Main",
            "name": "LD_Hotel_Main",
            "displayName": "Hotel Main",
            "description": "Main hotel area",
            "chapter": "Base Game - Hotel"
        }
    ]

@app.route('/api/fetch-teleport-spots', methods=['POST'])
def api_fetch_teleport_spots():
    """Fetch teleport spots by generating file and parsing it"""
    if not connected:
        return jsonify({
            "success": False,
            "error": "Not connected to UE4SS debugger",
            "locations": get_fallback_locations()
        })
    
    try:
        # Step 1: Call Lua command to generate the teleport_locations.txt file
        print("📝 Generating teleport locations file...")
        result = execute_lua_code("write_teleport_locations_to_file()")
        
        if not result.get("success"):
            print(f"⚠️ File generation command failed: {result.get('error', 'Unknown error')}")
            print("🔄 Trying alternative command...")
            # Try alternative command name if the first one fails
            result = execute_lua_code("WriteTeleportLocationsToFile()")
        
        # Step 2: Load locations from Python data structure
        print("📖 Loading teleport locations from Python data...")
        locations = get_teleport_locations_data()
        
        if locations:
            print(f"✅ Successfully loaded {len(locations)} locations from Python data")
            return jsonify({
                "success": True,
                "message": f"Loaded {len(locations)} teleport locations from Python data structure",
                "locations": locations,
                "file_generated": result.get("success", False),
                "lua_output": result.get("result", "") if result.get("success") else None,
                "data_source": "python_structure"
            })
        else:
            # Step 3: If data loading fails, return fallback locations
            print("⚠️ Python data loading failed, using fallback locations")
            fallback_locations = get_fallback_locations()
            return jsonify({
                "success": True,
                "message": f"Using {len(fallback_locations)} fallback locations (Python data not available)",
                "locations": fallback_locations,
                "file_generated": False,
                "lua_output": result.get("result", "") if result.get("success") else None,
                "data_source": "fallback"
            })
            
    except Exception as e:
        print(f"❌ Exception while fetching teleport spots: {str(e)}")
        fallback_locations = get_fallback_locations()
        return jsonify({
            "success": True,
            "message": f"Using {len(fallback_locations)} fallback locations (error occurred)",
            "locations": fallback_locations,
            "error_details": str(e)
        })

if __name__ == '__main__':
    print("🎮 UE4SS Lua Playground Server")
    print("=" * 40)
    print("🌐 Starting web server...")
    print("📁 Serving playground at: http://localhost:5000")
    print("🎯 Ready to connect to UE4SS debugger!")
    print()
    print("Instructions:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Start your game with UE4SS")
    print("3. Click Connect in the playground")
    print("4. Write Lua code and click RUN!")
    print()
    
    try:
        app.run(host='localhost', port=5000, debug=True, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
        disconnect_from_debugger() 