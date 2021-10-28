board = []
for i in range(8):
    board.append([])
    for j in range(8):
        if (i+1+j+1) % 2 == 0:
            board[i].append("B")
        else:
            board[i].append("W")
for row in board:
    print(row)