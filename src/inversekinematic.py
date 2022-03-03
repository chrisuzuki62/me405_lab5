import math

class InverseKinematic():
    
    def __init__(self):
        self.L_A = 4
        self.L_B = 3
        self.L_C = 6
    
    def IK(self, des_x, des_y):
        
        POS = [des_x, des_y]

        theta2 = -1 * abs(math.acos((POS[0]**2 + POS[1]**2 - self.L_A**2 - self.L_C**2)/(2*self.L_A*self.L_C)))
        theta1 = math.atan2(POS[1], POS[0]) - math.atan2(self.L_C*math.sin(theta2),(self.L_A + self.L_C*math.cos(theta2)))

        link_1 = round(math.degrees(theta1), 2)

        ## Calculate the next point to repeat the steps
        POS2 = [self.L_A * math.cos(theta1) + self.L_B * math.cos(theta1 + theta2 + math.pi),
                self.L_A * math.sin(theta1) + self.L_B * math.sin(theta1 + theta2 + math.pi)]

        theta4 = -1 * abs(math.acos((POS2[0]**2 + POS2[1]**2 - self.L_B**2 - self.L_A**2)/(2*self.L_B*self.L_A)))
        theta3 = math.atan2(POS2[1], POS2[0]) - math.atan2(self.L_A*math.sin(theta4),(self.L_B + self.L_A*math.cos(theta4)));

        link_2 = round(math.degrees(theta3), 2)

        return link_1, link_2
    
if __name__ == '__main__':
    Ink = InverseKinematic()    
    ans = Ink.IK(2, -3)
    print(ans[0], ans[1])
