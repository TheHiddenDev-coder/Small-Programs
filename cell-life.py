import pygame
import numpy as np
import math
import sys
import random

# =========================
# CONFIG
# =========================

USE_GPU = False   # <- set True if you have CuPy + CUDA

NUM_RED = 200
NUM_GREEN = 200
NUM_BLUE = 200
NUM_WHITE = 100

WIDTH, HEIGHT = 800, 800
FPS = 60

CELL_RADIUS = 3
MAX_R = 70.0
MAX_R2 = MAX_R * MAX_R

MAX_FORCE = 80.0
MAX_SPEED = 160.0
DAMPING = 0.996
SOFTENING = 0.5

ATTRACT = 50.0
REPEL = 100.0

GRID = int(MAX_R)
GW = WIDTH // GRID + 1
GH = HEIGHT // GRID + 1

# =========================
# NUMPY / CUPY SWITCH
# =========================

if USE_GPU:
    import cupy as xp
else:
    xp = np

# =========================
# TYPES / COLORS
# =========================

RED, GREEN, BLUE, WHITE = 0, 1, 2, 3

COLORS = np.array([
    (220, 50, 47),
    (38, 166, 91),
    (36, 123, 160),
    (240, 240, 240)
], dtype=np.uint8)

# =========================
# RULES
# =========================

SIGN = xp.ones((4, 4), dtype=xp.float32)

SIGN[RED, RED] = SIGN[RED, BLUE] = -1
SIGN[GREEN, GREEN] = SIGN[GREEN, RED] = -1
SIGN[BLUE, BLUE] = SIGN[BLUE, GREEN] = -1
SIGN[WHITE, :] = -1

STRENGTH = xp.where(SIGN < 0, REPEL, ATTRACT)

# =========================
# SIMULATION
# =========================


class Sim:
    def __init__(self):
        self.reset()

    def reset(self):
        types = (
            [RED]*NUM_RED +
            [GREEN]*NUM_GREEN +
            [BLUE]*NUM_BLUE +
            [WHITE]*NUM_WHITE
        )
        self.n = len(types)

        self.t = xp.array(types, dtype=xp.int32)

        self.x = xp.random.rand(self.n) * WIDTH
        self.y = xp.random.rand(self.n) * HEIGHT

        angles = xp.random.rand(self.n) * math.tau
        speeds = xp.random.rand(self.n) * 20

        self.vx = xp.cos(angles) * speeds
        self.vy = xp.sin(angles) * speeds

        self.grid = [[] for _ in range(GW * GH)]

    def step(self, dt):
        # clear grid
        for g in self.grid:
            g.clear()

        # insert particles
        gx = (self.x // GRID).astype(int) % GW
        gy = (self.y // GRID).astype(int) % GH
        for i in range(self.n):
            self.grid[gx[i] + gy[i] * GW].append(i)

        hw, hh = WIDTH * 0.5, HEIGHT * 0.5

        for cell in self.grid:
            if len(cell) < 2:
                continue

            idx = xp.array(cell)
            xi = self.x[idx][:, None]
            yi = self.y[idx][:, None]

            dx = xi - xi.T
            dy = yi - yi.T

            dx = xp.where(dx > hw, dx - WIDTH, dx)
            dx = xp.where(dx < -hw, dx + WIDTH, dx)
            dy = xp.where(dy > hh, dy - HEIGHT, dy)
            dy = xp.where(dy < -hh, dy + HEIGHT, dy)

            d2 = dx*dx + dy*dy
            mask = (d2 > 0) & (d2 < MAX_R2)

            if not mask.any():
                continue

            ti = self.t[idx][:, None]
            tj = self.t[idx][None, :]

            sign = SIGN[ti, tj]
            strength = STRENGTH[ti, tj]

            inv_d = 1.0 / (xp.sqrt(d2) + SOFTENING)
            fall = 1.0 - d2 / MAX_R2

            mag = sign * strength * fall * inv_d
            mag = xp.clip(mag, -MAX_FORCE, MAX_FORCE)
            mag *= mask

            fx = xp.sum(dx * mag, axis=1)
            fy = xp.sum(dy * mag, axis=1)

            self.vx[idx] = (self.vx[idx] + fx * dt) * DAMPING
            self.vy[idx] = (self.vy[idx] + fy * dt) * DAMPING

        speed2 = self.vx*self.vx + self.vy*self.vy
        over = speed2 > MAX_SPEED*MAX_SPEED
        scale = MAX_SPEED / xp.sqrt(speed2 + 1e-9)
        self.vx = xp.where(over, self.vx * scale, self.vx)
        self.vy = xp.where(over, self.vy * scale, self.vy)

        self.x = (self.x + self.vx * dt) % WIDTH
        self.y = (self.y + self.vy * dt) % HEIGHT

    def draw(self, surf):
        # bring back to CPU if using GPU
        xs = xp.asnumpy(self.x) if USE_GPU else self.x
        ys = xp.asnumpy(self.y) if USE_GPU else self.y
        ts = xp.asnumpy(self.t) if USE_GPU else self.t

        for i in range(self.n):
            pygame.draw.circle(
                surf,
                COLORS[ts[i]],
                (int(xs[i]), int(ys[i])),
                CELL_RADIUS
            )

# =========================
# APP
# =========================


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 18)

    sim = Sim()
    paused = False

    while True:
        dt = clock.tick(FPS) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    paused = not paused
                if e.key == pygame.K_r:
                    sim.reset()

        if not paused:
            sim.step(dt)

        screen.fill((8, 8, 10))
        sim.draw(screen)

        if paused:
            screen.blit(font.render("PAUSED", True, (220, 220, 220)), (8, 8))

        pygame.display.flip()


if __name__ == "__main__":
    main()
