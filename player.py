import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot
class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.gun_cooldown = 0
        self.ship_poly = [pygame.Vector2(x,y) * PLAYER_RADIUS for x,y in PLAYER_SHIP_POLYGON]
        self.thrust_poly = [pygame.Vector2(x,y) * PLAYER_RADIUS for x,y in PLAYER_THRUST_POLYGON]
        self.moved = False
        #self.gun_sound = pygame.mixer.Sound(file=SOUND_GUN)
        #self.thrust_sound = pygame.mixer.Sound(file=SOUND_THRUST)
        
    # Old polygon design
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def translate_ship(self):
        return [self.position + point.rotate(self.rotation) for point in self.ship_poly]

    def translate_thrust(self):
        return [self.position + point.rotate(self.rotation) for point in self.thrust_poly]
    
    def draw(self, screen):
        #pygame.draw.polygon(screen,0xFFFFFF, self.triangle(), 2)
        pygame.draw.polygon(screen,pygame.Color(255, 255, 255), self.translate_ship(), 2)
        if self.moved:
            pygame.draw.polygon(screen,pygame.Color(255, 127, 16), self.translate_thrust(), 2)

        return super().draw(screen)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        #self.thrust_sound.play()
        self.moved = True
        self.velocity += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_ACCELERATION * dt
        self.velocity = self.velocity.clamp_magnitude(PLAYER_SPEED)
        

    def update(self, dt):
        self.moved = False
        if self.gun_cooldown > 0:
            self.gun_cooldown -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_SPACE] and self.gun_cooldown <= 0:
            self.shoot()
        
        self.velocity *= 0.995
        self.position += self.velocity * dt
        self.position.x = (self.position.x + SCREEN_WIDTH * 4) % SCREEN_WIDTH
        self.position.y = (self.position.y + SCREEN_HEIGHT * 4) % SCREEN_HEIGHT

        return super().update(dt)
    
    def shoot(self):
        self.gun_cooldown = PLAYER_SHOOT_COOLDOWN
        new_shot = Shot(self.position.x, self.position.y)
        new_shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        #self.gun_sound.play()
        