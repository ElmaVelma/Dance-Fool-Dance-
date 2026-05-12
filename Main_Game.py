import pygame
import random
import sys
import os


pygame.init()
screen = pygame.display.set_mode((1440, 900))
bg_img = pygame.image.load("TENT.png")
bg_img = pygame.transform.scale(bg_img, (1440, 900))
font = pygame.font.SysFont("Arial", 50)
small_font = pygame.font.SysFont("Arial", 30)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

bg_img_two = pygame.image.load("TENT_TWO.png")
bg_img_two = pygame.transform.scale(bg_img_two, (1440, 900))

def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(new_high_score):
    with open("highscore.txt", "w") as f:
        f.write(str(new_high_score))



hs_score = load_high_score()

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def show_high_scores():
    while True:
        screen.blit(bg_img_two, (0, 0))
        draw_text("High Scores", font, BLACK, 580, 250)
        draw_text(f"Top Score: {hs_score}", small_font, BLACK, 630, 350)
        draw_text("Press B to go Back", small_font, BLACK, 580, 450)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return
        pygame.display.update()

def main_menu():
    while True:
        screen.blit(bg_img, (0, 0))
        draw_text("Dance Fool, Dance!", font, BLACK, 490, 360)
        draw_text("Press SPACE to Start", small_font, BLACK, 560, 415)
        draw_text("Press H for highscores", small_font, BLACK, 560, 450)
        draw_text("Press Q to Quit", small_font, BLACK, 560, 485)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 
                if event.key == pygame.K_h:
                    show_high_scores()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


def death_screen(screen, font, final_score):
    death_running = True
    while death_running:
        screen.fill((139, 0, 0))

        msg = font.render("GAME OVER", True, (220, 20, 60))
        score_msg = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
        retry_msg = font.render("Press R to restart or Q to quit", True, (200, 200, 200))

        screen.blit(msg, (1440 // 2 - 150, 300))
        screen.blit(score_msg, (1440 // 2 - 145, 400))
        screen.blit(retry_msg, (1440 // 2 - 250, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    return "quit"



def game_loop():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 900
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 36)
    font_two = pygame.font.SysFont("Arial", 50)

    Color_One = (255, 255, 255)
    Color_two   = (255, 255, 102)
    Color_three  = (255, 0, 0)
    Color_four = (200, 200, 200)

    high_score = load_high_score()

    player_rect = pygame.Rect(375, 540, 50, 50)
    player_speed = 8

    blocks = []

    score = 0
    lives = 5

    for i in range(3, 0, -1):
        screen.blit(bg_img_two, (0, 0))

        countdown_text = font_two.render(str(i), True, (0, 0, 0))
        text_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(countdown_text, text_rect)

        pygame.display.flip()
        pygame.time.delay(1000)



    running = True
    while running:
            block_speed = 4 + (score // 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
                player_rect.x += player_speed

            if random.randint(1, 80) == 1:
                new_block = pygame.Rect(random.randint(0, SCREEN_WIDTH-25), -25, 25, 25)
                blocks.append(new_block)

            for block in blocks[:]: 
                block.y += block_speed
                
                if player_rect.colliderect(block):
                    blocks.remove(block)
                    score += 5
                    if score > high_score:
                        high_score = score
                
                elif block.top > SCREEN_HEIGHT:
                    blocks.remove(block)
                    lives -= 1
                    if lives <= 0:
                        save_high_score(high_score)
                        action = death_screen(screen, font, score)
                        if action == "restart":
                            game_loop()
                            return
                        else:
                            running = False
                    

            screen.blit(bg_img_two, (0, 0))
            pygame.draw.rect(screen, Color_three, player_rect) 
            for block in blocks:
                pygame.draw.rect(screen, Color_two, block)
            
            score_text = font.render(f"Score: {score} High Score: {high_score} Lives: {lives}", True, (0, 0, 0))
            screen.blit(score_text, (20, 20))

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()


while True:
    main_menu()
    game_loop()

