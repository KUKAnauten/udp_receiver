#!/usr/bin/env python
import sys
import socket
import struct
import rospy
from std_msgs.msg import Float64

#Parameters - TODO make them CLI/ROS-Parameters
UDP_IP = "212.212.21.2"
UDP_PORT = 22223
SAMPLE_RATE = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def talker(topicName='GripperCommand'):
    pub = rospy.Publisher('gripperCommandFromUDP/'+topicName, Float64, queue_size=10)
    rospy.init_node('gripperCommandPublisher', anonymous=True)
    rate = rospy.Rate(SAMPLE_RATE)
    #print("Beginning receive loop...")
    
    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(8) 
        values = struct.unpack('<d', data)
        #rospy.loginfo(value)
        pub.publish(values[0])
        rate.sleep()

if __name__ == '__main__':
   try:
       talker()
   except rospy.ROSInterruptException:
       pass

    # if len(sys.argv) == 2:
    #     try:
    #         talker(sys.argv[1])
    #     except rospy.ROSInterruptException:
    #         pass
    # else:
    #     try:
    #         talker()
    #     except rospy.ROSInterruptException:
    #         pass
