import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *



def draw_cube():
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )

    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    )

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_menu():
    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to start the game", True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 300))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 800, 600))
    screen.blit(text, text_rect.center)

def main():
    global screen

    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    xMove = 0
    yMove = 0
    mouse_down = False

    menu_active = True

    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_active = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_menu()
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 indicates the left mouse button
                    mouse_down = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 1 indicates the left mouse button
                    mouse_down = False

            if event.type == pygame.MOUSEMOTION and mouse_down:
                i, j = event.rel
                xMove = i / 2
                yMove = j / 2
                glRotatef(1, yMove, xMove, 0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if not menu_active:
            draw_cube()
            
        pygame.display.flip()
        pygame.time.wait(10)
    


if __name__ == "__main__":
    main() 
