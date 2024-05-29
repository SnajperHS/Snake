import pygame

class QuestionButton:
    def __init__(self, image_path, position, size):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(bottomright=position)
        self.display_text = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.display_text = not self.display_text

    def _draw_text(self, screen, text, x, y, font):
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        background_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(screen, (255, 255, 255), background_rect)
        screen.blit(text_surface, text_rect)
