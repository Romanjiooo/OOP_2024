import pygame
import sys
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128,128,128)

class BaseMenu:
    '''
        Класс BaseMenu для создания меню в игре.
        Включает методы для инциализации объекта BaseMenu с :
        - __init__(self, screen, options): Инициализирует объект BaseMenu с экраном и списком опций.
        - draw(self): Отрисовывает опции меню на экране, выделяя текущую выбранную опцию.
        - update(self, event): Обрабатывает нажатия клавиш для изменения выбранной опции и подтверждения выбора.
    '''
    def __init__(self, screen, options):
        self.screen = screen
        self.font = pygame.font.Font("minecraft.ttf", 48)  # Попытка загрузки пользовательского шрифта
        self.options = options
        self.selected_index = 0

    def draw(self):
        for index, option in enumerate(self.options):
            color = GREEN if index == self.selected_index else RED
            label = self.font.render(option, True, color)
            x = 400 - label.get_width() // 2
            y = 300 - label.get_height() // 2 + 50 * index
            self.screen.blit(label, (x, y))

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_index = min(len(self.options) - 1, self.selected_index + 1)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_index]
        return None

class Menu(BaseMenu):
    '''
    Класс Menu наследует BaseMenu для создания меню с фоновым изображением.
    Включает методы для инициализации и отрисовки меню с фоновым изображением.
    - __init__(self, screen, background_image_path): Инициализирует объект Menu с экраном и путем к фоновому изображению.
    - draw(self): Отрисовывает фоновое изображение и опции меню на экране.
    - update(self, event): Обрабатывает нажатия клавиш для изменения выбранной опции и подтверждения выбора.
    '''
    def __init__(self, screen, background_image_path):
        super().__init__(screen, ["№;^&*(%()", "Числануться"])
        self.background_image = pygame.image.load(background_image_path)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        super().draw()

    def update(self, event):
        result = super().update(event)
        if result == "№;^&*(%()":
            return "start"
        elif result == "Числануться":
            pygame.quit()
            sys.exit()
        return None

class EscMenu(BaseMenu):
    '''
        Класс EscMenu наследует BaseMenu для создания меню паузы в игре.
        Включает методы для активации, отрисовки и обновления меню паузы.
        - __init__(self, screen, game): Инициализирует объект EscMenu с экраном и ссылкой на игровой объект.
        - draw(self): Отрисовывает меню паузы на затемненном фоне.
        - update(self, event): Обрабатывает нажатия клавиш для изменения выбранной опции и подтверждения выбора.
        - activate(self): Активирует меню паузы.
    '''
    def __init__(self, screen, game):
        super().__init__(screen, ["Академ", "Вернуться"])
        self.game = game
        self.active = False

    def draw(self):
        if self.active:
            self.screen.fill((0, 0, 0, 128))
            super().draw()

    def update(self, event):
        if self.active:
            result = super().update(event)
            if result == "Академ":
                pygame.quit()
                sys.exit()
            elif result == "Вернуться":
                self.active = False
                return "cancel"
        return None

    def activate(self):
        self.active = True

