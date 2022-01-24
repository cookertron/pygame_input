import sys, time
import pygame
from pygame import Rect
from pygame import Vector2
from pygame import gfxdraw
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 128, 0)
LIGHT_GREEN = (0, 255, 0)
DARK_RED = (128, 0, 0)

PALETTE = [0xf7f6db, 0x482632, 0x273635, 0x4d3d2f, 0x933633, 0x316436, 0x825c3a, 0xb95358, 0xc77331, 0x617a6f, 0x7fa533, 0xca9864, 0xafaa94, 0x7dcfa8, 0xe7dc58, 0x1d1819]

pygame.init()
PDR = Rect(0, 0, 1280, 720)
PDS = pygame.display.set_mode(PDR.size, FULLSCREEN | SCALED)

class font:
    def __init__(s, filename, charset, cols, rows=1):
        surface = pygame.image.load(filename).convert_alpha()
        size = surface.get_rect().size
        s.w, s.h = size[0] // cols, size[1] // rows
        s.font = {c:surface.subsurface(((i % cols * s.w, i // cols * s.h), (s.w, s.h))) for i,c in enumerate(charset)}

    def write(s, text, xy=(0,0), color=None, center=False, render=False):
        global PDS

        surface = pygame.Surface((s.w * len(text), s.h))
        surface.set_colorkey((0, 0, 0))
        for i,c in enumerate(text):
            surface.blit(s.font[c], (i * s.w, 0))
        if color:
            surface.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        if not render:
            PDS.blit(surface, xy)
        else:
            return surface

    def input(s, xy, win_width, max_length, title, title_color, text_color, win_color, cursor="_", centered=False):
        global PDS

        pos = Vector2(xy) if not centered else Vector2(xy) - (win_width / 2, 0)
        win_rect = Rect(pos, (win_width, s.h * 2 + 6))
        win_background = pygame.Surface(win_rect.size)
        win_background.blit(PDS, (0, 0), win_rect)

        pygame.draw.rect(PDS, win_color, win_rect)
        s.write(title, pos + (2, 2), title_color)
        pygame.display.update(win_rect)

        textarea_text_pos = pos + (2, 12)
        textarea_rect = Rect(textarea_text_pos, (win_rect.w - 4, 8))

        cursor_timestamp = time.time()
        cursor_visible = 1

        input_text = ""

        exit_input = False
        return_input = True

        while not exit_input:
            events = pygame.event.get()
            for event in events:
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        exit_input = True
                        return_input = False
                    if event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    if event.key == K_RETURN and len(input_text) > 0:
                        exit_input = True
                if event.type == KEYDOWN:
                    key = event.unicode
                    if key in s.font and len(input_text) < max_length:
                        input_text += key

            now = time.time()
            if now - cursor_timestamp >= 0.5:
                cursor_visible = 1 - cursor_visible
                cursor_timestamp = now
            
            pygame.draw.rect(PDS, win_color, textarea_rect)

            if cursor_visible:
                s.write(input_text + "_", textarea_text_pos, text_color)
            else:
                s.write(input_text, textarea_text_pos, text_color)
            pygame.display.update(textarea_rect)
        
        PDS.blit(win_background, win_rect.topleft)

        if return_input:
            return input_text
        return None

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()~*+,-./_:^[\];<=>?{|} "
FONT = font("font.png", CHARSET, 26, 4)

polygon = [PDR.topleft, PDR.topright, PDR.bottomright, PDR.bottomleft]

text = FONT.input(PDR.center, 600, 20, "Enter some text:", PALETTE[0], PALETTE[8], PALETTE[1], centered=True)
if not text:
    pygame.quit()
    sys.exit()

text_surface = FONT.write(text, color=PALETTE[4], render=True)
new_size = Vector2(text_surface.get_rect().size) * 5
scaled_text_surface = pygame.transform.scale(text_surface, (int(new_size.x), int(new_size.y)))

pygame.gfxdraw.textured_polygon(PDS, polygon, scaled_text_surface, 0, 0)
pygame.display.update()

texture_offset = Vector2(0)

exit_demo = False
while not exit_demo:
    events = pygame.event.get()
    for event in events:
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                exit_demo = True
    
    PDS.fill(PALETTE[1])
    mr = pygame.mouse.get_rel()
    texture_offset -= mr
    pygame.gfxdraw.textured_polygon(PDS, polygon, scaled_text_surface, int(texture_offset.x), int(texture_offset.y))
    pygame.display.update()
pygame.quit()