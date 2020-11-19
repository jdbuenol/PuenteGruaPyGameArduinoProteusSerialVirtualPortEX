import serial, sys, pygame
from typing import Tuple
from time import sleep
from random import randint

size : Tuple[int, int] = 600, 700
black : Tuple[int, int, int] = 0, 0, 0

screen : pygame.Surface = pygame.display.set_mode(size)

square : pygame.Surface = pygame.image.load("square.png")
bridge : pygame.Surface = pygame.image.load("puente.png")
claw : pygame.Surface = pygame.image.load("gancho.png")
box : pygame.Surface = pygame.image.load("caja.png")
box_selected : pygame.Surface = pygame.image.load("caja2.png")
rope : pygame.Surface = pygame.image.load("cuerda.png")

def print_matrix(matrix, grabbing):
    screen.fill(black)
    for x in range(20):
        for y in range(20):
            screen.blit(square, [x * 30, y * 30 + 100])
    
    screen.blit(bridge, [0, 0])
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if matrix[x][y] == 'c':
                screen.blit(claw, [(y - 1) * 30, (x - 1) * 30 + 100])
            elif matrix[x][y] == '▄':
                screen.blit(box, [(y - 1) * 30, (x - 1) * 30 + 100])
            elif matrix[x][y] == '|':
                screen.blit(rope, [(y - 1) * 30, (x - 1) * 30 + 100])
            elif matrix[x][y] == '®':
                screen.blit(box_selected, [(y - 1) * 30, (x - 1) * 30 + 100])
    pygame.display.flip()

def support_crane(old_crane_pos, new_crane_pos, matrix, grabbing, n_char):
    pos_x = old_crane_pos[0]
    pos_y = old_crane_pos[1]
    matrix[0][pos_y] = "-"
    matrix[0][pos_y - 1] = "-"
    matrix[0][pos_y + 1] = "-"
    for x in range(1, pos_x + 1):
        matrix[x][pos_y] = " "
    pos_x = new_crane_pos[0]
    pos_y = new_crane_pos[1]
    matrix[0][pos_y] = "="
    matrix[0][pos_y + 1] = ">"
    matrix[0][pos_y - 1] = "<"
    for x in range(1, pos_x):
        matrix[x][pos_y] = "|"
    matrix[pos_x][pos_y] = n_char

def updates_crane_pos(old_crane_pos, new_crane_pos, matrix, grabbing):
    if grabbing:
        support_crane(old_crane_pos, new_crane_pos, matrix, grabbing, '®')
    else:
        if old_crane_pos[0] + 1 == new_crane_pos[0]:
            if matrix[new_crane_pos[0]][new_crane_pos[1]] == '▄':
                support_crane(old_crane_pos, new_crane_pos, matrix, grabbing, '▄')
            else:
                support_crane(old_crane_pos, new_crane_pos, matrix, grabbing, 'c')
        elif old_crane_pos[0] - 1 == new_crane_pos[0]:
            if matrix[old_crane_pos[0]][old_crane_pos[1]] == '▄':
                support_crane(old_crane_pos, new_crane_pos, matrix, grabbing, 'c')
                matrix[old_crane_pos[0]][old_crane_pos[1]] = '▄'
            else:
                support_crane(old_crane_pos, new_crane_pos, matrix, grabbing, 'c')
        elif old_crane_pos[0] == new_crane_pos[0] and old_crane_pos[1] == new_crane_pos[1] and matrix[old_crane_pos[0]][old_crane_pos[1]] == '®':
            support_crane(old_crane_pos, new_crane_pos, matrix, grabbing, '▄')
        else:
            support_crane(old_crane_pos, new_crane_pos, matrix, grabbing, 'c')
    
def generate_boxes(matrix):
    for x in range(2, 20):
        for y in range(randint(15, 21), 21):
            matrix[y][x] = '▄'

if __name__ == '__main__':
    pygame.init()
    arduino = serial.Serial('COM4', 9600)
    crane_pos = (1, 1)
    grabbing = False
    print("opening...")
    matrix = []
    for _ in range(22):
        matrix.append([])
    matrix[0].append(" ")
    for _ in range(20):
        matrix[0].append("-")
    matrix[0].append(" ")
    matrix[-1].append(" ")
    for _ in range(20):
        matrix[-1].append("-")
    matrix[-1].append(" ")
    for x in range(1, 21):
        matrix[x].append("|")
        for _ in range(20):
            matrix[x].append(" ")
        matrix[x].append("|")
    sleep(1)
    updates_crane_pos(crane_pos, crane_pos, matrix, grabbing)
    generate_boxes(matrix)
    print_matrix(matrix, grabbing)
    while 1:
        print(crane_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        print_matrix(matrix, grabbing)
        dato_leido = str(arduino.readline())
        if "STRETCH" in dato_leido:
            while(matrix[crane_pos[0] + 1][crane_pos[1]] != "-" and matrix[crane_pos[0]][crane_pos[1]] != "▄"):
                if grabbing and matrix[crane_pos[0] + 1][crane_pos[1]] == "▄":
                    break
                crane_pos = (crane_pos[0] + 1, crane_pos[1])
                updates_crane_pos((crane_pos[0] - 1, crane_pos[1]), crane_pos, matrix, grabbing)
                print_matrix(matrix, grabbing)
                sleep(0.1)
        if "LEFT" in dato_leido:
            if crane_pos[1] > 1 and matrix[crane_pos[0]][crane_pos[1] - 1] != '▄':
                crane_pos
                crane_pos = (crane_pos[0], crane_pos[1] - 1)
                updates_crane_pos((crane_pos[0], crane_pos[1] + 1), crane_pos, matrix, grabbing)
                print_matrix(matrix, grabbing)
        if "RIGHT" in dato_leido:
            if crane_pos[1] < 20 and matrix[crane_pos[0]][crane_pos[1] + 1] != '▄':
                crane_pos = (crane_pos[0], crane_pos[1] + 1)
                updates_crane_pos((crane_pos[0], crane_pos[1] - 1), crane_pos, matrix, grabbing)
                print_matrix(matrix, grabbing)
        if "COLLAPSE" in dato_leido:
            while(crane_pos[0] != 1):
                crane_pos = (crane_pos[0] - 1, crane_pos[1])
                updates_crane_pos((crane_pos[0] + 1, crane_pos[1]), crane_pos, matrix, grabbing)
                print_matrix(matrix, grabbing)
                sleep(0.1)
        if "PICK" in dato_leido:
            if not grabbing and matrix[crane_pos[0]][crane_pos[1]] == '▄':
                grabbing = True
            elif grabbing and crane_pos[0] > 2 and (matrix[crane_pos[0] + 1][crane_pos[1]] == '▄' or matrix[crane_pos[0] + 1][crane_pos[1]] == '-'):
                grabbing = False
            updates_crane_pos(crane_pos, crane_pos, matrix, grabbing)
            print_matrix(matrix, grabbing)
            sleep(0.5)
        if "EXIT" in dato_leido:
            break
    print("Execution finished...")