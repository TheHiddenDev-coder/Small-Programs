import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Inside Circle 1.1")

clock = pygame.time.Clock()
FPS = 60

# Circle boundary
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250

# Ball properties
ball_pos = [WIDTH // 2, HEIGHT // 2 - 100]  # Start near the top
# Initial horizontal velocity, vertical will increase by gravity
ball_vel = [random.uniform(-3, 3), 0]
ball_radius = 10
gravity = 0.2
bounce_factor = 1.0  # Bounce is fully elastic

# Rainbow colors
rainbow = [
    (148, 0, 211),  # Violet
    (75, 0, 130),   # Indigo
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (255, 127, 0),  # Orange
    (255, 0, 0)     # Red
]
color_index = 0

# Store outlines
outlines = []

ball_exists = True  # Track if ball should be drawn

running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if ball_exists:
        # Apply gravity
        ball_vel[1] += gravity
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        # Distance from center
        dx = ball_pos[0] - CENTER[0]
        dy = ball_pos[1] - CENTER[1]
        dist = math.hypot(dx, dy)

        # Check collision with circle boundary
        if dist + ball_radius >= RADIUS:
            # Normal vector
            nx = dx / dist
            ny = dy / dist
            # Reflect velocity
            dot = ball_vel[0] * nx + ball_vel[1] * ny
            ball_vel[0] -= 2 * dot * nx
            ball_vel[1] -= 2 * dot * ny
            # Grow the ball
            ball_radius += 2
            # Cycle color
            color_index = (color_index + 1) % len(rainbow)
            # Push ball just inside the boundary
            overlap = dist + ball_radius - RADIUS
            ball_pos[0] -= nx * overlap
            ball_pos[1] -= ny * overlap

        # Add outline every frame
        outlines.append((tuple(ball_pos), ball_radius, rainbow[color_index]))

        # Check if ball reached circle size
        if ball_radius >= RADIUS:
            ball_exists = False  # Remove ball

    # Draw circle boundary
    pygame.draw.circle(screen, (255, 255, 255), CENTER, RADIUS, 2)

    # Draw all outlines
    for pos, rad, color in outlines:
        pygame.draw.circle(
            screen, color, (int(pos[0]), int(pos[1])), int(rad), 1)

    # Draw ball if it still exists
    if ball_exists:
        pygame.draw.circle(screen, (255, 255, 255), (int(
            ball_pos[0]), int(ball_pos[1])), int(ball_radius))

    pygame.display.flip()

pygame.quit()