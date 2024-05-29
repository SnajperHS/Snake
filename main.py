import pygame
import random
import math

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
    def __init__(self, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.fireworks = []
        self.running = True

        # Inicjalizacja Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Fajerwerki")

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
        self.screen.fill((0, 0, 0))
        for f in self.fireworks:
            pygame.draw.circle(self.screen, f.color, (int(f.x), int(f.y)), f.radius)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if random.randint(0, 10) == 0:  # Tworzenie fajerwerków z pewną losowością
                self.create_firework()

            self.update_fireworks()
            self.draw_fireworks()
            clock.tick(90)

        pygame.quit()

if __name__ == "__main__":
    animation = FireworkAnimation()
    animation.run()
