"""!
@file     main.py
@brief    Runs the main program; creates all objects and tasks to read an HPGL file run a 2.5 DOF plotter.
@details  This program is to be installed and ran on the MicroPython board. It creates the class objects for two DC motors,
          two encoders, one servo, an inverse kinematic calculator, as well as all the tasks and shares objects.
          The robot must be set to it's reset position before the program is run. The program will run in an endless
          loop until the user presses return on the keyboard.
@author Damond Li
@author Chris Or
@author Chris Suzuki
@date   13-Mar-2022
"""


import gc
import pyb
import motor
import utime
import cotask
import encoder
import task_share
import controller
import inversekinematic
        
def motor1_task():
    """!
    @brief      Task for motor 1
    @details    This task is responsible for setting the gain and desired position in the controller
                and sets a corresponding duty cycle in the motor driver for motor 1.
    """
    while True:
        ctr1.set_position(theta1.get())
        duty1 = ctr1.update(enc1.read())
        mtr1.set_duty_cycle(duty1)
        yield(0)
        
def motor2_task():
    """!
    @brief      Task for motor 2
    @details    This task is responsible for setting the gain and desired position in the controller
                and sets a corresponding duty cycle in the motor driver for motor 2.
    """
    while True:
        ctr2.set_position(theta2.get())
        duty2 = ctr2.update(enc2.read())
        mtr2.set_duty_cycle(duty2 * -1)
        yield(0)
        
        
