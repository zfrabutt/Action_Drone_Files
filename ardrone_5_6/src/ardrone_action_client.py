#! /usr/bin/env python
import rospy
import time
import actionlib
from geometry_msgs.msg import Twist
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback

PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4
nImage = 1

# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating a new message has been received
def feedback_callback(feedback):
    global nImage
    print('[Feedback] image n.%d received'%nImage)
    nImage += 1

# initializes the action client node
cmd_vel = Twist()
cmd_vel.linear.x = 0.0 #want to modify x for speed
cmd_vel.linear.z = 0.0
cmd_vel.angular.z = 0.0 #want to modify z for turning
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.init_node('drone_action_client')

# create the connection to the action server
client = actionlib.SimpleActionClient('/ardrone_action_server', ArdroneAction)
# waits until the action server is up and running
client.wait_for_server()

# creates a goal to send to the action server
goal = ArdroneGoal()
goal.nseconds = 10 # indicates, take pictures along 10 seconds

# sends the goal to the action server, specifying which feedback function
# to call when feedback received
client.send_goal(goal, feedback_cb=feedback_callback)

# Uncomment these lines to test goal preemption:
#time.sleep(3.0)
#client.cancel_goal()  # would cancel the goal 3 seconds after starting
state_result = client.get_state()
rate = rospy.Rate(1)
launch = rospy.Rate(3)
cmd_vel.linear.z = 0.5
launch.sleep()
cmd_vel.linear.z = 0.0

while state_result < DONE:
    cmd_vel.linear.x = 0.5
    pub.publish(cmd_vel)
    rate.sleep()
    state_result = client.get_state()
# wait until the result is obtained
# you can do other stuff here instead of waiting
# and check for status from time to time 
# status = client.get_state()
# check the client API link below for more info

cmd_vel.linear.x = 0.0
pub.publish(cmd_vel)

#client.wait_for_result()

print('[Result] State: %d'%(client.get_state()))