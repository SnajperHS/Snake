import pygame
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
        self.image = self.load_scaled_image(path, scale)
        self.position = (-56, 585)

    def load_scaled_image(self, path, scale):
        image = pygame.image.load(path)
        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)
        return pygame.transform.scale(image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, self.position)