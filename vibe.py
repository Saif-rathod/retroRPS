import pygame
import sys
import random
import math
import json
import os


pygame.init()


WIDTH, HEIGHT = 900, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
FONT = pygame.font.Font(None, 50)
BUTTON_FONT = pygame.font.Font(None, 40)
TABLE_FONT = pygame.font.Font(None, 30)


COLORS = {
    'glass': (255, 255, 255, 180),
    'glass_border': (255, 255, 255, 50),
    'glass_highlight': (255, 255, 255, 30),
    'shadow': (0, 0, 0, 100),
    'text_primary': (255, 255, 255),
    'text_secondary': (200, 200, 200),
    'accent': (0, 200, 255),
    'danger': (255, 50, 50),
    'success': (50, 255, 50),
    'button_hover': (255, 255, 255, 30)
}


CHOICES = ['Rock', 'Paper', 'Scissors']


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors - Multi-Theme")


stats = {'rounds': 0, 'ties': 0, 'ai_wins': 0, 'player_wins': 0}


THEMES = {
    'retro': {
        'name': 'Neon',
        'background_func': 'retro_background',
        'button_color': (28, 19, 74),  
        'text_color': (255, 255, 255),  
        'table_bg': (24, 17, 58),  
        'table_text': (255, 255, 255),  
        'header_text': (37, 24, 92),  
        'assets_folder': 'retro',
        'accent_color': (25, 18, 59),  
        'sound_effects': {
            'button_click': 'retro_click.wav',
            'win': 'retro_win.wav',
            'lose': 'retro_lose.wav',
            'tie': 'retro_tie.wav'
        }
    },

    'hacker': {
        'name': 'Matrix',
        'background_func': 'hacker_background',
        'button_color': (0, 200, 0),  
        'text_color': (0, 255, 0),  
        'table_bg': (10, 10, 10),  
        'table_text': (0, 255, 0),  
        'header_text': (0, 200, 0),  
        'assets_folder': 'hacker',
        'accent_color': (0, 150, 0),  
        'sound_effects': {
            'button_click': 'hacker_click.wav',
            'win': 'hacker_win.wav',
            'lose': 'hacker_lose.wav',
            'tie': 'hacker_tie.wav'
        }
    },

}

current_theme = 'retro'
theme_data = THEMES[current_theme]


theme_special_effects = {
    'retro': {'scanlines': True, 'color_shift': False, 'particles': False},
    'hacker': {'scanlines': True, 'color_shift': True, 'particles': True},
}


particles = []



def load_stats():
    try:
        with open('stats.json', 'r') as f:
            loaded_stats = json.load(f)
            
            if 'player_wins' not in loaded_stats:
                loaded_stats['player_wins'] = 0
            return loaded_stats
    except FileNotFoundError:
        return {'rounds': 0, 'ties': 0, 'ai_wins': 0, 'player_wins': 0}

def save_stats():
    with open('stats.json', 'w') as f:
        json.dump(stats, f)


def load_image(img_name):
    
    default_path = os.path.join('images', img_name)
    if os.path.exists(default_path):
        return pygame.image.load(default_path).convert_alpha()
    
    
    folder = theme_data['assets_folder']
    path = os.path.join('images', folder, img_name)
    if os.path.exists(path):
        return pygame.image.load(path).convert_alpha()
    
    print(f"⚠️ Image not found: {img_name}")
    return None


def load_sound(sound_name):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    
    default_path = os.path.join('sounds', 'vintage_click.wav')  
    if os.path.exists(default_path):
        return pygame.mixer.Sound(default_path)
    
    
    sound_file = theme_data['sound_effects'].get(sound_name)
    if not sound_file:
        return None
        
    path = os.path.join('sounds', theme_data['assets_folder'], sound_file)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    
    print(f"⚠️ Sound not found: {sound_file}")
    return None


