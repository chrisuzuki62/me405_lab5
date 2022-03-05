"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share

import inversekinematic
import controller
import motor
import encoder
        
def motor1_task():
    while True:
        ctr1.set_position(theta1.get())
        duty1 = ctr1.update(enc1.read())
        mtr1.set_duty_cycle(duty1)
        yield(0)
        
def motor2_task():
    while True:
        ctr2.set_position(theta2.get())
        duty2 = ctr2.update(enc2.read())
        mtr2.set_duty_cycle(duty2 * -1)
        yield(0)

"""
def user_task():
    while True:
        if VCP.any():
            serport = VCP.read():
                if serport == b'r':
                    pass
                elif serport == b'z':
                    pass
                elif serport == b'a':
                    pass
                
        yield(0)
"""
        
def plotter_task():
    not_finished = True
    buffer = ""
    while True:
        with open('Test.hpgl', 'r') as file:
            while not_finished:
                boolean = True
                # Have a buffer that collects all the strings
                while boolean:
                    char = file.read(1)
                    if char == "":
                        not_finished = False
                        boolean = False
                    elif char == ";":
                        boolean = False
                    else:
                        buffer += char
                
                if buffer[0:2] == "IN":
                    pass
                    
                elif buffer[0:2] == "PU":
                    pass
                    
                elif buffer[0:2] == "PD":
                    pass   
                    
                elif buffer[0:2] == "SP":
                    pass
                    
                coord = buffer[2::].split(',')
                if len(coord) >= 2:
                    x = 0
                    y = 1
                    for pp in range(len(coord)//2):
                        x_plot = (int(coord[x]) / max_hpgl * draw_width) + draw_zero_x
                        y_plot = (int(coord[y]) / max_hpgl * draw_height) + draw_zero_y
                        thetas = Ink.IK(x_plot, y_plot)
                        print(thetas[0], thetas[1])
                        theta1.put(thetas[0] * enc_ticks_per_rev * teeth_ratio / 360)
                        theta2.put((thetas[1] - 180) * enc_ticks_per_rev * teeth_ratio / 360)
                        x += 2
                        y += 2
                        
                        yield(0)
                        
                        ctr1.set_gain(0.10)
                        ctr2.set_gain(0.10)
                        
                buffer = ""
                boolean = True
                
                yield(0)
        yield(0)

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    
    """
    q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
                           name = "Queue 0")
    """
    ######################################################################################
    
    # Create motor and encoder objects
    
    mtr1 = motor.Motor(1)
    mtr2 = motor.Motor(2)
    
    
    
    enc1 = encoder.Encoder(1)
    enc2 = encoder.Encoder(2)
    
    Ink = inversekinematic.InverseKinematic()
    
    ctr1 = controller.Controller()
    ctr2 = controller.Controller()
    
    enc_ticks_per_rev = 16384
    teeth_ratio = 60/16
    
    # Set up drawing location with both actuation linkages at (0,0)
    draw_width = 4                    # inches
    draw_height = 4                   # inches

    draw_zero_x = 4                   # inches
    draw_zero_y = -2 # draw_height / -2    # inches
    
    max_hpgl = 10_000
    
    # Desired positions in ticks
    des_theta_1 = task_share.Share ('h', thread_protect = False, name = "Desired Theta 1")
    des_theta_2 = task_share.Share ('h', thread_protect = False, name = "Desired Theta 2")
    
    # Duty cycle to operate each motor
    duty_cycle_1 = task_share.Share ('h', thread_protect = False, name = "Duty Cycle 1")
    duty_cycle_2 = task_share.Share ('h', thread_protect = False, name = "Duty Cycle 2")
    
    # Shares for the linkage angles
    theta1 = task_share.Share ('f', thread_protect = False, name = "Theta for Link 1")
    theta2 = task_share.Share ('f', thread_protect = False, name = "Theta for Link 2")
    
    mtr1.enable()
    mtr2.enable()
    enc1.zero()
    enc2.zero()
    
    ctr1.set_gain(0.05)
    ctr2.set_gain(0.05)

    ######################################################################################

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (motor1_task, name = 'Motor_Task_1', priority = 2, 
                         period = 5, profile = True, trace = False)
    task2 = cotask.Task (motor2_task, name = 'Motor_Task_2', priority = 1, 
                         period = 5, profile = True, trace = False)
    task3 = cotask.Task (plotter_task, name = 'Plotter_Task', priority = 0, 
                         period = 100, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()
    
    mtr1.disable()
    mtr2.disable()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
