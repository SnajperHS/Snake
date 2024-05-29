import random
import math
import pygame
import time


class Firework:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = random.randint(2, 4)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(3, 7)
        self.lifetime = random.randint(20, 60)

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0


class FireworkAnimation:
    def __init__(self, screen, background_image_path, sound_file_path, screen_width=900, screen_height=515):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.fireworks = []
        self.running = True

        # Ładowanie tła
        self.background = pygame.image.load(background_image_path)
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

        # Ładowanie dźwięku
        pygame.mixer.init()
        self.sound_file_path = sound_file_path
        pygame.mixer.music.load(self.sound_file_path)

        # Czcionka do wyświetlania napisu
        self.font = pygame.font.Font(None, 200)  # Zwiększono wielkość czcionki do 100

    def create_firework(self):
        x = random.randint(0, self.screen_width)
        y = random.randint(self.screen_height // 2, self.screen_height)
        color = random.choice(self.colors)
        for _ in range(random.randint(50, 100)):
            self.fireworks.append(Firework(x, y, color))

    def update_fireworks(self):
        self.fireworks = [f for f in self.fireworks if f.is_alive()]
        for f in self.fireworks:
            f.update()

    def draw_fireworks(self):
        self.screen.blit(self.background, (0, 0))
        for f in self.fireworks:
            pygame.draw.circle(self.screen, f.color, (int(f.x), int(f.y)), f.radius)
        text = self.font.render("You Won!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        start_time = time.time()
        pygame.mixer.music.play(-1)

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > 4:
                self.running = False
                pygame.mixer.music.stop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.create_firework()
            self.update_fireworks()
            self.draw_fireworks()
            clock.tick(60)

        pygame.quit()


# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((900, 515))  # Zmieniono rozmiar ekranu na 900x515
pygame.display.set_caption("Fireworks Animation")

# Ścieżka do tła i pliku dźwiękowego
background_image_path = "table.PNG"  # Podaj odpowiednią ścieżkę do pliku tła
sound_file_path = "fireworks.mp3"  # Podaj odpowiednią ścieżkę do pliku dźwiękowego

# Tworzenie i uruchamianie animacji
fireworks_animation = FireworkAnimation(screen, background_image_path, sound_file_path)
fireworks_animation.run()
