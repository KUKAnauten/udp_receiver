#!/usr/bin/env python
import sys
import csv
import rospy
import time
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Time 

SAMPLE_RATE = 100

def talker(filename, topicName='PoseStamped'):
    pub = rospy.Publisher('iiwa/poseFromFile/'+topicName, PoseStamped, queue_size=1)
    time_pub = rospy.Publisher('iiwa/poseFromFile/receiveTime', Time, queue_size=1)
    #rosTime_pub = rospy.Publisher('poseFromFile/receiveRosTime', Time, queue_size=1)
    rospy.init_node('posePublisher', anonymous=True)
    # Without delay the first few values could not be received by the subscriber despite it had been 
    # already registered. Apparently it takes some time until the connection is established after the 
    # publisher (node) is created.
    time.sleep(0.5) 
    rate = rospy.Rate(SAMPLE_RATE)
    reader = csv.reader(open(filename))

    for line in reader:
        if rospy.is_shutdown(): break
        values = [float(x) for x in line]
        #rospy.loginfo(values)
        receiveTime = Time()
        #receiveRosTime = Time()
        receiveTime.data = rospy.Time.from_sec(time.time())
        #receiveRosTime.data = rospy.Time.now()
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
        pub.publish(pose)
        time_pub.publish(receiveTime)
        #rosTime_pub.publish(receiveRosTime)
        rate.sleep()

if __name__ == '__main__':
    if len(sys.argv) >  4 or len(sys.argv) < 2:
        print 'Usage: ' + 'filename [sample rate] [topicName]'
    elif len(sys.argv) == 2:
        try:
            talker(sys.argv[1])
        except rospy.ROSInterruptException:
            pass
    elif len(sys.argv) == 3:
        try:
            SAMPLE_RATE = float(sys.argv[2])
            talker(sys.argv[1])
        except rospy.ROSInterruptException:
            pass
    elif len(sys.argv) == 4:
        try:
            SAMPLE_RATE = float(sys.argv[2])
            talker(sys.argv[1], sys.argv[3])
        except rospy.ROSInterruptException:
            pass