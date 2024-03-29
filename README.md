# simpleAutonomousDriving

ROS package containing a navigation system of an autonomous car-like robot. 
The aim of this package is focused on the parking problem maneuvers on a 2D plane.
No obstacles are considered and no position sensors are required.
The package has been tested on a real prototype equipped as previously described.

Main Features:

1. Manual driving of a car-like robot throught wifi connection and a joystick

2. Simulation of car-like robot with a rear motor and a front steering wheel

3. Autonomous driving of a car-like robot to a goal pose


# Requirements

For running each sample code:

- [Python 3.x](https://www.python.org/)
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [Matplotlib](https://matplotlib.org/)
- [ROS joy](http://wiki.ros.org/joy)
- [ROS rosserial_server](http://wiki.ros.org/rosserial_server)
 

# How to install

1. Open the catkin_ws/src directory

> cd ~/catkin_ws/src

2. Clone this repo.

> git clone https://github.com/Matteo-99/lego_ferrari.git

3. Install the package dependancy.

initialize rosdep (if not already initialized):

> sudo rosdep init

> rosdep update

install dependacy for the lego_ferrari package :

> rosdep install lego_ferrari

4. Make the lego_ferrari package

> cd ~/catkin_ws

> catkin_make

5. The installation is complete and the package is ready to be used.


# Contents

## Config files

The configuration file ./config/my_param.yaml contains all the parameters used in the package like:
- limits of the commands
- frequency of the system
- parameters of the simulated car and of DC motor dynamical model
- parameters for the control algorithm

## Launch files

### autonomous_ferrari.launch

This launcher starts:
- the joy_node node to control the PS4 joystick connected as /dev/input/js2 (change if necessary). If it is not possible to use a joystick, in order to start an autonomous drive, publish the following message:

> rostopic pub /joy sensor_msgs/Joy '{ header: {}, axes: [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0], buttons: [0, 0, 1, 0, 0, 0, 0, 0]}'

- the rosserial_server socket_node is used to connect the robot at port 11411 as TCP client.
- the [joy_mux_navigation_node](#joy_mux_navigation_node) is used to switch between autonomous and manual driving
- the [navigator_node](#navigator_node) that provides the control algorithm for navigation
- the [simulated_car_node](#simulated_car_node) that simulates the behaviour of the car-like robot
- the [saturate_cmd_node](#saturate_cmd_node) that saturates the command according to the chosen limits

### test_simulate_car.launch

This launcher starts:
- the rosserial_server socket_node is used to connect the robot at port 11411 as TCP client.
- the [test_node](#test_node) that generates the test graphical results
- the [simulated_car_node](#simulated_car_node) that simulates the behaviour of the car-like robot
- the [saturate_cmd_node](#saturate_cmd_node) that saturates the command according to the chosen limits

## Ros nodes

### joy_mux_navigation_node

It selects the automatic or manual driving. Pressing “∆” on the PS4 controller it’s possible to set the autonomous driving and the goal is inserted on the keyboard. In order to return to manual driving, it’s possible to press “X” at any time. It is also responsible to clear the used variables in the navigator and in the simulated_car before each new iteration and to deliver the output commands to the saturate_cmd node.

### navigator_node

This node is used to navigate a car-like robot on a 2-D plane, it computes the trajectory to be travelled in order to reach the goal by means of the path planning functions.

### saturate_cmd_node

It saturates the command values to their maximum and minimum values, also in terms of accelerations.

### simulated_car_node

This node simulates the behavior of a car-like robot through a properly adapted bicycle-like model, and delivers as output the actual pose, linear velocity and steering angle of the robot.

### test_node

The test_node provides all the functions to properly test and evaluate the parameter of the simulated car.

# Authors

- [Matteo Sperti](https://github.com/Matteo-Sperti)
- [Morgan Casale](https://github.com/morgancasale)
- [Federico Moscato](https://github.com/JMFede)
- [Francesco Stolcis](https://github.com/FraStolcis)
- Paolo Timis

# References

- [AtsushiSakai/PythonRobotics](https://arxiv.org/abs/1808.10703)
- B. Siciliano, L. S. (2007). Robotics. Modelling, planning and control. Springer.
- Corke, P. (2011). Robotics, vision and control. Springer.
