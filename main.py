import pygame
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    #pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    Particle.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    #Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)
        if any([a.touching(player) for a in asteroids]):
            print("Game over!")
            print(f"Your score is: {score}")
            return
        
        for hit_a, hit_s in [(a, s) for a in asteroids for s in shots if a.touching(s)]:
            for i in range(random.randrange(*PARTICLE_COUNT_RANGE)):
                Particle(hit_a.position.x,hit_a.position.y)
            score += hit_a.split(hit_s.velocity)
            hit_s.kill()

        screen.fill(pygame.Color(0x000000))
        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()