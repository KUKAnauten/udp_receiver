#!/usr/bin/env python

import socket
import struct
import rospy
from iiwa_msgs.msg import JointPosition

#Parameters - TODO make them CLI/ROS-Parameters
UDP_IP = "212.212.21.2"
UDP_PORT = 22223
SAMPLE_RATE = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def talker():
    pub = rospy.Publisher('jointAnglesFromUDP/JointPosition', JointPosition, queue_size=10)
    rospy.init_node('jointPosPublisher', anonymous=True)
    rate = rospy.Rate(SAMPLE_RATE)
    #print("Beginning receive loop...")
    
    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(56) # buffer size is 7*8 bytes
        #print("Received 56 bytes!")
        values = struct.unpack('<ddddddd', data)
        #rospy.loginfo(value)
        pose = JointPosition()
        pose.header.frame_id = "/base_link"
        pose.header.stamp = rospy.Time.now()
        pose.position.a1 = values[0]
        pose.position.a2 = values[1]
        pose.position.a3 = values[2]
        pose.position.a4 = values[3]
        pose.position.a5 = values[4]
        pose.position.a6 = values[5]
        pose.position.a7 = values[6]
        pub.publish(pose)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass