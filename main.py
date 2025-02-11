import pygame
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle
from vectortext import VectorText

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
    lives = PLAYER_LIVES

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    Particle.containers = (updatable, drawable, particles)
    VectorText.containers = (updatable, drawable)

    score_text = VectorText(30, 30, f"SCORE {score}", 7, pygame.Color(200, 220, 255, 180))
    # The ^ symbol is the player ship sprite in the vector library.
    lives_text = VectorText(30, 60, "^" * lives, 5, pygame.Color(200, 220, 255, 180))

    #Game Loop
    respawn = False

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)

        # Check if the player died and is waiting for respawn (particles to fade out) if not check for collisions
        if not respawn:
            # Was player hit by a asteroid
            if any([a.touching(player) for a in asteroids]):
                lives -= 1
                lives_text.update_text("^" * lives)
                for i in range(random.randrange(*PARTICLE_COUNT_RANGE)):
                    Particle(player.position.x,player.position.y, random.uniform(2.0, 10.0))
                player.kill()
                asteroid_field.kill()
                for sprite in asteroids:
                    sprite.kill()
                for sprite in shots:
                    sprite.kill()
                respawn = True

            # Iterate through every asteroid and shot to see if any shots have hit an asteroid 
            shot_asteroid = False
            for hit_a, hit_s in [(a, s) for a in asteroids for s in shots if a.touching(s)]:
                # Generate a spray of temporary particles
                for i in range(random.randrange(*PARTICLE_COUNT_RANGE)):
                    Particle(hit_a.position.x,hit_a.position.y)
                    
                # Perform split and add asteroid value to the score 
                score += hit_a.split(hit_s.velocity)
                shot_asteroid = True
                hit_s.kill()

            # Update score on hit
            if shot_asteroid:
                score_text.update_text(f"SCORE {score}")    

        # Clear the screen
        screen.fill(pygame.Color(0x000000))

        # Draw all sprite objects in the drawable group
        for sprite in drawable:
            sprite.draw(screen)

        # If player is dead and all particles are gone respawn or end game
        if respawn and len(particles) == 0:
            if lives < 0:
                print("Game Over!")
                print(f"Your final score was: {score}")
                return
            player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            asteroid_field = AsteroidField()
            respawn = False

        pygame.display.flip()
        dt = clock.tick(60) / 1000 
        

    print("Game over!")
    print(f"Your score is: {score}")

if __name__ == "__main__":
    main()