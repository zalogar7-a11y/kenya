import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
DARK_GREEN = (0, 50, 0)

# Screen setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CLASSROOM COMPROMISED - HANGMAN")

# Fonts
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# Game variables
word_list = ["PYTHON", "HACKER", "SECRET", "COMPUTER", "KEYBOARD", "NETWORK", "ENCRYPTION", "MALWARE", "FIREWALL", "DATABASE"]
secret_word = random.choice(word_list)
guessed_letters = []
wrong_guesses = 0
max_wrong = 6
game_over = False
won = False

# Sound effects (using generated tones since we can't load external files easily)
def play_sound(sound_type):
    if sound_type == "correct":
        freq, duration = 800, 100
    elif sound_type == "wrong":
        freq, duration = 200, 150
    elif sound_type == "win":
        freq, duration = 1000, 300
    else:  # game over
        freq, duration = 150, 400
    
    sample_rate = 44100
    n_samples = int(sample_rate * duration / 1000)
    buf = bytes([int(128 + 127 * __import__('math').sin(2 * __import__('math').pi * freq * i / sample_rate)) for i in range(n_samples)])
    sound = pygame.mixer.Sound(buffer=buf)
    sound.play()

def draw_hangman(wrong):
    pygame.draw.line(screen, GREEN, (150, 650), (350, 650), 4)
    pygame.draw.line(screen, GREEN, (250, 650), (250, 100), 4)
    pygame.draw.line(screen, GREEN, (250, 100), (450, 100), 4)
    pygame.draw.line(screen, GREEN, (450, 100), (450, 150), 4)
    
    if wrong >= 1:
        pygame.draw.circle(screen, GREEN, (450, 180), 30, 4)
    if wrong >= 2:
        pygame.draw.line(screen, GREEN, (450, 210), (450, 350), 4)
    if wrong >= 3:
        pygame.draw.line(screen, GREEN, (450, 240), (400, 300), 4)
    if wrong >= 4:
        pygame.draw.line(screen, GREEN, (450, 240), (500, 300), 4)
    if wrong >= 5:
        pygame.draw.line(screen, GREEN, (450, 350), (400, 450), 4)
    if wrong >= 6:
        pygame.draw.line(screen, GREEN, (450, 350), (500, 450), 4)

def draw_word():
    display = ""
    x_pos = 150
    y_pos = 450
    word_width = 0
    
    for letter in secret_word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    
    text = font_large.render(display, True, GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2, y_pos))
    screen.blit(text, text_rect)

def draw_keyboard():
    keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    x_start = 150
    y_start = 520
    key_width = 40
    key_height = 40
    gap = 10
    
    for i, key in enumerate(keys):
        row = i // 9
        col = i % 9
        x = x_start + col * (key_width + gap)
        y = y_start + row * (key_height + gap)
        
        color = GREEN
        if key in guessed_letters:
            if key in secret_word:
                color = CYAN
            else:
                color = RED
        
        pygame.draw.rect(screen, color, (x, y, key_width, key_height), 2)
        letter_text = font_small.render(key, True, color)
        screen.blit(letter_text, (x + 12, y + 8))

def main():
    global wrong_guesses, game_over, won, guessed_letters, secret_word
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                for i in range(26):
                    if event.key == pygame.K_a + i:
                        letter = chr(ord('A') + i)
                        if letter not in guessed_letters:
                            guessed_letters.append(letter)
                            if letter in secret_word:
                                play_sound("correct")
                                if all(l in guessed_letters for l in secret_word):
                                    won = True
                                    game_over = True
                                    play_sound("win")
                            else:
                                wrong_guesses += 1
                                play_sound("wrong")
                                if wrong_guesses >= max_wrong:
                                    game_over = True
                                    play_sound("gameover")
        
        # Draw everything
        draw_hangman(wrong_guesses)
        draw_word()
        draw_keyboard()
        
        # Draw status
        lives_text = font_medium.render(f"LIVES: {max_wrong - wrong_guesses}", True, YELLOW)
        screen.blit(lives_text, (WIDTH - 250, 50))
        
        if game_over:
            if won:
                msg = font_large.render("YOU WIN!", True, GREEN)
            else:
                msg = font_large.render(f"GAME OVER! Word: {secret_word}", True, RED)
            msg_rect = msg.get_rect(center=(WIDTH // 2, 80))
            screen.blit(msg, msg_rect)
            
            restart_text = font_small.render("Press R to Restart or ESC to Quit", True, CYAN)
            screen.blit(restart_text, (WIDTH // 2 - 180, 650))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Reset game
                secret_word = random.choice(word_list)
                guessed_letters = []
                wrong_guesses = 0
                game_over = False
                won = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
