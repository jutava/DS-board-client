import pygame
import requests
import json

WIDTH =  400
HEIGHT = 400
margin = 5

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

URL = 'http://localhost:8080'
DEBUG = True 


COLORS = {
    "WHITE" : (200, 200, 200),
    "BLACK" : (0, 0, 0),
    "RED" : (255, 0, 0),
    "ORANGE" : (255, 128, 0),
    "YELLOW" : (255, 255, 0),
    "GREEN" : (128, 255, 0),
    "GREEN_1" : (0, 255, 0),
}

board = [ ["WHITE"] * 500 for i in range(500) ]

def main():
    '''
    Main loop of the game
    '''
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((HEIGHT, WIDTH))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    count = 0

    board[1][1] = "BLACK"
    board[2][2] = "RED"
    board[3][3] = "ORANGE"
    board[4][4] = "YELLOW"
    board[499][499] = "GREEN"
    while True:
        # SCREEN.fill(WHITE)
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed:
                print(count)
                count += 1

        pygame.display.update()

def drawGrid():
    size = 20
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            rect = pygame.Rect(x * size + 1, y * size + 1,
                    size, size)
            # image = pygame.Surface(20, 20)
            # image.fill(WHITE, rect)

            pygame.draw.rect(SCREEN, board[x][y], rect, 0)
            pygame.draw.rect(SCREEN, "BLACK", rect, 1)
            # fillArea(x, y, board[x][y])

        
        pygame.draw.rect(SCREEN, board[x][y], rect, 1)

def getCurrentBoard(state):
    
    r = requests.get(url = URL + '?state=' + state)
    r.status_code

def postNewChange(state, x, y, color):

    data = {
        "state" : state,
        "x" : x,
        "y" : y,
        "color" : color
    }

    URL = 'http://localhost:8080'
    r = requests.post(url = URL, data=json.dumps(data))
    print(r)
    

main()