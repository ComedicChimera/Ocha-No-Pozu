from pygame import BLEND_RGBA_MULT


def draw_color_overlay(screen, color, opacity):
    screen.fill((*color, opacity))


def draw_image_overlay(screen, image, opacity):
    image = image.convert_alpha()
    image.fill((255, 255, 255, opacity), None, BLEND_RGBA_MULT)
    screen.blit(screen, image)
