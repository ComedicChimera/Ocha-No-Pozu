from util import HEIGHT


def draw_sprite(screen, entity):
    sprite = entity.sprite()
    screen.blit(sprite.convert(), (entity.position.x, HEIGHT - entity.position.y - entity.dimensions().y))
    return screen
