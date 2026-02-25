from genie.metaparser.util.exceptions import SchemaEmptyParserError
from pprint import pprint
from pyats.topology import Device

# Raw output copied from a device (or file)
raw_output = """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       192.168.1.1     YES manual up                    up      
GigabitEthernet2       unassigned      YES unset  administratively down down    
"""

# We manually invoke the logic that Genie would use inside a testbed
from genie.libs.parser.iosxe.show_interface import ShowIpInterfaceBrief

def parse_with_genie(text):

    # 1. Create a Mock Device object (This satisfies the parser's requirement)
    test_device = Device('mock_device', os='iosxe')
    # 2. Pass the device object as the first positional argument
    parser = ShowIpInterfaceBrief(Device)
    '''parser = ShowIpInterfaceBrief(device_os='iosxe', device_name='csr1000v')'''
    try:
        # Genie turns the string into a nested Dictionary automatically
        parsed_dict = parser.parse(output=text)
        return parsed_dict
    except Exception as e:
        return {"error": str(e)}
    except SchemaEmptyParserError:
        return {"error": "No data found"}

if __name__ == "__main__":
    structured_data = parse_with_genie(raw_output)
    
    print("--- Structured Data from Genie ---")
    pprint(structured_data)
    
    # Genie Logic: Accessing data is now easy and reliable
    status = structured_data['interface']['GigabitEthernet1']['status']
    print(f"\nStatus of Gig1 is: {status}")
