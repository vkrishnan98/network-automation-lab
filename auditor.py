import json

def run_audit(actual_data, intent_data):
    compliance_report = []
    
    # actual_data['interface'] comes from the Genie parser structure
    interfaces = actual_data.get('interface', {})

    for intf_name, config in intent_data.items():
        actual_intf = interfaces.get(intf_name)

        if not actual_intf:
            compliance_report.append(f"CRITICAL: {intf_name} is MISSING from device!")
            continue

        actual_status = actual_intf.get('status')
        actual_ip = actual_intf.get('ip_address')

        # Validation Logic
        if actual_status == config['expected_status'] and actual_ip == config['expected_ip']:
            compliance_report.append(f"PASS: {intf_name} is compliant.")
        else:
            compliance_report.append(
                f"FAIL: {intf_name} state mismatch! "
                f"Expected {config['expected_status']}/{config['expected_ip']}, "
                f"Got {actual_status}/{actual_ip}"
            )
            
    return compliance_report

if __name__ == "__main__":
    # In a real scenario, we would  load these from files
    with open('intent.json', 'r') as f:
        my_intent = json.load(f)

    # Mocking the Genie output from previous output (Day 2)
    mock_actual = {
        "interface": {
            "GigabitEthernet1": {"status": "up", "ip_address": "192.168.1.1"},
            "GigabitEthernet2": {"status": "administratively down", "ip_address": "unassigned"}
        }
    }

    report = run_audit(mock_actual, my_intent)
    
    print("--- NETWORK COMPLIANCE REPORT ---")
    for line in report:
        print(line)
