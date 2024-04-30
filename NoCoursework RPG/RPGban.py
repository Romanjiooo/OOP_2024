import pygame
import sys
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (11,111,11)
GREY = (11,111,11)


class EscMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.Font(None, 48)
        self.options = ["Quit", "Cancel"]
        self.selected_index = 0
        self.active = False

    def draw(self):
        if self.active:
            self.screen.fill((0, 0, 0, 128))
            for index, option in enumerate(self.options):
                color = GREEN if index == self.selected_index else RED
                label = self.font.render(option, True, color)
                position = (SCREEN_WIDTH // 2 - label.get_width() // 2,
                            SCREEN_HEIGHT // 2 - label.get_height() // 2 + 50 * index)
                self.screen.blit(label, position)

    def update(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = max(0, self.selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = min(len(self.options) - 1, self.selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected_index] == "Quit":
                        pygame.quit()
                        sys.exit()
                    elif self.options[self.selected_index] == "Cancel":
                        self.active = False
                        return "cancel"
            return None

    def activate(self):
        self.active = True

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.options = ["Start Game", "Quit"]
        self.selected_index = 0

    def draw(self):
        self.screen.fill(WHITE)
        for index, option in enumerate(self.options):
            color = GREEN if index == self.selected_index else RED
            label = self.font.render(option, True, color)
            position = (SCREEN_WIDTH // 2 - label.get_width() // 2,
                        SCREEN_HEIGHT // 2 - label.get_height() // 2 + 50 * index)
            self.screen.blit(label, position)

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.options) - 1, self.selected_index + 1)
            elif event.key == pygame.K_RETURN:
                if self.options[self.selected_index] == "Start Game":
                    return "start"
                elif self.options[self.selected_index] == "Quit":
                    pygame.quit()
                    sys.exit()
        return None



class Game:
    def __init__(self, screen):
        self.screen = screen
        self.character = Character(screen, "character.png", [50, 50])
        self.background = pygame.transform.scale(pygame.image.load("auditorium_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.door = pygame.transform.scale(pygame.image.load("door.png"), (100, 200))
        self.door_pos = [SCREEN_WIDTH - 150, 280]
        self.action_button = pygame.transform.scale(pygame.image.load("action_button.png"), (50, 50))
        self.action_button_pos = [SCREEN_WIDTH - 200, 50]
        self.at_door = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.door, self.door_pos)
        self.character.draw()
        if self.at_door:
            self.screen.blit(self.action_button, self.action_button_pos)

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx -= 5
        if keys[pygame.K_RIGHT]:
            dx += 5
        if keys[pygame.K_UP]:
            dy -= 5
        if keys[pygame.K_DOWN]:
            dy += 5
        self.character.move(dx, dy)
        if abs(self.character.position[0] - self.door_pos[0]) < 50 and abs(self.character.position[1] - self.door_pos[1]) < 100:
            self.at_door = True
        else:
            self.at_door = False

class GameObject:
    def __init__(self, screen, image_path, position, scale=(50, 100)):
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image_path), scale)
        self.position = list(position)
        self.rect = self.image.get_rect(topleft=self.position)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        pass

class Character(GameObject):
    def __init__(self, screen, image_path, position):
        super().__init__(screen, image_path, position, scale=(50, 100))

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy
        self.rect.topleft = self.position

class Inventory:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.items = []
        self.max_items = 5
        self.health = 1000
        self.health_bar_width = 20

    def draw(self):
        x_start = 200
        y_start = 500
        icon_size = 40
        for idx, item in enumerate(self.items):
            self.screen.blit(item['icon'], (x_start + idx * (icon_size + 5), y_start))

        pygame.draw.rect(self.screen, RED, (10, y_start + 50, self.health_bar_width, 20))
        pygame.draw.rect(self.screen, GREEN, (10, y_start + 50, self.health_bar_width * (self.health / 100), 20))

    def add_item(self, icon_path):
        if len(self.items) < self.max_items:
            icon = pygame.image.load(icon_path)
            icon = pygame.transform.scale(icon, (40, 40))
            self.items.append({'icon': icon})

    def reduce_health(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.reset_game()

    def reset_game(self):
        print("Game Over! Restarting...")
        self.health = 1000
        self.items = []
        return 'restart'

class Combat:
    def __init__(self, character, enemies):
        self.character = character
        self.enemies = enemies

    def attack(self, enemy):
        if enemy in self.enemies:
            damage = 0.00000001
            enemy.health -= damage
            print(f"Attacked {enemy.name} for {damage} damage!")

    def check_defeat(self):
        for enemy in self.enemies:
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                print(f"{enemy.name} defeated!")

class EnemySpawner:
    def __init__(self, screen, image_path, num_enemies):
        self.screen = screen
        self.enemies = []
        self.image_path = image_path
        self.num_enemies = num_enemies

    def spawn_enemies(self):
        for _ in range(self.num_enemies):
            start_pos = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
            self.enemies.append(Enemy(self.screen, self.image_path, start_pos))

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw()

    def update_enemies(self, target_pos):
        for enemy in self.enemies:
            enemy.update(target_pos)

    def check_collisions(self, target_pos, damage_range):
        damage = 0
        for enemy in self.enemies:
            if enemy.check_collision(target_pos, damage_range):
                damage += 5
        return damage

    def clear_enemies(self):
        self.enemies.clear()
class Enemy:
    def __init__(self, screen, image_path, start_pos):
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image_path), (50, 100))
        self.pos = list(start_pos)
        self.speed = 2

    def draw(self):
        self.screen.blit(self.image, self.pos)

    def update(self, target_pos):
        if self.pos[0] < target_pos[0]:
            self.pos[0] += self.speed
        elif self.pos[0] > target_pos[0]:
            self.pos[0] -= self.speed

        if self.pos[1] < target_pos[1]:
            self.pos[1] += self.speed
        elif self.pos[1] > target_pos[1]:
            self.pos[1] -= self.speed

    def check_collision(self, target_pos, damage_range):
        if abs(self.pos[0] - target_pos[0]) < damage_range and abs(self.pos[1] - target_pos[1]) < damage_range:
            return True
        return False

