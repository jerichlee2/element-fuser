#by Jerich Lee, 6/2/23
from sympy import *
import pandas as pd
from PIL import Image, ImageDraw
import numpy as np


class ModifyElement:
    def __init__(self, location, row, length):
        self.location = location
        self.row = row
        self.length = length
        
    #Clean row to get rid of string values and only keep numerical ones    
    def Truncate(self):
        truncated_data = self.row
        pos_list = []
        
        
        for i in range(4, len(truncated_data) - 1):
            if truncated_data[i] != 0:
                pos_list.append(truncated_data[i])
            
        return pos_list
    
    #Create tuple out of row
    def Tuplify(self, thelist):
        tuplify = []
        tuplify.append(tuple(thelist))
        return tuplify
    
    #Generate list of positions
    def GetPosDual(self):
        pos_list = []
        truncated_data = self.Truncate()
        for i in range(0, len(truncated_data) - 2, 3):
            pos_list.append(truncated_data[i])
            
        return pos_list
    
    #Get angles from row
    def GetAngles(self):
        pos_list = []
        truncated_data = self.Truncate()
        for i in range(1, len(truncated_data) - 1, 3):
            if truncated_data[i] != 0:
                pos_list.append(truncated_data[i])
            
        return pos_list
    
    #Get differences in each position and store in list
    def GetDiffDual(self):
        diff_list = []
        pos_list = self.GetPosDual()
        for i in range(0, len(pos_list)-1):
            diff_list.append(abs(pos_list[i] - pos_list[i+1]))
                                
        return diff_list

    #return a list of differences with the corrected offset
    def EditElementLength(self):

        pos_list = self.GetPosDual()
        combined_list = self.GetDiffDual()
        new_length_list = combined_list
         
        loc = self.location
        
        if loc == 1:
            new_length_list.insert(0, pos_list[0] + self.length)

        else:
            new_length_list.insert(0, pos_list[0])
            new_length_list[loc - 1] = pos_list[loc-1] + self.length
        
        return new_length_list
    
    def GetFinalDiff(self):

        editedlist = self.EditElementLength()
        newlist = []
        for i in range(1, len(editedlist)):
            newlist.append(editedlist[i])

        return newlist

    def MyRound(self, x, base=5):
        return base * round(x/base)
    
    def RoundAngles(self):
        angles_list = []
        angles = self.GetAngles()
        for i in range(0, len(angles)):
            if angles[i] <= 60 and angles[i] >= 40:
                angles_list.append(45)
                
            elif angles[i] <= 100 and angles [i] >= 70:
                angles_list.append(90)
                
            elif angles[i] >= -60 and angles[i] <= -40:
                angles_list.append(-45)
                
            elif angles[i] >= -100 and angles [i] <= -70:
                angles_list.append(-90)

        return angles_list

    #calculate list of final positions
    def GetPosFinal(self):

        pos_list = [0]
            
        truncated_data = self.EditElementLength()
        for i in range(0, len(truncated_data)):
            pos_list.append(truncated_data[i]+pos_list[i])
            
        return pos_list
    
    def GetTotalLengthFinal(self):
        sum = 2*self.GetPosFinal()[0]
        pos_list = self.GetFinalDiff()
        for i in range(0, len(pos_list)):
            sum += pos_list[i]
        return round(sum,2)
    
    def GetElementLength(self):
        return self.row[2]
    
    def GetRemainderLength(self):
        sum = self.GetPosFinal()[0]
        pos_list = self.GetFinalDiff()
        for i in range(0, len(pos_list)):
            sum += pos_list[i]
        return round(self.GetElementLength() - sum, 2)
    
    def GetFlatLength(self):
        sum = 0
        pos_list = self.GetPosFinal()
        sum = pos_list[0] + pos_list[-1] + 2
        return round(sum,2)
    
    #return final row with positions, angles, and speed
    def GetFinalRow(self):
        finalRow = []
        pos = self.GetPosFinal()
        angles = self.GetAngles()
        speed = 100
        
        for i in range(0, 3):
            finalRow.append(self.row[i])
            
        finalRow.append(self.GetFlatLength())
        
        
        for i in range(0, len(pos)-1):
            finalRow.append(round(pos[i], 2))
            finalRow.append(angles[i])
            finalRow.append(speed)      
            
        finalRow = self.Tuplify(finalRow)
        return finalRow
    
    def GetBoundary(self):
        pos_list = self.GetPosDual()
        diff_list = self.GetFinalDiff()
        angles = self.RoundAngles()
                
        total_angle = 0
        total_pos_x = 5*pos_list[0]
        total_pos_y = 0
        x_boundary = [0, 0]
        y_boundary = [0, 0]
        
        for i in range(0, len(angles)-1):
            
            total_angle += angles[i]
            total_pos_x += 5*diff_list[i]*cos(np.deg2rad(total_angle))
            total_pos_y += 5*diff_list[i]*sin(np.deg2rad(total_angle))

            if total_pos_x < x_boundary[0]:
                x_boundary[0] = total_pos_x
            if total_pos_x > x_boundary[1]:
                x_boundary[1] = total_pos_x

            if total_pos_y < y_boundary[0]:
                y_boundary[0] = total_pos_y
            if total_pos_y > y_boundary[1]:
                y_boundary[1] = total_pos_y

        if total_pos_x < x_boundary[0]:
            x_boundary[0] = total_pos_x
        if total_pos_x > x_boundary[1]:
            x_boundary[1] = total_pos_x

        if total_pos_y < y_boundary[0]:
            y_boundary[0] = total_pos_y
        if total_pos_y > y_boundary[1]:
            y_boundary[1] = total_pos_y
            
        boundary = [x_boundary, y_boundary]

        return boundary
    
    # TODO: Fix final length angle, always make final angle opposite sign of angle before it //DONE
    # TODO: Fix symmetry //DONE
    # TODO: Fix boundary //DONE
    # TODO: Fix canvas resizing //DONE

    # TODO: Fix image rotation, depending on orientation of diagram //try using CoM

    # TODO: Fix angle tolerance
    # TODO: Fix empty rows
    # TODO: Fix negative values added

    def FinalAngleDirection(self, angle):
        if angle*self.GetAngles()[-2] > 1:
            return 1
        
        else:
            return -1

    # def CalculateAngle(self, point1, point2):
    #     i_hat = Matrix([1, 0])
    #     vector12 = point2 - point1
    #     vector = Matrix([vector12[0], vector12[1]])
    #     theta = acos((i_hat.dot(vector))/(vector.norm()))
    #     return theta
    
    # def GetRotationPoints(self):
    #     diff_list = self.GetDiff()
    #     angles = self.RoundAngles()


    #     total_angle = 0
    #     total_pos_x = 0
    #     total_pos_y = 0
    #     point1 = Matrix([0,0])
    #     point2 = Matrix([0,0])

    #     for i in range(0, len(angles)-1):
            
    #         if abs(angles[i]) == 45:
                
    #             point1 = Matrix([total_pos_x, total_pos_y])
    #             point2 = Matrix([total_pos_x + 5*diff_list[i]*cos(np.deg2rad(total_angle + angles[i])), total_pos_y + 5*diff_list[i]*sin(np.deg2rad(total_angle + angles[i]))])
    #             break

    #         total_angle += angles[i]
    #         total_pos_x += 5*diff_list[i]*cos(np.deg2rad(total_angle))
    #         total_pos_y += 5*diff_list[i]*sin(np.deg2rad(total_angle))

    #     return [point1, point2]
    

    # figure out how much to rotate image for U-shaped element orientation
    # def GetRotationAngle(self):
    #     points = self.GetRotationPoints()
    #     calculatedangle = int(self.CalculateAngle(points[0], points[1])*(180/np.pi))
    #     value = 0

    #     if calculatedangle == 45:
    #         value = 0
        
    #     if calculatedangle == 135:
    #         value = -90

    #     if calculatedangle == 270:
    #         value = 180
        
    #     if calculatedangle == 315:
    #         value = 90

    #     return value

            

    
    def GeneratePoints(self):
        init_x = self.GetBoundary()[0][0] + 50
        init_y = -1*self.GetBoundary()[1][0] + 50
        pos_list = self.GetPosFinal()
        diff_list = self.GetFinalDiff()
        angles = self.RoundAngles()
        
        canvas = [(init_x, init_y)]
        
        total_angle = 0
        total_pos_x = 5*pos_list[1] + init_x
        total_pos_y = init_y
        
        for i in range(0, len(angles)-1):
            canvas.append((total_pos_x, total_pos_y))
            

            total_angle += angles[i]
            total_pos_x += 5*diff_list[i]*cos(np.deg2rad(total_angle))
            total_pos_y += 5*diff_list[i]*sin(np.deg2rad(total_angle))
            
        canvas.append((total_pos_x, total_pos_y))
        canvas.append((total_pos_x + self.FinalAngleDirection(total_angle)*5*self.GetPosDual()[0], total_pos_y))

        return canvas
        
        
        
    def line(self, output_path):
        canvas_x = max(abs(int(self.GetBoundary()[0][0])) + 100, abs(int(self.GetBoundary()[0][1])) + 100)
        canvas_y = max(abs(int(self.GetBoundary()[1][0])) + 100, abs(int(self.GetBoundary()[1][1])) + 100)

        image = Image.new("RGB", (canvas_x, canvas_y), "white")
        points = self.GeneratePoints()
        draw = ImageDraw.Draw(image)
        draw.line(points, width=5, fill="black", joint="curve")
        image.save(output_path)
    # def GeneratePoints(self):
    #     init_x = 700
    #     init_y = 700
    #     pos_list = self.GetPosFinal()
    #     diff_list = self.GetFinalDiff()
    #     angles = self.GetAngles()
        
    #     canvas = [(init_x, init_y)]
        
    #     total_angle = 0
    #     total_pos_x = 10*pos_list[0] + init_x
    #     total_pos_y = init_y
        
    #     for i in range(0, len(angles)-1):
    #         canvas.append((total_pos_x, total_pos_y))
            
    #         if angles[i] <= 60 and angles[i] >= 40:
    #             total_angle += 45
                
    #         elif angles[i] <= 100 and angles [i] >= 70:
    #             total_angle += 90
                
    #         elif angles[i] >= -60 and angles[i] <= -40:
    #             total_angle += -45
                
    #         elif angles[i] >= -100 and angles [i] <= -70:
    #             total_angle += -90
            
    #         total_pos_x += 10*diff_list[i]*cos(np.deg2rad(total_angle))
    #         total_pos_y += 10*diff_list[i]*sin(np.deg2rad(total_angle))
            
    #     canvas.append((total_pos_x, total_pos_y))
    #     canvas.append((total_pos_x - 10*self.GetRemainderLength(), total_pos_y))

    #     return canvas
        
        
        
    # def line(self, output_path):
    #     canvas_x = 1000
    #     canvas_y = 1000
    #     image = Image.new("RGB", (canvas_x, canvas_y), "white")
    #     points = self.GeneratePoints()
    #     draw = ImageDraw.Draw(image)
    #     draw.line(points, width=5, fill="black", joint="curve")
    #     image.save(output_path)
        
        
    
