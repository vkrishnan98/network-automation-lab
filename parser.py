import json

def parse_interface_output(file_path):
    parsed_results = []
    
    try:
        with open(file_path, 'r') as f:
            # Skip the first header line
            lines = f.readlines()[1:]
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 6:
                    # Logic: Map the parts to keys
                    data = {
                        "interface": parts[0],
                        "ip_address": parts[1],
                        "status": parts[4],
                        "protocol": parts[5]
                    }
                    parsed_results.append(data)
        
        return parsed_results

    except FileNotFoundError:
        print("File not found.")
        return []

if __name__ == "__main__":
    interfaces = parse_interface_output('show_ip_int_brief.txt')
    
    # Senior Logic: Use List Comprehension to find only 'down' interfaces
    down_interfaces = [i['interface'] for i in interfaces if i['status'] != 'up']
    
    print("Full Parsed Data:")
    print(json.dumps(interfaces, indent=4))
    
    print(f"\nAlert! The following interfaces are NOT up: {down_interfaces}")
