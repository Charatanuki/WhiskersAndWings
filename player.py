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
        self.img = [pygame.image.load("./characters/bird1_frame1.png"),
                    pygame.image.load("./characters/bird1_frame2.png"),
                    pygame.image.load("./characters/bird1_frame3.png"),
                    pygame.image.load("./characters/bird1_frame2.png"),]
        self.is_facing_left = True
    def pos(self):
        for pos in range(len(self.img)):
            self.img[pos] = pygame.transform.flip(self.img[pos],True,False)

    def mov(self, keys):
        if keys[pygame.K_q]:
            if not self.is_facing_left:
                self.is_facing_left=True
                self.pos()
            self.a -= self.speed
        if keys[pygame.K_d]:
            if self.is_facing_left:
                self.is_facing_left=False
                self.pos()
            self.a += self.speed
        if keys[pygame.K_z]:
            self.b -= self.speed
        if keys[pygame.K_s]:
            self.b += self.speed