import pygame
import random
import sys
import subprocess
from class_question import QuestionButton
from class_money_display import MoneyDisplay, BeltImage

python_path = sys.executable
script_path = "class_fireworks.py"
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 515
CARD_WIDTH, CARD_HEIGHT = 70, 100
FONT = pygame.font.Font(None, 36)

# Global bet variable
final_bet = 0

# Read the final_bet value from the file
def read_final_bet():
    try:
        with open("final_bet.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

# Write the final_bet value to the file
def write_final_bet(value):
    with open("final_bet.txt", "w") as file:
        file.write(str(value))

final_bet = read_final_bet()

# Initialize the mixer and load the sound file
pygame.mixer.init()
card_sound = pygame.mixer.Sound('putting_cards.mp3')

class BlackjackQuestionButton(QuestionButton):
    def __init__(self, image_path, position, size, font):
        super().__init__(image_path, position, size)
        self.font = font

    def draw_text(self, screen):
        if self.display_text:
            pygame.draw.rect(screen, (255, 255, 255), (150, 100, 650, 300))
            self._draw_text(screen, "You must try to get a score as close as possible to 21", 470, 160, self.font)
            self._draw_text(screen, "but can't exceed 21.", 280, 190, self.font)
            self._draw_text(screen, "1=1, 2=2, 3=3, 4=4, 5=5, 6=6, 7=7, 8=8, 9=9, 10=10,", 470, 250, self.font)
            self._draw_text(screen, "J,Q,K = 10, AS = 1 or 11", 470, 280, self.font)

class MoneyBeltDisplay(MoneyDisplay, BeltImage):
    def __init__(self, font, money_file_path, belt_image_path, belt_scale):
        MoneyDisplay.__init__(self, font, money_file_path)
        BeltImage.__init__(self, belt_image_path, belt_scale)

    def draw(self, screen):
        self.draw_belt(screen)
        self.draw_money(screen)

    def draw_money(self, screen):
        money_display = self.font.render(f"{self.money}$", True, pygame.Color('black'))
        screen.blit(money_display, (15, 455))  # Adjusted position to fit within screen height

    def draw_belt(self, screen):
        screen.blit(self.image, (-65, 390))  # Adjusted position to fit within screen height

# Ustawienia ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Blackjack')

# Ładowanie tła
def load_background(image_path):
    background = pygame.image.load(image_path)
    return background

def load_card_images(deck):
    card_images = {}
    for card_path in deck:
        image = pygame.image.load(card_path)
        image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        card_images[card_path] = image
    back_image = pygame.image.load('cards/back.PNG')
    back_image = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))
    card_images['cards/back.PNG'] = back_image
    return card_images

def shuffle_deck(deck):
    shuffled_deck = deck[:]
    random.shuffle(shuffled_deck)
    return shuffled_deck

def card_value(card_path):
    rank = card_path.split('/')[2].split('.')[0]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'AS':
        return 11
    else:
        return int(rank)

def hand_value(hand):
    value = sum(card_value(card) for card in hand)
    aces = sum(1 for card in hand if 'AS' in card)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def draw_cards(screen, card_images, card_paths, x_start, y, show_score=True):
    card_spacing = 20
    total_width = len(card_paths) * (CARD_WIDTH + card_spacing) - card_spacing
    start_x = x_start - total_width // 2

    for i, card in enumerate(card_paths):
        screen.blit(card_images[card], (start_x + i * (CARD_WIDTH + card_spacing), y))

    if show_score:
        score = hand_value(card_paths)
        draw_text(screen, f'Score: {score}', start_x + total_width + 100, y + 50)

def draw_text(screen, text, x, y):
    text_surface = FONT.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x, y))
    background_rect = text_rect.inflate(20, 10)
    pygame.draw.rect(screen, (255, 255, 255), background_rect)
    screen.blit(text_surface, text_rect)

def draw_current_bet(screen, bet):
    text = f"current bet : {bet}"
    draw_text(screen, text, 130, 390)

def reset_game(deck_of_cards):
    shuffled_deck = shuffle_deck(deck_of_cards)
    player_hand = [shuffled_deck.pop() for _ in range(2)]
    dealer_hand = [shuffled_deck.pop() for _ in range(2)]
    return shuffled_deck, player_hand, dealer_hand

background_image = 'table.PNG'
background = load_background(background_image)

