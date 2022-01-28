class Sudoku:
    
    def __init__(self, grid):
        self.grid = grid
        self.row = 0
        self.col = 0
        
    def edit_cell(self, new):
        self.grid[self.row][self.col] = new
        
    def read_cell(self):
        return self.grid[self.row][self.col]
        
    def iscorrect(self) -> bool:
        digit = self.grid[self.row][self.col]
        myrow = self.grid[self.row]
        mycol = []
        mybox = []
        for i in range(9):
            mycol.append(self.grid[i][self.col])
            mybox.append(self.grid[self.row - self.row%3 + i//3][self.col - self.col%3 + i%3])
        
        return not (myrow.count(digit) > 1 or mycol.count(digit) > 1 
                    or mybox.count(digit) > 1)
    
    def last_cell(self):
         self.row = self.row + (self.col - 1) // 9
         self.col = (self.col - 1) % 9   

    def next_cell(self):
        self.row = self.row  + (self.col + 1) // 9
        self.col = (self.col + 1) % 9
    

def main():
    grid1 = [
        [5,1,6, 8,4,9, 7,3,2],
        [3,0,7, 6,0,5, 0,0,0],
        [8,0,9, 7,0,0, 0,6,5],
        
        [1,3,5, 0,6,0, 9,0,7],
        [4,7,2, 5,9,1, 0,0,6],
        [9,6,8, 3,7,0, 0,5,0],
        
        [2,5,3, 1,8,6, 0,7,4],
        [6,8,4, 2,0,7, 5,0,0],
        [7,9,1, 0,5,0, 6,0,8],
    ] # no solution
    
    grid2 = [
        [0,0,0, 8,0,1, 0,0,0],
        [0,0,0, 0,0,0, 0,4,3],
        [5,0,0, 0,0,0, 0,0,0],
        
        [0,0,0, 0,7,0, 8,0,0],
        [0,0,0, 0,0,0, 1,0,0],
        [0,2,0, 0,3,0, 0,0,0],
        
        [6,0,0, 0,0,0, 0,7,5],
        [0,0,3, 4,0,0, 0,0,0],
        [0,0,0, 2,0,0, 6,0,0],
    ] # barely solvable ~ 15 mins
    
    grid3 = [
        [0,0,0, 8,0,0, 0,0,0],
        [7,8,9, 0,1,0, 0,0,6],
        [0,0,0, 0,0,6, 1,0,0],
        
        [0,0,7, 0,0,0, 0,5,0],
        [5,0,8, 7,0,9, 3,0,4],
        [0,4,0, 0,0,0, 2,0,0],
        
        [0,0,3, 2,0,0, 0,0,0],
        [8,0,0, 0,7,0, 4,3,9],
        [0,0,0, 0,0,1, 0,0,0],
    ] # doable
    
    sudoku = Sudoku(grid3)    
    for row in sudoku.grid:
        print(row)
    print("")
    
    fixed_cells = []
    for i in range(9):
        for j in range(9):
            if sudoku.grid[i][j] != 0:
                fixed_cells.append((i,j))

    # find the first empty cell and plug in 1
    while (sudoku.row, sudoku.col) in fixed_cells:
        sudoku.next_cell()
    sudoku.edit_cell(sudoku.read_cell() + 1)
        
    while True: 
        
        # if rules aren't violated, move to the next cell
        if sudoku.iscorrect():
            # reached the end of the sudoku: solution found
            if sudoku.row == sudoku.col == 8:
                print("Solution found:")
                for row in sudoku.grid:
                    print(row)
                print("")
                return
            
            sudoku.next_cell()
            # if cell is empty, plug in 1
            if sudoku.read_cell() == 0:
                sudoku.edit_cell(sudoku.read_cell() + 1)
       
        else:
            # rules are violated, try to go to previous cell
            while True:  
                #cell is fixed
                if (sudoku.row, sudoku.col) in fixed_cells:
                    if sudoku.row == sudoku.col == 0: # check if can't go back
                        print("No solution found!")
                        return
                    sudoku.last_cell()
                
                # tried every possible digit
                elif sudoku.read_cell() == 9:
                    if sudoku.row == sudoku.col == 0: # check if can't go back
                        print("No solution found!")
                        return
                    sudoku.edit_cell(0)
                    sudoku.last_cell()
                else:
                    # try the next digit
                    sudoku.edit_cell(sudoku.read_cell() + 1)
                    break


if __name__ == "__main__":
    main()