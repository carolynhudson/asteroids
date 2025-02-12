import pygame
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle
from vectortext import VectorText
from saucer import Saucer
from audio import Audio

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    audio = Audio()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    next_life = PLAYER_EXTRA_LIFE
    lives = PLAYER_LIVES

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    saucers = pygame.sprite.Group()
    destroyable = pygame.sprite.Group()
    collidable = pygame.sprite.Group()
    players = pygame.sprite.Group()

    Player.containers = (updatable, drawable, players)
    Asteroid.containers = (updatable, drawable, asteroids, destroyable, collidable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots, collidable)
    Particle.containers = (updatable, drawable, particles)
    VectorText.containers = (updatable, drawable)
    Saucer.containers = (updatable, drawable, saucers, destroyable, collidable)    

    score_text = VectorText(30, 30, f"SCORE {score}", 7, pygame.Color(200, 220, 255, 180))
    # The ^ symbol is the player ship sprite in the vector library.
    lives_text = VectorText(30, 60, "^" * lives, 5, pygame.Color(200, 220, 255, 180))

    #Game Loop
    respawn = False

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField(asteroids, players, saucers)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)

        # Check if the player died and is waiting for respawn (particles to fade out) if not check for collisions
        if not respawn:
            # Was player hit by a asteroid
            if any([(o.touching(player) and o.hurts_player) for o in collidable]):
                lives -= 1
                lives_text.update_text("^" * lives)

                for i in range(random.randrange(*PARTICLE_COUNT_RANGE)):
                    Particle(player.position.x,player.position.y, random.uniform(2.0, 10.0))

                audio.play_sound("bang_large")
                player.kill()
                asteroid_field.remaning_spawn_mass = -1
                for sprite in collidable:
                    sprite.kill()
                respawn = True

            # Iterate through every asteroid and shot to see if any shots have hit an asteroid 
            shot_something = False
            for hit_object, shot in [(o, s) for o in destroyable for s in shots if not s.hurts_player and o.touching(s)]:
                # Call got_shot method to handle scoring and other effects 
                score += hit_object.got_shot(shot.velocity)
                shot_something = True
                shot.kill() 

            # Update score on hit
            if shot_something:
                score_text.update_text(f"SCORE {score}") 
                if score >= next_life:
                    next_life += PLAYER_EXTRA_LIFE
                    lives += 1
                    lives_text.update_text("^" * lives)
                    audio.play_sound("extra_ship")

            a_list = list(asteroids)
            for asteroid_1, asteroid_2 in [(a_list[a1], a_list[a2]) for a1 in range(len(asteroids) - 1) for a2 in range(a1 + 1, len(asteroids)) if a_list[a1].touching(a_list[a2])]:
                asteroid_1.collide(asteroid_2)

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
            asteroid_field.remaning_spawn_mass = asteroid_field.wave_mass_limit
            respawn = False

        pygame.display.flip()
        dt = clock.tick(60) / 1000 
        

    print("Game over!")
    print(f"Your score is: {score}")

if __name__ == "__main__":
    main()