import scapy.all as scapy
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP Address/Adresses')
    options = parser.parse_args()

    #Check for errors i.e if the user does not specify the target IP Address
    #Quit the program the argument is missing
    #While quitting also display an error message
    if not options.target:
        #Handling the code if interface is not specified
        parser.error("[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options

def scan(ip):
    # scapy.arping(ip)

    '''
    Creating a ARP Packet using Scapy's ARP() class
    object.pdst = ARP() class uses this as a member variable for IP Address of a/the Destination/s.
    object.summary() = shows the member variables of the class
    object.show() = shows the details of the object
    '''
    arp_req_frame = scapy.ARP(pdst = ip)
    # arp_req_frame.show()

    '''
    Creating an Ethernet frame so that we can incorporate Source and Destination MAC Address
    object = Scapy.Ether() where Ether is the class that enables us to create an Ethernet frame
    object.show() = shows the details of the object
    '''
    broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    # broadcast_ether_frame.show()

    '''
    Now we have to combine both the frames so that we can transmit it using ethernet
    Forward slash (/) in scapy allows us to combine frames
    '''
    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame
    # broadcast_ether_arp_req_frame.show()

    '''
    The frame to be send is ready and now we just have to send the frame and capture the responses.
    To send the packets and receive the responses we'll use the scapy.srp(frame , timeout = 1)
    scapy.srp(frame , timeout = 1) sends the frame (specified as an argument) to an IP address , and the timeout argument is 
    also important as it tells for how much time to wait for an response. Eg: timeout = 1 means wait for 1 sec for the response and
    if there is no response proceed with other IP addresses.

    scapy.srp() returns the responses captured as two lists out of which the 1st list contains the answered responses from devices on the network and the 
    2nd list contains the records of IP Addresses which did not respond.

    verbose = False means the srp method will not print any message of its own in the output
    '''
    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1, verbose = False)[0]
    result = []
    for i in range(0,len(answered_list)):
        client_dict = {"ip" : answered_list[i][1].psrc, "mac" : answered_list[i][1].hwsrc}
        result.append(client_dict)

    return result


def display_result(result):
    print("-----------------------------------\nIP Address\tMAC Address\n-----------------------------------")
    for i in result:
        print("{}\t{}".format(i["ip"], i["mac"]))


options = get_args()
scanned_output = scan(options.target)
display_result(scanned_output)
