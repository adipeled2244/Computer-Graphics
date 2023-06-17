# names:
# noy shabo
# adi peled

import pygame
from rhombus import Rhombus

class MyGraphic:
    '''
      my graphic class to do all the drawing
    '''
    def __init__(self, screen):
        self.screen = screen
        self.color = (255, 255, 255)

    def draw_bresenham_line(self,color, x0, y0, x1, y1):
        '''
        Draw a line from (x0, y0) to (x1, y1)- accourding to bresenham algorithm
        '''
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while x0 != x1 or y0 != y1:
            self.screen.set_at((x0, y0), color)
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        self.screen.set_at((x0, y0), color)
    
    def get_middle_line(self, start_pos , end_pos):
        '''
        get the middle point of a line
        '''
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        x = start_pos[0] + dx // 2
        y = start_pos[1] + dy // 2
        return (x, y)
    
  
    def draw_rhombus(self, start_pos_main_diagonal, end_pos_main_diagonal):
        '''
        draw a rhombus from the main diagonal
        '''
       
        # Draw the main line
        self.draw_bresenham_line("orange",start_pos_main_diagonal[0], start_pos_main_diagonal[1], end_pos_main_diagonal[0], end_pos_main_diagonal[1])
        
        # Calculate the length and center of the secondary line
        dx = end_pos_main_diagonal[0] - start_pos_main_diagonal[0]
        dy = end_pos_main_diagonal[1] - start_pos_main_diagonal[1]
        length = int(((dx ** 2) + (dy ** 2)) ** 0.5)
        secondary_len = int((2/3) * length)
        middle = self.get_middle_line(start_pos_main_diagonal , end_pos_main_diagonal)
        mid_x = middle[0]
        mid_y = middle[1]
        
        # Calculate the start and end points of the secondary line
        readuis_secondery_diagnoal=secondary_len / 2
        
        start_pos_secondary_diagonal = (mid_x - int(readuis_secondery_diagnoal * (dy / length)),
                                mid_y + int(readuis_secondery_diagnoal * (dx / length)))
        end_pos_secondary_diagonal = (mid_x + int(readuis_secondery_diagnoal* (dy / length)),
                                mid_y - int(readuis_secondery_diagnoal * (dx / length)))
        
        # Draw the secondary line
        self.draw_bresenham_line("orange", start_pos_secondary_diagonal[0], start_pos_secondary_diagonal[1],
                                        end_pos_secondary_diagonal[0], end_pos_secondary_diagonal[1])
        
        # Draw the Rhombus lines
        self.draw_bresenham_line("blue",start_pos_main_diagonal[0], start_pos_main_diagonal[1],  start_pos_secondary_diagonal[0], start_pos_secondary_diagonal[1])
        self.draw_bresenham_line("blue",start_pos_main_diagonal[0], start_pos_main_diagonal[1],  end_pos_secondary_diagonal[0], end_pos_secondary_diagonal[1])
        self.draw_bresenham_line("blue",end_pos_main_diagonal[0], end_pos_main_diagonal[1],  start_pos_secondary_diagonal[0], start_pos_secondary_diagonal[1])
        self.draw_bresenham_line("blue",end_pos_main_diagonal[0], end_pos_main_diagonal[1],  end_pos_secondary_diagonal[0], end_pos_secondary_diagonal[1])
        
        #return rombus middle, main diagonal start and end points and secondary diagonal start and end points
        return Rhombus(middle,[start_pos_main_diagonal, end_pos_main_diagonal], [start_pos_secondary_diagonal, end_pos_secondary_diagonal])

    # draw circle according to bresenham circle algorithm
    def bresenham_circle(self,x0, y0, radius, color):
        x = 0
        y = radius
        d = 3 - 2 * radius
        while x <= y:
            #draw mirror points
            self.plot_circle_points(x0, y0, x, y ,color)
            if d < 0:
                d = d + 4 * x + 6
            else:
                d = d + 4 * (x - y) + 10
                y -= 1
            x += 1

    def plot_circle_points(self, x0, y0, x, y, color):
        '''
        plot miror points of circle
        '''
        self.plot_point(x0 + x, y0 + y, color)
        self.plot_point(x0 - x, y0 + y, color)
        self.plot_point(x0 + x, y0 - y, color)
        self.plot_point(x0 - x, y0 - y, color)
        self.plot_point(x0 + y, y0 + x, color)
        self.plot_point(x0 - y, y0 + x, color)
        self.plot_point(x0 + y, y0 - x, color)
        self.plot_point(x0 - y, y0 - x, color)

    def plot_point(self, x, y, color):
        '''
        plot poinet/pixel in position (x,y) in color
        '''
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, 1, 1))

    def draw_curve(self,x1,y1,x2,y2,x3,y3,x4,y4,numberLines=33):
        '''
       draw curve by using bezier curve algorithm 
        '''
        # Calculate coefficients of the cubic Bezier curve
        t_step=1/numberLines
        ax=-x1 +3*x2 -3*x3 +x4
        bx=3*x1 -6*x2 +3*x3 
        cx=-3*x1 +3*x2 
        dx=x1

        ay=-y1 +3*y2 -3*y3 +y4
        by=3*y1 -6*y2 +3*y3 
        cy=-3*y1 +3*y2 
        dy=y1
        
        curr_x=x1
        curr_y=y1
        t=t_step

        
        new_x=x1
        new_y=y1
        
        # Draw the curve by drawing multiple line segments
        while t<1.0:
            new_x = int(ax*t**3 + bx*t**2 + cx*t + dx)
            new_y = int(ay*t**3 + by*t**2 + cy*t + dy)
            self.draw_bresenham_line("black",curr_x,curr_y,new_x,new_y)
            curr_x=new_x
            curr_y=new_y
            t=t+t_step

        # Draw the last line segment to complete the curve
        self.draw_bresenham_line("black",new_x,new_y,x4,y4)




    