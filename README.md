# Term Project - Drawing Bot

# System Description

The goal of our project is to create a 2.5 degree of freedom pen plotter that does not operate using a cartesian coordinate system. Our system accomplishes this goal by using a four-bar linkage system that actuates similar to a SCARA robot. Any user using an HPGL file to replicate their digital drawing will be able to use this device.


# Hardware Design

Our system consists of a robot arm-type system inspired by the Line-us drawing robot. We will use the two Pittman DC geared motors found in the ME405 tubs to control a set of four linkages. The two motors will me mounted inline vertically, facing each other, and connect at the center location to two of the linkages. A Tower Pro SG90 servo motor borrowed from the robotics lab will be used to control an up and down movement to raise and lower the pen from the drawing surface. We will have a 2.5 degree of freedom system with two degrees of freedom from the two DC geared motors and a half degree of freedom from the servo motor to raise and lower the system. The four linkages form a semi-diamond shape that creates a robot arm that functions similarly to a SCARA-type robot arm. We plan on 3D printing the linkages from PLA plastic. The motors will be mounted on a 3D-printed frame. Additional components required for the up and down movement of the system will also be 3D-printed. Gears and bearings will be added to improve the resolution and smoothness of our robot's movements. The current design of the Drawing bot is seen in Figure 1. below.


![test](CAD.JPG)

Figure 1. CAD of concept Drawing Bot

## Bill of Materials for Drawing Bot

| Qty. | Part                    | Source                | Est. Cost |
|:----:|:----------------------  |:----------------------|:---------:|
|  2   | ME405 Pittman DC Motors | ME405 Tub             |     -     |
|  1   | Nucleo Board with Shoe  | ME405 Tub             |     -     |
|  1   | Mini Tower Pro SG90 Ser.| Robotics Club         |     -     |
|  1   | Pen                     | Someone on Team       |     -     |
|  1   | PLA 3D Filament         | Someone on Team       |     -     |
|  8   | M3-8mm Screws           | REV Robotics          |     -     |
|  2   | KHK-BSS0.5-60B Gears    | Robotics Club         |     -     |
|  3   | ID 6mm OD 17mm Bearing  | Robotics Club         |     -     |
|  2   | Stainless Bars Tools    | Robotics Club         |     -     |
|  2   | M4 x 17mm Screws        | Robotics Club         |     -     |
|  2   | M4 x 10mm Screws        | Robotics Club         |     -     |

# Software Design

The program for our plotter reads from an HPGL file uploaded onto the Nucleo micrcoprocessor and carries out each step of the file to create a 2D drawing. The X-Y coordinates specified in the HPGL file are sequentially inputted into a function that calculates the inverse kinematics for both of the driven linkages on our robot. The program also allows for the location and size of the drawing to be altered as long as the drawing area is within the robot's reach. For more information on the layout our asynchronous cooperative multitasking program, please refer to our Documentation of Code linked below.

Documentation of Code: https://chrisuzuki62.github.io/me405_termproject/

# Results

The final demonstration video can be seen here: https://youtu.be/_0DGsNZlUL0

From the video and other tests performed, we found that our system overall was able to achieve its goal replicating the digital drawings. We had the Drawing bot draw two images: a star and a graffiti style "S". Running our plotter showed that it struggles to draw long straight lines as both linkages travel independently of each other without any sort of trejectory planning. Both linkages will travel to the next specified location as fast as possible and the resultant path is rarely straight.  A solution to this problem would include adding a series of intermediary points along the path. However, we found that it is possible to add too many intermendiate points for our program to raise a memory allocation error. This memory allocation error is mainly due to the current structure of our program. With more time, we are confident that we can restructure our program to read extremely high resolution HPGL files. Lastly, as seen in the video, our device experiences some overshoot when traveling longer distances. There is a fine balance when choosing the appropriate gain for our controller. Increasing the gain improves the smaller movements of our robot, but there is a risk of oversooting with larger movements. Decreasing the gain reduces overshoot, but our robot seems less responsive to smaller movements.

From this project, our group has learned the importance of spending more time thinking of alternative designs because not every features will work the way it is designed. We had three alternative designs for the half degree freedom to the lift the pen, but all of them did not work due to manufacturing inconsistencies or products not capable of their rated strength. We quickly resolved this issue by ising a mini servo attached to the arm to set the pen up and down resulting in pen swipe marks at the beginning and end of each stroke. If additional improvments were to made to this project, the first would to improve the pen lifting mechanism followed by better tuning the controller gains and restructuring our software to handle higher resolution images.

# Resources
Reference for concept: https://www.line-us.com/

GrabCAD repository: https://workbench.grabcad.com/workbench/projects/gcqKvgfJRzyWo_CtzvtAKlI-tx9kWjHW_sFcfrkAEgMBij#/space/gcChDJD7kWcv_jVIQOxMI8suMSjF-Yvh4EW6TlkZzvZ4QA

*Includes Part files, STL and drawings
