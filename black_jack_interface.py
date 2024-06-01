import pygame
import subprocess

# Inicjalizacja Pygame
pygame.init()

# Konfiguracja ekranu
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 515
BACKGROUND_COLOR = '#076128'
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra Startowa")

# Ładowanie i skalowanie obrazów
logo = pygame.image.load('bj.png')
logo = pygame.transform.scale(logo, (int(logo.get_width() * 0.3), int(logo.get_height() * 0.25)))

play_button = pygame.image.load('buttons/play.png')
play_button = pygame.transform.scale(play_button, (int(play_button.get_width() * 0.13), int(play_button.get_height() * 0.13)))

set_bet_button = pygame.image.load('buttons/set_bet.png')
set_bet_button = pygame.transform.scale(set_bet_button, (int(set_bet_button.get_width() * 0.13), int(set_bet_button.get_height() * 0.13)))

place_bet_button = pygame.image.load('buttons/place_bet.png')
place_bet_button = pygame.transform.scale(place_bet_button, (int(place_bet_button.get_width() * 0.13), int(place_bet_button.get_height() * 0.13)))

# Pozycje
logo_rect = logo.get_rect(center=(SCREEN_WIDTH // 2, 90))
play_button_rect = play_button.get_rect(center=(SCREEN_WIDTH // 2, 250))
set_bet_button_rect = set_bet_button.get_rect(center=(SCREEN_WIDTH // 2, 360))
place_bet_button_rect = place_bet_button.get_rect(center=(SCREEN_WIDTH // 2, 470))

# Aktualna wartość zakładu
final_bet = 0  # Zmienna globalna na początku

# Funkcja do odczytu final_bet z pliku
def read_final_bet():
    try:
        with open("final_bet.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

# Funkcja do uruchamiania skryptów
def run_black_jack():
    subprocess.call(['python', 'black_jack_game.py'])

def run_black_jack_bet():
    subprocess.call(['python', 'black_jack_bet.py'])

def update_current_bet():
    global final_bet
    final_bet = read_final_bet()  # Aktualizacja final_bet

# Inicjalizacja final_bet na początku
final_bet = read_final_bet()

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                run_black_jack()
            elif set_bet_button_rect.collidepoint(event.pos):
                run_black_jack_bet()
            elif place_bet_button_rect.collidepoint(event.pos):
                update_current_bet()

    # Rysowanie ekranu
    screen.fill(pygame.Color(BACKGROUND_COLOR))
    screen.blit(logo, logo_rect)
    screen.blit(play_button, play_button_rect)
    screen.blit(set_bet_button, set_bet_button_rect)
    screen.blit(place_bet_button, place_bet_button_rect)

    # Rysowanie napisu aktualnego zakładu
    font = pygame.font.Font(None, 36)
    bet_text = font.render(f"current bet: {final_bet}", True, pygame.Color('black'), pygame.Color('white'))
    bet_rect = bet_text.get_rect(center=(SCREEN_WIDTH // 2, 510))
    screen.blit(bet_text, bet_rect)

    pygame.display.flip()

pygame.quit()
