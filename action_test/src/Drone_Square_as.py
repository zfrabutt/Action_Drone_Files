#! /usr/bin/env python
import rospy
import time 
import actionlib
from geometry_msgs.msg import Twist
from actionlib.msg import TestFeedback, TestResult, TestAction

class DroneSquareClass(object):
    
  # create messages that are used to publish feedback/result
  _feedback = TestFeedback()
  _result   = TestResult()

  def __init__(self):
    # creates the action server
    self._as = actionlib.SimpleActionServer("Drone_Square_as", TestAction, self.goal_callback, False)
    self._as.start()
    
  def goal_callback(self, goal):
    # this callback is called when the action server is called.
    # this is the function that computes the Fibonacci sequence
    # and returns the sequence to the node that called the action server
    
    # helper variables
    rate = goal
    #r = rospy.Rate(10)
    success = True
    cmd_vel = Twist()
    cmd_vel.linear.x = 0.0 #want to modify x for speed
    cmd_vel.linear.y = 0.0 #want to modify z for turning
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    print("test")
    cmd_vel.linear.x = 0.3
    pub.publish(cmd_vel)
    time.sleep(5)
    cmd_vel.linear.x = 0.0
    pub.publish(cmd_vel)
    
    cmd_vel.linear.y = 0.3
    pub.publish(cmd_vel)
    time.sleep(5)
    cmd_vel.linear.y = 0.0
    pub.publish(cmd_vel)

    cmd_vel.linear.x = -0.3
    pub.publish(cmd_vel)
    time.sleep(5)
    cmd_vel.linear.x = 0.0
    pub.publish(cmd_vel)

    cmd_vel.linear.y = -0.3
    pub.publish(cmd_vel)
    time.sleep(5)
    cmd_vel.linear.y = 0.0
    pub.publish(cmd_vel)
    
    # append the seeds for the fibonacci sequence
    #self._feedback.sequence = []
    #self._feedback.sequence.append(0)
    #self._feedback.sequence.append(1)
    
    # publish info to the console for the user
    #rospy.loginfo('"fibonacci_as": Executing, creating fibonacci sequence of order %i with seeds %i, %i' % ( goal.order, self._feedback.sequence[0], self._feedback.sequence[1]))
    
    # starts calculating the Fibonacci sequence
    #fibonacciOrder = goal.order
    #for i in xrange(1, fibonacciOrder):
    
      # check that preempt (cancelation) has not been requested by the action client
      #if self._as.is_preempt_requested():
        #rospy.loginfo('The goal has been cancelled/preempted')
        # the following line, sets the client in preempted state (goal cancelled)
        #self._as.set_preempted()
        #success = False
        # we end the calculation of the Fibonacci sequence
        #break
      
      # builds the next feedback msg to be sent
      #self._feedback.sequence.append(self._feedback.sequence[i] + self._feedback.sequence[i-1])
      # publish the feedback
      #self._as.publish_feedback(self._feedback)
      # the sequence is computed at 1 Hz frequency
      #r.sleep()
    
    # at this point, either the goal has been achieved (success==true)
    # or the client preempted the goal (success==false)
    # If success, then we publish the final result
    # If not success, we do not publish anything in the result
    #if success:
    #  self._result.sequence = self._feedback.sequence
    #  rospy.loginfo('Succeeded calculating the Fibonacci of order %i' % fibonacciOrder )
    self._as.set_succeeded(self._result)
      
if __name__ == '__main__':
  rospy.init_node('Drone_Square')
  DroneSquareClass()
  rospy.spin()