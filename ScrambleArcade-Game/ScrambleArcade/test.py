import pygame, os, random
from main import *


WIDTH = 480
HEIGHT = 600
FPS = 60

def main():
    # # gameObject(HEIGHT,WIDTH,LIVES,True,False)
    # Initialise screen
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Scramble Game')
    clock = pygame.time.Clock()

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Display some text

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # user variables
    wave_1 = True
    wave_2 = False

    # Sprites
    spaceship = SpaceShip()
    space = Space()

    # sprite groups
    # rocketSprites = pygame.sprite.Group()
    # shootSprites = pygame.sprite.Group()
    systemSprites = pygame.sprite.Group(space)
    userSprites = pygame.sprite.Group(spaceship)
    enemySprites = pygame.sprite.Group()
    fuelSprites = pygame.sprite.Group()

    # Event loop
    while wave_1:
        for i in range(50):
            enemy = Enemy1()
            enemy.rect.x = random.randrange(600, 1400)
            enemy.rect.y = random.randrange(10, 490)
            enemySprites.add(enemy)
            # pass

        for i in range(2):
            fuel = Fuels()
            # fuel.rect.x += 50
            # fuel.rect.y += 10
            fuel.rect.x = random.randrange(600, 1400)
            fuel.rect.y = random.randrange(10, 490)
            fuelSprites.add(fuel)

        wave_1 = False

        # while wave_2:
        #     for i in range(100):
        #         enemy_2 = Enemy2()
        #         enemy.rect.x = random.randrange(6000,8000)
        #         enemy.rect.y = random.randrange(10, 490)
        #         enemySprites.add(enemy)
        #         wave_1 = False
        #         wave_2 = False

    keepGoing = True

    while keepGoing:
        clock.tick(45)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                keepGoing = False

        # bullet-fuel collider
        fuel_hit_by_bullet = pygame.sprite.groupcollide(fuelSprites, shootSprites, True, True)
        if fuel_hit_by_bullet:
            spaceship.fuel += 10

        # rocket-fuel collider
        fuel_hit_by_rocket = pygame.sprite.groupcollide(fuelSprites, rocketSprites, True, True)
        if fuel_hit_by_rocket:
            spaceship.fuel += 10

        # bullet-enemy collider
        bullethits = pygame.sprite.groupcollide(enemySprites, shootSprites, True, True)
        if bullethits:
            spaceship.score += 1
        # player-enemy collider
        spaceshiphits = pygame.sprite.spritecollide(spaceship, enemySprites, True)
        if spaceshiphits:
            spaceship.score -= 10
        # rocket-enemy collider
        rockethits = pygame.sprite.groupcollide(enemySprites, rocketSprites, True, True)
        if rockethits:
            spaceship.score += 1
        print(spaceship.score)

        if spaceshiphits:
            spaceship.lives -= 1

        if spaceship.lives == 0:
            keepGoing = False

        systemSprites.clear(screen, background)
        userSprites.clear(screen, background)
        shootSprites.clear(screen, background)
        enemySprites.clear(screen, background)
        rocketSprites.clear(screen, background)
        fuelSprites.clear(screen, background)

        systemSprites.update()
        userSprites.update()
        shootSprites.update()
        enemySprites.update()
        rocketSprites.update()
        fuelSprites.update()

        systemSprites.draw(screen)
        userSprites.draw(screen)
        shootSprites.draw(screen)
        enemySprites.draw(screen)
        rocketSprites.draw(screen)
        fuelSprites.draw(screen)

        pygame.display.flip()


if __name__ == '__main__': main()