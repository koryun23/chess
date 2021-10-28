def get_board():
    board = []
    coords = []

    for i in range(8):
        board.append([])
        for j in range(8):
            if (i+1+j+1) % 2 == 0:
                board[i].append("W")
            else:
                board[i].append("B")
            d = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
            coords.append(d[j]+str(8-i))
    print(coords)
    return board
    