def retro_background():
    
    screen.fill((20, 20, 20))  
    
    
    grid_color = (40, 40, 40)
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y))
    
    
    corner_size = 60
    corner_color = (25, 18, 59)  

    
    
    for i in range(3):
        glow_color = (0, 255, 255, 100 - i * 30)
        
        pygame.draw.line(screen, corner_color, (20 + i, 20 + i), (corner_size - i, 20 + i), 3)
        pygame.draw.line(screen, corner_color, (20 + i, 20 + i), (20 + i, corner_size - i), 3)
        
        
        pygame.draw.line(screen, corner_color, (WIDTH-20-i, 20+i), (WIDTH-corner_size+i, 20+i), 3)
        pygame.draw.line(screen, corner_color, (WIDTH-20-i, 20+i), (WIDTH-20-i, corner_size-i), 3)
        
        
        pygame.draw.line(screen, corner_color, (20+i, HEIGHT-20-i), (corner_size-i, HEIGHT-20-i), 3)
        pygame.draw.line(screen, corner_color, (20+i, HEIGHT-20-i), (20+i, HEIGHT-corner_size+i), 3)
        
        
        pygame.draw.line(screen, corner_color, (WIDTH-20-i, HEIGHT-20-i), (WIDTH-corner_size+i, HEIGHT-20-i), 3)
        pygame.draw.line(screen, corner_color, (WIDTH-20-i, HEIGHT-20-i), (WIDTH-20-i, HEIGHT-corner_size+i), 3)
    
    
    if theme_special_effects['retro']['scanlines']:
        for i in range(0, HEIGHT, 4):
            pygame.draw.line(screen, (0, 255, 255, 20), (0, i), (WIDTH, i), 1)
    
    
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice([(255, 0, 255), (0, 255, 255), (255, 255, 0)])
        pygame.draw.circle(screen, color, (x, y), 1)

def hacker_background():
    
    screen.fill((40, 40, 40))  
    
    
    grid_color = (60, 60, 60)
    for x in range(0, WIDTH, 60):
        pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 60):
        pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y))
    
    
    corner_size = 80
    corner_color = (0, 200, 0)  

    
    for i in range(3):
        glow_color = (255, 255, 0, 100 - i * 30)
        
        pygame.draw.line(screen, corner_color, (20 + i, 20 + i), (corner_size - i, 20 + i), 3)
        pygame.draw.line(screen, corner_color, (20 + i, 20 + i), (20 + i, corner_size - i), 3)
        
        
        pygame.draw.line(screen, corner_color, (WIDTH-20-i, 20+i), (WIDTH-corner_size+i, 20+i), 3)
        pygame.draw.line(screen, corner_color, (WIDTH-20-i, 20+i), (WIDTH-20-i, corner_size-i), 3)
        
        
        pygame.draw.line(screen, corner_color, (20+i, HEIGHT-20-i), (corner_size-i, HEIGHT-20-i), 3)
        pygame.draw.line(screen, corner_color, (20+i, HEIGHT-20-i), (20+i, HEIGHT-corner_size+i), 3)
        
        
        pygame.draw.line(screen, corner_color, (WIDTH-20-i, HEIGHT-20-i), (WIDTH-corner_size+i, HEIGHT-20-i), 3)
        pygame.draw.line(screen, corner_color, (WIDTH-20-i, HEIGHT-20-i), (WIDTH-20-i, HEIGHT-corner_size+i), 3)
    
    
    if theme_special_effects['hacker']['scanlines']:
        for i in range(0, HEIGHT, 2):
            if random.random() > 0.95:  
                continue
            alpha = random.randint(10, 30)
            glitch_color = (255, 255, 0, alpha)
            pygame.draw.line(screen, glitch_color, (0, i), (WIDTH, i), 1)
    
    
    if theme_special_effects['hacker']['particles']:
        for _ in range(30):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)
            color = random.choice([(255, 0, 0), (255, 255, 0), (255, 255, 255)])
            pygame.draw.circle(screen, color, (x, y), size)
    
    
    if random.random() < 0.05:  
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        text = random.choice(['WANTED', 'STAR', 'POLICE', 'GTA'])
        font = pygame.font.Font(None, 20)
        text_surface = font.render(text, True, (255, 255, 0))
        screen.blit(text_surface, (x, y))


def create_particles(x, y, count=10):
    for _ in range(count):
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(0.5, 2)
        size = random.uniform(1, 3)
        life = random.uniform(30, 60)
        color = (
            random.randint(150, 255),
            random.randint(150, 255),
            random.randint(150, 255)
        )
        particles.append({
            'x': x,
            'y': y,
            'dx': speed * math.cos(angle),
            'dy': speed * math.sin(angle),
            'size': size,
            'life': life,
            'color': color
        })

def update_particles():
    global particles
    for p in particles[:]:
        p['x'] += p['dx']
        p['y'] += p['dy']
        p['life'] -= 1
        if p['life'] <= 0 or p['x'] < 0 or p['x'] > WIDTH or p['y'] < 0 or p['y'] > HEIGHT:
            particles.remove(p)

