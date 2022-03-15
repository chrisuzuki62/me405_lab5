'''!
   @file                mainpage.py
   @brief               Main page for documentation site.
   @details             This is the main page for the doxygen site. It contains links to 
                        the code for each component of ther term project some information about each one. 

   @mainpage

   @section sec_rep     Repository
                        The repository for all the files can be found at https://github.com/chrisuzuki62/me405_termproject

   @section sec_design      Software Design
                            
    
    @subsection sec_1 Overview 
    Our program is written in micropython and uses asynchronous cooperative multitasking to run the tasks needed for <br>
    our 2D pen plotter which include the following files: <br><br>
    <b>controller.py</b> - Provides proportional controller for the motors <br>
    <b>encoder.py</b> - Encoder driver for our Pittman DC motors <br>
    <b>inversekinematic.py</b> - Inverse kinematic calculator for our four-bar linkage <br>
    <b>main.py</b> - Main script to run our 2D pen plotter <br>
    <b>motor.py</b> - Motor driver for our Pittman DC motors and our Tower Pro SG90 servo motor <br>
    <b>S.hpgl</b> - HPGL file for the sketch of a grafitti style "S" <br><br>
    The following files were provided by Dr. John R. Ridgley: <br>
    <b>cotask.py</b> - Allows for asynchronous cooperative multitasking <br>
    <b>task_share.py</b> - Allows for shared variables between tasks <br><br>
    
    
    @subsection sec_2 Task Diagram
    The task digram, shown below in Figure 1, consists of three task contained within main.py: two motor tasks <br>
    and one plotter task. The plotter tasks is responsible for reading the HPGL file and calculating the inverse <br>
    kinematics for the two driven linkages on our pen plotter. After calculating the desired angular position for <br>
    each motor, the plotter task places those values in their respective shared variable for the two motor tasks to <br>
    read. The motor tasks simply read from the shared variable and runs a proportional controller to get to the <br>
    desired location.
    
    
    \image html TermTD.png "Figure 1: Term Project Task Diagram"
    
    
    @subsection sec_3 FSM for Plotter Task
    The finite state machine (FSM) for the plotter task consists of six states: read HPGL, initialize, pen up, <br>
    pen down, calculate inverse kinematics, and finished/waiting. When the program is run, the plotter task <br>
    starts off reading a section of the HPGL file up to the first semicolon. The first two strings of each <br>
    section will determine which state the FSM will transition to next: "IN" for initialize, "PU" for lifting <br>
    the pen up, "PD" for setting the pen down, etc. At their respective state, the program will carry out a <br>
    function such as setting the appropriate duty cycle for the servo motor to lift the pen up. The FSM then <br>
    checks to see if there is any coordinate data following the first two strings. If there is coordinate data, <br>
    the program will take the coordinate and perform the inverse kinematics, using inversekinematic.py, and write <br>
    the desired encoder position into a shared object which will then be handled by the motor tasks. When the plotter <br>
    task finishes processing all the coordinate data, the FSM jumps back to the state where it reads the HPGL file <br>
    for the next set of instructions. Finally, when the program raches the end of the HPGL file, it simply enters a <br>
    waiting or finishd state. Please refer to Figure 2 below for the state transition diagram. <br> 

    \image html TermTD.png "Figure 2: State Transition Diagram for Plotter Task"
    
   
   @author              Damond Li
   @author              Chris Or
   @author              Chris Suzuki

   @date                March 14, 2022

                        
                        
                        
                        

                        

'''






