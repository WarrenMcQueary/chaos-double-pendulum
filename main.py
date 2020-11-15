"""Double pendulum simulation.
All units are SI.  Meters, seconds, kilograms, radians.
This version uses tkinter instead of turtle graphics, in an effort to reduce the frame draw time and thereby
allow for smaller dt.
This is still not fully real-time, though it is close.
"""

# Imports
from math import sin
from math import cos
from math import pi
import time
# Drawing
import turtle
import tkinter
# Animations
import imageio
from pathlib import Path
from pygifsicle import optimize

# Todos
# TODO: Where's the mystery energy coming from?  Probably one of my physics equations is wrong.
# TODO: Scale frame for shorter lengths.
# TODO: GUI for user-set parameters, including whether to trace, and if so, how often.
# TODO: Incorporate friction, then auto-stop after a minimum amount of movement for a certain number of frames.
# TODO: Keep a list of states.


def simulate_and_draw_frame():
    """Simulates a frame of double pendulum movement, then updates sim_canvas."""
    time_start = time.time()

    # Grab parameters
    global g, dt, w0, w1, theta0, theta1, m0, m1, l0, l1, I0, I1, ctbd

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
    coords_origin = (ctbd, ctbd)
    coords_0 = (l0*cos(theta0) + coords_origin[0], -l0*sin(theta0) + coords_origin[1])
    coords_1 = (coords_0[0] + l1*cos(theta1), coords_0[1] - l1*sin(theta1))

    sim_canvas.delete("all")
    sim_canvas.create_line(coords_origin[0], coords_origin[1], coords_0[0], coords_0[1], fill="black")
    sim_canvas.create_line(coords_0[0], coords_0[1], coords_1[0], coords_1[1], fill="blue")

    # Debugging: Print energy in the system.  This shouldn't change over time.
    v0 = (l0*w0*-sin(theta0), l0*w0*cos(theta0))     # Velocity vector
    v1 = (v0[0] + l1*w1*-sin(theta1), v0[1] + l1*w1*cos(theta1))     # Velocity vector
    v0_magnitude = (v0[0]**2 + v0[1]**2)**0.5
    v1_magnitude = (v1[0]**2 + v1[1]**2)**0.5
    kinetic_energy0 = 0.5 * m0 * v0_magnitude**2
    kinetic_energy1 = 0.5 * m1 * v1_magnitude**2
    potential_energy0 = m0 * g * l0 * sin(theta0)
    potential_energy1 = m1 * g * (l0 * sin(theta0) + l1 * sin(theta1))
    energy_total = kinetic_energy0 + kinetic_energy1 + potential_energy0 + potential_energy1
    print(energy_total)

    # Schedule the next run of simulate_and_draw_frame for after the rest of dt has elapsed
    time_taken = time.time() - time_start
    #time.sleep(dt - time_taken)
    #simulate_and_draw_frame()
    sim_canvas.after(int((dt-time_taken)*1000), simulate_and_draw_frame)


# User-set parameters
dt = 0.001  # Must be a multiple of 0.001
g = 9.81
w0, w1 = 0, 0
theta0, theta1 = 0, pi  # 0, pi may be an illustrative way to test for conservation.  Creates a "scissor motion".
m0, m1 = 1, 1
l0, l1 = 100, 100

# Determine static dependent variables
I0 = m0*l0**2
I1 = m1*l1**2

# Set up dimensions for the screen.
ctbd = l0 + l1     # Center to bottom displacement.  Distance from the center of the screen to the bottom middle.

# Set up the screen.
simulation = tkinter.Tk()
simulation.geometry(str(ctbd*2) + "x" + str(ctbd*2))
sim_canvas = tkinter.Canvas(simulation, width=ctbd*2, height=ctbd*2, background="white")
sim_canvas.grid(row=0, column=0)
sim_canvas.after(int(dt*1000), simulate_and_draw_frame)
sim_canvas.mainloop()
