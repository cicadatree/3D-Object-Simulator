from __future__ import annotations
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Window:
    def __init__(self):
        pygame.init()
        self.display = (800, 600)
        self.screen = pygame.display.set_mode(self.display)
        
    def draw_menu(self):
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("Press SPACE to start the game", True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(400, 300))
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 800, 600))
        self.screen.blit(self.text, self.text_rect.topleft)


class Shape:
    def __init__(self):
        pass

    def draw_shape(self):
        pass


class Cube(Shape):
    def __init__(self):
        super().__init__()

    def draw_shape(self):
        self.vertices = (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1)
        )

        self.edges = (
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
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()


def main():
    cube_1 = Cube()
    window = Window()
    menu_active = True

    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_active = False

        window.screen.fill((0, 0, 0))  # Fill the screen with black
        window.draw_menu()
        pygame.display.flip()

    window.screen = pygame.display.set_mode(window.display, DOUBLEBUF|OPENGL)  # Switch to an OpenGL context

    gluPerspective(45, (window.display[0] / window.display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    xMove = 0
    yMove = 0
    mouse_down = False

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
                glRotatef(2, yMove, xMove, 0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        cube_1.draw_shape()
        pygame.display.flip()
        pygame.time.wait(10)



if __name__ == "__main__":
    main() 
