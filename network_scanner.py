import scapy.all as scapy

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

    scapy.srp() returns the responses captured as a 
    '''
    answered, unanswered = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1)
    print(answered.summary())
    print(unanswered.summary())

scan("10.0.2.0/24")