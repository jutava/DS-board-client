import requests
import json

WIDTH =  50
HEIGHT = 50
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
    state = 0

    c_Pos_Screen = [0, 0]

    try:
        state = getCurrentBoard(state)
    except ValueError:
        print("Could not connect with server.")


    while True:

        option = input("(1) for insert, (2) refresh board: ")

        if int(option) == 1:
            x = input("Give X coordinate (0-99): ")
            y = input("Give Y coordinate (0-99): ")
            print(COLORS)

            if int(x) < 100 and int(y) < 100:
                color = input("Type color of your choosing: ")
                print("------")
                if postNewChange(state, int(x), int(y), color):
                    board[int(x)][int(y)] = color
                    state += 1
                    print("Boards was updated with: ", int(x), " ", int(y), "COLOR: ", color)
                else:
                    state = getCurrentBoard(state)
                    print("Board was outdated, try again!")
        elif int(option) == 2:
            state = getCurrentBoard(state)
        else:
            print("Invalid input, try again!")


def getCurrentBoard(state):
    
    payload = {"state" : state}
    r = requests.get(url = URL, params=payload)
    if r.status_code == 200:
        # Dunno why this needs to be done twice xd
        r_dict = json.loads(r.text)
        r_dict = json.loads(r_dict)
        if "is_whole_board" in r_dict:
            for s in r_dict.keys():
                if s != "is_whole_board":
                    for x in range(WIDTH):
                        for y in range(HEIGHT):
                            if board[x][y] != r_dict[s]:
                                board[x][y] = r_dict[s][x][y]
                    return int(s)
        
        elif not r_dict:
            return state

        else:
            s = int(max(list(r_dict.keys())))
            for k in list(r_dict.keys()):
                board[r_dict[k]['x']][r_dict[k]['y']] = r_dict[k]['color']
            return s            

            
    else:
        print("open broker")

def postNewChange(state, x, y, color):
    data = {
        "state" : state,
        "x" : x,
        "y" : y,
        "color" : color
    }

    URL = 'http://localhost:8080'
    r = requests.post(url = URL, data=json.dumps(data))
    if r.status_code == 200:
        return True
    else:
        return False
    
    

main()