def plotter_task():
    """!
    @brief      Task for the plotter or controller
    @details    This task is responsible for reading from the HPGL file, processing the inputs, and
                calculating the desired angular position given the X-Y coordinates in the HPGL file.
                This task is also responsible for all plotter function such as lifting the pen up and down.
    """
    
    ## A variable representing whether the entire HPGL file has been read
    not_finished = True
    ## A string buffer for each process/section in the HPGL file (Pen Up, Pen Down, Initialize, etc.)
    buffer = ""
    ## A variable for a set time in the future to continue a task. This will be used to set a delay after lifting the pen up and down
    deadline = utime.ticks_ms()
    
    # Create the over arching loop that continues to run even if the HPGL file is finished reading
    while True:
        
        ## A variable for the HPGL file using the 'with open' function
        with open('S.hpgl', 'r') as file:
            
            # This loop encapsulates the finite state machine
            while not_finished:
                ## A boolean variable representing whether to continue appending strings to the buffer
                boolean = True
                
                # Have a buffer that collects all the strings
                while boolean:
                    
                    # If the next character is numerical or is a number, append the string
                    # otherwise you have reached the end of a section or file
                    char = file.read(1)
                    if char == "":
                        not_finished = False
                        boolean = False
                    elif char == ";":
                        boolean = False
                    else:
                        buffer += char
                
                # Read the first two strings of each section
                if buffer[0:2] == "IN":
                    print("Initializing")
                
                # Read the first two strings of each section
                elif buffer[0:2] == "PU":
                    print("Setting Pen Up")
                    servo.set_servo_pos(20)
                    # Set the deadline to resume the FSM after 1000ms
                    deadline = utime.ticks_add(utime.ticks_ms(), 1000)
                    
                # Read the first two strings of each section
                elif buffer[0:2] == "PD":
                    print("Setting Pen Down")
                    servo.set_servo_pos(0)
                    # Set the deadline to resume the FSM after 1000ms
                    deadline = utime.ticks_add(utime.ticks_ms(), 1000)

                
                # After processing the first two strings of each section, see if a delay is needed
                # This essentially freezes the program until the current time excededs the deadline
                while utime.ticks_diff(deadline, utime.ticks_ms()) > 0:
                    pass
                    yield(0)

                
                # Split everything after the two strings by the comma
                coord = buffer[2::].split(',')
                if len(coord) >= 2:
                    x = 0
                    y = 1
                    for pp in range(len(coord)//2):
                        x_plot = (int(coord[x]) / max_hpgl * draw_width) + draw_zero_x
                        y_plot = (int(coord[y]) / max_hpgl * draw_height) + draw_zero_y
                        # Process X-Y coord into thetas through the inverse kinematic calculator
                        thetas = Ink.IK(x_plot, y_plot)
                        # Convert to encoder position and put into shares object
                        theta1.put(thetas[0] * enc_ticks_per_rev * teeth_ratio / 360)
                        theta2.put((thetas[1] - 180) * enc_ticks_per_rev * teeth_ratio / 360)
                        x += 2
                        y += 2
                        
                        yield(0)
                        
                        
                        # Increase the gain after the machine starts running (optional). Use 0.12 for star
                        ctr1.set_gain(0.12)
                        ctr2.set_gain(0.12)
                
                # Reset the buffer and boolean for the next section
                buffer = ""
                boolean = True
                
                yield(0)
                
        yield(0)
        

# Notes from Dr: Ridgley:
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.

if __name__ == "__main__":
                           
    # Create motor and encoder objects
    ## Object for motor 1; this is for the motor with the shaft facing upwards
    mtr1 = motor.Motor(1)
    ## Object for motor 2; this is for the motor with the shaft facing downwards
    mtr2 = motor.Motor(2)
    ## Object for motor 3; this is for the servo motor lifting the pen up and down
    servo = motor.Motor(3)
    
    ## Object for encoder 1; linked with motor 1
    enc1 = encoder.Encoder(1)
    ## Object for encoder 2: linked with motor 2
    enc2 = encoder.Encoder(2)
    
    ## Object for the inverse kinematic calculator
    Ink = inversekinematic.InverseKinematic()
    
    ## Object for the proportional controller for motor 1
    ctr1 = controller.Controller()
    ## Object for the proportional controller for motor 2
    ctr2 = controller.Controller()
    
    ## Constant representing the number of encoder ticks per revolution
    enc_ticks_per_rev = 16384
    ## Constant for the ratio of teeth between the output and input gear
    teeth_ratio = 60/16
    
    ###############################################################################
    # Set up drawing location with both actuation linkages at (0,0)
    
    ## Constant for the drawing width used to scale the X-Y coord in the HPGL
    draw_width = 6                    # inches
    ## Constant for the drawing height used to scale the X-Y coord in the HPGL
    draw_height = 6                   # inches

    ## Location of the y-axis relative to the center of the output gear
    draw_zero_x = 7                   # inches
    ## Location of the x-axis relative to the center of the output gear
    draw_zero_y = -2                  # inches
    
    ## Constant for the largest value in the HPGL file, used to scale the drawing
    max_hpgl = 9_000
    
    # Shares for the linkage angles
    ## A shares object. Handles the desired position of motor 1
    theta1 = task_share.Share ('f', thread_protect = False, name = "Theta for Link 1")
    ## A shares object. Handles the desired position of motor 2
    theta2 = task_share.Share ('f', thread_protect = False, name = "Theta for Link 2")
    
    # Enable motor 1
    mtr1.enable()
    # Enable motor 2
    mtr2.enable()
    # Zero encoder 1
    enc1.zero()
    # Zero encoder 2
    enc2.zero()
    
    # Set gain
    ctr1.set_gain(0.05)
    ctr2.set_gain(0.05)

    ######################################################################################
    
    # Notes from Dr: Ridgley:
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    
    task1 = cotask.Task (motor1_task, name = 'Motor_Task_1', priority = 1, 
                         period = 5, profile = True, trace = False)
    task2 = cotask.Task (motor2_task, name = 'Motor_Task_2', priority = 1, 
                         period = 5, profile = True, trace = False)
    task3 = cotask.Task (plotter_task, name = 'Plotter_Task', priority = 0, 
                         period = 100, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)
    
    # Notes from Dr: Ridgley:
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()
    
    # Notes from Dr: Ridgley:
    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()
    
    # Notes from Dr: Ridgley:
    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()
    
    # Disable motor 1
    mtr1.disable()
    # Disable motor 2
    mtr2.disable()

    # Notes from Dr: Ridgley:
    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
    
