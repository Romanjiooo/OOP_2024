import pygame
import sys
import random
import win32gui
import win32con

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128,128,128)

class BaseMenu:
    def __init__(self, screen, options):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.options = options
        self.selected_index = 0

    def draw(self):
        for index, option in enumerate(self.options):
            color = GREEN if index == self.selected_index else RED
            label = self.font.render(option, True, color)
            x = SCREEN_WIDTH // 2 - label.get_width() // 2
            y = SCREEN_HEIGHT // 2 - label.get_height() // 2 + 50 * index
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
    def __init__(self, screen, background_image_path):
        super().__init__(screen, ["Start Game", "Quit"])
        # Загрузка и масштабирование фонового изображения
        self.background_image = pygame.image.load(background_image_path)

    def draw(self):
        # Отрисовка фонового изображения вместо заливки цветом
        self.screen.blit(self.background_image, (0, 0))
        super().draw()

    def update(self, event):
        result = super().update(event)
        if result == "Start Game":
            return "start"
        elif result == "Quit":
            pygame.quit()
            sys.exit()
        return None

class EscMenu(BaseMenu):
    def __init__(self, screen, game):
        super().__init__(screen, ["Quit", "Cancel"])
        self.game = game
        self.active = False

    def draw(self):
        if self.active:
            self.screen.fill((0, 0, 0, 128))  # Полупрозрачный фон
            super().draw()

    def update(self, event):
        if self.active:
            result = super().update(event)
            if result == "Quit":
                pygame.quit()
                sys.exit()
            elif result == "Cancel":
                self.active = False
                return "cancel"
        return None

    def activate(self):
        self.active = True

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.character = Character(screen, "character_image.png", [50, 450])
        self.background = pygame.transform.scale(pygame.image.load("auditorium_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_scene = "initial_scene"
        self.damage_boost = 0

    def update_scene(self, new_scene):
        if new_scene != self.current_scene:
            self.current_scene = new_scene
            self.damage_boost += 10

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
        self._position = [x, y]
        self._rect.topleft = self._position

    def get_position(self):
        return self._position



class Health:
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
            base_damage = 50
            total_damage = base_damage + self.game.damage_boost
            enemy.health -= total_damage
            print(f"Attacked {enemy.name} for {total_damage} damage!")
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                print(f"{enemy.name} defeated!")


class EnemySpawner:
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
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, GREY, self.rect)

    def check_collision(self, character_rect):
        return self.rect.colliderect(character_rect)


class Auditorium:
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
    def __init__(self, screen, image_path, position, door, enemy_spawner, inventory):
        dialogue_data = {
            "start": ("Привет, первокур! Что тебе нужно?",
                      (["Cпросить как пройти к аудитории.", "Сказать 'Пошёл ты'."],
                       [lambda: self.dialogue.display_conversation("quest"), lambda: self.dialogue.display_conversation("goodbye")])),
            "quest": ("Пройди через зал и победи всех нарушителей, затем я открою дверь.",
                      (["Принять вызов.", "Отказаться."],
                       [lambda: self.dialogue.display_conversation("accept"), lambda: self.dialogue.display_conversation("decline")])),
            "goodbye": ("Чао какао.", ([], [])),
            "accept": ("Удачи в битве!", ([], [lambda: self.activate_enemies()])),
            "decline": ("Ну и ладно, сторонись от меня.", ([], []))
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

    def draw_enemies(self):
        if self.enemies_active:
            self.enemy_spawner.draw_enemies()

    def unlock_door(self):
        if self.door:
            self.door.unlock()
            print("Door unlocked!")

class VarvaraNPC(NPC):
    def __init__(self, screen, image_path, position, door, enemy_spawner, inventory):
        self.quiz_questions = [
            ("Как в Python выводится число на экран?", ["print(число)", "echo(число)", "display(число)", "show(число)"], 0),
            ("Как создается экземпляр класса?", ["Класс()", "new Класс()", "class Класс()", "Класс.new()"], 0),
            ("Какой метод для добавления элемента в список?", ["append()", "add()", "push()", "put()"], 0),
            ("Какой метод вызывается при создании объекта класса?", ["__init__()", "__new__()", "__start__()", "__create__()"], 0),
            ("Какая функция измеряет длину списка?", ["len()", "count()", "length()", "size()"], 0),
            ("Чем класс отличается от объекта?",
             ["Класс - это шаблон для создания объектов", "Объект - это просто для красоты",
              "Класс это когда очень нужно, а объект это когда очень хочется",
              "Объект - это вообще-то функция, ну типа..."], 0),

            ("Что такое инкапсуляция в ООП?",
             ["Скрытие внутренних деталей реализации класса", "Инкапсуляция? Это когда в капсулу запихиваем",
              "Тайный клуб, куда не все могут зайти", "Это когда все в одном флаконе, как шампунь 2 в 1"], 0),

            ("Что такое наследование в ООП?",
             ["Классы могут наследовать свойства и методы других классов",
              "Наследование? Это когда дедушка оставил тебе в наследство класс",
              "Это когда ты похож на маму или папу, но в коде", "Когда твой код богат и знатен"], 0),

            ("Что такое полиморфизм в ООП?",
             ["Объекты могут принимать множество форм", "Полиморфизм - это когда ты одновременно и кофе, и чай",
              "Это вид магии, не так ли?", "Когда код мутирует и начинает жить своей жизнью"], 0),

            ("Что такое абстракция в ООП?",
             ["Сокрытие сложности, оставляя только релевантные детали", "Абстракция это когда очень абстрактно всё",
              "Это когда всё зависит от контекста", "Ну это как искусство, каждый видит что хочет"], 0),

            ("Как в Python создать анонимную функцию?",
             ["lambda x: x * x", "def функция: создаём нечто анонимное", "function(x): x * x, секретное агентство",
              "func x: x * x, шпионские страсти"], 0),

            ("Что такое декоратор в Python?",
             ["Функция, которая модифицирует другую функцию", "Способ стилизации кода, как в доме твоей бабушки",
              "Инструмент для написания декларативного Python кода, очень секретный",
              "Модуль Python, который наводит ужас на другие модули"], 0),

            ("Какая функция в Python проверяет принадлежность элемента к списку?",
             ["x in list", "x belongs to list, почти как в клубе", "list.contains(x), список знает всё",
              "find(x in list), ищем пока не найдем"], 0),

            ("Как в Python проверить, является ли число четным?",
             ["x % 2 == 0", "x делится на 2 без остатка, как пирог на дне рождения", "even(x), спроси у Python",
              "x // 2, деление как искусство"], 0),

            ("Какой метод в Python используется для вывода данных на экран?",
             ["print()", "show()", "display()", "echo(), это не только в горах"], 0)
        ]
        self.current_question_index = 0
        self.total_questions = len(self.quiz_questions)

        dialogue_data = {
            "start": ("Поздравляю с поступлением на ИУ-10. Тебя ждёт тяжелое испытание длиной в 6 курсов.",
                      (["Я готов к этому.", "Да ну, опять учиться…"],
                       [lambda: self.dialogue.display_conversation("ready"), lambda: self.dialogue.display_conversation("reluctant")])),
            "ready": ("Молодец! Вот твоё расписание, иди и покоряй вершины знаний!",
                      ([], [lambda: self.hand_over_schedule()])),
            "reluctant": ("Ты справишься! Вот твоё расписание, не забудь про первую пару в 503.",
                          ([], [lambda: self.hand_over_schedule()])),
            "hand_over_schedule": ("(в мыслях) 1 пара ЯП, 503 кабинет...",
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
    def __init__(self, screen, image_path, position, door, enemy_spawner, inventory):
        dialogue_data = {
            "start": ("Привет, первокур! Что тебе нужно?",
                      (["Cпросить как пройти к аудитории.", "Сказать 'Пошёл ты'."],
                       [lambda: self.dialogue.display_conversation("quest"),
                        lambda: self.dialogue.display_conversation("goodbye")])),
            "quest": ("Пройди через зал и победи всех нарушителей, затем я открою дверь.",
                      (["Принять вызов.", "Отказаться."],
                       [lambda: self.dialogue.display_conversation("accept"),
                        lambda: self.dialogue.display_conversation("decline")])),
            "goodbye": ("Чао какао.", ([], [])),
            "accept": ("Удачи в битве!", ([], [lambda: self.activate_enemies()])),
            "decline": ("Ну и ладно, сторонись от меня.", ([], []))
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

    def draw_enemies(self):
        if self.enemies_active:
            self.enemy_spawner.draw_enemies()

    def unlock_door(self):
        if self.door:
            self.door.unlock()
            print("Door unlocked!")

class ExitDoor(Door):
    def interact(self, character_rect, current_scene):
        return super().interact(character_rect, current_scene)

class SecurityDoor(Door):
    def interact(self, character_rect, current_scene):
        return super().interact(character_rect, current_scene)

class StairDoor(Door):
    def interact(self, character_rect, current_scene):
        return super().interact(character_rect, current_scene)

walls_security = [
    Wall(-10, 0, 800, -1),  # левая
    Wall(-1, 1, -1, 600),  # верхняя
    Wall(800, -1, 800, 600),  # правая
    Wall(-1, 600, 800, -2),  # нижняя
    Wall(50, 0, 800, 120)
]

walls_faculty = [
    Wall(-10, 0, 800, -1),
    Wall(-1, 1, -1, 600),
    Wall(800, -1, 800, 600),
]

walls = [
    Wall(-10, 0, 800, -1), #левая
    Wall(-1, 1, -1, 600), #верхняя
    Wall(800, -1, 800, 600), #правая
    Wall(-1, 600, 800, -2), #нижняя
    Wall(50,0, 800,120)
]

