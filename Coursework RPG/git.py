import pygame
import sys
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (11,111,11)
GREY = (128,128,128)


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
        if abs(self.character._position[0] - self.door_pos[0]) < 50 and abs(self.character._position[1] - self.door_pos[1]) < 100:
            self.at_door = True
        else:
            self.at_door = False

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

        # Подготовка новой позиции персонажа для проверки столкновения
        new_rect = self.character._rect.move(dx, dy)

        # Проверяем столкновение с каждой стеной
        if not any(wall.check_collision(new_rect) for wall in walls):
            self.character.move(dx, dy)  # Перемещаем персонажа, только если нет столкновения
        else:
            print("Collision detected!")  # Можно добавить обработку столкновения


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

class Character:
    def __init__(self, screen, image_path, position):
        self._screen = screen
        self._image = pygame.transform.scale(pygame.image.load(image_path), (50, 100))
        self._position = list(position)
        self._rect = self._image.get_rect(topleft=self._position)

    def draw(self):
        self._screen.blit(self._image, self._rect)

    def move(self, dx, dy):
        self._set_position(self._position[0] + dx, self._position[1] + dy)

    def _set_position(self, x, y):
        """Устанавливает новую позицию персонажа и обновляет положение прямоугольника."""
        self._position = [x, y]
        self._rect.topleft = self._position

    def get_position(self):
        """Возвращает текущую позицию персонажа."""
        return self._position



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

    def find_closest_enemy(self):
        closest_enemy = None
        min_distance = float('inf')
        for enemy in self.enemies:
            # Рассчитываем расстояние от персонажа до врага
            distance = ((self.character._position[0] - enemy.pos[0]) ** 2 + (
                        self.character._position[1] - enemy.pos[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        return closest_enemy

    def attack_closest_enemy(self):
        if not self.enemies:
            print("No enemies to attack.")
            return

        enemy = self.find_closest_enemy()
        if enemy:
            damage = 50
            enemy.health -= damage
            print(f"Attacked {enemy.name} for {damage} damage!")
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
            enemy = Enemy(self.screen, self.image_path, start_pos)
            self.enemies.append(enemy)

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
                damage += 0
        return damage

class Enemy:
    def __init__(self, screen, image_path, start_pos, health=100):
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image_path), (50, 100))
        self.pos = list(start_pos)
        self.speed = 2
        self.health = health  # Здоровье врага
        self.name = "Enemy"  # Название для вывод

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

class NPC(GameObject):
    def __init__(self, screen, image_path, position, dialogue_data):
        super().__init__(screen, image_path, position)
        self.dialogue = Dialogue(dialogue_data)  # Используем новый класс Dialogue

    def interact(self):
        # Начинаем диалог с начального ключа, например "start"
        self.dialogue.start_conversation("start")



class Dialogue:
    def __init__(self, conversations):
        self.conversations = conversations
        self.current_conversation = None

    def start_conversation(self, start_key):
        self.current_conversation = start_key
        self.display_conversation(start_key)

    def display_conversation(self, key):
        if key not in self.conversations:
            print("Dialogue finished or not found.")
            return

        question, responses = self.conversations[key]
        print(question)
        for idx, response in enumerate(responses[0]):
            print(f"{idx + 1}: {response}")

        self.get_player_input(responses)

    def get_player_input(self, responses):
        try:
            choice = int(input("Выбери ответ (напиши цифру/число): ")) - 1
            if 0 <= choice < len(responses[1]):
                responses[1][choice]()  # вызов callback функции для выбранного ответа
        except (ValueError, IndexError):
            print("Неверная цифра/число.")
            self.display_conversation(self.current_conversation)  # Перезапустить текущий диалог при ошибке ввода


class Door(GameObject):
    def __init__(self, screen, image_path, position, from_scene, to_scene, scale=(100, 200)):
        super().__init__(screen, image_path, position, scale)
        self.from_scene = from_scene  # Сцена, из которой "выходит" дверь
        self.to_scene = to_scene      # Сцена, в которую "входит" дверь

    def interact(self, character_rect):
        if self.rect.colliderect(character_rect):
            return self.to_scene


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


character = Character(screen, "character_image.png", [50,50])
dialogue_data = {
    "start": ("Привет, первокур! Че надо?",
             (["Cпросить как пройти к ноге.", "Сказать 'Пошёл ты'. "],
              [lambda: npc.dialogue.display_conversation("quest"), lambda: npc.dialogue.display_conversation("goodbye")])),
    "quest": ("Победи всех МСУшников, которые сюда лезут. Потом скажу где это.",
             (["Окэ, квест принят.", "Аревуар, сам разберусь."],
              [lambda: npc.dialogue.display_conversation("accept"), lambda: npc.dialogue.display_conversation("decline")])),
    "goodbye": ("Чао какао.",
                ([], [])),
    "accept": ("В атаку на нежить, вот тебе лук.",
               ([], [])),
    "decline": ("Адьос.",
                ([], []))
}

npc1 = NPC(screen, "npc_image.png", (30, 50), dialogue_data)
npc2 = NPC(screen, "npc_image (2).png", (350, 350), ["Need help?", "I lost something important."])

npcs = [
    npc1,
    npc2
]

door_scale = (100, 200)

door1 = Door(screen, "door_image.png", (100, 100), "game", "auditorium2", (100, 200))
door2 = Door(screen, "door_image.png", (200, 200), "auditorium2", "game", (100, 200))

doors = [
door1,
door2
]

walls = [
    Wall(-10, 0, 800, -1),
    Wall(-1, 1, -1, 600),
    Wall(800, -1, 800, 600),
    Wall(-1, 600, 800, -2)
]

combat_system = Combat(character, enemy_spawner.enemies)  # Передаем экземпляр


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
                        if npc.rect.collidepoint(game.character._position):
                            npc.interact()
                if event.key == pygame.K_a:
                    # Пример атаки первого врага при нажатии пробела
                    if enemy_spawner.enemies:  # Проверяем, есть ли враги
                        combat_system.attack_closest_enemy()
                for door in doors:
                    if door.rect.colliderect(game.character._rect):
                        current_scene = door.to_scene
        elif current_scene == "esc":
            result = esc_menu.update(event)
            if result == "cancel":
                current_scene = "game"

    if current_scene == "game":
        game.update()
        enemy_spawner.update_enemies(game.character._position)
        damage = enemy_spawner.check_collisions(game.character._position, 50)
        inventory.reduce_health(damage)
    elif current_scene == "auditorium2":
        game.update()

    screen.fill(WHITE)
    if current_scene == "menu":
        menu.draw()
    elif current_scene == "game":
        game.draw()

        for wall in walls:  # Отрисовка каждой стены
            wall.draw(screen)

        for npc in npcs:
            npc.draw()
        inventory.draw()
        enemy_spawner.draw_enemies()
        for door in doors:
            door.draw()
    elif current_scene == "auditorium2":
        game.draw()
        for npc in npcs:
            npc.draw()
        inventory.draw()
        for door in doors:
            door.draw()
    elif current_scene == "esc" :
        esc_menu.draw()

    pygame.display.flip()
    clock.tick(FPS)