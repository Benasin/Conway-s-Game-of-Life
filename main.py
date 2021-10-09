import pygame
from pygame.locals import *
pygame.init()

width = 900
height = 900

def create_window(width, height):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game of life")
    return screen

class Cell(object):
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.isAlive = False
        self.willLive = False
    def color(self, color, screen):
        pygame.draw.rect(screen, (color), (self.x_pos * 20, self.y_pos * 20, 20, 20))
        pygame.draw.rect(screen, (0,0,0), (self.x_pos * 20, self.y_pos * 20, 20, 20), 1)
    def check_env(self, grid, col, row):
        alive_neighbor_num = 0
        if self.x_pos < col - 1:
            alive_neighbor_num += grid[self.x_pos + 1][self.y_pos].isAlive
        if self.x_pos > 0: 
            alive_neighbor_num += grid[self.x_pos - 1][self.y_pos].isAlive
        if self.y_pos < row - 1:
            alive_neighbor_num += grid[self.x_pos][self.y_pos + 1].isAlive
        if self.y_pos > 0:
            alive_neighbor_num += grid[self.x_pos][self.y_pos - 1].isAlive
        if self.x_pos < (col - 1) and self.y_pos > 0:
            alive_neighbor_num += grid[self.x_pos + 1][self.y_pos - 1].isAlive
        if self.x_pos > 0 and self.y_pos > 0:
            alive_neighbor_num += grid[self.x_pos - 1][self.y_pos - 1].isAlive
        if self.x_pos > 0 and self.y_pos < (row - 1):
            alive_neighbor_num += grid[self.x_pos - 1][self.y_pos + 1].isAlive
        if self.x_pos < (col - 1) and self.y_pos < (row - 1):
            alive_neighbor_num += grid[self.x_pos + 1][self.y_pos + 1].isAlive
        print(alive_neighbor_num)
        if self.isAlive:
            if alive_neighbor_num < 2 or alive_neighbor_num > 3:
                self.willLive = False
            else:
                self.willLive = True
        elif not self.isAlive:
            if alive_neighbor_num == 3:
                self.willLive = True
            else:
                self.willLive = False



def main():
    global width, height
    screen = create_window(width, height)
    col = width // 20 + 1
    row = height // 20 + 1
    grid = []
    running = False
    dragging_draw = False
    dragging_erase = False
    clock=pygame.time.Clock()
    for i in range(col):
        container = []
        for j in range(row):
            container.append(Cell(i, j))
        grid.append(container)
    for i in range(col):
        for j in range(row):
            grid[i][j].color((255,255,255), screen)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            x, y = pygame.mouse.get_pos()
            x_index = round(abs(x) / 20 + 0.5) - 1
            y_index = round(abs(y) / 20 + 0.5) - 1
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 3: #Erase on right click
                    if grid[x_index][y_index].isAlive:
                        grid[x_index][y_index].isAlive = False
                        grid[x_index][y_index].color((255,255,255), screen)
                        dragging_erase = True
                elif event.button == 1: #Add cell on left click
                    if not grid[x_index][y_index].isAlive:
                        grid[x_index][y_index].isAlive = True
                        grid[x_index][y_index].color((0,0,0), screen)
                        dragging_draw = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_draw = False
                elif event.button == 3:
                    dragging_erase = False
            elif event.type == pygame.MOUSEMOTION: #Add dragging effect
                if dragging_draw and not grid[x_index][y_index].isAlive:
                    grid[x_index][y_index].color((0,0,0), screen)
                    grid[x_index][y_index].isAlive = True
                elif dragging_erase and grid[x_index][y_index].isAlive:
                    grid[x_index][y_index].isAlive = False
                    grid[x_index][y_index].color((255,255,255),screen)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    running = not running 
                elif event.key == pygame.K_r:
                    main()
        if running:
            for i in range(col):
                for j in range(row):
                    grid[i][j].check_env(grid, col, row)
            for i in range(col):
                for j in range(row):
                    if grid[i][j].willLive == False:
                        grid[i][j].isAlive = False
                        grid[i][j].color((255,255,255), screen)
                    else:
                        grid[i][j].isAlive = True
                        grid[i][j].color((0,0,0), screen)
            clock.tick(15)
        pygame.display.update()
if __name__ == '__main__':
    main()
