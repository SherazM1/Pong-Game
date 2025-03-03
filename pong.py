#!/usr/bin/env python3
import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEFAULT_PADDLE_COLOR = (255, 255, 255)
DEFAULT_BALL_COLOR = (255, 255, 255)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
PADDLE_SPEED = 6
BALL_SPEED_X, BALL_SPEED_Y = 7, 7
WINNING_SCORE = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 90)
message_font = pygame.font.Font(None, 36)

left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

ball_dir_x = BALL_SPEED_X
ball_dir_y = BALL_SPEED_Y

left_score = 0
right_score = 0

paddle_color = DEFAULT_PADDLE_COLOR
ball_color = DEFAULT_BALL_COLOR

clock = pygame.time.Clock()

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, paddle_color, left_paddle)
    pygame.draw.rect(screen, paddle_color, right_paddle)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 4 - left_text.get_width() // 2, 20))
    screen.blit(right_text, (WIDTH * 3 // 4 - right_text.get_width() // 2, 20))
    pygame.display.flip()

def move_paddles():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

def move_ball():
    global ball_dir_x, ball_dir_y, left_score, right_score
    ball.x += ball_dir_x
    ball.y += ball_dir_y
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dir_y *= -1
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_dir_x *= -1
    if ball.left <= 0:
        right_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        left_score += 1
        reset_ball()

def reset_ball():
    global ball_dir_x, ball_dir_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_dir_x *= -1
    ball_dir_y = random.choice([BALL_SPEED_Y, -BALL_SPEED_Y])

def change_colors(key):
    global paddle_color, ball_color
    if key == pygame.K_1:
        paddle_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    if key == pygame.K_2:
        ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def start_screen():
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
    running = True
    while running:
        screen.fill(BLACK)
        title_text = title_font.render("Sheraz's Pong", True, WHITE)
        message_text = message_font.render("First to ten wins!", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, 150))
        pygame.draw.rect(screen, WHITE, start_button)
        text = button_font.render("Start", True, BLACK)
        screen.blit(text, (start_button.x + start_button.width // 2 - text.get_width() // 2,
                           start_button.y + start_button.height // 2 - text.get_height() // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    running = False

def game_over_screen(winner):
    running = True
    while running:
        screen.fill(BLACK)
        text = font.render(f"{winner} Wins!", True, WHITE)
        message_text = message_font.render("Press Enter to play again", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 40))
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

def main():
    start_screen()
    global left_score, right_score
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                change_colors(event.key)
        move_paddles()
        move_ball()
        draw()
        if left_score == WINNING_SCORE:
            game_over_screen("Left Player")
            left_score, right_score = 0, 0
            start_screen()
        if right_score == WINNING_SCORE:
            game_over_screen("Right Player")
            left_score, right_score = 0, 0
            start_screen()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
