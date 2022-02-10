import pygame
import math as m

class Slider:
    
    def  __init__(
            self, window, name, values, pos, size, val=None, axis_color=(255,255,255), 
            control_color=(150,150,150), text_color=(255,255,255)):
        self.window = window
        self.valmin, self.valmax = values
        self.val = val if val is not None else (self.valmin - self.valmax)//2
        self.x, self.y = pos
        self.width, self.height = size
        
        self.axis_color = axis_color
        self.fixed_color = control_color
        self.control_color = control_color
        self.text_color = text_color
        self.name = name
        self.font = pygame.font.SysFont("Arial", self.height//3 - 5)

        self.axis = pygame.Rect(self.x, self.y + self.height//3, 
                                self.width, self.height//3)  
        self.control = pygame.Rect(
            m.floor(self.x + self.width * 
                    (self.val-self.valmin) / (self.valmax-self.valmin)),
                                   self.y, self.width//16, self.height)
        
        self.holding = False
        
        
    def on_clicked(self, event):
        x, y = pygame.mouse.get_pos()
        if self.control.collidepoint(x, y):
            if pygame.mouse.get_pressed()[0]:
                self.holding = True
            else:
                self.control_color = [
                    x + 32 if x < 224 else x for x in self.fixed_color
                ]
        else:
            self.control_color = self.fixed_color
        if not pygame.mouse.get_pressed()[0]:
            self.holding = False
            
        if self.holding:
            self.control_color = [x - 64 if x > 63 else x for x in self.fixed_color]
            if x < self.x:
                x = self.x
            if x > self.x + self.width:
                x = self.x + self.width
            self.control.x = x - self.control.width//2
            factor = (x - self.x)/self.width
            self.val = m.floor(self.valmin + (self.valmax - self.valmin) * factor)
            
        
    def draw_slider(self):
        pygame.draw.rect(self.window, self.axis_color, self.axis)
        pygame.draw.rect(self.window, self.control_color, self.control)
        valmin = self.font.render(str(self.valmin), 1, self.text_color)
        self.window.blit(valmin, (self.x, self.y + 2*self.height//3 + 5))
        valmax = self.font.render(str(self.valmax), 1, self.text_color)
        self.window.blit(
            valmax,
            (self.x + self.width - valmax.get_width(),
            self.y + 2*self.height//3 + 5)
        )
        name = self.font.render(self.name, 1, self.text_color)
        self.window.blit(name, (self.x, self.y))
        val = self.font.render(str(self.val), 1, self.text_color)
        self.window.blit(val, (self.x + self.width - valmax.get_width(), self.y))



class Button:
    
    def __init__(self, window, text, pos, size, color=(223,223,223),
                 text_color=(0,0,0)):
        self.window = window
        self.x, self.y = pos
        self.width , self.height = size
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.fixed_color = color
        self.color = color
        font = pygame.font.SysFont("Arial", self.height//2)
        self.text = font.render(text, 1, text_color)
        
        
    def check_clicked(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            if pygame.mouse.get_pressed()[0]:
                self.color = [x - 64 if x > 63 else x for x in self.fixed_color]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
            else:
                self.color = [x + 32 if x < 224 else x for x in self.fixed_color]
        else:
            self.color = self.fixed_color
        return False
          
    
    def draw_button(self):
        pygame.draw.rect(self.window, self.color, self.rect)
        self.window.blit(
            self.text, 
            (self.x + (self.width - self.text.get_width())//2,
             self.y + (self.height - self.text.get_height())//2)
        )