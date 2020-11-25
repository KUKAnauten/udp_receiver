#!/usr/bin/env python
import sys
import csv
import rospy
import time
from iiwa_msgs.msg import JointPosition
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Time 

SAMPLE_RATE = 100
NUM_OF_ITERATIONS = 1

def talker(filename, jointTopicName='JointPosition', poseTopicName='PoseStampedRelative'):
    pub = rospy.Publisher('jointAnglesFromFile/'+jointTopicName, JointPosition, queue_size=10)
    pose_pub = rospy.Publisher('poseFromFile/'+poseTopicName, PoseStamped, queue_size=10)
    time_pub = rospy.Publisher('iiwa/poseFromFile/receiveTime', Time, queue_size=1)    
    rospy.init_node('jointPosPublisher', anonymous=True)
    time.sleep(0.5)
    rate = rospy.Rate(SAMPLE_RATE)
    reader = csv.reader(open(filename))
    reader_list = list(reader)
    
    for i in range(0, NUM_OF_ITERATIONS):
        if i % 2 == 0:
            for line in reader_list:
                if rospy.is_shutdown(): break
                values = [float(x) for x in line]

                receiveTime = Time()
                receiveTime.data = rospy.Time.from_sec(time.time())

                #rospy.loginfo(value)
                joints = JointPosition()
                joints.header.frame_id = "/base_link" 
                joints.header.stamp = rospy.Time.now()
                joints.position.a1 = values[0]
                joints.position.a2 = values[1]
                joints.position.a3 = values[2]
                joints.position.a4 = values[3]
                joints.position.a5 = values[4]
                joints.position.a6 = values[5]
                joints.position.a7 = values[6]

                pose = PoseStamped()
                pose.header.frame_id = "/world"
                pose.header.stamp = rospy.Time.now()
                pose.pose.position.x = values[7]
                pose.pose.position.y = values[8]
                pose.pose.position.z = values[9]
                pose.pose.orientation.x = values[10]
                pose.pose.orientation.y = values[11]
                pose.pose.orientation.z = values[12]
                pose.pose.orientation.w = values[13]  

                pub.publish(joints)
                pose_pub.publish(pose)
                time_pub.publish(receiveTime)
                rate.sleep()
        else:
            for line in reversed(reader_list):
                if rospy.is_shutdown(): break
                values = [float(x) for x in line]
                #rospy.loginfo(value)
                joints = JointPosition()
                joints.header.frame_id = "/base_link"
                joints.header.stamp = rospy.Time.now()
                joints.position.a1 = values[0]
                joints.position.a2 = values[1]
                joints.position.a3 = values[2]
                joints.position.a4 = values[3]
                joints.position.a5 = values[4]
                joints.position.a6 = values[5]
                joints.position.a7 = values[6]

                pose = PoseStamped()
                pose.header.frame_id = "/world"
                pose.header.stamp = rospy.Time.now()
                pose.pose.position.x = values[7]
                pose.pose.position.y = values[8]
                pose.pose.position.z = values[9]
                pose.pose.orientation.x = values[10]
                pose.pose.orientation.y = values[11]
                pose.pose.orientation.z = values[12]
                pose.pose.orientation.w = values[13]  

                pub.publish(joints)
                pose_pub.publish(pose)
                rate.sleep()
        time.sleep(0.5)


if __name__ == '__main__':
    # if len(sys.argv) >  5 or len(sys.argv) < 2:
    #     print 'Usage: ' + 'filename [sample rate] [topicName]'
    # elif len(sys.argv) == 2:
    #     try:
    #         talker(sys.argv[1])
    #     except rospy.ROSInterruptException:
    #         pass
    # elif len(sys.argv) == 3:
    #     try:
    #         SAMPLE_RATE = float(sys.argv[2])
    #         talker(sys.argv[1])
    #     except rospy.ROSInterruptException:
    #         pass
    # elif len(sys.argv) == 4:
    #     try:
    #         SAMPLE_RATE = float(sys.argv[2])
    #         talker(sys.argv[1], sys.argv[3])
    #     except rospy.ROSInterruptException:
    #         pass
    # elif len(sys.argv) == 5:
    #     try:
    #         SAMPLE_RATE = float(sys.argv[2])
    #         NUM_OF_ITERATIONS = int(sys.argv[4])
    #         talker(sys.argv[1], sys.argv[3])
    #     except rospy.ROSInterruptException:
    #         pass
    try:
        SAMPLE_RATE = float(sys.argv[2])
        NUM_OF_ITERATIONS = int(sys.argv[5])
        talker(sys.argv[1], sys.argv[3], sys.argv[4])
    except rospy.ROSInterruptException:
        pass