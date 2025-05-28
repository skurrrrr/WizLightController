import socket
import json
from datetime import datetime

# Define the request payload
request_payload = '{"method":"getPilot","params":{}}'

def send_request(ip):
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)  # Set timeout to avoid hanging
        # Send the request payload to the IP address and port
        sock.sendto(request_payload.encode(), (ip, 38899))
        # Receive the response
        data, _ = sock.recvfrom(4096)
        response = data.decode()
        return response
    except socket.timeout:
        print(f"Request timed out for {ip}")
    except Exception as e:
        print(f"Error sending request to {ip}: {e}")
    return None

def save_response(ip, response):
    # Load existing data from base_state.json if it exists
    try:
        with open('base_state.json', 'r') as file:
            status_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        status_data = []

    # Update or add the entry for the given IP
    updated = False
    for entry in status_data:
        if entry['ip'] == ip:
            entry['response'] = response
            entry['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated = True
            break

    if not updated:
        status_data.append({
            'ip': ip,
            'response': response,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    # Save the updated data back to base_state.json
    try:
        with open('base_state.json', 'w') as file:
            json.dump(status_data, file, indent=4)
        print(f"Updated status for {ip} in base_state.json")
    except Exception as e:
        print(f"Error saving response for {ip}: {e}")

def main():
    start_ip = 9
    end_ip = 255

    while True:
        for i in range(start_ip, end_ip + 1):
            ip = f"192.168.50.{i}"
            print(f"Sending request to {ip}...")
            response = send_request(ip)
            if response:
                save_response(ip, response)

if __name__ == "__main__":
    main()