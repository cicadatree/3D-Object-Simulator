import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Window:
    def __init__(self):
        pygame.init()
        self.font_size = 24
        self.display = (800, 600)
        self.screen = pygame.display.set_mode(self.display)
        self.font = pygame.font.Font(None, self.font_size)
        
    def draw_menu(self, events):
        self.screen.fill((255, 255, 255))
        action1 = self.draw_button("Render Cube", (275, 250, 250, 50), 1, events)
        action2 = self.draw_button("Render Triangular Prism", (275, 320, 250, 50), 2, events)
        return action1 or action2
        
    def draw_button(self, text, rect, action_id, events):
        # Draw button and text
        button = pygame.draw.rect(self.screen, (0, 128, 255), rect)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button.center)
        self.screen.blit(text_surface, text_rect)

        # Check for clicks
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button.collidepoint(event.pos):
                    return action_id

class Shape:
    def __init__(self):
        pass

    def draw_shape(self):
        pass


class Cube(Shape):
    def __init__(self):
        super().__init__()
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

    def draw_shape(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()


class TriangularPrism(Shape):
    def __init__(self):
        super().__init__()
        self.vertices = (
            (1, -1, -1),  # A: Bottom triangle
            (0, -1, 1),   # B
            (-1, -1, -1), # C
            (1, 1, -1),   # A': Top triangle
            (0, 1, 1),    # B'
            (-1, 1, -1)   # C'
        )

        # Defining the edges
        self.edges = (
            (0, 1),  # Bottom triangle edges
            (1, 2),
            (2, 0),
            (3, 4),  # Top triangle edges
            (4, 5),
            (5, 3),
            (0, 3),  # Edges connecting bottom and top triangles
            (1, 4),
            (2, 5)
        )

    def draw_shape(self):
        # Drawing the shape using OpenGL
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()


def main():
    cube_1 = Cube()
    triangular_prism_1 = TriangularPrism()
    window = Window()
    menu_active = True
    selected_shape = None

    while menu_active:
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        action = window.draw_menu(events)
        pygame.display.flip()
        
        if action == 1:
            selected_shape = cube_1
            menu_active = False
        elif action == 2:
            selected_shape = triangular_prism_1
            menu_active = False

        pygame.time.wait(10)

    window.screen = pygame.display.set_mode(window.display, DOUBLEBUF|OPENGL)  # Switch to an OpenGL context

    gluPerspective(45, (window.display[0] / window.display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    xMove = 0
    yMove = 0
    left_mouse_button_down = False  # Initialize outside of the loop

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 indicates the left mouse button
                    left_mouse_button_down = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 1 indicates the left mouse button
                    left_mouse_button_down = False

            if event.type == pygame.MOUSEMOTION and left_mouse_button_down:
                i, j = event.rel
                xMove = i / 2
                yMove = j / 2
                glRotatef(2, yMove, xMove, 0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        selected_shape.draw_shape()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
