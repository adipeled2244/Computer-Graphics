# names:
# noy shabo
# adi peled

import pygame
from my_graphic import MyGraphic
import math

# Initialize Pygame library
pygame.init()

# Set up the display screen
size = (640, 480)
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))

# Set up the font
font = pygame.font.Font(None, 32)

# Set up the text input box
text = '33'
input = pygame.Rect(10, 10, 200, 32)
input_active = False
pygame.draw.rect(screen, (255, 0, 0), input, 2)
screen.fill((204, 229, 255), input)

# Set up variables to track user input
user_input = '33'
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')

# Draw the placeholder text
# placeholder_surface = font.render("Enter number", True, (128, 128, 128))
# screen.blit(placeholder_surface, (input.x + 5, input.y + 5))

# Create MyGraphic object to use my graphic functions
myGraphic = MyGraphic(screen)

# Set up variables to track clicks
click_count = 0
start_pos_main_diagonal = None
end_pos_main_diagonal = None


# Main loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if this is the first or second click
            if click_count == 0:
                # Check if the mouse click is inside the input box
                if input.collidepoint(event.pos):
                    # Activate the input box and clear the text
                    input_active = True
                    # text = ''
                else:
                    start_pos_main_diagonal = event.pos
                    click_count += 1

            # 2 clicks from the user
            elif click_count == 1:
                end_pos_main_diagonal = event.pos
                click_count += 1
                if text!='':
                    user_input = int(text.strip()) 
                if user_input!='':
                    number_lines_curve =user_input;
                else:
                    number_lines_curve = 33
                
                # Draw rhombus and export the coordinates of the rhombus
                my_rhombus = myGraphic.draw_rhombus(start_pos_main_diagonal,end_pos_main_diagonal)
                x1_main_diagnol=my_rhombus.main_diagnol[0][0]
                y1_main_diagnol=my_rhombus.main_diagnol[0][1]
                x2_main_diagnol=my_rhombus.main_diagnol[1][0]
                y2_main_diagnol=my_rhombus.main_diagnol[1][1]
                
                x1_second_diagnoal=my_rhombus.second_diagnol[0][0]
                y1_second_diagnoal=my_rhombus.second_diagnol[0][1]
                x2_second_diagnoal=my_rhombus.second_diagnol[1][0]
                y2_second_diagnoal=my_rhombus.second_diagnol[1][1]
                
                x_center_rhombus=my_rhombus.center[0]
                y_center_rhombus=my_rhombus.center[1]

                # Draw the small circle
                radius_small_circle = math.sqrt((x1_second_diagnoal - x_center_rhombus)**2 + (y1_second_diagnoal - y_center_rhombus)**2)
                myGraphic.bresenham_circle(x_center_rhombus, y_center_rhombus ,radius_small_circle, "green" )
                
                
                # Draw the big circle
                radius_big_circle = math.sqrt((x1_main_diagnol - x_center_rhombus)**2 + (y1_main_diagnol - y_center_rhombus)**2)
                myGraphic.bresenham_circle(x_center_rhombus, y_center_rhombus ,radius_big_circle, "red" )
               
                # Draw the curve
                myGraphic.draw_curve(x1_main_diagnol,y1_main_diagnol,x1_second_diagnoal,y1_second_diagnoal,x2_second_diagnoal,y2_second_diagnoal,x2_main_diagnol,y2_main_diagnol,number_lines_curve)
                
                # Reset variables for next pair of clicks
                start_pos_main_diagonal = None
                end_pos_main_diagonal = None
                click_count = 0
        
        elif event.type == pygame.KEYDOWN:
             if input_active:
                if event.key == pygame.K_RETURN:
                    # Deactivate the input box
                    input_active = False
                    # Copy the input text to user_input
                    user_input = text
                elif event.key == pygame.K_BACKSPACE:
                    if len(text) > 0 and text[-1].isdigit():
                        # Remove the last character
                        text = text[:-1]
                    # Remove the old text by filling the input box with the background color
                    pygame.draw.rect(screen, (204, 229, 255), input)
                    # Render and blit the updated input text
                    input_text = font.render(text, True, (0, 0, 0))
                    screen.blit(input_text, (input.x + 5, input.y + 5))
                elif event.unicode.isdigit():
                    # Append the pressed numeric key to the text
                    text += event.unicode
        
                        
        # Draw the input box
        if input_active:
            color = color_active
        else:
            color = color_inactive
    
        pygame.draw.rect(screen, color, input, 2)
        
        # Draw the input text
        input_text = font.render(text, True, (0, 0, 0))
        screen.blit(input_text, (input.x + 5, input.y + 5))
    
    # Update the display
    pygame.display.flip()

# Quit


# Quit Pygame
pygame.quit()
