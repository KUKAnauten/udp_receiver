#!/usr/bin/env python

import socket
import struct
import rospy
from std_msgs.msg import Float64

#Parameters - TODO make them CLI/ROS-Parameters
UDP_IP = "192.168.16.86"
UDP_PORT = 22223
SAMPLE_RATE = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def talker():
    pub = rospy.Publisher('poseFromUDP/double', Float64, queue_size=10)
    pub2 = rospy.Publisher('poseFromUDP/double2', Float64, queue_size=10)
    pub3 = rospy.Publisher('poseFromUDP/double3', Float64, queue_size=10)
    rospy.init_node('doublePublisher', anonymous=True)
    rate = rospy.Rate(SAMPLE_RATE)
    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(24) # buffer size is 8 bytes
        values = struct.unpack('<ddd', data)
        #rospy.loginfo(value)
        pub.publish(values[0])
        pub2.publish(values[1])
        pub3.publish(values[2])
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass