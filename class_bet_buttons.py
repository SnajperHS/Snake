import pygame
from dict_number_rects import number_rects

class BetButtons:
    def __init__(self, font):
        self.font = font
        self.buttons = self.load_buttons()
        self.current_bet = 0
        self.bets = {}

    def load_buttons(self):
        buttons = {
            '100': {'image': self.load_scaled_image('buttons/100.png', 0.08), 'bet': 100},
            '1000': {'image': self.load_scaled_image('buttons/1000.png', 0.08), 'bet': 1000},
            '10000': {'image': self.load_scaled_image('buttons/10000.png', 0.08), 'bet': 10000},
            'ALL-IN': {'image': self.load_scaled_image('buttons/ALL-IN.png', 0.08), 'bet': 'all-in'},
            'CLEAR': {'image': self.load_scaled_image('buttons/clear.png', 0.08), 'bet': 'clear'}
        }

        x_start = 170
        for key, button in buttons.items():
            button['rect'] = button['image'].get_rect(topleft=(x_start, 701 - 80))
            x_start += button['rect'].width   # Add spacing between buttons
        return buttons

    def load_scaled_image(self, path, scale):
        image = pygame.image.load(path)
        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)
        return pygame.transform.scale(image, (width, height))

    def draw(self, screen):
        for button_info in self.buttons.values():
            screen.blit(button_info['image'], button_info['rect'])
        bet_display = self.font.render(f"Current Bet: ${self.current_bet}", True, (255, 255, 255))
        screen.blit(bet_display, (450, 580))

    def handle_event(self, event, money_display):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for key, button in self.buttons.items():
                if button['rect'].collidepoint(pos):
                    bet_amount = button['bet']
                    if bet_amount == 'clear':
                        self.current_bet = 0
                        self.bets.clear()
                    elif bet_amount == 'all-in':
                        self.current_bet = money_display.money
                    else:
                        self.current_bet += bet_amount
                    print(f"Current bet: {self.current_bet}")
            for number, rect in number_rects.items():
                if rect.collidepoint(pos):
                    if number not in self.bets:
                        self.bets[number] = self.current_bet
                    print(f"Bet placed on number: {number}")
