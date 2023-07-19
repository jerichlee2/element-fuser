#by Jerich Lee, 6/2/23
from sympy import *
import pandas as pd
from PIL import Image, ImageDraw
import numpy as np


class ModifyElement:
    def __init__(self, row, innerLength, elementWidth, clearance, speed, flatbridge, angleThree, depthChange, fusetype):
        self.row = row
        self.innerLength = innerLength
        self.elementWidth = elementWidth
        self.clearance = clearance
        self.speed = speed
        self.flatbridge = flatbridge
        self.angleThree = angleThree
        self.depthChange = depthChange
        self.fusetype = fusetype
        self.canvas_x = 400
        self.canvas_y = 400
        
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
    
    #Calculate offset needed based on cross section geometry
    def GenerateOffsetOB1K(self):
        return (self.innerLength-self.elementWidth-2*self.clearance)/2
    
    def GenerateOffsetIGBT(self):
        # return (self.innerLength - self.clearance)/2
        return (self.innerLength)/2

    #return a list of differences with the corrected offset
    def GetPosOffset(self):
        if self.fusetype == "ob1k":
            offset = self.GenerateOffsetOB1K()
        else:
            offset = self.GenerateOffsetIGBT()
        
        
        combined_list = self.GetDiffDual()
        combined_list[1] = offset
        combined_list[-2] = offset
        
        return combined_list

    #calculate list of final positions
    def GetPosFinal(self):

        pos_list = [self.row[4] + self.GetDiffDual()[1] - self.GenerateOffsetOB1K()]
            
        truncated_data = self.GetPosOffset()
        for i in range(0, len(truncated_data)):
            pos_list.append(truncated_data[i]+pos_list[i])
            
        return pos_list
    
    def GetFlatLength(self):
        sum = 0
        pos_list = self.GetPosFinal()
        sum = pos_list[0] + pos_list[-1] + 2
        return round(sum,2)
    
    def GetTotalLengthPrev(self):
        sum = 2*self.GetPosDual()[0]
        pos_list = self.GetDiffDual()
        for i in range(0, len(pos_list)):
            sum += pos_list[i]
        return round(sum,2)
    
    def GetTotalLengthFinal(self):
        sum = 2*self.GetPosFinal()[0]
        pos_list = self.GetPosOffset()
        for i in range(0, len(pos_list)):
            sum += pos_list[i]
        return round(sum,2)
    
    def GetElementLength(self):
        return self.row[2]
    
    def GetRemainderLength(self):
        sum = self.GetPosFinal()[0]
        pos_list = self.GetPosOffset()
        for i in range(0, len(pos_list)):
            sum += pos_list[i]
        return round(self.GetElementLength() - sum, 2)
    
    
    #return final row with positions, angles, and speed
    def GetFinalRow(self):
        finalRow = []
        pos = self.GetPosFinal()
        angles = self.GetAngles()
        
        for i in range(0, 3):
            finalRow.append(self.row[i])
            
        finalRow.append(self.GetFlatLength())
        
        
        for i in range(0, len(pos)):
            finalRow.append(round(pos[i], 2))
            finalRow.append(angles[i])
            finalRow.append(speed)      
            
        finalRow = self.Tuplify(finalRow)
        return finalRow
    
    
    def GeneratePoints(self):
        init_x = 700
        init_y = 700
        pos_list = self.GetPosFinal()
        diff_list = self.GetPosOffset()
        angles = self.GetAngles()
        
        canvas = [(init_x, init_y)]
        
        total_angle = 0
        total_pos_x = 10*pos_list[0] + init_x
        total_pos_y = init_y
        
        for i in range(0, len(angles)-1):
            canvas.append((total_pos_x, total_pos_y))
            
            if angles[i] <= 60 and angles[i] >= 40:
                total_angle += 45
                
            elif angles[i] <= 100 and angles [i] >= 70:
                total_angle += 90
                
            elif angles[i] >= -60 and angles[i] <= -40:
                total_angle += -45
                
            elif angles[i] >= -100 and angles [i] <= -70:
                total_angle += -90
            
            total_pos_x += 10*diff_list[i]*cos(np.deg2rad(total_angle))
            total_pos_y += 10*diff_list[i]*sin(np.deg2rad(total_angle))
            
        canvas.append((total_pos_x, total_pos_y))
        canvas.append((total_pos_x - 10*self.GetRemainderLength(), total_pos_y))

        return canvas
        
        
        
    def line(self, output_path):
        canvas_x = 1000
        canvas_y = 1000
        image = Image.new("RGB", (canvas_x, canvas_y), "white")
        points = self.GeneratePoints()
        draw = ImageDraw.Draw(image)
        draw.line(points, width=5, fill="black", joint="curve")
        image.save(output_path)
        
        
    
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
# #Read row from csv file
# df = pd.read_csv('activerecipesheet.csv')
# #get the entire row of data
# OB1K71_6_bridge = df.loc[187,:].tolist()
# OB1K71_5_bridge = df.loc[190,:].tolist()
# # IGBT_offset = df.loc[193,:].tolist()
# # IGBT_6_bridge = df.loc[197,:].tolist()

# p1 = MetalBending(OB1K71_6_bridge, innerLength, five_leg, clearance, speed, flatbridgep1, angleThree, depthChangep1, fusetype)
# p2 = MetalBending(OB1K71_5_bridge, innerLength, five_leg, clearance, speed, flatbridgep1, angleThree, depthChangep1, fusetype)


# df_194 = p1.GetFinalRow()
# df_198 = p2.GetFinalRow()

# df1 = pd.DataFrame(df_194)
# df2 = pd.DataFrame(df_198)

# print(p1.GetTotalLengthFinal())
# print(p1.GetTotalLengthPrev())
# p1.line('testd.png')

# df1.to_csv('OB1K71by.csv', header=True, mode='w', index = False)