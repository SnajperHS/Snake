import sys
import pygame
import subprocess
from class_create_player import Player, PLAYER_SIZE_H, PLAYER_SIZE_W

python_path = sys.executable
script_path = "black_jack_game.py"

pygame.init()

SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 768

TABLE_INTERACTION_RECTS = [
    pygame.Rect(830, 580, 230, 130),
    pygame.Rect(485, 225, 160, 85),
    pygame.Rect(840, 225, 160, 85),
    pygame.Rect(965, 370, 200, 110),
    pygame.Rect(650, 370, 200, 110),
    pygame.Rect(310, 370, 200, 110),
    pygame.Rect(410, 580, 230, 130)
]

button_image = pygame.image.load('przycisk.png')  # Make sure the button image file exists

class ImageButton:
    def __init__(self, center_pos, image, target_rect):
        self.original_image = image
        scale_width = target_rect.width / self.original_image.get_width()
        scale_height = target_rect.height / self.original_image.get_height()
        scale = min(scale_width, scale_height) * 1  # scale to fit within the rectangle, with some padding
        width = int(self.original_image.get_width() * scale)
        height = int(self.original_image.get_height() * scale)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect(center=center_pos)
        self.highlighted = False  # kontrola widocznosci

    def draw(self, screen):
        if self.highlighted:
            screen.blit(self.image, self.rect.topleft)

class Black_Jack_Player(Player):
    def __init__(self, images, position=(700, 600), width=60, height=160):
        super().__init__(images, position)
        self.size = (width, height)
        self.resize_images()

    def resize_images(self):
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], self.size)

def game_loop():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Casino Game Simulation')

    background_image = pygame.image.load('rooms/blackjack.jpg')
    player_images = {
        'down': pygame.image.load('player/front.png'),
        'up': pygame.image.load('player/back.png'),
        'left': pygame.image.load('player/left.png'),
        'right': pygame.image.load('player/right.png')
    }

    player = Black_Jack_Player(player_images)
    buttons = [ImageButton(rect.center, button_image, rect) for rect in TABLE_INTERACTION_RECTS]

    # zegar
    clock = pygame.time.Clock()
    running = True
    interact_rect = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and interact_rect:
                    for button in buttons:
                        if button.rect.colliderect(interact_rect):
                            subprocess.call([python_path, "black_jack_game.py"])

        keys = pygame.key.get_pressed()
        player.move(keys)

        interact_rect = player.check_interaction(TABLE_INTERACTION_RECTS)

        screen.blit(background_image, (0, 0))
        player.draw(screen)

        # wyświetlanie przycisku podczas kontaktu
        for button in buttons:
            button.highlighted = button.rect.colliderect(interact_rect) if interact_rect else False
            if button.highlighted:
                button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    game_loop()
