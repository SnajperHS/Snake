import random
import sys
import pygame
from dict_number_rects import number_rects


color_map = {
    'Red': {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36},
    'Black': {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
}

odd_numbers = {num for num in range(1, 37) if num % 2 != 0}
even_numbers = {num for num in range(1, 37) if num % 2 == 0}
first_12 = {num for num in range(1, 13)}
second_12 = {num for num in range(13, 25)}
third_12 = {num for num in range(25, 37)}
first_column = {num for num in range(1, 37) if num % 3 == 1}
second_column = {num for num in range(1, 37) if num % 3 == 2}
third_column = {num for num in range(1, 37) if num % 3 == 0}
first_18 = {num for num in range(1, 19)}
second_18 = {num for num in range(19, 37)}


class MoneyDisplay:
    def __init__(self, font, file_path="money.txt"):
        self.font = font
        self.file_path = file_path
        self.money = self.load_money()

    def load_money(self):
        try:
            with open(self.file_path, "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading money: {e}")
            return 0

    def update_money(self, amount):
        self.money += amount
        with open(self.file_path, "w") as file:
            file.write(str(self.money))

    def draw(self, screen):
        money_display = self.font.render(f"{self.money}$", True, pygame.Color('black'))
        screen.blit(money_display, (12, 640))

    def handle_win(self, bet_amount, multiplier=1):
        self.update_money(bet_amount * multiplier)

    def handle_loss(self, bet_amount):
        self.update_money(-bet_amount)


class BeltImage:
    def __init__(self, path, scale):
        self.image = load_scaled_image(path, scale)
        self.position = (-56, 585)

    def draw(self, screen):
        screen.blit(self.image, self.position)


class BetButtons:
    def __init__(self, font):
        self.font = font
        self.buttons = self.load_buttons()
        self.current_bet = 0
        self.bets = {}

    def load_buttons(self):
        buttons = {
            '100': {'image': load_scaled_image('buttons/100.png', 0.08), 'bet': 100},
            '1000': {'image': load_scaled_image('buttons/1000.png', 0.08), 'bet': 1000},
            '10000': {'image': load_scaled_image('buttons/10000.png', 0.08), 'bet': 10000},
            'ALL-IN': {'image': load_scaled_image('buttons/ALL-IN.png', 0.08), 'bet': 'all-in'},
            'CLEAR': {'image': load_scaled_image('buttons/clear.png', 0.08), 'bet': 'clear'}
        }

        x_start = 170
        for key, button in buttons.items():
            button['rect'] = button['image'].get_rect(topleft=(x_start, 701 - 80))
            x_start += button['rect'].width + 10  # Add spacing between buttons
        return buttons

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


def load_scaled_image(path, scale):
    image = pygame.image.load(path)
    width = int(image.get_width() * scale)
    height = int(image.get_height() * scale)
    return pygame.transform.scale(image, (width, height))


def rotate_image(image, angle, center):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center)
    return rotated_image, new_rect


