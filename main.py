import pygame
from ball import Ball
from paddle import Paddle
from bricks import Brick

WHITE = (255, 255, 255)
DARKBLUE = (36, 90, 190)
LIGHTBLUE = (0, 176, 240)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)

score = 0
lives = 3

pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Breakout !!")

all_sprites_list = pygame.sprite.Group()

paddle = Paddle(LIGHTBLUE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 750

ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 495

all_bricks = pygame.sprite.Group()
for i in range(7):
    brick = Brick(RED, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(ORANGE, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(YELLOW, 80, 30)
    brick.rect.x = 60 + i * 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

all_sprites_list.add(paddle)
all_sprites_list.add(ball)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move_left(5)
    if keys[pygame.K_RIGHT]:
        paddle.move_right(5)

    all_sprites_list.update()

    if ball.rect.x >= 790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y < 40:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y > 790:
        ball.velocity[1] = -ball.velocity[1]
        lives -= 1
        if lives == 0:
            font = pygame.font.Font(None, 74)
            over_text = font.render("GAME OVER", 1, WHITE)
            window.blit(over_text, (300, 400))
            pygame.display.flip()
            pygame.time.wait(3000)

            running = False
            break

    if pygame.sprite.collide_mask(ball, paddle):
        ball.rect.x -= ball.velocity[0]
        ball.rect.y -= ball.velocity[1]
        ball.bounce()

    brick_collision_list = pygame.sprite.spritecollide(ball, all_bricks, False)
    for brick in brick_collision_list:
        ball.bounce()
        score += 1
        brick.kill()
        if len(all_bricks) == 0:
            font = pygame.font.Font(None, 74)
            level_text = font.render("LEVEL PASSED", 1, WHITE)
            window.blit(level_text, (300, 400))
            pygame.display.flip()
            pygame.time.wait(3000)

            running = False

    window.fill(DARKBLUE)
    pygame.draw.line(window, WHITE, [0, 38], [800, 38], 2)

    font = pygame.font.Font(None, 34)
    score_text = font.render("Score: " + str(score), 1, WHITE)
    window.blit(score_text, (20, 10))
    lives_text = font.render("Lives: " + str(lives), 1, WHITE)
    window.blit(lives_text, (650, 10))

    all_sprites_list.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