deck_of_cards = [
    'cards/karo/AS.PNG', 'cards/karo/2.PNG', 'cards/karo/3.PNG', 'cards/karo/4.PNG', 'cards/karo/5.PNG',
    'cards/karo/6.PNG', 'cards/karo/7.PNG', 'cards/karo/8.PNG', 'cards/karo/9.PNG', 'cards/karo/10.PNG', 'cards/karo/J.PNG',
    'cards/karo/Q.PNG', 'cards/karo/K.PNG', 'cards/pik/AS.PNG', 'cards/pik/2.PNG', 'cards/pik/3.PNG', 'cards/pik/4.PNG',
    'cards/pik/5.PNG', 'cards/pik/6.PNG', 'cards/pik/7.PNG', 'cards/pik/8.PNG', 'cards/pik/9.PNG', 'cards/pik/10.PNG',
    'cards/pik/J.PNG', 'cards/pik/Q.PNG', 'cards/pik/K.PNG', 'cards/kier/AS.PNG', 'cards/kier/2.PNG', 'cards/kier/3.PNG',
    'cards/kier/4.PNG', 'cards/kier/5.PNG', 'cards/kier/6.PNG', 'cards/kier/7.PNG', 'cards/kier/8.PNG', 'cards/kier/9.PNG',
    'cards/kier/10.PNG', 'cards/kier/J.PNG', 'cards/kier/Q.PNG', 'cards/kier/K.PNG', 'cards/trefl/AS.PNG', 'cards/trefl/2.PNG',
    'cards/trefl/3.PNG', 'cards/trefl/4.PNG', 'cards/trefl/5.PNG', 'cards/trefl/6.PNG', 'cards/trefl/7.PNG', 'cards/trefl/8.PNG',
    'cards/trefl/9.PNG', 'cards/trefl/10.PNG', 'cards/trefl/J.PNG', 'cards/trefl/Q.PNG', 'cards/trefl/K.PNG'
]

card_images = load_card_images(deck_of_cards)
shuffled_deck, player_hand, dealer_hand = reset_game(deck_of_cards)

button = BlackjackQuestionButton('question.png', (900,500), (100, 50), FONT)
money_belt_display = MoneyBeltDisplay(FONT, "money.txt", 'belt.png', 0.15)

game_over = False
player_turn = True
interface_launched = False  # Flaga śledząca uruchomienie interface.py

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        button.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h and player_turn and not game_over:
                player_hand.append(shuffled_deck.pop())
                card_sound.play()  # Play sound when player hits
                if hand_value(player_hand) > 21:
                    game_over = True
                    player_turn = False
                    money_belt_display.handle_loss(final_bet)  # Update money on player bust
            elif event.key == pygame.K_s and not game_over:
                player_turn = False
                while hand_value(dealer_hand) < 17:
                    dealer_hand.append(shuffled_deck.pop())
                game_over = True
                dealer_score = hand_value(dealer_hand)
                player_score = hand_value(player_hand)
                if player_score > 21:
                    money_belt_display.handle_loss(final_bet)  # Update money on player bust
                elif dealer_score > 21 or player_score > dealer_score:
                    money_belt_display.handle_win(final_bet, 2)  # Update money on player win
                elif player_score < dealer_score:
                    money_belt_display.handle_loss(final_bet)  # Update money on dealer win
            elif event.key == pygame.K_r and game_over:
                shuffled_deck, player_hand, dealer_hand = reset_game(deck_of_cards)
                game_over = False
                player_turn = True
                interface_launched = False  # Reset flagi przy restarcie gry

    screen.blit(background, (0, 0))

    draw_cards(screen, card_images, player_hand, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4, show_score=True)
    draw_cards(screen, card_images, dealer_hand, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, show_score=True)

    if game_over:
        dealer_score = hand_value(dealer_hand)
        player_score = hand_value(player_hand)
        if player_score > 21:
            result = "Player busts! You lose."
        elif dealer_score > 21 or player_score > dealer_score:
            result = "Player wins!"
            if not interface_launched:
                subprocess.call([python_path, script_path])
                interface_launched = True  # Ustawienie flagi po uruchomieniu interface.py
        elif player_score < dealer_score:
            result = "Dealer wins!"
        else:
            result = "Push! It's a tie."
        draw_text(screen, result, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    if not game_over:
        draw_text(screen, 'H for hit, S for stand, R to restart', 440, 315)

    # Draw the current bet amount in the center of the screen
    draw_current_bet(screen, final_bet)

    button.draw(screen)
    button.draw_text(screen)
    money_belt_display.draw(screen)

    pygame.display.update()

# Save the final bet to the file when exiting
write_final_bet(final_bet)

pygame.quit()
