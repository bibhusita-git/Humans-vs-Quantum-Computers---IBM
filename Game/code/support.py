import pygame
from os import walk

def import_folder(path):
    
    surface_list = []

    for _, __, img_files in walk(path): # walk return a tupple of three items: dir_path, dir_name, a list of files in that dir. _ = dirpath, __ = dirname; we are using _, __ to denote these just to show that we don't care what these are and we don't need them, we can use any name instead of _, __
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    
    return surface_list