#!/usr/bin/env python

import socket
import struct
import rospy
#from iiwa_msgs.msg import JointPosition
from sensor_msgs.msg import JointState

#Parameters - TODO make them CLI/ROS-Parameters
UDP_IP = "212.212.21.2"
UDP_PORT = 22223
SAMPLE_RATE = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def talker():
    pub = rospy.Publisher('jointAnglesFromUDP/JointPositionArray', JointState, queue_size=10)
    rospy.init_node('jointPosPublisher', anonymous=True)
    rate = rospy.Rate(SAMPLE_RATE)
    #print("Beginning receive loop...")
    
    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(56) # buffer size is 7*8 bytes
        #print("Received 56 bytes!")
        values = struct.unpack('<ddddddd', data)
        #rospy.loginfo(value)
        pose = JointState()
        pose.header.frame_id = "/base_link"
        pose.header.stamp = rospy.Time.now()
        pose.position = values
        pub.publish(pose)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass