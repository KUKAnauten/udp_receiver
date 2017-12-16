#!/usr/bin/env python

import socket
import struct
import rospy
from geometry_msgs.msg import PoseStamped

#Parameters - TODO make them CLI/ROS-Parameters
UDP_IP = "192.168.16.86"
UDP_PORT = 22223
SAMPLE_RATE = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def talker(topicName='PoseStamped'):
    pub = rospy.Publisher('poseFromUDP/'+topicName, PoseStamped, queue_size=10)
    rospy.init_node('posePublisher', anonymous=True)
    rate = rospy.Rate(SAMPLE_RATE)
    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(56) # buffer size is 7*8 bytes
        values = struct.unpack('<ddddddd', data)
        #rospy.loginfo(value)
        pose = PoseStamped()
        pose.header.frame_id = "/map"
        pose.header.stamp = rospy.Time.now()
        pose.pose.position.x = values[0]
        pose.pose.position.y = values[1]
        pose.pose.position.z = values[2]
        pose.pose.orientation.x = values[3]
        pose.pose.orientation.y = values[4]
        pose.pose.orientation.z = values[5]
        pose.pose.orientation.w = values[6]
        pub.publish(pose)
        rate.sleep()

if __name__ == '__main__':
    if len(argv) == 2:
        try:
            talker(argv[1])
        except rospy.ROSInterruptException:
            pass
    else:
        try:
            talker()
        except rospy.ROSInterruptException:
            pass