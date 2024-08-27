import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Paddle dimensions
paddle_width = 10
paddle_height = 100

# Ball dimensions
ball_size = 20

# Speeds
paddle_speed = 6
ball_speed_x = 5
ball_speed_y = 5

# Fonts
font = pygame.font.Font(None, 74)

# Initialize the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Paddles
player1_paddle = pygame.Rect(50, (screen_height - paddle_height) // 2, paddle_width, paddle_height)
player2_paddle = pygame.Rect(screen_width - 50 - paddle_width, (screen_height - paddle_height) // 2, paddle_width, paddle_height)

# Ball
ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)

# Scores
player1_score = 0
player2_score = 0

# Game loop flag
running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player 1 controls (W/S)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_paddle.top > 0:
        player1_paddle.y -= paddle_speed
    if keys[pygame.K_s] and player1_paddle.bottom < screen_height:
        player1_paddle.y += paddle_speed

    # Player 2 (Bot) prediction
    if ball_speed_x > 0:  # Ball is moving towards the bot
        player2_target_y = ball.y
        if player2_paddle.centery > player2_target_y and player2_paddle.top > 0:
            player2_paddle.y -= paddle_speed
        if player2_paddle.centery < player2_target_y and player2_paddle.bottom < screen_height:
            player2_paddle.y += paddle_speed

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y = -ball_speed_y

    # Ball collision with human paddle
    if ball.colliderect(player1_paddle):
        ball_speed_x = -ball_speed_x
        #player2_target_y = math.tan(math.pi / 4) * (800 - (ball.centery / math.tan(math.pi / 4))) 

    # Ball collision with bot paddle
    elif ball.colliderect(player2_paddle):
        ball_speed_x = -ball_speed_x

    # Ball out of bounds
    if ball.left <= 0:
        player2_score += 1
        ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
        ball_speed_x = 5
        ball_speed_y = random.choice((-5, 5))
    if ball.right >= screen_width:
        player1_score += 1
        ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
        ball_speed_x = -5
        ball_speed_y = random.choice((-5, 5))

    # Check for winning condition
    if player1_score == 10 or player2_score == 10:
        player1_score = 0
        player2_score = 0

    # Clear the screen
    screen.fill(black)

    # Draw paddles, ball, and middle line
    pygame.draw.rect(screen, white, player1_paddle)
    pygame.draw.rect(screen, white, player2_paddle)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height))

    # Draw scores
    player1_text = font.render(str(player1_score), True, white)
    screen.blit(player1_text, (screen_width // 4, 20))

    player2_text = font.render(str(player2_score), True, white)
    screen.blit(player2_text, (screen_width * 3 // 4, 20))

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
