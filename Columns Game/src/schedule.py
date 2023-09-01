import pygame


def _draw_text(surface: pygame.Surface, font: pygame.font.SysFont, text: str) -> None:
    text_image = font.render(text, True, pygame.Color(255, 255, 255))
    surface.blit(text_image, (10, 10))


def run() -> None:
    pygame.init()

    try:
        surface = pygame.display.set_mode((600, 600))
        font = pygame.font.SysFont(None, 24)
        clock = pygame.time.Clock()

        running = True

        while running:
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            surface.fill(pygame.Color(128, 128, 128))

            _draw_text(surface, font, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            
            pygame.display.flip()

    finally:
        pygame.quit()


if __name__ == '__main__':
    run()
