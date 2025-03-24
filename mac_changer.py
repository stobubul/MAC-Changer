import subprocess
import optparse
import re

def intro():
    print(r'''

   \  |    \     __|     __|  |                                   
  |\/ |   _ \   (       (       \    _` |    \    _` |   -_)   _| 
 _|  _| _/  _\ \___|   \___| _| _| \__,_| _| _| \__, | \___| _|   
                                                ____/             
   _|             | _)                                            
   _| _ \   _|    |  |    \   |  | \ \ /                          
 _| \___/ _|     _| _| _| _| \_,_|  _\_\                          
                                                                                                                  
''')

    print(r'''
                                         _____ __  
                     _  _  _| _  |_     (_  | |__) 
                    |||(_|(_|(-  |_)\/  __) | |__) 
                                    /              

''')

def change_mac(user_interface, user_mac):
    subprocess.call(["ifconfig", user_interface, "down"])
    subprocess.call(["ifconfig", user_interface, "hw", "ether", user_mac])
    subprocess.call(["ifconfig", user_interface, "up"])

def get_arguments():

    parse_object = optparse.OptionParser(usage="%prog [options]\n\nThis tool allows you to change the MAC address of a network interface.\n")

    parse_object.add_option("-i", "--interface", dest="interface", help="Specify the network interface (e.g: eth0, wlan0)")
    parse_object.add_option("-m", "--mac", dest="new_mac", help="Set the new MAC address (format: XX:XX:XX:XX:XX:XX)")

    (inputs,arguments) = parse_object.parse_args()

    if not inputs.interface:
        print("[-] You need to specify the interface to change MAC address, use --help for more info.")
    elif not inputs.new_mac:
        print("[-] You need to specify the new MAC address, use --help for more info.")
    else:
        return inputs

def is_valid_mac(mac):
    # Regular expression for validating MAC address format
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(pattern, mac))

def get_current_mac(interface):
    try:
        ifconfig_interface_result = subprocess.check_output(["ifconfig", interface], text=True, stderr=subprocess.DEVNULL)
        current_mac_address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_interface_result)
        if not current_mac_address:
            print(f"[-] No MAC address found in {interface} interface.    ")
            return None
        return current_mac_address.group(0)
    except subprocess.CalledProcessError:
        print(f"[-] Interface '{interface}' not found. Please check your interface name and try again.")
        exit(1)

def main():
    #subprocess.call("clear")
    intro()
    inputs = get_arguments()

    # Exit if there are no inputs
    if inputs is None:
        return

    # Controls the MAC address format
    mac_control = is_valid_mac(inputs.new_mac)

    if mac_control:
        #New MAC address is valid

        current_mac = get_current_mac(inputs.interface)
        #Check if interface exists
        if current_mac is None:
            exit(1)

        print(f"[~] The Current MAC address is        \t\t{current_mac}   ")
        change_mac(inputs.interface, inputs.new_mac)
        current_mac = get_current_mac(inputs.interface)

        if current_mac != inputs.new_mac.lower():
            print(f"[-] MAC address did not changed.    ")
        else:
            print(f"[+] MAC address successfully changed to\t\t{current_mac}  ")

    else:
        #New MAC address is invalid
        print("[-] An invalid MAC address was entered.  ")

main()