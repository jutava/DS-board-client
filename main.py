import pygame
import requests
import json

WIDTH =  100
HEIGHT = 100
margin = 5
SIZE = 10

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

board = [ ["WHITE"] * WIDTH for i in range(HEIGHT) ]

def main():
    '''
    Main loop of the game
    '''
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode(((HEIGHT * SIZE) + 100, WIDTH * SIZE))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    count = 0

    c_Pos_Screen = [0, 0]
    c_Pos_Panel = [1040, 100]
    s_Color = "BLACK"

    mode = True
    while True:
        drawColorPanel()
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                button = pygame.key.name(event.key)
                if button == "x" or button == "X":
                    if mode:
                        print(len(COLORS))
                        colors_List = list(COLORS.keys())
                        i = (c_Pos_Panel[1] - 100) / (SIZE * 2)
                        s_Color = colors_List[int(i)]
                        mode = not mode
                    else:
                        x_C, y_C = turnCoordsToIndex(c_Pos_Screen[0], c_Pos_Screen[1])
                        board[x_C][y_C] = s_Color 
                        print("Sending")

                if button == "p" or button == "P":
                    mode = not mode
                elif button == "up":
                    if mode:
                        if c_Pos_Panel[1] > 100:
                            c_Pos_Panel[1] -= SIZE * 2
                    else:
                        if c_Pos_Screen[1] > 0:
                            c_Pos_Screen[1] -= SIZE
                elif button == "down":
                    if mode:
                        if c_Pos_Panel[1] < 220:
                            c_Pos_Panel[1] += SIZE * 2
                    else:
                        if c_Pos_Screen[1] < 990:
                            c_Pos_Screen[1] += SIZE
                elif button == "left":
                    if not mode:
                        if c_Pos_Screen[0] > 0:
                            c_Pos_Screen[0] -= SIZE

                elif button == "right":
                    if not mode:
                        if c_Pos_Screen[0] < 990:
                            c_Pos_Screen[0] += SIZE
                
                print("Screen: ", c_Pos_Screen)
                print("Panel: ", c_Pos_Panel)

        drawCursors(c_Pos_Panel, c_Pos_Screen, s_Color)
        pygame.display.update()


def turnCoordsToIndex(x, y):
    i_x = x / SIZE
    i_y = y / SIZE
    return int(i_x), int(i_y)

def drawCursors(c_Panel, c_Screen, s_Color):
    '''
    function draws cursor
    '''
    rect = pygame.Rect(c_Panel[0], c_Panel[1], SIZE * 2, SIZE * 2)
    pygame.draw.rect(SCREEN, "PINK", rect, 3)

    rect = pygame.Rect(c_Screen[0], c_Screen[1], SIZE, SIZE)
    pygame.draw.rect(SCREEN, COLORS[s_Color], rect, 0)
    pygame.draw.rect(SCREEN, "PINK", rect, 3)

def drawColorPanel():
    values = COLORS.values()
    values_list = list(values)
    for c in range(len(values)):
        rect = pygame.Rect( WIDTH * SIZE + 40, 100 + (c * SIZE * 2), SIZE * 2, SIZE * 2)
        pygame.draw.rect(SCREEN, values_list[c], rect, 0)
        pygame.draw.rect(SCREEN, "WHITE", rect, 1)

def drawGrid():
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            rect = pygame.Rect(x * SIZE + 1, y * SIZE + 1,
                    SIZE, SIZE)

            pygame.draw.rect(SCREEN, COLORS[board[x][y]], rect, 0)
            pygame.draw.rect(SCREEN, "BLACK", rect, 1)


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