def draw_particles():
    for p in particles:
        alpha = int(255 * (p['life'] / 60))
        color = (p['color'][0], p['color'][1], p['color'][2], alpha)
        pygame.draw.circle(screen, color, (int(p['x']), int(p['y'])), int(p['size']))


def draw_buttons():
    
    button_style = {
        'width': 180,
        'height': 80,
        'border_radius': 15,
        'hover_color': (min(theme_data['button_color'][0] + 30, 255),
                       min(theme_data['button_color'][1] + 30, 255),
                       min(theme_data['button_color'][2] + 30, 255))
    }
    
    
    button_rects = {}
    
    
    for i, (text, pos) in enumerate([('Rock', (150, 500)), ('Paper', (370, 500)), ('Scissors', (590, 500))]):
        
        shadow_rect = pygame.Rect(pos[0] + 5, pos[1] + 5, button_style['width'], button_style['height'])
        pygame.draw.rect(screen, COLORS['shadow'], shadow_rect, border_radius=button_style['border_radius'])
        
        
        btn_rect = pygame.Rect(pos[0], pos[1], button_style['width'], button_style['height'])
        pygame.draw.rect(screen, theme_data['button_color'], btn_rect, border_radius=button_style['border_radius'])
        
        
        for i in range(3):
            glow_rect = pygame.Rect(pos[0] - i, pos[1] - i, 
                                  button_style['width'] + i*2, 
                                  button_style['height'] + i*2)
            pygame.draw.rect(screen, theme_data['accent_color'], glow_rect, 1, 
                           border_radius=button_style['border_radius'])
        
        
        button_rects[text.lower()] = btn_rect
        
        
        text_surface = BUTTON_FONT.render(text, True, theme_data['text_color'])
        text_shadow = BUTTON_FONT.render(text, True, COLORS['shadow'])
        
        
        text_x = pos[0] + (button_style['width'] - text_surface.get_width()) // 2
        text_y = pos[1] + (button_style['height'] - text_surface.get_height()) // 2
        
        
        screen.blit(text_shadow, (text_x + 2, text_y + 2))
        screen.blit(text_surface, (text_x, text_y))

    
    clear_btn = pygame.draw.rect(screen, (255, 0, 0), 
                                (WIDTH - 150, 10, 140, 40), 
                                border_radius=10)
    clear_shadow = pygame.Rect(WIDTH - 145, 15, 140, 40)
    pygame.draw.rect(screen, COLORS['shadow'], clear_shadow, border_radius=10)
    
    
    clear_text = BUTTON_FONT.render("Clear Stats", True, WHITE)
    clear_shadow_text = BUTTON_FONT.render("Clear Stats", True, COLORS['shadow'])
    clear_text_x = WIDTH - 150 + (140 - clear_text.get_width()) // 2
    clear_text_y = 10 + (40 - clear_text.get_height()) // 2
    screen.blit(clear_shadow_text, (clear_text_x + 2, clear_text_y + 2))
    screen.blit(clear_text, (clear_text_x, clear_text_y))

    
    theme_btn_width = WIDTH // len(THEMES)
    theme_buttons = []
    
    for i, (theme_key, theme_info) in enumerate(THEMES.items()):
        
        btn_rect = pygame.Rect(i * theme_btn_width, HEIGHT - 40, theme_btn_width, 40)
        is_active = theme_key == current_theme
        
        
        pygame.draw.rect(screen, 
                        (60, 60, 60) if is_active else (40, 40, 40),
                        btn_rect)
        
        
        if is_active:
            pygame.draw.rect(screen, theme_data['accent_color'], btn_rect, 2)
        
        theme_buttons.append((btn_rect, theme_key))
        
        
        btn_text = pygame.font.Font(None, 25).render(theme_info['name'], True, WHITE)
        text_shadow = pygame.font.Font(None, 25).render(theme_info['name'], True, COLORS['shadow'])
        
        
        text_x = i * theme_btn_width + (theme_btn_width - btn_text.get_width()) // 2
        text_y = HEIGHT - 40 + (40 - btn_text.get_height()) // 2
        
        screen.blit(text_shadow, (text_x + 2, text_y + 2))
        screen.blit(btn_text, (text_x, text_y))

    return button_rects['rock'], button_rects['paper'], button_rects['scissors'], theme_buttons, clear_btn


