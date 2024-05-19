from classes import *
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

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 600, 250, 800, 600, 0)

menu = Menu(screen, "start.png")
game = Game(screen)
esc_menu = EscMenu(screen, game)
inventory = Health(screen)
current_scene = "menu"
previous_scene = None

enemy_spawner = EnemySpawner(screen, "enemy_icon.png", 5)
character = Character(screen, "character_image.png", [50,50])

combat_system = Combat(character, enemy_spawner.enemies, game)
enemies = enemy_spawner.enemies

DoorGameToFaculty = SecurityDoor(screen, "SecurityDoor.png", (450, 100), "game", "faculty")
DoorFacultytoStair = StairDoor(screen, "DoorFacultytoStair.png", (100, 280), "faculty", "stair")
DoorStairtoIU = StairDoor(screen, "exit.png", (700, 400), "stair", "iu404")
DoorIUtoFinal = StairDoor(screen, "door_image.png", (600, 350), "iu404", "final")

doors = [
DoorGameToFaculty,
DoorFacultytoStair,
DoorStairtoIU,
DoorIUtoFinal
]

Security = SecurityNPC(screen, "security.png", (400, 150), DoorGameToFaculty, enemy_spawner, inventory)
Varvara = VarvaraNPC(screen, "varvara.png", (200, 450), DoorFacultytoStair, enemy_spawner, inventory)
Gopnik = GopnikNPC(screen, "enemy_icon.png", (250, 250), DoorStairtoIU, enemy_spawner, inventory)
KA = KANPC(screen, "KA.png", (250, 300), DoorIUtoFinal, enemy_spawner, inventory)

npcs = [
    Security,
    Varvara,
    Gopnik,
    KA
]

class SecurityLocation(Auditorium):
    def __init__(self, screen, background_image_path, npcs, doors, walls, enemies, inventory):
        super().__init__(screen, background_image_path, npcs, doors, walls, enemies)
        self.inventory = inventory

    def update(self, event):
        super().update(event)
        for enemy in self.enemies:
            enemy.update(game.character.get_position())

            if enemy.check_collision(game.character.get_position(), 50):
                self.inventory.reduce_health(5)

    def draw(self):
        super().draw()
        self.inventory.draw()
        game.character.draw()

class FacultyLocation(Auditorium):
    def __init__(self, screen, background_image_path, npcs, doors, walls, enemies, inventory):
        super().__init__(screen, background_image_path, npcs, doors, walls, enemies)
        self.inventory = inventory

    def update(self, event):
        super().update(event)
        for enemy in self.enemies:
            enemy.update(game.character.get_position())

            if enemy.check_collision(game.character.get_position(), 50):
                self.inventory.reduce_health(5)

    def draw(self):
        super().draw()
        self.inventory.draw()
        game.character.draw()

class stairLocation(Auditorium):
    def __init__(self, screen, background_image_path, npcs, doors, walls, enemies, inventory):
        super().__init__(screen, background_image_path, npcs, doors, walls, enemies)
        self.inventory = inventory

    def update(self, event):
        super().update(event)
        for enemy in self.enemies:
            enemy.update(game.character.get_position())

            if enemy.check_collision(game.character.get_position(), 50):
                self.inventory.reduce_health(5)

    def draw(self):
        super().draw()
        self.inventory.draw()
        game.character.draw()

class iuLocation(Auditorium):
    def __init__(self, screen, background_image_path, npcs, doors, walls, enemies, inventory):
        super().__init__(screen, background_image_path, npcs, doors, walls, enemies)
        self.inventory = inventory

    def update(self, event):
        super().update(event)
        for enemy in self.enemies:
            enemy.update(game.character.get_position())

            if enemy.check_collision(game.character.get_position(), 50):
                self.inventory.reduce_health(5)

    def draw(self):
        super().draw()
        self.inventory.draw()
        game.character.draw()

class finalLocation(Auditorium):
    def __init__(self, screen, background_image_path, npcs, doors, walls, enemies, inventory):
        super().__init__(screen, background_image_path, npcs, doors, walls, enemies)
        self.inventory = inventory

    def update(self, event):
        super().update(event)
        for enemy in self.enemies:
            enemy.update(game.character.get_position())

            if enemy.check_collision(game.character.get_position(), 50):
                self.inventory.reduce_health(5)

    def draw(self):
        super().draw()
        self.inventory.draw()
        game.character.draw()

security_location = SecurityLocation(screen, "auditorium_background.png", [Security], [DoorGameToFaculty], walls[:4], enemies, inventory)
faculty_location = FacultyLocation(screen, "faculty.webp", [Varvara], [DoorFacultytoStair,DoorStairtoIU], walls[:3], enemies, inventory)
stair = stairLocation(screen, "stair.webp", [Gopnik], [DoorStairtoIU], walls[:3], enemies, inventory)
IU = iuLocation(screen, "iu404.png", [KA], [DoorIUtoFinal], walls[:3], enemies, inventory)
final = finalLocation(screen, "Final.png", [KA], [DoorIUtoFinal], walls[:3], enemies, inventory)

auditoriums = {
    "game": security_location,
    "faculty": faculty_location,
    "stair": stair,
    "iu404": IU,
    "final": final
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_scene == "menu":
            result = menu.update(event)
            if result == "start":
                game = Game(screen)
                enemy_spawner.reset_spawn()
                current_scene = "game"
            elif result == "quit":
                pygame.quit()
                sys.exit()

        elif current_scene == "esc":
            result = esc_menu.update(event)
            if result == "cancel":
                current_scene = previous_scene
            elif result is None:
                continue

        elif game:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    previous_scene = current_scene
                    esc_menu.activate()
                    current_scene = "esc"
                if event.key == pygame.K_SPACE:
                    for npc in npcs:
                        if npc.rect.collidepoint(game.character._position):
                            npc.interact()
                if event.key == pygame.K_a:
                    if enemy_spawner.enemies:
                        combat_system.attack_closest_enemy()
                for door in doors:
                    if door.rect.colliderect(game.character._rect):
                        new_scene = door.interact(game.character._rect, current_scene)
                        if new_scene:
                            current_scene = new_scene
                            print(f"Переход в сцену {current_scene}")
                        else:
                            print("Дверь не может быть использована с этой локации или она закрыта.")

    if current_scene == "game" and game:
        auditoriums[current_scene].draw()
        game.update()

        if Security.enemies_active:
            Security.update_enemies(game.character.get_position())

    elif current_scene == "faculty":
        enemy_spawner.reset_spawn()
        auditoriums[current_scene].draw()
        game.update()

    elif current_scene == "stair":
        enemy_spawner.reset_spawn()
        auditoriums[current_scene].draw()
        game.update()
        Gopnik.update_enemies(game.character.get_position())
        Gopnik.draw_enemies()

    elif current_scene == "iu404":
        enemy_spawner.reset_spawn()
        auditoriums[current_scene].draw()
        game.update()

        if KA.enemies_active:
            KA.update_enemies(game.character.get_position())
    elif current_scene == "final":
        auditoriums[current_scene].draw()


    screen.fill(WHITE)

    if current_scene == "menu":
        menu.draw()

    elif current_scene == "game" and game:
        auditoriums[current_scene].draw()
        game.update()

    elif current_scene == "faculty" or current_scene == "stair":
        auditoriums[current_scene].draw()
        game.update()
    elif current_scene == "iu404":
        auditoriums[current_scene].draw()
        game.update()
    elif current_scene == "final":
        auditoriums[current_scene].draw()
        game.update()

    elif current_scene == "esc" :
        esc_menu.draw()

    pygame.display.flip()
    clock.tick(FPS)