class Game:
    '''
        Класс Game для управления основными элементами игры.
        Включает методы для инициализации, обновления сцены, отрисовки и обновления игрового процесса.
        - __init__(self, screen): Инициализирует объект Game с экраном и основными игровыми элементами.
        - update_scene(self, new_scene): Обновляет текущую сцену игры.
        - draw(self): Отрисовывает фон и персонажа на экране.
        - update(self): Обрабатывает ввод с клавиатуры для перемещения персонажа и проверки столкновений.
    '''
    def __init__(self, screen):
        self.screen = screen
        self.character = Character(screen, "character_image.png", [50, 450])
        self.background = pygame.transform.scale(pygame.image.load("auditorium_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_scene = "initial_scene"

    def update_scene(self, new_scene):
        if new_scene != self.current_scene:
            self.current_scene = new_scene

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.character.draw()

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

        new_rect = self.character._rect.move(dx, dy)

        if not any(wall.check_collision(new_rect) for wall in walls):
            self.character.move(dx, dy)
        else:
            print("Нельзя пройти!")

class GameObject:
    '''
        Класс GameObject для создания объектов игры с изображением.
        Включает методы для инициализации, отрисовки и обновления объектов.
        - __init__(self, screen, image_path, position, scale=(50, 100)): Инициализирует объект GameObject с экраном, путем к изображению, позицией и масштабом.
        - draw(self): Отрисовывает объект на экране.
        - update(self): Обновляет состояние объекта (пустой метод для переопределения).
    '''
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
    '''
        Класс Character для создания и управления персонажем игры.
        Включает методы для инициализации, отрисовки, перемещения и получения позиции персонажа.
        - __init__(self, screen, image_path, position): Инициализирует объект Character с экраном, путем к изображению и позицией.
        - draw(self): Отрисовывает персонажа на экране.
        - move(self, dx, dy): Перемещает персонажа на заданное расстояние.
        - _set_position(self, x, y): Устанавливает новую позицию персонажа.
        - get_position(self): Возвращает текущую позицию персонажа.
    '''
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
        self._position = [x, y]
        self._rect.topleft = self._position

    def get_position(self):
        return self._position



class Health:
    '''
        Класс Health для управления здоровьем персонажа и отображением здоровья на экране.
        Включает методы для инициализации, отрисовки здоровья, уменьшения здоровья и сброса игры.
        - __init__(self, screen): Инициализирует объект Health с экраном и начальным значением здоровья.
        - draw(self): Отрисовывает индикатор здоровья и иконки предметов на экране.
        - reduce_health(self, amount): Уменьшает здоровье на заданное количество и перезапускает игру, если здоровье равно нулю.
        - reset_game(self): Перезапускает игру при окончании здоровья.
    '''
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

    def reduce_health(self, amount):
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.reset_game()

    def reset_game(self):
        print("Game Over! Restarting...")
        global current_scene, enemy_spawner, game
        current_scene = "menu"
        enemy_spawner.reset_spawn()
        game = None
        self.health = 1000


class Combat:
    '''
       Класс Combat для управления боями между персонажем и врагами.
       Включает методы для поиска ближайшего врага и атаки ближайшего врага.
       - __init__(self, character, enemies, game): Инициализирует объект Combat с персонажем, списком врагов и игрой.
       - find_closest_enemy(self): Ищет ближайшего врага к персонажу.
       - attack_closest_enemy(self): Атакует ближайшего врага и удаляет его из списка, если его здоровье становится нулевым.
    '''
    def __init__(self, character, enemies, game):
        self.character = character
        self.enemies = enemies
        self.game = game

    def find_closest_enemy(self):
        closest_enemy = None
        min_distance = float('inf')
        for enemy in self.enemies:
            distance = ((self.character._position[0] - enemy.pos[0]) ** 2 + (
                        self.character._position[1] - enemy.pos[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        return closest_enemy

    def attack_closest_enemy(self):
        enemy = self.find_closest_enemy()
        if enemy:
            total_damage = 50
            enemy.health -= total_damage
            print(f"Attacked {enemy.name} for {total_damage} damage!")
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                print(f"{enemy.name} defeated!")


class EnemySpawner:
    '''
        Класс EnemySpawner для управления созданием врагов в игре.
        Включает методы для создания, сброса, отрисовки и обновления врагов, а также проверки столкновений с врагами.
        - __init__(self, screen, image_path, num_enemies): Инициализирует объект EnemySpawner с экраном, путем к изображению и количеством врагов.
        - spawn_enemies(self): Создает врагов и добавляет их в список врагов.
        - reset_spawn(self): Сбрасывает флаг создания врагов.
        - draw_enemies(self): Отрисовывает всех врагов на экране.
        - update_enemies(self, target_pos): Обновляет положение всех врагов в зависимости от позиции цели.
        - check_collisions(self, target_pos, damage_range): Проверяет столкновения врагов с целью и возвращает общее количество урона.
    '''
    def __init__(self, screen, image_path, num_enemies):
        self.screen = screen
        self.enemies = []
        self.image_path = image_path
        self.num_enemies = num_enemies
        self.spawned = False

    def spawn_enemies(self):
        if not self.spawned:
            for _ in range(self.num_enemies):
                start_pos = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
                enemy = Enemy(self.screen, self.image_path, start_pos)
                self.enemies.append(enemy)
            self.spawned = True

    def reset_spawn(self):
        self.spawned = False

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

    def activate_enemies(self):
        self.enemies_active = True
        print("Enemies activated:", self.enemies_active)
        self.unlock_door()

    def enemies_active(self):
        self.enemies_active = True
        print("Enemies activated:", self.enemies_active)
        self.unlock_door()

    def draw_enemies(self):
        if self.enemies_active:
            for enemy in self.enemies:
                enemy.draw()

    def update_enemies(self, target_pos):
        if self.enemies_active:
            for enemy in self.enemies:
                enemy.update(target_pos)


class Enemy:
    '''
        Класс Enemy для создания врагов в игре.
        Включает методы для инициализации, отрисовки, обновления положения и проверки столкновений врага.
        - __init__(self, screen, image_path, start_pos, health=100): Инициализирует объект Enemy с экраном, путем к изображению, начальной позицией и здоровьем.
        - draw(self): Отрисовывает врага на экране.
        - update(self, target_pos): Обновляет положение врага в зависимости от позиции цели.
        - check_collision(self, target_pos, damage_range): Проверяет столкновение врага с целью и возвращает True, если произошло столкновение.
    '''
    def __init__(self, screen, image_path, start_pos, health=100):
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image_path), (50, 100))
        self.pos = list(start_pos)
        self.speed = 1
        self.health = health
        self.name = "Enemy"

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
    '''
        Класс NPC для создания неписей (неигровых персонажей) в игре.
        Включает методы для инициализации, взаимодействия и разблокировки дверей.
        - __init__(self, screen, image_path, position, dialogue_data, door): Инициализирует объект NPC с экраном, путем к изображению, позицией, данными диалогов и дверью.
        - on_dialogue_complete(self): Вызывается при завершении диалога, активирует врагов и разблокирует дверь.
        - interact(self): Начинает взаимодействие с NPC, инициирует диалог и активирует врагов при необходимости.
        - unlock_door(self): Разблокирует дверь после выполнения условий.
    '''
    def __init__(self, screen, image_path, position, dialogue_data, door):
        super().__init__(screen, image_path, position)
        self.door = door
        self.enemies_active = False
        self.dialogue = Dialogue(dialogue_data, self.on_dialogue_complete)

    def on_dialogue_complete(self):
        self.enemies_active = True
        if self.door and self.door.is_locked:
            self.door.unlock()

    def interact(self):
        result = self.dialogue.start_conversation("start")
        if result == "quest":
            self.enemies_active = True
            self.door.unlock()
        return result

    def unlock_door(self):
        print("Открыта дверь")

        self.door.unlock()


class Dialogue:
    '''
        Класс Dialogue для управления диалогами в игре.
        Включает методы для начала, отображения и обработки диалогов.
        - __init__(self, conversations, callback=None): Инициализирует объект Dialogue с данными диалогов и callback-функцией.
        - start_conversation(self, start_key): Начинает диалог с заданного ключа.
        - display_conversation(self, key): Отображает диалог с заданным ключом.
        - get_player_input(self, responses): Получает ответ игрока и вызывает соответствующую функцию.
    '''
    def __init__(self, conversations, callback=None):
        self.conversations = conversations
        self.current_conversation = None
        self.callback = callback

    def start_conversation(self, start_key):
        self.current_conversation = start_key
        self.display_conversation(start_key)

    def display_conversation(self, key):
        if key not in self.conversations:
            print("Диалог не найден.")
            return
        question, responses = self.conversations[key]
        print(question)
        for idx, response in enumerate(responses[0]):
            print(f"{idx + 1}: {response}")
        self.get_player_input(responses[1])

    def get_player_input(self, responses):
        try:
            choice = int(input("Выбери ответ (напиши цифру/число): ")) - 1
            if 0 <= choice < len(responses):
                responses[choice]()
                if self.callback:
                    self.callback()
        except (ValueError, IndexError):
            print("Неверная цифра/число.")
            self.display_conversation(self.current_conversation)


class Door(GameObject):
    '''
        Класс Door для создания дверей в игре.
        Включает методы для инициализации, разблокировки, блокировки и взаимодействия с дверями.
        - __init__(self, screen, image_path, position, from_scene, to_scene, scale=(100, 200)): Инициализирует объект Door с экраном, путем к изображению, позицией, сценами и масштабом.
        - unlock(self): Разблокирует дверь.
        - lock(self): Блокирует дверь.
        - interact(self, character_rect, current_scene): Взаимодействует с дверью, проверяет возможность перехода между сценами.
    '''
    def __init__(self, screen, image_path, position, from_scene, to_scene, scale=(100, 200)):
        super().__init__(screen, image_path, position, scale)
        self.from_scene = from_scene
        self.to_scene = to_scene
        self.is_locked = True

    def unlock(self):
        print("Дверь открыта!")
        self.is_locked = False

    def lock(self):
        print("Дверь закрыта!")
        self.is_locked = True

    def interact(self, character_rect, current_scene):
        if self.rect.colliderect(character_rect) and not self.is_locked and self.from_scene == current_scene:
            print(f"Переход из {self.from_scene} в {self.to_scene}")
            return self.to_scene
        elif self.is_locked:
            print("Дверь закрыта, поговорите сначала с NPC!")
        else:
            print("Дверь не активна из текущей локации!")
            return None


class Wall:
    '''
        Класс Wall для создания стен в игре.
        Включает методы для инициализации, отрисовки и проверки столкновений со стенами.
        - __init__(self, x, y, width, height): Инициализирует объект Wall с позицией и размерами.
        - draw(self, screen): Отрисовывает стену на экране.
        - check_collision(self, character_rect): Проверяет столкновение стены с прямоугольником персонажа.
    '''
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, GREY, self.rect)

    def check_collision(self, character_rect):
        return self.rect.colliderect(character_rect)


class Auditorium:
    '''
        Класс Auditorium для создания аудитории в игре.
        Включает методы для инициализации, отрисовки и обновления состояния аудитории.
        - __init__(self, screen, background_image_path, npcs, doors, walls, enemies): Инициализирует объект Auditorium с экраном, путем к фоновому изображению, NPC, дверями, стенами и врагами.
        - draw(self): Отрисовывает фон, стены, двери, NPC и врагов на экране.
        - update(self, event): Обновляет состояние аудитории, обрабатывая события взаимодействия с NPC и дверями.
    '''
    def __init__(self, screen, background_image_path, npcs, doors, walls, enemies):
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load(background_image_path), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.npcs = npcs
        self.doors = doors
        self.walls = walls
        self.enemies = enemies

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for wall in self.walls:
            wall.draw(self.screen)
        for door in self.doors:
            door.draw()
        for npc in self.npcs:
            npc.draw()
        for enemy in self.enemies:
            enemy.draw()


    def update(self, event):
        for npc in self.npcs:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if npc.rect.collidepoint(game.character._position):
                        npc.interact()
        for door in self.doors:
            if door.rect.colliderect(game.character._rect):
                if not door.is_locked:
                    return door.to_scene
        return None

class SecurityNPC(NPC):
    '''
        Класс SecurityNPC наследует NPC для создания охранников в игре.
        Включает методы для активации врагов и обновления состояния врагов.
        - __init__(self, screen, image_path, position, door, enemy_spawner, inventory): Инициализирует объект SecurityNPC с экраном, путем к изображению, позицией, дверью, спаунером врагов и инвентарем.
        - activate_enemies(self): Активирует врагов и разблокирует дверь.
        - update_enemies(self, character_position): Обновляет состояние врагов и проверяет столкновения с персонажем.
        - draw_enemies(self): Отрисовывает врагов на экране.
        - unlock_door(self): Разблокирует дверь после выполнения условий.
    '''
    def __init__(self, screen, image_path, position, door, enemy_spawner, inventory):
        dialogue_data = {
            "start": ("Привет, первокур! Что тебе нужно?",
                      (["Спросить как пройти к аудитории.", "Сказать 'Пошёл ты'."],
                       [lambda: self.dialogue.display_conversation("quest"), lambda: self.dialogue.display_conversation("goodbye")])),
            "quest": ("Пройди через зал и победи всех нарушителей, затем я открою дверь.",
                      (["Принять вызов.", "Отказаться."],
                       [lambda: self.accept_challenge(), lambda: self.dialogue.display_conversation("decline")])),
            "goodbye": ("Чао какао.", ([], [])),
            "accept": ("Удачи в битве!", ([], [])),
            "decline": ("Ну и ладно, сторонись от меня.", ([], []))
        }
        super().__init__(screen, image_path, position, dialogue_data, door)
        self.door = door
        self.enemies_active = False
        self.enemy_spawner = enemy_spawner
        self.inventory = inventory

    def accept_challenge(self):
        self.dialogue.display_conversation("accept")
        # Здесь мы вызываем функцию активации после завершения диалога
        self.activate_enemies()

    def activate_enemies(self):
        print("Activating enemies...")
        self.enemies_active = True
        self.enemy_spawner.spawn_enemies()
        self.unlock_door()

    def update_enemies(self, character_position):
        if self.enemies_active:
            self.enemy_spawner.update_enemies(character_position)
            damage = self.enemy_spawner.check_collisions(character_position, 50)
            if damage:
                self.inventory.reduce_health(damage)

    def draw_enemies(self):
        if self.enemies_active:
            self.enemy_spawner.draw_enemies()

    def unlock_door(self):
        if self.door:
            self.door.unlock()
            print("Door unlocked!")

class VarvaraNPC(NPC):
    '''
        Класс VarvaraNPC наследует NPC для создания персонажа Варвары с викториной в игре.
        Включает методы для проведения викторины, проверки ответов и отображения результатов.
        - __init__(self, screen, image_path, position, door, enemy_spawner, inventory): Инициализирует объект VarvaraNPC с экраном, путем к изображению, позицией, дверью, спаунером врагов и инвентарем.
        - hand_over_schedule(self): Выдает расписание и начинает викторину.
        - ask_next_question(self): Задает следующий вопрос викторины.
        - display_question(self, question, options, correct_index): Отображает текущий вопрос викторины и варианты ответов.
        - get_player_response(self, correct_index): Получает ответ игрока и проверяет его правильность.
        - show_quiz_results(self): Отображает результаты викторины и завершает диалог.
        - disappear(self): Убирает Варвару с экрана после завершения диалога.
        - unlock_door(self): Разблокирует дверь после завершения викторины.
    '''
    def __init__(self, screen, image_path, position, door, enemy_spawner, inventory):
        self.quiz_questions = [
            ("Как в Python выводится число на экран?", ["print(число)", "echo(число)", "display(число)", "show(число)"], 0),
            ("Как создается экземпляр класса?", ["Класс()", "new Класс()", "class Класс()", "Класс.new()"], 2),
            ("Какой метод для добавления элемента в список?", ["append()", "add()", "push()", "append()"], 3),
            ("Какой метод вызывается при создании объекта класса?", ["__init__()", "__new__()", "__start__()", "__create__()"], 0),
            ("Какая функция измеряет длину списка?", ["lena()", "count()", "length()", "len()"], 0),
            ("Чем класс отличается от объекта?",
             ["Класс - это шаблон для создания объектов", "Это одно и то же",
              "Объект это когда =, а класс когда class name():",
              "Объект - это вообще-то функция, ну типа..."], 0),

            ("Что такое инкапсуляция в ООП?",
             ["Скрытие внутренних деталей реализации класса", "Это не относится к ООП, это лекарство",
              "Это когда код типа в капсуле", "Я не знаю, help"], 0),

            ("Что такое наследование в ООП?",
             ["Классы могут наследовать свойства и методы других классов",
              "Ну когда один и другой типа похожи",
              "Когда объекты наследуют свойства классов", "Это очень интересная парадигма, которая ставит вопрос о правильной сущности бытия..."], 0),

            ("Что такое полиморфизм в ООП?",
             ["Полиморфизм позволяет использовать разные реализации.", "Это когда много форм",
              "Это вид магии?", "Когда код мутирует"], 0),

            ("Что такое абстракция в ООП?",
             ["Сокрытие сложности, оставляя только релевантные детали", "Абстракция это когда очень абстрактно всё",
              "Это когда всё зависит от контекста", "Ну это как искусство, каждый видит что хочет"], 0),

            ("Как в Python создать анонимную функцию?",
             ["lambda x: x * x", "def функция: создаём нечто анонимное", "function(x): x * x",
              "func x: x * x"], 0),


        ]
        self.current_question_index = 0
        self.total_questions = len(self.quiz_questions)

        dialogue_data = {
            "start": ("Поздравляю с поступлением на ИУ-10. Тебя ждёт тяжелое испытание длиной в 6 курсов.",
                      (["Я готов к этому.", "Да ну, опять учиться…"],
                       [lambda: self.dialogue.display_conversation("ready"), lambda: self.dialogue.display_conversation("reluctant")])),
            "ready": ("Молодец! Вот твоё расписание, иди и покоряй вершины знаний! Но перед этим ответь на вопросы.",
                      ([], [lambda: self.hand_over_schedule()])),
            "reluctant": ("Ты справишься! Вот твоё расписание, не забудь про первую пару в 501ю. Но перед этим ответь на прочку вопросов.",
                          ([], [lambda: self.hand_over_schedule()])),
            "hand_over_schedule": ("(в мыслях) 1 парой опставили... 501ю 501ю 501ю 501ю 501ю кабинет...",
                                   ([], []))
        }
        super().__init__(screen, image_path, position, dialogue_data, door)
        self.door = door
        self.enemies_active = False
        self.enemy_spawner = enemy_spawner
        self.inventory = inventory
        self.quiz_answers = []

    def hand_over_schedule(self):
        print("(вслух) А где это?")
        print("(в мыслях) Похоже, придётся искать самому.")
        self.door.unlock()
        self.ask_next_question()

    def ask_next_question(self):
        if self.current_question_index < self.total_questions:
            question, options, correct_index = self.quiz_questions[self.current_question_index]
            self.display_question(question, options, correct_index)
        else:
            self.show_quiz_results()

    def display_question(self, question, options, correct_index):
        print(question)
        for idx, option in enumerate(options):
            print(f"{idx + 1}. {option}")
        self.get_player_response(correct_index)

    def get_player_response(self, correct_index):
        try:
            choice = int(input("Выбери ответ (напиши цифру/число): ")) - 1
            is_correct = choice == correct_index
            self.quiz_answers.append(is_correct)
            self.current_question_index += 1
            self.ask_next_question()
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")
            self.display_question(*self.quiz_questions[self.current_question_index])

    def show_quiz_results(self):
        correct_answers = sum(self.quiz_answers)
        print(f"Вот и все вопросы. Ты ответил правильно на {correct_answers} из {self.total_questions}.")
        self.disappear()

    def disappear(self):
        print("Варвара Александровна ушла за синюю дверь.")
        self.visible = False

    def unlock_door(self):
        if self.door:
            self.door.unlock()
            print("Проход в новую локацию открыт!")

class GopnikNPC(NPC):
    '''
        Класс GopnikNPC наследует NPC для создания гопников в игре.
        Включает методы для начала боя, активации волн врагов и обновления состояния врагов.
        - __init__(self, screen, image_path, position, door, enemy_spawner, inventory): Инициализирует объект GopnikNPC с экраном, путем к изображению, позицией, дверью, спаунером врагов и инвентарем.
        - start_fight(self): Начинает бой с первой волной гопников.
        - activate_next_wave(self): Активирует следующую волну гопников.
        - update_enemies(self, character_position): Обновляет состояние врагов и активирует следующую волну при необходимости.
        - draw_enemies(self): Отрисовывает врагов на экране.
        - unlock_door(self): Разблокирует дверь после окончания всех волн.
    '''
    def __init__(self, screen, image_path, position, door, enemy_spawner, inventory):
        dialogue_data = {
            "start": ("Студент гопник - деньги на булку!?",
                      (["Да, да, конечно.", "Обойдёшься."],
                       [lambda: self.dialogue.display_conversation("money"), lambda: self.dialogue.display_conversation("fight")])),
            "money": ("Откуда у студента деньги?",
                      ([], [lambda: self.start_fight()])),
            "fight": ("Сейчас увидишь, что значит настоящий гопник!",
                      ([], [lambda: self.start_fight()]))
        }
        super().__init__(screen, image_path, position, dialogue_data, door)
        self.door = door
        self.enemies_active = False
        self.enemy_spawner = enemy_spawner
        self.inventory = inventory
        self.current_wave = 0
        self.total_waves = 5

    def start_fight(self):
        """Начать бой с первой волной гопников и активировать бой"""
        print("Готовься к драке с гопниками...")
        self.enemies_active = True
        self.current_wave = 1
        self.enemy_spawner.spawn_enemies()  # Первая волна
        self.unlock_door()

    def activate_next_wave(self):
        """Активировать следующую волну гопников, если не превышен лимит"""
        if self.current_wave < self.total_waves:
            self.current_wave += 1
            print(f"Волна {self.current_wave} гопников приближается...")
            self.enemy_spawner.spawn_enemies()
        else:
            print("Все волны гопников побеждены.")
            self.enemies_active = False

    def update_enemies(self, character_position):
        """Обновить состояние врагов и активировать следующую волну, если предыдущая волна побеждена"""
        if self.enemies_active:
            self.enemy_spawner.update_enemies(character_position)
            damage = self.enemy_spawner.check_collisions(character_position, 50)
            if damage:
                self.inventory.reduce_health(damage)

            if not self.enemy_spawner.enemies and self.enemies_active:
                # Активировать следующую волну гопников, если все текущие побеждены
                self.activate_next_wave()

    def draw_enemies(self):
        """Отрисовать врагов на экране"""
        if self.enemies_active:
            self.enemy_spawner.draw_enemies()

    def unlock_door(self):
        """Открыть дверь после окончания всех волн"""
        if self.current_wave == self.total_waves and self.door:
            self.door.unlock()
            print("Door unlocked!")

class KANPC(NPC):
    '''
        Класс KANPC наследует NPC для создания персонажа КА в игре.
        Включает методы для активации врагов и обновления состояния врагов.
        - __init__(...): Инициализирует объект KANPC с экраном, путем к изображению, позицией, дверью, спаунером врагов и инвентарем.
        - activate_enemies(self): Активирует врагов и разблокирует дверь.
        - update_enemies(self, character_position): Обновляет состояние врагов и проверяет столкновения с персонажем.
        - draw_enemies(self): Отрисовывает врагов на экране.
        - unlock_door(self): Разблокирует дверь после выполнения условий.
    '''
    def __init__(self, screen, image_path, position, door, enemy_spawner, inventory):
        dialogue_data = {
            "start": ("Студент - вот мы и встретились! Где ты был на первой лабе? Надеюсь ты её сделал?",
                      (["Лабу? Какую лабу?", "Сделал"],
                       [lambda: self.dialogue.display_conversation("truth"),
                        lambda: self.dialogue.display_conversation("lie")])),
            "truth": ("Ты у нас кто?",
                      (["Уася Орешин"],
                       [lambda: self.dialogue.display_conversation("gorin")])),
            "gorin": ("Ясно. *Смотрит почту*. Я ничего не вижу, у меня на почте два отчета с вашей группы.",
                      ([], [lambda: self.unlock_door()])),
            "lie": ("Что-то я не вижу отчёта у себя на электронной почте.  Если сможешь противостоять этим гопникам, так уж и быть поставлю 5.",
                    (["Отчёты для слабых"],
                     [lambda: self.dialogue.display_conversation("no_report")])),
            "no_report": ("Ты скажи ещё, что не сделал блок схему?",
                          (["Нет, но я могу предложить вам сделать подокон..."],
                           [lambda: self.dialogue.display_conversation("no_block_scheme")])),
            "no_block_scheme": ("Задайте жару этому строителю!",
                                ([], [lambda: self.activate_enemies()])),
        }
        super().__init__(screen, image_path, position, dialogue_data, door)
        self.door = door
        self.enemies_active = False
        self.enemy_spawner = enemy_spawner
        self.inventory = inventory

    def activate_enemies(self):
        print("Activating enemies...")
        self.enemies_active = True
        self.enemy_spawner.spawn_enemies()
        self.unlock_door()

    def update_enemies(self, character_position):
        if self.enemies_active:
            self.enemy_spawner.update_enemies(character_position)
            damage = self.enemy_spawner.check_collisions(character_position, 50)
            if damage:
                self.inventory.reduce_health(damage)
            if not self.enemy_spawner.enemies:
                self.enemies_active = False
                print("Не думал, что ты справишься! Заслуженный автомат!")

    def draw_enemies(self):
        if self.enemies_active:
            self.enemy_spawner.draw_enemies()

    def unlock_door(self):
        if self.door:
            self.door.unlock()
            print("Door unlocked!")

class ExitDoor(Door):
    '''
        Класс ExitDoor наследует Door для создания двери выхода в игре.
        Включает метод для взаимодействия с дверью.
        - interact(self, character_rect, current_scene):Взаимодействует с дверью, проверяет возможность перехода между сценами.
    '''
    def interact(self, character_rect, current_scene):
        return super().interact(character_rect, current_scene)

class SecurityDoor(Door):
    def interact(self, character_rect, current_scene):
        return super().interact(character_rect, current_scene)

class StairDoor(Door):
    def interact(self, character_rect, current_scene):
        return super().interact(character_rect, current_scene)

walls = [
    Wall(-10, 0, 800, -1), #левая
    Wall(-1, 1, -1, 600), #верхняя
    Wall(800, -1, 800, 600), #правая
    Wall(-1, 600, 800, -2), #нижняя
    Wall(50,0, 800,120)
]