def display_stats_table():
    
    table_rect = pygame.Rect(60, 50, 780, 180)  
    pygame.draw.rect(screen, COLORS['glass'], table_rect, border_radius=15)
    
    
    for i in range(180):
        alpha = int(30 * (1 - i/180))
        pygame.draw.line(screen, (255, 255, 255, alpha), 
                        (60, 50 + i), (840, 50 + i))
    
    
    pygame.draw.rect(screen, COLORS['glass_border'], table_rect, 2, border_radius=15)
    pygame.draw.rect(screen, theme_data['accent_color'], table_rect, 1, border_radius=15)
    
    
    header_rect = pygame.Rect(60, 50, 780, 40)
    pygame.draw.rect(screen, (0, 0, 0, 200), header_rect, border_radius=15)
    
    
    table_data = [
        ['Rounds', str(stats['rounds'])],
        ['Wins', str(stats['player_wins'])],
        ['AI Wins', str(stats['ai_wins'])],
        ['Ties', str(stats['ties'])],
        ['Win Rate', f"{(stats['player_wins']) / stats['rounds'] * 100:.2f}%" if stats['rounds'] > 0 else '0.00%']
    ]

    
    header_font = pygame.font.Font(None, 35)
    table_font = pygame.font.Font(None, 30)
    
    
    header_text = header_font.render("Game Statistics", True, COLORS['text_primary'])
    header_shadow = header_font.render("Game Statistics", True, COLORS['shadow'])
    screen.blit(header_shadow, (WIDTH//2 - header_text.get_width()//2 + 2, 62))
    screen.blit(header_text, (WIDTH//2 - header_text.get_width()//2, 60))
    
    
    for i, (label, value) in enumerate(table_data):
        
        stat_rect = pygame.Rect(70 + (i % 3) * 260, 100 + (i // 3) * 40, 240, 35)
        pygame.draw.rect(screen, (0, 0, 0, 100), stat_rect, border_radius=8)
        pygame.draw.rect(screen, theme_data['accent_color'], stat_rect, 1, border_radius=8)
        
        
        label_text = table_font.render(label, True, COLORS['text_secondary'])
        value_text = table_font.render(value, True, COLORS['text_primary'])
        
        
        label_shadow = table_font.render(label, True, COLORS['shadow'])
        value_shadow = table_font.render(value, True, COLORS['shadow'])
        
        screen.blit(label_shadow, (82 + (i % 3) * 260, 107 + (i // 3) * 40))
        screen.blit(value_shadow, (82 + (i % 3) * 260 + 122, 107 + (i // 3) * 40))
        screen.blit(label_text, (80 + (i % 3) * 260, 105 + (i // 3) * 40))
        screen.blit(value_text, (80 + (i % 3) * 260 + 120, 105 + (i // 3) * 40))


def countdown_animation():
    sounds = {}
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        
        
        globals()[theme_data['background_func']]()
        
        display_stats_table()

        
        countdown_text = FONT.render(f"{i}", True, theme_data['accent_color'])
        countdown_shadow = FONT.render(f"{i}", True, COLORS['shadow'])
        screen.blit(countdown_shadow, (WIDTH // 2 - 18, HEIGHT // 2 - 48))
        screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2 - 50))

        pygame.display.flip()
        pygame.time.delay(800)  


def display_result(player_choice):
    global stats
    screen.fill(BLACK)
    
    
    globals()[theme_data['background_func']]()
    display_stats_table()

    stats['rounds'] += 1

    
    chance = random.random()
    if chance < 0.3:  
        ai_choice = player_choice
        result = "It's a tie!"
        stats['ties'] += 1
        sound_to_play = load_sound('tie')
    else:  
        
        if player_choice == 'Rock':
            ai_choice = 'Paper'
        elif player_choice == 'Paper':
            ai_choice = 'Scissors'
        else:  
            ai_choice = 'Rock'
        result = "AI wins!"
        stats['ai_wins'] += 1
        sound_to_play = load_sound('lose')

    
    countdown_animation()

    
    if sound_to_play:
        sound_to_play.play()

    
    image_size = (150, 150)
    image_y = 400

    
    rock_image = load_image('rock.png')
    paper_image = load_image('paper.png')
    scissors_image = load_image('scissors.png')

    
    player_img = {
        'Rock': rock_image,
        'Paper': paper_image,
        'Scissors': scissors_image
    }.get(player_choice)

    
    ai_img = {
        'Rock': rock_image,
        'Paper': paper_image,
        'Scissors': scissors_image
    }.get(ai_choice)

    
    if result == "AI wins!":
        if theme_special_effects[current_theme]['particles']:
            create_particles(650, 400, 30)

    
    if player_img:
        player_img = pygame.transform.scale(player_img, image_size)
        
        shadow_surface = pygame.Surface(image_size, pygame.SRCALPHA)
        shadow_surface.fill(COLORS['shadow'])
        screen.blit(shadow_surface, (155, 405))
        screen.blit(player_img, (150, 400))
        
        pygame.draw.rect(screen, theme_data['accent_color'], 
                        (145, 390, 160, 160), 1, border_radius=10)
    else:
        text = FONT.render(player_choice, True, theme_data['text_color'])
        screen.blit(text, (150, 400))

    
    if ai_img:
        ai_img = pygame.transform.scale(ai_img, image_size)
        
        shadow_surface = pygame.Surface(image_size, pygame.SRCALPHA)
        shadow_surface.fill(COLORS['shadow'])
        screen.blit(shadow_surface, (555, 405))
        screen.blit(ai_img, (550, 400))
        
        pygame.draw.rect(screen, theme_data['accent_color'], 
                        (545, 390, 160, 160), 1, border_radius=10)
    else:
        text = FONT.render(ai_choice, True, theme_data['text_color'])
        screen.blit(text, (550, 400))

    
    player_label = BUTTON_FONT.render("Your Choice", True, theme_data['text_color'])
    ai_label = BUTTON_FONT.render("AI's Choice", True, theme_data['text_color'])
    
    
    player_shadow = BUTTON_FONT.render("Your Choice", True, COLORS['shadow'])
    ai_shadow = BUTTON_FONT.render("AI's Choice", True, COLORS['shadow'])
    screen.blit(player_shadow, (152, image_y + 162))
    screen.blit(ai_shadow, (552, image_y + 162))
    screen.blit(player_label, (150, image_y + 160))
    screen.blit(ai_label, (550, image_y + 160))

    
    result_text = FONT.render(result, True, theme_data['accent_color'])
    result_shadow = FONT.render(result, True, COLORS['shadow'])
    screen.blit(result_shadow, (WIDTH//2 - 98, HEIGHT//2 + 102))
    screen.blit(result_text, (WIDTH//2 - 100, HEIGHT//2 + 100))
    
    save_stats()
    
    
    pygame.display.flip()
    pygame.time.delay(2000)  


def change_theme(new_theme):
    global current_theme, theme_data
    current_theme = new_theme
    theme_data = THEMES[current_theme]
    
    
    click_sound = load_sound('button_click')
    if click_sound:
        click_sound.play()


def main():
    global stats, current_theme
    stats = load_stats()
    clock = pygame.time.Clock()
    running = True

    
    os.makedirs('images', exist_ok=True)
    os.makedirs('sounds', exist_ok=True)
    os.makedirs('images/retro', exist_ok=True)
    os.makedirs('sounds/retro', exist_ok=True)
    os.makedirs('images/hacker', exist_ok=True)
    os.makedirs('sounds/hacker', exist_ok=True)

    while running:
        
        globals()[theme_data['background_func']]()
        
        rock_btn, paper_btn, scissors_btn, theme_buttons, clear_btn = draw_buttons()
        display_stats_table()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                
                if clear_btn.collidepoint((x, y)):
                    stats = {'rounds': 0, 'ties': 0, 'ai_wins': 0, 'player_wins': 0}
                    save_stats()
                    sound = load_sound('button_click')
                    if sound:
                        sound.play()
                    continue
                
                
                for btn, theme_key in theme_buttons:
                    if btn.collidepoint((x, y)):
                        change_theme(theme_key)
                        break
                
                
                if rock_btn.collidepoint((x, y)):
                    player_choice = 'Rock'
                    sound = load_sound('button_click')
                    if sound:
                        sound.play()
                    display_result(player_choice)
                elif paper_btn.collidepoint((x, y)):
                    player_choice = 'Paper'
                    sound = load_sound('button_click')
                    if sound:
                        sound.play()
                    display_result(player_choice)
                elif scissors_btn.collidepoint((x, y)):
                    player_choice = 'Scissors'
                    sound = load_sound('button_click')
                    if sound:
                        sound.play()
                    display_result(player_choice)
                else:
                    continue

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()