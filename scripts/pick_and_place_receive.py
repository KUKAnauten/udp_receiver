#!/usr/bin/env python
import sys
import socket
import struct
import rospy
from geometry_msgs.msg import PoseStamped
from iiwa_msgs.msg import JointPosition
from std_msgs.msg import Float64

#Parameters - TODO make them CLI/ROS-Parameters
UDP_IP = "192.168.16.86"
UDP_PORT = 22223
SAMPLE_RATE = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def talker(poseTopicName='PoseStamped', jointTopicName='JointAngles', gripperCommandTopicName='GripperCommand'):
    pose_pub = rospy.Publisher('poseFromUDP/'+topicName, PoseStamped, queue_size=10)
    joint_pub = rospy.Publisher('jointAnglesFromUDP/'+topicName, JointPosition, queue_size=10)
    gripper_command_pub = rospy.Publisher('gripperCommandFromUDP/'+topicName, Float64, queue_size=10)
    rospy.init_node('mcsPublisher', anonymous=True)
    rate = rospy.Rate(SAMPLE_RATE)
    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(120) # buffer size is (7+7+1)*8 bytes
        values = struct.unpack('<ddddddddddddddd', data)
        #rospy.loginfo(value)
        pose = PoseStamped()
        pose.header.frame_id = "/world"
        pose.header.stamp = rospy.Time.now()
        pose.pose.position.x = values[0]
        pose.pose.position.y = values[1]
        pose.pose.position.z = values[2]
        pose.pose.orientation.x = values[3]
        pose.pose.orientation.y = values[4]
        pose.pose.orientation.z = values[5]
        pose.pose.orientation.w = values[6]

        joints = JointPosition()
        joints.header.frame_id = "/world"
        joints.header.stamp = rospy.Time.now()
        joints.position.a1 = values[7]
        joints.position.a2 = values[8]
        joints.position.a3 = values[9]
        joints.position.a4 = values[10]
        joints.position.a5 = values[11]
        joints.position.a6 = values[12]
        joints.position.a7 = values[13]

        gripper_command = Float64()
        gripper_command.data = values[14]

        pose_pub.publish(pose)
        joint_pub.publish(joints)
        gripper_command_pub.publish(gripper_command)
        rate.sleep()

if __name__ == '__main__':
   try:
       talker()
   except rospy.ROSInterruptException:
       pass
