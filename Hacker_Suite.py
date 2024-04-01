
import ipaddress
import socket 
import re
import subprocess
import threading
import time
import random
 


                
class HackerSuite:
    def __init__(self):
        try:
            self.well_known_ouis = {
            "Cisco Systems Inc." : "00:00:0C",
            "Hewlett Packard (HP)": "00:04:23",
            "Microsoft Corporation": "00:15:5D",
            "Intel Corporation" : "00:1C:C0",
            "Apple, Inc.": "00:1C:BA",
            "Dell Inc.": "00:26:B9",
            "Juniper Networks": "00:05:85" }#add more for greater randomness/less repition
            self.successful_conns = 0
            self.conn_durations = {}
            result = subprocess.run("ipconfig", capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for i in range(len(lines)):
                if 'Wireless LAN adapter Wi-Fi' in lines[i]:
                    for j in range(i+1, i+4):  # Check the next 3 lines
                        if 'IPv4 Address' in lines[j]:
                            ip_address = re.findall(r'[0-9]+(?:\.[0-9]+){3}', lines[j])[0]
                            print(f"IP Address: {ip_address}")
                            self.LHOSTs = ip_address 
                            break
        except Exception as e:
            raise subprocess.CalledProcessError("Error retrieving IP address.") from e
        
    
    def inconspicuous_mac(self):
                #randomly select a company (OUI) from the dictionary
                selected_company = random.choice(list(self.well_known_ouis.keys()))
                selected_oui = self.well_known_ouis[selected_company]
                #generate the remaining three pairs (6 characters) randomly
                
                remaining_pairs = [random.choice("012345679ABCDEF") +  random.choice("012345679ABCDEF")for _ in range(3)]
                #combine OUI with remaining pairs
                new_mac = f"{selected_oui}:{':'.join(remaining_pairs)}"
                return selected_company, new_mac 

                
    @staticmethod                      
    def handle_connection(conn, addr):
                #set a timeout of 900 seconds (15 minutes)
                conn.settimeout(900) 
                msg_count = 0
                start_time = time.time()
                while True:
                    try:
                        #recieve data and send response
                        data = conn.recv(1024)
                        print(f"Recieved: {data.decode('utf-8')}")
                        if not data:
                            break
                        msg_count += 1
                        response = input("Enter reply: ")
                        conn.send(response.encode('utf-8'))
                    except socket.timeout:
                        print("No activity for 15 minutes. Closing connection")
                        conn.close()
                        break
                    end_time = time.time()
                    duration = end_time - start_time
                    return msg_count, duration 
                                

    
    def create_listener(self, port):
                #create a socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind((self.LHOSTs, port))
                sock.listen(5)
    
                while True:
                    #Accept connections
                    conn, addr = sock.accept()
                    self.successful_conns +=1
                    print(f"Connection #{self.successful_conns} from: {addr} accepted")
                    #handle the connection and get the message count and duration
                    msg_count, duration = HackerSuite.handle_connection(conn, addr)
                    #store the message count and duration in conn_durations dict
                    self.conn_durations[self.successful_conns] = (msg_count, duration)
    
    @staticmethod
    def power_fetch_mac(device_name):
                try:
                    # Execute the PowerShell command to get the MAC address
                    fetch = f"(Get-NetAdapter | Where-Object {{ $_.Name -eq '{device_name}' }}).MacAddress"
                    mac_address = subprocess.check_output(["powershell", fetch], text=True).strip()

                    # Return the device name and its MAC address
                    return f"Device Name: {device_name}\nMAC Address: {mac_address}"
                except subprocess.CalledProcessError as e:
                    return "Error executing PowerShell command: {e}"# Device not found or other error occurred
                except FileNotFoundError:
                    return "PowerShell executable not found. Make sure PowerShell is installed."
            

                                 
                            
    #HackerSuite.power_fetch_mac('Wi-Fi') 
    @staticmethod
    def mac_generator():
                secure_random = random.SystemRandom()
                #List of 12 hex digits
                mac_pairs = [secure_random.choice('0123456789ABCDEF') + secure_random.choice('0123456789ABCDEF')
                            for _ in range(6)]
                #Insert ':' after every second digit to format the MAC address
                new_mac = ':'.join(mac_pairs)
                return new_mac
            #og wifi mac: 48-5F-99-BC-D1-D1
       
    
  
    #Example usage
    #hacker_suite = HackerSuite()
    #company_name, new_mac = hacker_suite.inconspicuous_mac()
    #print(f"Company Name (OUI): {company_name}'\n' + Generated MAC Address: {company_name}")
        
        

    @staticmethod
    def windy_mcspoof(device_name, new_mac_address):
                try:
                    # Execute the PowerShell command to set the new MAC address
                    new_mac_address = HackerSuite.mac_generator()
                    cmd = f"Set-NetAdapter -Name '{device_name}' -MacAddress '{new_mac_address}'"
                    subprocess.check_call(["powershell", cmd], text=True)
                    fetch = f"(Get-NetAdapter | Where-Object {{ $_.Name -eq '{device_name}'}}).MacAddress"
                    current_mac_address = subprocess.check_output(["powershell", fetch], text=True).strip()
                    if current_mac_address == new_mac_address:
                        # Construct the success message
                        return f"Updated MAC Address for '{device_name}': {new_mac_address}"
                    else:
                        print("MAC did not change.")
                except Exception as e:
                    return "Unexpected error changing MAC address."  
            
                except subprocess.CalledProcessError as e:
                        # Construct the error message
                        return f"Error changing MAC address for '{device_name}'. {e}"
                except Exception as e:
                        # Handle other exceptions
                        return f"An unexpected error occurred: {e}"

# Example usage:
#print(HackerSuite.mac_generator)        
                            
      
                    
 #def uni_mcspoof(
 #def arp_spoof
 #def ip_spoof
 #def gps_spoof)   
            

        
    def handle_connection(self, conn, addr):
            #set timeout of 900 seconds (15 minutes)
            conn.settimeout(900)
            msg_count = 0
            start_time = time.time()
            while True:
                try:
                    #recieve data and send response
                    data = conn.recv(1024)
                    message = data.decode('utf-8')
                    print(f"Received: {message}")
                    self.message_history.append((addr, message))
                    if not data:
                     break
                    msg_count += 1
                    response = input("Enter reply: ")
                    conn.send(response.encode('utf-8'))
                except socket.timeout:
                    print("No activity for 15 minutes. Closing connection")
                    conn.close()
                    break
                end_time = time.time()
                duration = end_time - start_time
            return msg_count, duration 
    def get_message_history(self):
            return self.message_history
    

hacker_suite = HackerSuite()
new_mac, company_name = hacker_suite.inconspicuous_mac()
print(f"Name (OUI): {new_mac}\nNew MAC Address: {company_name}")
    
     






            
#print(HackerSuite.inconspicuous_mac())