class NPC:
    def __init__(self, screen, image_path, position, dialogue):
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image_path), (50, 100))
        self.position = position
        self.dialogue = dialogue
        self.dialogue_index = 0
        self.rect = self.image.get_rect(topleft=self.position)

    def draw(self):
        self.screen.blit(self.image, self.position)

    def interact(self):
        if self.dialogue_index < len(self.dialogue):
            print(self.dialogue[self.dialogue_index])
            self.dialogue_index += 1
        else:
            print("You have already completed my dialogue.")


class Door:
    def __init__(self, screen, image_path, position, rect, to_scene, scale):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, scale)
        self.position = position
        self.rect = self.image.get_rect(topleft=rect)
        self.to_scene = to_scene

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def interact(self, character_rect):
        if self.rect.colliderect(character_rect):
            return self.target_scene
        return None

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, GREY, self.rect)

    def check_collision(self, character_rect):
        return self.rect.colliderect(character_rect)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

menu = Menu(screen)
game = Game(screen)
esc_menu = EscMenu(screen, game)
inventory = Inventory(screen)
current_scene = "menu"

enemy_spawner = EnemySpawner(screen, "enemy_icon.png", 5)
enemy_spawner.spawn_enemies()

npcs = [
    NPC(screen, "npc_image.png", (200, 200), ["Hello, adventurer!", "Complete my quest!"]),
    NPC(screen, "npc_image (2).png", (400, 400), ["Need help?", "I lost something important."])
]
door_scale = (100, 200)
doors = [
    Door(screen, "door.png", (100, 100), (100, 120), "auditorium2", door_scale)

]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_scene == "menu":
            result = menu.update(event)
            if result == "start":
                current_scene = "game"
            elif result == "quit":
                pygame.quit()
                sys.exit()
        elif current_scene == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_menu.activate()
                    current_scene = "esc"
                if event.key == pygame.K_SPACE:
                    for npc in npcs:
                        if npc.rect.collidepoint(game.character.pos):
                            npc.interact()
                for door in doors:
                    if door.rect.colliderect(game.character.rect):
                        current_scene = door.to_scene
        elif current_scene == "esc":
            result = esc_menu.update(event)
            if result == "cancel":
                current_scene = "game"

    if current_scene == "game":
        game.update()
        enemy_spawner.update_enemies(game.character.position)
        damage = enemy_spawner.check_collisions(game.character.position, 50)
        inventory.reduce_health(damage)

    screen.fill(WHITE)
    if current_scene == "menu":
        menu.draw()
    elif current_scene == "game":
        game.draw()
        for npc in npcs:
            npc.draw()
        inventory.draw()
        enemy_spawner.draw_enemies()
        for door in doors:
            door.draw(screen)
    elif current_scene == "esc":
        esc_menu.draw()

    pygame.display.flip()
    clock.tick(FPS)

