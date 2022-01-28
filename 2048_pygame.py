import pygame
game = __import__('2048')
import math

pygame.font.init()

WIDTH = 600
HEIGHT = (5*WIDTH) // 4
FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
CELL_SIZE = WIDTH//6
FONT = pygame.font.SysFont("Arial", CELL_SIZE//3)
END_FONT = pygame.font.SysFont("Arial", WIDTH//6)


class Button:
    
    def __init__(self, text, pos):
        self.x, self.y = pos
        self.text = FONT.render(text, 1, (255,255,255))
        self.width = 2*CELL_SIZE + CELL_SIZE//3
        self.height = CELL_SIZE
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255,0,0)
        
    def check_clicked(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False
            
    def draw(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)
        WINDOW.blit(
            self.text, 
            (self.x + (self.width - self.text.get_width())//2,
             self.y + (self.height - self.text.get_height())//2)
        )
        

def cell_pos(row, col):
    return (CELL_SIZE//2 + (CELL_SIZE+CELL_SIZE//3) * col, 
            CELL_SIZE//2 + (CELL_SIZE+CELL_SIZE//3) * row)


EMPTY_BOARD = []
for row in range(4):
    for col in range(4):
        empty_cell = pygame.Rect(*cell_pos(row, col), CELL_SIZE, CELL_SIZE)
        EMPTY_BOARD.append(empty_cell)


def draw_window(board, buttons):
    WINDOW.fill((255,255,255))
    for i, cell in enumerate(EMPTY_BOARD):
        row, col = i//4, i%4
        if board.board[row][col] == 0:
            pygame.draw.rect(WINDOW, (200,200,200), cell)
        else:
            cell_value = board.board[row][col]
            factor = math.log(cell_value, 2)
            color = (255, 255 - factor * 16, 0 + factor * 16)
            pygame.draw.rect(WINDOW, color, cell)
            cell_text = FONT.render(str(cell_value),1,(0,0,0))
            x, y = cell_pos(row, col)
            x += (CELL_SIZE - cell_text.get_width())//2
            y += CELL_SIZE//3
            WINDOW.blit(cell_text, (x, y))
    for button in buttons.values():
        button.draw()


def end_game(board_state):
    string = "Congratulations!\nYou won!" if board_state == 1 else "You lost!"
    text = END_FONT.render(string ,1 , (0,0,0))
    x = (WIDTH - text.get_width())//2
    y = (WIDTH - text.get_height())//2
    WINDOW.blit(text, (x, y))
    pygame.display.update()


def get_direction(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            return "w"
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            return "s"
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            return "a"
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            return "d"
        return None


def main():
    clock = pygame.time.Clock()
    board = game.Board()
    board.spawn_tile()
    board_state = False
    gameloop = True
    
    buttons = {
        "quit": Button("Quit", (cell_pos(0,0)[0], 6*CELL_SIZE)),
        "restart": Button("Restart", (cell_pos(0,2)[0], 6*CELL_SIZE))
    }
    
    while gameloop:
        
        clock.tick(FPS)
        
        #checking for events
        for event in pygame.event.get():
            if not board_state:
                direction = get_direction(event)
            else:
                direction = None
            if direction is not None:
                moved = board.move(direction)
                if moved:
                    board.spawn_tile()
                board_state = board.check_board()
            
            if event.type == pygame.QUIT or buttons["quit"].check_clicked(event):
                gameloop = False
            
            if buttons["restart"].check_clicked(event):
                main()
                
        draw_window(board, buttons)
        if board_state:
            end_game(board_state)
        pygame.display.update()

    pygame.quit()
        
if __name__ == "__main__":
    main()
        