import pygame

class Cat:
    def __init__(self, speed, x, y,velocity, jump_height, gravity):
        self.speed = speed
        self.x = x
        self.y = y
        self.velocity = velocity
        self.jump_height = jump_height
        self.gravity = gravity
        self.jumping = False
        
    def mov(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        if keys[pygame.K_UP] and not self.jumping :
            self.jumping = True
            self.velocity = self.jump_height
        
        if self.jumping:
            self.y-=self.velocity
            self.velocity-=self.gravity
        if self.velocity<- self.jump_height:
            self.jumping = False

        if keys[pygame.K_DOWN]:
            self.y += self.speed

        
        
        
class Bird:
    def __init__(self, speed, a,b):
        self.speed = speed
        self.a = a 
        self.b = b