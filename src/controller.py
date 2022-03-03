"""!
    @file       controller.py
    @brief      A module for proportional gain control
    @details    This controller module is written to be a generic proportional controller
                which can easily be integrated with other procedures. After specifying
                a desired gain, simply pass in the current value/position/state of the
                system and the controller will output the necessary value for the plant in
                the closed-loop negative feedback system.
    @author Damond Li
    @author Chris Or
    @author Chris Suzuki
    @date 2/10/22
"""

import pyb
import motor
import encoder
import time
import utime

class Controller:
    '''! 
    @brief      Class for a proportional controller
    @details    This class contains the approprate methods to set the gain,
                set the desired position, run the proportional controller, run a step response for a
                motor, and print out the data from the step response.
    '''

    def __init__(self):
        '''! 
        @brief      Constructs a controller object
        @details    Establishes the initial values used by the methods in this class. The proportional
                    gain is initially set to zero. There is an empty list used to collect encoder data.
                    Variables to keep track of time are also established
        '''
        
        ## Proportional gain for the controller
        self.gain = 0
        
            
    def update(self, current_position):
        '''! 
        @brief      Runs one instance of the proportional controller
        @details    Calculates the error between the current position and the desired position.
                    This error is multiplied by a proportional gain to get an input for the plant.
        @param current_position  The current value/position of the system. This is the negative
                                 feedback loop for the closed-loop system.
        @return     Returns the input that goes into the plant of the closed loop system
        '''
        
        ## Difference between the desired value and the current value
        error = self.des_pos - current_position
        
        ## The controller output
        output = error * self.gain
        
        if output > 100:
            output = 100
        elif output < -100:
            output = -100
        
        # Return output
        return output
        
        
    def set_gain(self, desired_gain):
        '''! 
        @brief      Sets the proportional gain for the controller
        @param desired_gain The desired gain for the controller
        '''
        self.gain = desired_gain

    def set_position(self, desired_position):
        '''! 
        @brief      Sets the desired value/position for the controller
        @details    The controller will used this value to calculate the necessary output
                    to bring the system closer to the desired position
        @param desired_position The desired value/position for the system
        '''
        ## Desired position/value for the controller
        self.des_pos = desired_position
        

if __name__ == '__main__':
    # Establish reference time
    start_time = time.time()
    
    # Create motor, encoder, and controller objects
    mtr1 = motor.Motor(1)
    enc1 = encoder.Encoder(1)
    ctr = Controller()
    
    # Enable motor
    mtr1.enable()
    
    # Set desired gain and position
    ctr.set_gain(0.1)
    ctr.set_position(16300)
    
    # Run the controller for two seconds
    while time.time() - start_time < 2:
        power = ctr.update(enc1.read())
        mtr1.set_duty_cycle(power)
        print(enc1.read())
    
    # Disable motor after two seconds
    mtr1.disable()
   