def main():
    pygame.init()
    screen = pygame.display.set_mode((1125, 701))
    pygame.display.set_caption("Roulette Table")

    roulette_table = pygame.image.load('r_table.png')
    circle1 = load_scaled_image('circle/border.png', 0.5)
    circle2 = load_scaled_image('circle/nummers.PNG', 0.95)
    circle3 = load_scaled_image('circle/zielony.png', 0.7)
    belt_image = BeltImage('belt.png', 0.13)
    circle1_rect = circle1.get_rect(center=(300, 350))
    circle2_rect = circle2.get_rect(center=(300, 350))
    circle3_rect = circle3.get_rect(center=(300, 350))

    font = pygame.font.Font(None, 36)
    money_display = MoneyDisplay(font)
    bet_buttons = BetButtons(font)

    spin_button = font.render('Spin', True, pygame.Color('black'))
    spin_button_rect = spin_button.get_rect(center=circle1_rect.center)
    message_font = pygame.font.Font(None, 48)

    bets = {}
    result_text = ""
    message_text = ""
    result_color = pygame.Color('white')
    message_color = None

    running = True
    spinning = False
    angle = 0
    clock = pygame.time.Clock()
    winning_number = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if spin_button_rect.collidepoint(pos) and circle1_rect.collidepoint(pos) and not spinning:
                    if bet_buttons.current_bet > 0:
                        money_display.handle_loss(bet_buttons.current_bet)
                        spinning = True
                        start_ticks = pygame.time.get_ticks()
                        winning_number = random.randint(0, 36)
                        result_text = f"Number: {winning_number}"
                        message_text = "You lose!"
                        message_color = pygame.Color('red')
                        total_win_amount = 0
                        win = False

                        if winning_number in bet_buttons.bets:
                            total_win_amount += bet_buttons.current_bet * 35
                            win = True
                        else:
                            for bet, amount in bet_buttons.bets.items():
                                if bet == 'Red' and winning_number in color_map['Red']:
                                    total_win_amount += amount * 2
                                    win = True
                                elif bet == 'Black' and winning_number in color_map['Black']:
                                    total_win_amount += amount * 2
                                    win = True
                                elif bet == 'Odd' and winning_number in odd_numbers:
                                    total_win_amount += amount * 2
                                    win = True
                                elif bet == 'Even' and winning_number in even_numbers:
                                    total_win_amount += amount * 2
                                    win = True
                                elif bet == '1st_12' and winning_number in first_12:
                                    total_win_amount += amount * 3
                                    win = True
                                elif bet == '2nd_12' and winning_number in second_12:
                                    total_win_amount += amount * 3
                                    win = True
                                elif bet == '3rd_12' and winning_number in third_12:
                                    total_win_amount += amount * 3
                                    win = True
                                elif bet == '1_column' and winning_number in first_column:
                                    total_win_amount += amount * 3
                                    win = True
                                elif bet == '2_column' and winning_number in second_column:
                                    total_win_amount += amount * 3
                                    win = True
                                elif bet == '3_column' and winning_number in third_column:
                                    total_win_amount += amount * 3
                                    win = True
                                elif bet == '1-18' and winning_number in first_18:
                                    total_win_amount += amount * 2
                                    win = True
                                elif bet == '19-36' and winning_number in second_18:
                                    total_win_amount += amount * 2
                                    win = True

                        if win:
                            message_text = "You win!"
                            win_amount_text = f"Won: ${total_win_amount}"
                            message_color = pygame.Color('white')
                        else:
                            win_amount_text = ""

                        bet_buttons.current_bet = 0
                        bet_buttons.bets = {}

                bet_buttons.handle_event(event, money_display)

        screen.fill((0, 0, 0))
        screen.blit(roulette_table, (0, 0))
        belt_image.draw(screen)
        money_display.draw(screen)
        screen.blit(circle1, circle1_rect.topleft)

        if spinning:
            elapsed_ticks = pygame.time.get_ticks() - start_ticks
            if elapsed_ticks < 3000:
                angle += 5
                rotated_image, new_rect = rotate_image(circle2, angle, circle2_rect.center)
                screen.blit(rotated_image, new_rect.topleft)
            else:
                spinning = False
                angle = 0
                if win:
                    money_display.update_money(total_win_amount)

        else:
            screen.blit(circle2, circle2_rect.topleft)

        screen.blit(circle3, circle3_rect.topleft)

        if circle1_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(spin_button, spin_button_rect.topleft)

        bet_buttons.draw(screen)

        if not spinning and winning_number is not None:
            result_surface = font.render(result_text, True, result_color)
            screen.blit(result_surface, (600, 250))
            message_surface = message_font.render(message_text, True, message_color)
            screen.blit(message_surface, (600, 300))

            if win:
                win_amount_surface = message_font.render(win_amount_text, True, message_color)
                screen.blit(win_amount_surface, (600, 350))

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
