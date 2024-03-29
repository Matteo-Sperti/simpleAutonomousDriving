#!/usr/bin/env python3

""""
P. I. Corke, "Robotics, Vision & Control", Springer 2017
"""

import numpy as np

class PathFinderController:
    """
    Constructs an instantiate of the PathFinderController for navigating a
    3-DOF wheeled robot on a 2D plane
    Parameters
    ----------
    Kp_rho : The linear velocity gain to translate the robot along a line
             towards the goal
    Kp_alpha : The angular velocity gain to rotate the robot towards the goal
    Kp_beta : The offset angular velocity gain accounting for smooth merging to
              the goal angle (i.e., it helps the robot heading to be parallel
              to the target angle.)
    """

    def __init__(self, Kp_rho, Kp_alpha, Kp_beta, wheelbase, max_angle, max_speed):
        self.Kp_rho = Kp_rho
        self.Kp_alpha = Kp_alpha
        self.Kp_beta = Kp_beta
        self.wheelbase = wheelbase
        self.max_angle = max_angle
        self.max_speed = max_speed

    def calc_control_command(self, x_diff, y_diff, theta, theta_goal, direction):
        """
        Returns the control command for the linear and angular velocities
        Parameters
        ----------
        x_diff : The position of target with respect to current robot position
                 in x direction
        y_diff : The position of target with respect to current robot position
                 in y direction
        theta : The current heading angle of robot with respect to x axis
        theta_goal: The target angle of robot with respect to x axis
        Returns
        -------
        rho : The distance between the robot and the goal position
        v : Linear velocity
        psi : Steering angle of the sterring wheel
        """

        # Description of local variables:
        # - alpha is the angle to the goal relative to the heading of the robot
        # - beta is the angle between the robot's position and the goal
        #   position plus the goal angle
        # - Kp_rho*rho and Kp_alpha*alpha drive the robot along a line towards
        #   the goal
        # - Kp_beta*beta rotates the line so that it is parallel to the goal
        #   angle
        #
        # Note:
        # we restrict alpha and beta (angle differences) to the range
        # [-pi, pi] to prevent unstable behavior e.g. difference going
        # from 0 rad to 2*pi rad with slight turn

        rho = np.hypot(x_diff, y_diff)
        alpha = (np.arctan2(y_diff, x_diff)
                 - theta + np.pi) % (2 * np.pi) - np.pi
        beta = (theta_goal - theta - alpha + np.pi) % (2 * np.pi) - np.pi
        v = self.Kp_rho * rho                                   # from rho to v
        w = self.Kp_alpha * alpha - self.Kp_beta * beta         # from alpha and beta to w

        v = v*direction      
        if abs(v) > self.max_speed:                  # security check for the motor speed
                v = np.sign(v) * self.max_speed
        
        psi = np.arctan(w*self.wheelbase/abs(v))     # calculate the steering angle in rad
        psi = psi*(180/np.pi)                        # conversion to deg   
        if abs(psi) > self.max_angle:                # security check for the steering angle
            psi = np.sign(psi) * self.max_angle

        
        return v, psi