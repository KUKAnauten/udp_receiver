#!/usr/bin/env python
import sys
import socket
import struct
import rospy
from geometry_msgs.msg import PoseStamped
from iiwa_msgs.msg import JointPosition
from std_msgs.msg import Float64
from joint_follower.srv import *

#Parameters - TODO make them CLI/ROS-Parameters
UDP_IP = "212.212.21.2"
UDP_PORT = 22223
SAMPLE_RATE = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def uncouple_client(uncouple_req, service_handle):
  #rospy.wait_for_service('coupler')
  try:
    #uncouple = rospy.ServiceProxy('coupler', Coupler)
    #response = uncouple(uncouple_req)
    response = service_handle(uncouple_req)
    if uncouple_req:
      print "Uncouple request"
    else:
      print "Couple request"
  except rospy.ServiceException, e:
    print "Service call failed: %s"%e

def talker(poseTopicName='PoseStamped', jointTopicName='JointPosition', gripperCommandTopicName='GripperCommand'):
    pose_pub = rospy.Publisher('poseFromUDP/'+poseTopicName, PoseStamped, queue_size=10)
    joint_pub = rospy.Publisher('jointAnglesFromUDP/'+jointTopicName, JointPosition, queue_size=10)
    gripper_command_pub = rospy.Publisher('gripperCommandFromUDP/'+gripperCommandTopicName, Float64, queue_size=10)
    rospy.init_node('mcsPublisher', anonymous=True)
    
    rospy.wait_for_service('coupler')
    uncouple = rospy.ServiceProxy('coupler', Coupler)

    rate = rospy.Rate(SAMPLE_RATE)
    last_value = 0
    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(128) # buffer size is (7+7+1+1)*8 bytes
        values = struct.unpack('<dddddddddddddddd', data)
        #rospy.loginfo(value)         
        pose = PoseStamped()
        pose.header.frame_id = "/operator"
        pose.header.stamp = rospy.Time.now()
        pose.pose.position.x = values[0]
        pose.pose.position.y = values[1]
        pose.pose.position.z = values[2]
        pose.pose.orientation.x = values[3]
        pose.pose.orientation.y = values[4]
        pose.pose.orientation.z = values[5]
        pose.pose.orientation.w = values[6]

        joints = JointPosition()
        joints.header.frame_id = "/base_link"
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

        if values[15]==1 and last_value==0:
          uncouple_client(True, uncouple)  
        elif values[15]==0 and last_value==1:
          uncouple_client(False, uncouple)

        last_value = values[15]

        pose_pub.publish(pose)
        joint_pub.publish(joints)
        gripper_command_pub.publish(gripper_command)

        #print "Test"
        rate.sleep()

if __name__ == '__main__':
   try:
       talker()
   except rospy.ROSInterruptException:
       pass
