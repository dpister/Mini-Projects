import random


class Board:
    
    def __init__(self):
        self.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
        ]

    def clear_board(self):
        self.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
        ]

    def move(self, direction) -> bool: 
        board_copy = list(map(list, self.board))
        self.remove_empty_spaces(direction)
    
        if direction == "w": # stack equal tiles
            for col in range(4):
                for row in range(3): # top to bottom, upper stacks have priority
                    if self.board[row][col] == self.board[row+1][col]: 
                        self.board[row][col] *= 2
                        self.board[row+1][col] = 0
                        self.remove_empty_spaces(direction)
                        #remove spaces created by stacking
                        
        if direction == "a":
            for row in range(4):
                for col in range(3):
                    if self.board[row][col] == self.board[row][col+1]:
                        self.board[row][col] *= 2
                        self.board[row][col+1] = 0
                        self.remove_empty_spaces(direction)
        
        if direction == "s":
            for col in range(4):
                for row in range(3,0,-1):
                    if self.board[row][col] == self.board[row-1][col]:
                        self.board[row][col] *= 2
                        self.board[row-1][col] = 0
                        self.remove_empty_spaces(direction)
    
        if direction == "d":
            for row in range(4):
                for col in range(3,0,-1):
                    if self.board[row][col] == self.board[row][col-1]:
                        self.board[row][col] *= 2
                        self.board[row][col-1] = 0
                        self.remove_empty_spaces(direction)
        
        return not board_copy == self.board
    
    
    def remove_empty_spaces(self, direction) -> int: 
        # move everything as close to the wall as possible
        
        if direction == "w":
            for col in range(4):
                for row in (2,1,0): # check from bottom to top
                    if self.board[row][col] == 0: # check if space is empty
                        for k in range(row,3): # move up all tiles below
                            self.board[k][col] = self.board[k+1][col] 
                            self.board[k+1][col] = 0
                            
        if direction == "a":
            for row in range(4):
                for col in (2,1,0):
                    if self.board[row][col] == 0:
                        for k in range(col,3):
                            self.board[row][k] = self.board[row][k+1]
                            self.board[row][k+1] = 0
            
        if direction == "s":
            for col in range(4):
                for row in range(1,4):
                    if self.board[row][col] == 0:
                        for k in range(row):
                            self.board[row-k][col] = self.board[row-k-1][col]
                            self.board[row-k-1][col] = 0
                            
        if direction == "d":
            for row in range(4):
                for col in range(1,4):
                    if self.board[row][col] == 0:
                        for k in range(col):
                            self.board[row][col-k] = self.board[row][col-k-1]
                            self.board[row][col-k-1] = 0
                            
                            
    def print_board(self):
        board_to_print = "\n"
        for i in range(4):
            board_to_print += " "
            for j in range(4):
                board_to_print += str(self.board[i][j]) + " "      
            board_to_print += "\n"
        print(board_to_print)
    
    def check_board(self):
        neighbor_check = False
        counter = 0
        for i in range(4):
            for j in range(4):
                if self.board[i][j] > 2047: # checks win
                    return 1
                if self.board[i][j] != 0:
                    counter +=1   
                if j != 3:
                    if self.board[i][j] == self.board[i][j+1]:
                        neighbor_check = True
                    if self.board[j][i] == self.board[j+1][i]:
                        neighbor_check = True    
        if counter == 16 and neighbor_check is False: # checks loss
            return -1
        return 0 # game continues

    def spawn_tile(self):
        mylist = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    mylist.append((i,j))
        i, j = random.choice(mylist)
        self.board[i][j] = 2


def main():
    board = Board()
    board.spawn_tile()
    board.print_board()
    directions = ["w", "s", "a", "d"]
    
    while True:
        direction = input("Pick a direction. w=up/s=down/a=left/d=right\n")   
        if direction not in directions:
            print("Invalid input!")
            continue
        
        moved = board.move(direction)
        if moved:
            board.spawn_tile()
        board.print_board()
        if board.check_board():
            again= ""
            while again != "y" and again != "n":
                if board.check_board() == 1:
                    again = input("You have won! Would you like to play again? y/n\n")
                if board.check_board() == -1:
                    again = input("You lost! Would you like to play again? y/n\n")
            if again == "y":
                board.clear_board()
                board.spawn_tile()
                board.print_board()
            else:
                break
                
                   
if __name__ == "__main__":
    main()