import pygame

# Constants
PLAYER_SIZE_H = 300
PLAYER_SIZE_W = 100

class Player:
    def __init__(self, images, position=(700, 600)):
        self.images = images
        self.position = list(position)
        self.direction = 'down'
        self.size = (PLAYER_SIZE_W, PLAYER_SIZE_H)

    def draw(self, screen):
        screen.blit(self.images[self.direction], self.position)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.position[0] -= 5
            self.direction = 'left'
        if keys[pygame.K_RIGHT]:
            self.position[0] += 5
            self.direction = 'right'
        if keys[pygame.K_UP]:
            self.position[1] -= 5
            self.direction = 'up'
        if keys[pygame.K_DOWN]:
            self.position[1] += 5
            self.direction = 'down'

    def check_interaction(self, interact_rects):
        player_rect = pygame.Rect(self.position[0], self.position[1], PLAYER_SIZE_W, PLAYER_SIZE_H)
        for interact_rect in interact_rects:
            if player_rect.colliderect(interact_rect):
                return interact_rect
        return None
