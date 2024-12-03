# Modeling a spacecrafts reentry into a planets atmosphere.

Project with the current objective of modeling a spacecrafts reentry into a planets atmopshere, and with that information,
plot a heat map of the likely landing locations as well as studying ideal reentry angle, given the crafts material characteristics,
to maximize slow down but not burning up the craft.

Ive broken the overall projet down into levels, 1 being the simplest, and increasing in complexity and higher level factors being accounted
for as the levels increase.
## Level 1:
   * Treat the spacecraft as a point mass
   * Simple ballistics trajectory with only gravity
   * No atmospheric effects (i.e. no drag)

     ** Desired output: Get the Runge-Kutta integrator functioning and have the model predict a single landing point, given the crafts initial conditions. **
## Level 2:
   * Add atmospheric effects (simple model of atmosphere density to start)
   * Basic drag, so slightly more complex spacecraft model (Im not delving into any computational fluid dynamics in this project,
     so it will still be a high level approximation in the end)

     ** Desired output: Generate a basic probability distribution of where, given initial conditions, the spacecraft will likely land. **
## Level 3:
   * More complex/realistic atmospheric density and effects approximation.
   * Start to delve into basic thermal effects felt on the spacecraft. I want to eventually have the criteria of it not burning up too quickly given the crafts material constraints.
   * Possibly factor in basic lift forces.


## Level 1 Outputs:
This is the simple trajectory model that is generated given some spacecrafts initial conditions such as position and velocity.
![Screenshot 2024-12-02 at 8 05 09 PM](https://github.com/user-attachments/assets/4743519c-29e8-484c-9ae4-7ed1563d19ed)
As can be seen in this example, it was given such a velocity that it will continually miss the surface.

This second plot is showing the point that the spacecraft will hit the surface and where it believes that location correlates to on the actual Earth.
<img width="1350" alt="Screenshot 2024-12-02 at 8 13 05 PM" src="https://github.com/user-attachments/assets/06cc66f0-d3e9-449b-878a-91f5b7483034">


