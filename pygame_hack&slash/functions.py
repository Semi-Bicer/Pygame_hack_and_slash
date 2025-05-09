import os
import pygame

# Sprite loading functions
def load_sprite_sheet(sheet_path, sprite_width, sprite_height, num_sprites):
    sheet = pygame.image.load(sheet_path)
    frames = []
    for i in range(num_sprites):
        frame = sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
        frames.append(frame)
    return frames

def load_individual_sprites(directory_path):
    frames = []

    try:
        # Get all files in the directory
        files = os.listdir(directory_path)
        # Filter for PNG files and sort them
        png_files = sorted([f for f in files if f.lower().endswith('.png')])

        for file_name in png_files:
            file_path = os.path.join(directory_path, file_name)
            frame = pygame.image.load(file_path)
            frames.append(frame)
    except Exception as e:
        print(f"Error loading sprites from {directory_path}: {e}")

    return frames