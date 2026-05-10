import pygame
import random
import sys

# --- Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PADDLE_WIDTH = 12
PADDLE_HEIGHT = 100
PADDLE_MARGIN = 20
PLAYER_SPEED = 420  # pixels per second
AI_SPEED = 350

BALL_RADIUS = 9
BALL_SPEED_START = 360  # initial ball speed (pixels/sec)
BALL_SPEED_INCREMENT = 30  # speed up after each paddle hit
MAX_SCORE = 10

# Colors
BG_COLOR = (10, 10, 30)
PADDLE_COLOR = (230, 230, 230)
BALL_COLOR = (250, 120, 60)
TEXT_COLOR = (230, 230, 230)

# --- Game objects ---


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 0

    def move(self, dy):
        self.rect.y += dy
        # clamp to screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update(self, dt):
        if self.speed != 0:
            self.move(self.speed * dt)

    def draw(self, surf):
        pygame.draw.rect(surf, PADDLE_COLOR, self.rect, border_radius=4)


class Ball:
    def __init__(self):
        self.reset()

    def reset(self, direction=None):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vx = 0
        self.vy = 0
        self.speed = BALL_SPEED_START
        # give a short pause before serving
        self.serve_delay = 0.6
        # random initial direction if not specified (-1 left, 1 right)
        dir_sign = direction if direction is not None else random.choice(
            [-1, 1])
        # radians approx for vertical component
        angle = random.uniform(-0.4, 0.4)
        self.vx = dir_sign * self.speed * (1 - abs(angle))
        self.vy = self.speed * angle

    def update(self, dt):
        if getattr(self, "serve_delay", 0) > 0:
            self.serve_delay -= dt
            if self.serve_delay <= 0:
                # start moving (vx, vy already set)
                pass
            return

        self.x += self.vx * dt
        self.y += self.vy * dt

        # bounce top/bottom
        if self.y - BALL_RADIUS <= 0:
            self.y = BALL_RADIUS
            self.vy = -self.vy
        if self.y + BALL_RADIUS >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - BALL_RADIUS
            self.vy = -self.vy

    def draw(self, surf):
        pygame.draw.circle(
            surf, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)


# --- Main game ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong — W/S to move left paddle")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)

    # Create paddles and ball
    left_paddle = Paddle(PADDLE_MARGIN, SCREEN_HEIGHT //
                         2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH,
                          SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    score_left = 0
    score_right = 0

    running = True
    paused = False

    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds since last frame

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    # reset match
                    score_left = 0
                    score_right = 0
                    ball.reset(direction=random.choice([-1, 1]))
                # player controls
                if event.key == pygame.K_w:
                    left_paddle.speed = -PLAYER_SPEED
                if event.key == pygame.K_s:
                    left_paddle.speed = PLAYER_SPEED
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    # stop paddle if released (handles when both pressed quickly)
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_w] and not keys[pygame.K_s]:
                        left_paddle.speed = -PLAYER_SPEED
                    elif keys[pygame.K_s] and not keys[pygame.K_w]:
                        left_paddle.speed = PLAYER_SPEED
                    else:
                        left_paddle.speed = 0

        # --- Update objects ---
        left_paddle.update(dt)

        # Simple AI for right paddle: follow the ball with a max speed; add deadzone for fairness
        if getattr(ball, "serve_delay", 0) > 0:
            # center the AI paddle slowly when ball is paused
            ai_target = SCREEN_HEIGHT // 2
        else:
            ai_target = ball.y
        diff = ai_target - right_paddle.rect.centery
        deadzone = 8
        if abs(diff) > deadzone:
            move = max(-AI_SPEED, min(AI_SPEED, diff / abs(diff) * AI_SPEED))
            right_paddle.move(move * dt)

        # Update ball (may be paused briefly during serve)
        prev_x = ball.x
        ball.update(dt)

        # Paddle collision detection (only when ball is active)
        if getattr(ball, "serve_delay", 0) <= 0:
            ball_rect = pygame.Rect(int(ball.x - BALL_RADIUS), int(ball.y - BALL_RADIUS),
                                    BALL_RADIUS * 2, BALL_RADIUS * 2)
            if ball_rect.colliderect(left_paddle.rect):
                # ensure ball moves right
                ball.x = left_paddle.rect.right + BALL_RADIUS
                ball.vx = abs(ball.vx) + BALL_SPEED_INCREMENT
                # add spin based on where it hit the paddle
                offset = (ball.y - left_paddle.rect.centery) / \
                    (PADDLE_HEIGHT / 2)
                ball.vy = ball.speed * offset
                ball.speed = abs(ball.vx)  # sync speed
            elif ball_rect.colliderect(right_paddle.rect):
                ball.x = right_paddle.rect.left - BALL_RADIUS
                ball.vx = -abs(ball.vx) - BALL_SPEED_INCREMENT
                offset = (ball.y - right_paddle.rect.centery) / \
                    (PADDLE_HEIGHT / 2)
                ball.vy = ball.speed * offset
                ball.speed = abs(ball.vx)

        # Score handling: if ball goes off left or right
        if ball.x < -BALL_RADIUS:
            score_right += 1
            if score_right >= MAX_SCORE:
                paused = True
            ball.reset(direction=-1)  # serve to left (loser just conceded)
        elif ball.x > SCREEN_WIDTH + BALL_RADIUS:
            score_left += 1
            if score_left >= MAX_SCORE:
                paused = True
            ball.reset(direction=1)

        # --- Drawing ---
        screen.fill(BG_COLOR)

        # center line
        for i in range(0, SCREEN_HEIGHT, 24):
            pygame.draw.rect(screen, (60, 60, 80),
                             (SCREEN_WIDTH // 2 - 2, i + 6, 4, 12))

        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)

        # Scores
        left_surf = font.render(str(score_left), True, TEXT_COLOR)
        right_surf = font.render(str(score_right), True, TEXT_COLOR)
        screen.blit(left_surf, (SCREEN_WIDTH * 0.25 -
                    left_surf.get_width() // 2, 16))
        screen.blit(right_surf, (SCREEN_WIDTH * 0.75 -
                    right_surf.get_width() // 2, 16))

        # Instructions
        instr = small_font.render(
            "W/S to move left paddle. Press R to restart. ESC to quit.", True, TEXT_COLOR)
        screen.blit(instr, (SCREEN_WIDTH // 2 -
                    instr.get_width() // 2, SCREEN_HEIGHT - 28))

        # If someone reached MAX_SCORE show winner
        if paused:
            winner = "Left Player Wins!" if score_left > score_right else "Right Player Wins!"
            win_surf = font.render(winner, True, (200, 200, 60))
            screen.blit(win_surf, (SCREEN_WIDTH // 2 -
                        win_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 24))
            sub = small_font.render("Press R to play again.", True, TEXT_COLOR)
            screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() //
                        2, SCREEN_HEIGHT // 2 + 28))

        pygame.display.flip()

        # If paused (match over), just wait for R or Quit
        if paused:
            # handle pause loop (still catches events)
            while paused:
                ev = pygame.event.wait()
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_r:
                        score_left = 0
                        score_right = 0
                        ball.reset(direction=random.choice([-1, 1]))
                        paused = False
                    elif ev.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    pygame.quit()


if __name__ == "__main__":
    main()
