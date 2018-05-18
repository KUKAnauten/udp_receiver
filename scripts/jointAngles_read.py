#!/usr/bin/env python
import sys
import csv
import rospy
import time
from iiwa_msgs.msg import JointPosition

SAMPLE_RATE = 100

def talker(filename, topicName='JointPosition'):
    pub = rospy.Publisher('jointAnglesFromFile/'+topicName, JointPosition, queue_size=10)
    rospy.init_node('jointPosPublisher', anonymous=True)
    time.sleep(0.5)
    rate = rospy.Rate(SAMPLE_RATE)
    reader = csv.reader(open(filename))
    
    for line in reader:
        if rospy.is_shutdown(): break
        values = [float(x) for x in line]
        #rospy.loginfo(value)
        pose = JointPosition()
        pose.header.frame_id = "/base_link" # mod?
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
