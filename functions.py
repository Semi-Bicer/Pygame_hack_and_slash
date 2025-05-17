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

# Menu functionality moved to menu.py
