import pygame
import random
import numpy as np

FPS = 60

class PongGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        self.screen_width = 800
        self.screen_height = 600

        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # Paddle dimensions
        self.paddle_width = 10
        self.paddle_height = 100

        # Ball dimensions
        self.ball_size = 20

        # Speeds
        self.paddle_speed = 6
        self.ball_speed_x = 6
        self.ball_speed_y = 6

        # Initialize the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Pong: DQN vs Bot')

        # Paddles
        self.player1_paddle = pygame.Rect(50, (self.screen_height - self.paddle_height) // 2, self.paddle_width, self.paddle_height)
        self.player2_paddle = pygame.Rect(self.screen_width - 50 - self.paddle_width, (self.screen_height - self.paddle_height) // 2, self.paddle_width, self.paddle_height)

        # Ball
        self.ball = pygame.Rect(self.screen_width // 2 - self.ball_size // 2, self.screen_height // 2 - self.ball_size // 2, self.ball_size, self.ball_size)

        # Scores
        self.player1_score = 0
        self.player2_score = 0
        self.score = 0

        # Font for scores
        self.font = pygame.font.Font(None, 74)

    def reset(self):
        self.player1_paddle.y = (self.screen_height - self.paddle_height) // 2
        self.player2_paddle.y = (self.screen_height - self.paddle_height) // 2
        self.ball.x = self.screen_width // 2 - self.ball_size // 2
        self.ball.y = self.screen_height // 2 - self.ball_size // 2
        self.ball_speed_x = random.choice([-6, 6])
        self.ball_speed_y = random.choice([-6, 6])
        self.player1_score = 0
        self.player2_score = 0
        self.score = 0

    def step(self, action): # 0 (up), 1 (down), 2 (remain still)
        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Player 1 (AI) action
        if np.array_equal(action, [1,0,0]) and self.player1_paddle.top > 0:  # Arriba
            self.player1_paddle.y -= self.paddle_speed
        elif np.array_equal(action, [0,1,0]) and self.player1_paddle.bottom < self.screen_height:  # Abajo
            self.player1_paddle.y += self.paddle_speed
        # action == 2 (remain still) no changes required        

        # Player 2 (Bot) prediction
        if self.ball_speed_x > 0:  # Ball is moving towards the bot
            player2_target_y = self.ball.y
            if self.player2_paddle.centery > player2_target_y and self.player2_paddle.top > 0:
                self.player2_paddle.y -= self.paddle_speed
            if self.player2_paddle.centery < player2_target_y and self.player2_paddle.bottom < self.screen_height:
                self.player2_paddle.y += self.paddle_speed

        # Move ball
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # Ball collisions with top/bottom boundaries
        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            self.ball_speed_y = -self.ball_speed_y

        # Ball collision with player 1 (AI)
        if self.ball.colliderect(self.player1_paddle):
            self.ball_speed_x = -self.ball_speed_x
            self.score += 1
            reward = 1

        # Ball collision with player 2 (bot)
        elif self.ball.colliderect(self.player2_paddle):
            self.ball_speed_x = -self.ball_speed_x

        # Reward and game over if bot scores
        reward = 0
        done = False

        if self.ball.left <= 0:
            self.player2_score += 1
            reward = -5
            done = True
        elif self.ball.right >= self.screen_width:
            self.player1_score += 1
            reward = 5
        
        # Render
        self._render()
        
        # Frame rate
        pygame.time.Clock().tick(FPS)

        return reward, done, self.score

    def _render(self):
        # Render game
        self.screen.fill(self.black)
        pygame.draw.rect(self.screen, self.white, self.player1_paddle)
        pygame.draw.rect(self.screen, self.white, self.player2_paddle)
        pygame.draw.ellipse(self.screen, self.white, self.ball)
        pygame.draw.aaline(self.screen, self.white, (self.screen_width // 2, 0), (self.screen_width // 2, self.screen_height))

        # Render scores
        player1_text = self.font.render(str(self.player1_score), True, self.white)
        self.screen.blit(player1_text, (self.screen_width // 4, 20))
        player2_text = self.font.render(str(self.player2_score), True, self.white)
        self.screen.blit(player2_text, (self.screen_width * 3 // 4, 20))

        pygame.display.flip()