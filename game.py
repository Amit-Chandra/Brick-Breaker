import pygame
import random
import sys


pygame.init()


WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_COLOR = (255, 255, 255)
BALL_RADIUS = 10
BALL_COLOR = (255, 255, 255)
BRICK_WIDTH = 60
BRICK_HEIGHT = 30
BRICK_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255)]  # Red, Orange, Yellow, Green, Blue
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_GAP = 10
BORDER_COLOR = (255, 255, 255)
FONT_COLOR = (255, 255, 255)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")


clock = pygame.time.Clock()


def draw_paddle(paddle_x):
    pygame.draw.rect(screen, PADDLE_COLOR, (paddle_x, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))


def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)


def draw_brick(x, y, color):
    pygame.draw.rect(screen, color, (x, y, BRICK_WIDTH, BRICK_HEIGHT))


def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick_x = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP
            brick_y = row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP + 50
            brick_color = random.choice(BRICK_COLORS)
            bricks.append((brick_x, brick_y, brick_color))
    return bricks


def draw_bricks(bricks):
    for brick in bricks:
        draw_brick(brick[0], brick[1], brick[2])


def display_text(text, font_size, x, y):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, FONT_COLOR)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, active_color, button_rect)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, button_rect)

    display_text(text, 36, x + width / 2, y + height / 2)


def show_final_score(score):
    final_score_message = f"Your Final Score: {score}"
    pygame.display.set_caption(final_score_message)
    display_text(final_score_message, 48, WIDTH // 2, HEIGHT // 2)


def start_again():
    main()


def main():
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2
    ball_x = WIDTH // 2
    ball_y = HEIGHT - PADDLE_HEIGHT - BALL_RADIUS
    ball_dx = random.choice([-5, 5])
    ball_dy = -5
    bricks = create_bricks()
    score = 0
    
    running = True
    game_over = False
    game_over_time = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not game_over:
            
            screen.fill((0, 0, 0))
            
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle_x -= 5
            if keys[pygame.K_RIGHT]:
                paddle_x += 5
            
            
            paddle_x = max(0, min(paddle_x, WIDTH - PADDLE_WIDTH))
            
            
            draw_paddle(paddle_x)
            
           
            ball_x += ball_dx
            ball_y += ball_dy
            
            
            if ball_x <= BALL_RADIUS or ball_x >= WIDTH - BALL_RADIUS:
                ball_dx *= -1
            if ball_y <= BALL_RADIUS:
                ball_dy *= -1
            
            
            if ball_y >= HEIGHT - PADDLE_HEIGHT - BALL_RADIUS and paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH:
                ball_dy *= -1
            
           
            for brick in bricks:
                brick_rect = pygame.Rect(brick[0], brick[1], BRICK_WIDTH, BRICK_HEIGHT)
                if brick_rect.collidepoint(ball_x, ball_y):
                    bricks.remove(brick)
                    ball_dy *= -1
                    score += 1
            
            
            draw_bricks(bricks)
            
            
            draw_ball(ball_x, ball_y)
            
            
            if ball_y >= HEIGHT:
                game_over = True
                game_over_time = pygame.time.get_ticks()
        
        
        display_text(f"Score: {score}", 36, WIDTH // 2, HEIGHT // 2)
        
       
        if game_over and pygame.time.get_ticks() - game_over_time > 1000:
            screen.fill((0, 0, 0))
            draw_button("My Final Score", 150, 200, 200, 50, (0, 255, 0), (0, 200, 0), lambda: show_final_score(score))
            draw_button("Start Again", 450, 200, 200, 50, (255, 0, 0), (200, 0, 0), start_again)
        
        
        pygame.display.flip()
        
        
        clock.tick(60)

if __name__ == "__main__":
    main()

