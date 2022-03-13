"""!
@file       inversekinematic.py
@brief      Performs the inverse kinematic of the three-linkage plotter
@details    Calculates the desired angular position of the two driven linkages for a given X-Y coord

@author Damond Li
@author Chris Or
@author Chris Suzuki
@date   13-Mar-2022
"""

import math

class InverseKinematic():
    '''! 
    @brief      Class containing the method to perform IK
    '''
    
    def __init__(self):
        '''! 
        @brief      Constructs a calculator object
        @details    This constructor also establishes the lengths of each linkage
        '''
        ## Length of Linkage A; length of linkage attached to motor 1
        self.L_A = 4
        ## Length of Linkage B; length of linkage attached to motor 2
        self.L_B = 3
        ## Length of Linkage C; length of linkage from the end of Linkage A and the pen/pencil
        self.L_C = 6
    
    def IK(self, des_x, des_y):
        '''!
        @brief      Calculates the IK
        @detials    This method takes the X-Y coordinates and calculates the appropriate angles for each linkage
        @param des_x Desired position of the X coordinate
        @param des_y Desired position of the y coordinate
        @return     Returns a list containing the angles for each driven linkage
        '''
        
        ## Positional list with the desired coordinate
        POS = [des_x, des_y]
        
        theta2 = -1 * abs(math.acos((POS[0]**2 + POS[1]**2 - self.L_A**2 - self.L_C**2)/(2*self.L_A*self.L_C)))
        theta1 = math.atan2(POS[1], POS[0]) - math.atan2(self.L_C*math.sin(theta2),(self.L_A + self.L_C*math.cos(theta2)))
        
        ## Angle of the linkage attached to motor 1
        link_1 = round(math.degrees(theta1), 2)
        
        ## Positional list of the second IK needed for the other linkage
        POS2 = [self.L_A * math.cos(theta1) + self.L_B * math.cos(theta1 + theta2 + math.pi),
                self.L_A * math.sin(theta1) + self.L_B * math.sin(theta1 + theta2 + math.pi)]

        theta4 = -1 * abs(math.acos((POS2[0]**2 + POS2[1]**2 - self.L_B**2 - self.L_A**2)/(2*self.L_B*self.L_A)))
        theta3 = math.atan2(POS2[1], POS2[0]) - math.atan2(self.L_A*math.sin(theta4),(self.L_B + self.L_A*math.cos(theta4)));
        
        ## Angle of the linkage attached to motor 2
        link_2 = round(math.degrees(theta3), 2)

        return link_1, link_2
    
if __name__ == '__main__':
    Ink = InverseKinematic()    
    ans = Ink.IK(2, -3)
    print(ans[0], ans[1])
