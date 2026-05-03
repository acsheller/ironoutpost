import pygame
import random
from dataclasses import dataclass

pygame.init()

TILE_SIZE = 32
GRID_WIDTH = 25
GRID_HEIGHT = 18

SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE + 80

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("IronOutpost - RTS Survival Starter")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)


@dataclass
class Unit:
    x: int
    y: int
    kind: str
    hp: int = 10


resources = []
workers = []
enemies = []

base = Unit(GRID_WIDTH // 2, GRID_HEIGHT // 2, "base", hp=100)

wood = 0
wave_timer = 0


def spawn_resources():
    for _ in range(25):
        resources.append(
            Unit(
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
                "tree",
            )
        )


def spawn_worker():
    workers.append(Unit(base.x + random.choice([-1, 1]), base.y, "worker"))


def spawn_enemy_wave():
    for _ in range(4):
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            enemies.append(Unit(random.randint(0, GRID_WIDTH - 1), 0, "enemy"))
        elif side == "bottom":
            enemies.append(Unit(random.randint(0, GRID_WIDTH - 1), GRID_HEIGHT - 1, "enemy"))
        elif side == "left":
            enemies.append(Unit(0, random.randint(0, GRID_HEIGHT - 1), "enemy"))
        else:
            enemies.append(Unit(GRID_WIDTH - 1, random.randint(0, GRID_HEIGHT - 1), "enemy"))


def move_toward(unit, target_x, target_y):
    if unit.x < target_x:
        unit.x += 1
    elif unit.x > target_x:
        unit.x -= 1

    if unit.y < target_y:
        unit.y += 1
    elif unit.y > target_y:
        unit.y -= 1


def update_workers():
    global wood

    for worker in workers:
        if not resources:
            return

        nearest = min(
            resources,
            key=lambda r: abs(worker.x - r.x) + abs(worker.y - r.y),
        )

        if worker.x == nearest.x and worker.y == nearest.y:
            resources.remove(nearest)
            wood += 1
        else:
            move_toward(worker, nearest.x, nearest.y)


def update_enemies():
    global running

    for enemy in enemies[:]:
        if enemy.x == base.x and enemy.y == base.y:
            base.hp -= 5
            enemies.remove(enemy)

            if base.hp <= 0:
                running = False
        else:
            move_toward(enemy, base.x, base.y)


def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (35, 35, 35), rect, 1)


def draw_unit(unit):
    colors = {
        "base": (80, 160, 255),
        "worker": (255, 220, 80),
        "tree": (80, 200, 100),
        "enemy": (220, 60, 60),
    }

    color = colors[unit.kind]
    rect = pygame.Rect(
        unit.x * TILE_SIZE + 4,
        unit.y * TILE_SIZE + 4,
        TILE_SIZE - 8,
        TILE_SIZE - 8,
    )
    pygame.draw.rect(screen, color, rect)


def draw_ui():
    panel_y = GRID_HEIGHT * TILE_SIZE
    pygame.draw.rect(screen, (20, 20, 20), (0, panel_y, SCREEN_WIDTH, 80))

    text = font.render(
        f"Wood: {wood}   Workers: {len(workers)}   Enemies: {len(enemies)}   Base HP: {base.hp}",
        True,
        (240, 240, 240),
    )
    screen.blit(text, (20, panel_y + 15))

    help_text = font.render(
        "Press W = build worker (cost 5 wood) | SPACE = spawn wave | ESC = quit",
        True,
        (180, 180, 180),
    )
    screen.blit(help_text, (20, panel_y + 45))


spawn_resources()
spawn_worker()

running = True

while running:
    screen.fill((10, 10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                spawn_enemy_wave()

            if event.key == pygame.K_w:
                if wood >= 5:
                    wood -= 5
                    spawn_worker()

    wave_timer += 1
    if wave_timer > 600:
        spawn_enemy_wave()
        wave_timer = 0

    update_workers()
    update_enemies()

    draw_grid()

    for resource in resources:
        draw_unit(resource)

    draw_unit(base)

    for worker in workers:
        draw_unit(worker)

    for enemy in enemies:
        draw_unit(enemy)

    draw_ui()

    pygame.display.flip()
    clock.tick(8)

pygame.quit()

print("Game over!")