#*******************************************************
#Inputs to change

# innerLength = 31 #mm
# five_leg = 13.1318 #mm
# six_leg = 15.3162 #mm
# clearance = 2
# speed = 100 #mm
# flatbridgep1 = 0 #mm
# angleThree = -3
# depthChangep1 = 0
# fusetype = "ob1k"

# #*******************************************************  
#Read row from csv file
df = pd.read_csv('activerecipesheet.csv')
#get the entire row of data
OB1K71_6_bridge = df.loc[187,:].tolist()
# OB1K71_5_bridge = df.loc[190,:].tolist()
# IGBT_offset = df.loc[193,:].tolist()
# IGBT_6_bridge = df.loc[197,:].tolist()

p1 = ModifyElement(1, OB1K71_6_bridge, 15)
# p2 = MetalBending(OB1K71_5_bridge, innerLength, five_leg, clearance, speed, flatbridgep1, angleThree, depthChangep1, fusetype)


# df_194 = p1.GetFinalRow()
# # df_198 = p2.GetFinalRow()

# df1 = pd.DataFrame(df_194)
# df2 = pd.DataFrame(df_198)

# print(p1.EditElementLength())
print(p1.GetPosFinal())
p1.line('testd.png')

# df1.to_csv('OB1K71by.csv', header=True, mode='w', index = False)