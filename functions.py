#functionts.py
import os
import pygame
import constants

def load_sprite_sheet(sheet_path, sprite_width, sprite_height, num_sprites):
    sheet = pygame.image.load(sheet_path).convert_alpha()
    frames = []
    for i in range(num_sprites):
        frame = sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
        frames.append(frame)
    return frames

def load_individual_sprites(directory_path):
    frames = []
    try:
        files = os.listdir(directory_path)
        png_files = sorted([f for f in files if f.lower().endswith('.png')])
        for file_name in png_files:
            file_path = os.path.join(directory_path, file_name)
            frame = pygame.image.load(file_path).convert_alpha()
            frames.append(frame)
    except Exception as e:
        print(f"Error loading sprites from {directory_path}: {e}")
    return frames

def load_and_scale_sheet(sheet_path, sprite_width, sprite_height, num_sprites, scale=constants.scale):
    frames = load_sprite_sheet(sheet_path, sprite_width, sprite_height, num_sprites)
    scaled_frames = []
    for frame in frames:
        original_width = frame.get_width()
        original_height = frame.get_height()
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        scaled_frame = pygame.transform.scale(frame, (new_width, new_height))
        scaled_frames.append(scaled_frame)
    return scaled_frames

def draw_health_bar(surface, x, y, health, maxHealth, width=100):
    barHeight = 10
    fill = (health / maxHealth) * width
    border_rect = pygame.Rect(x, y, width, barHeight)
    fill_rect = pygame.Rect(x, y, fill, barHeight)
    pygame.draw.rect(surface, (255, 0, 0), fill_rect)
    pygame.draw.rect(surface, (255, 255, 255), border_rect, 2)

def load_single_image(image_path, scale=1.0):
    frames = []
    try:
        image = pygame.image.load(image_path).convert_alpha()
        if scale != 1.0:
            width = int(image.get_width() * scale)
            height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (width, height))
        frames.append(image)
    except Exception as e:
        print(f"Error loading image from {image_path}: {e}")
    return frames

def draw_start_menu(win, constants, fonts):
    """Samuray temalı başlangıç menüsü"""
    win.fill((20, 0, 0))
    pygame.draw.rect(win, (40, 0, 0), (0, constants.screenHeight // 2, constants.screenWidth, constants.screenHeight // 2))

    title_text = fonts["large"].render("SHADOW FIGHT", True, (255, 215, 0))
    title_shadow = fonts["large"].render("SHADOW FIGHT", True, (100, 0, 0))
    win.blit(title_shadow, (constants.screenWidth // 2 - title_text.get_width() // 2 + 3, 100 + 3))
    win.blit(title_text, (constants.screenWidth // 2 - title_text.get_width() // 2, 100))

    subtitle_text = fonts["medium"].render("İki Kılıcın Kader Savaşı", True, (200, 200, 200))
    win.blit(subtitle_text, (constants.screenWidth // 2 - subtitle_text.get_width() // 2, 180))

    btn_width, btn_height = 300, 60
    btn_x = constants.screenWidth // 2 - btn_width // 2
    btn_y = constants.screenHeight // 2 + 50

    pygame.draw.rect(win, (100, 0, 0), (btn_x + 5, btn_y + 5, btn_width, btn_height))
    mouse_pos = pygame.mouse.get_pos()
    btn_hover = pygame.Rect(btn_x, btn_y, btn_width, btn_height).collidepoint(mouse_pos)
    btn_color = (180, 0, 0) if not btn_hover else (220, 0, 0)
    pygame.draw.rect(win, btn_color, (btn_x, btn_y, btn_width, btn_height))
    pygame.draw.rect(win, (255, 215, 0), (btn_x, btn_y, btn_width, btn_height), 3)

    btn_text = fonts["medium"].render("Savaşa Başla", True, constants.WHITE)
    win.blit(btn_text, (constants.screenWidth // 2 - btn_text.get_width() // 2, btn_y + btn_height // 2 - btn_text.get_height() // 2))

    info_text = fonts["small"].render("WASD: Hareket | F: Saldırı | V: Shuriken | L-Shift: Dash", True, (150, 150, 150))
    win.blit(info_text, (constants.screenWidth // 2 - info_text.get_width() // 2, constants.screenHeight - 50))

    pygame.draw.polygon(win, (80, 80, 80), [(50, 300), (100, 200), (150, 300)])
    pygame.draw.polygon(win, (80, 80, 80), [(constants.screenWidth - 50, 300), (constants.screenWidth - 100, 200), (constants.screenWidth - 150, 300)])

    return pygame.Rect(btn_x, btn_y, btn_width, btn_height)
