import pygame
from class_money_display import MoneyDisplay, BeltImage
from dict_number_rects import number_rects

# Global variable to store the final bet
final_bet = 0

class MoneyBeltDisplay(MoneyDisplay, BeltImage):
    def __init__(self, font, money_file="money.txt", belt_image_path="belt.png", scale=1.0):
        MoneyDisplay.__init__(self, font, money_file)
        BeltImage.__init__(self, belt_image_path, scale)

    def draw_money(self, screen):
        money_display = self.font.render(f"{self.money}$", True, pygame.Color('black'))
        screen.blit(money_display, (15, 455))  # Adjusted position to fit within screen height

    def draw_belt(self, screen):
        screen.blit(self.image, (-65, 390))  # Adjusted position to fit within screen height

    def draw(self, screen):
        self.draw_belt(screen)
        self.draw_money(screen)


class BetButtons:
    def __init__(self, font):
        self.font = font
        self.buttons = self.load_buttons()
        self.current_bet = 0
        self.bets = {}
        self.bet_placed = False  # Flag to indicate if bet is placed

    def load_buttons(self):
        buttons = {
            '100': {'image': self.load_scaled_image('buttons/100.png', 0.09), 'bet': 100},
            '1000': {'image': self.load_scaled_image('buttons/1000.png', 0.09), 'bet': 1000},
            '10000': {'image': self.load_scaled_image('buttons/10000.png', 0.09), 'bet': 10000},
            'ALL-IN': {'image': self.load_scaled_image('buttons/ALL-IN.png', 0.09), 'bet': 'all-in'},
            'CLEAR': {'image': self.load_scaled_image('buttons/clear.png', 0.09), 'bet': 'clear'},
            'PLACE BET': {'image': self.load_scaled_image('buttons/place_bet.png', 0.13), 'bet': 'place_bet'}
        }

        x_start = 140
        y_position = 415  # Adjusted to fit within screen height
        for key, button in buttons.items():
            button['rect'] = button['image'].get_rect(topleft=(x_start, y_position))
            x_start += button['rect'].width   # Add spacing between buttons

        # Center the "Place Bet" button on the screen
        place_bet_button = buttons['PLACE BET']
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        place_bet_button['rect'] = place_bet_button['image'].get_rect(center=(900//2, 300))
        # 538, 330

        return buttons

    def load_scaled_image(self, path, scale):
        try:
            image = pygame.image.load(path)
            width = int(image.get_width() * scale)
            height = int(image.get_height() * scale)
            return pygame.transform.scale(image, (width, height))
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            return pygame.Surface((1, 1))  # Return a small empty surface as a placeholder

    def draw(self, screen):
        for button_info in self.buttons.values():
            screen.blit(button_info['image'], button_info['rect'])

        # Create a surface for the text with a white background
        bet_text = f"Current Bet: ${self.current_bet}"
        bet_display = self.font.render(bet_text, True, (0, 0, 0), (255, 255, 255))  # Text with black color and white background

        # Get the rectangle of the text surface to position it
        bet_rect = bet_display.get_rect()
        bet_rect.topleft = (360, 350)  # Adjusted position to fit within screen height

        # Blit the text surface onto the screen
        screen.blit(bet_display, bet_rect)

    def handle_event(self, event, money_display):
        global final_bet  # Declare the global variable to modify it

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
                    elif bet_amount == 'place_bet':
                        self.bet_placed = True  # Set the flag to indicate the bet is placed
                        final_bet = self.current_bet  # Update the global variable
                        print(f"Bet placed: {self.current_bet}")
                    else:
                        self.current_bet += bet_amount
                    print(f"Current bet: {self.current_bet}")
            for number, rect in number_rects.items():
                if rect.collidepoint(pos):
                    if number not in self.bets:
                        self.bets[number] = self.current_bet
                    print(f"Bet placed on number: {number}")


def main():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions and setup
    SCREEN_WIDTH, SCREEN_HEIGHT = 900, 515
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Money Display")

    # Initialize font
    font = pygame.font.Font(None, 36)

    # Create MoneyBeltDisplay instance
    money_belt_display = MoneyBeltDisplay(font, "money.txt", "belt.png", 0.15)

    # Create BetButtons instance
    bet_buttons = BetButtons(font)

    # Load background image
    background = pygame.image.load("table.PNG")

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            bet_buttons.handle_event(event, money_belt_display)

        # Check if the bet is placed
        if bet_buttons.bet_placed:
            running = False

        # Draw background
        screen.blit(background, (0, 0))

        # Draw money belt display
        money_belt_display.draw(screen)

        # Draw bet buttons
        bet_buttons.draw(screen)

        # Update display
        pygame.display.flip()

    # Print final bet value for debugging purposes
    print(f"Final bet: {final_bet}")

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
