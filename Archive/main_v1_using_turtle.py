"""Double pendulum simulation.
All units are SI.  Meters, seconds, kilograms, radians.
"""

# Imports
from math import sin
from math import cos
from math import pi
import time
# Drawing
import turtle
# Animations
import imageio
from pathlib import Path
from pygifsicle import optimize

# Todos
# TODO: GUI for user-set parameters
# TODO: Graphicalize, making it update at regular, timed intervals such that it's in real time.
# TODO: Incorporate friction, then auto-stop after a minimum amount of movement for a certain number of frames.
# TODO: Keep a list of states.

# Givens
g = 9.81

# User-set parameters
dt = 0.2  # TODO: Too big
w0, w1 = 0, 0
theta0, theta1 = 0, -1
m0, m1 = 1, 10
l0, l1 = 5, 3

# Determine static dependent variables
I0 = m0*l0**2
I1 = m1*l1**2

# Set up dimensions for the screen.
ctbd = l0 + l1     # Center to bottom displacement.  Distance from the center of the screen to the bottom middle.

# Set up the screen.
#s = turtle.getscreen()
#s.setworldcoordinates(-ctbd, -ctbd, ctbd, ctbd)
turtle.setworldcoordinates(-ctbd, -ctbd, ctbd, ctbd)

# Simulation loop
while True:
    time_start = time.time()
    # Find forces
    F01 = m1 * l1 * w1 ** 2
    # Find torques
    T0 = -m0 * g * l0 * cos(theta0) + F01 * l0 * sin(theta1 - theta0)
    T1 = -m1 * g * l1 * cos(theta1)
    # Find angular accelerations
    a0 = T0/I0
    a1 = T1/I1
    # Find angular velocities
    w0 = w0 + a0*dt
    w1 = w1 + a1*dt
    # Find angular positions
    theta0 = theta0 + w0*dt
    theta1 = theta1 + w1*dt
    # Draw
    theta0deg, theta1deg = theta0*180/pi, theta1*180/pi
    turtle.reset()
    turtle.speed(0)
    turtle.right(90)
    turtle.shape("triangle")
    turtle.stamp()
    turtle.left(90)
    turtle.shape("circle")
    turtle.left(theta0deg)
    turtle.forward(l0)
    turtle.stamp()
    turtle.left(theta1deg - theta0deg)
    turtle.forward(l1)
    turtle.stamp()

    # Wait the rest of dt
    time_taken = time.time() - time_start
    time.sleep(dt - time_taken)
