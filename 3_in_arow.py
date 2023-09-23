import g2d_pygame as g2d
from time import time


W, H = 40, 40
LONG_PRESS = 0.5


class BoardGame:
    def play_at(self, x: int, y: int): abstract()
    def flag_at(self, x: int, y: int): abstract()
    def value_at(self, x: int, y: int) -> str: abstract()
    def col(self) -> int: abstract()
    def row(self) -> int: abstract()
    def finished(self) -> bool: abstract()
    def message(self) -> str: abstract()


def abstract():
    raise NotImplementedError("Abstract method")

def gui_play(game: BoardGame):
    g2d.init_canvas((game.col() * W, game.row() * H))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)

def start() -> str:
    control = g2d.prompt("Please insert the matrix's dimension [4;6;8;10;12]: ")
    diz_k_v = {"4":"conf4.txt","6":"conf6.txt","8":"conf8.txt","10":"conf10.txt","12":"conf12.txt"}
    return diz_k_v[control]
    
    
    
class Tinr(BoardGame):
    def __init__(self,file:str):
        self._board = []
        self._row = 0
        self._forb = [] # In this list there are the indices of the "forbidden" cells

        with open (file,"r") as f:
            for line in f:
                conf_line = line.strip()
                conf_line = conf_line.split(",")
                if conf_line[0] == "#":
                    conf_line.remove("#")
                    for element in conf_line:
                        self._board.append(int(element))
                elif conf_line[0] == "@":
                    conf_line.remove("@")
                    for element in conf_line:
                        self._forb.append(int(element))
                elif conf_line[0] == "r":
                    conf_line.remove("r")
                    self._row = int(conf_line[0])               
        self._col = len(self._board) // self._row

    def row(self) -> int :
        return self._row
    
    def col(self) -> int:
        return self._col
    
    def play_at(self,x,y):
        pos = y*self._col+x
        if (x >= 0 and x < self._col) and (y >= 0 and y < self._row) and pos not in self._forb :
            if self._board[pos] == 0:
                self._board[pos] = 1
            elif self._board[pos] == 1:
                self._board[pos] = -1
            elif self._board[pos] == -1:
                self._board[pos] = 0
  
        
    def value_at(self,x,y) -> int:
        pos = y*self._col+x
        if (x >= 0 and x < self._col) and (y >= 0 and y < self._row)  :
            return self._board[pos]
        
        
    def finished(self) -> bool :
        control_1 = 0 #This variable represents the number of not gray cells
        control_2 = 0 #this variable represents the number of "not contiguos group of three cells"
        control_3 = 0 #This variable represents the number of rows and cols with the same amount of cells of the same color
        wcounter = 0
        bcounter = 0
        for elem in self._board:
            if elem != 0:
                control_1 += 1
        for y in range(self._row):
            for x in range(self._col-2):
                pos = y*self._col+x
                if (self._board[pos] != self._board[pos+1]) or (self._board[pos] != self._board[pos+2]):
                    control_2 += 1
        for x in range(self._col):
            for y in range(self._row-2):
                pos = y*self._col+x
                if (self._board[pos] != self._board[pos+self._col]) or (self._board[pos] != self._board[pos+(2*self._col)]):
                    control_2 += 1
                    
        for y in range(self._row):
            for x in range(self._col):
                pos = y*self._col+x
                if self._board[pos] == 1:
                    wcounter += 1
                elif self._board[pos] == -1:
                    bcounter += 1
            if bcounter == wcounter :
                control_3 += 1
                wcounter = 0
                bcounter = 0

        for x in range(self._col):
            for y in range(self._row):
                pos = y*self._col+x
                if self._board[pos] == 1:
                    wcounter += 1
                elif self._board[pos] == -1:
                    bcounter += 1
            if bcounter == wcounter :
                control_3 += 1
                wcounter = 0
                bcounter = 0

                
        if control_1 == (self._col*self._row) and control_2 == (2*(self._row-2)*(self._col)) and control_3 == self._col + self._row :
            return True
        else:
            return False
        
    def message(self) -> str :
        return ("YOU WON")

    def unsolvable(self) -> bool:
        bcounter = 0
        wcounter = 0
        for y in range(self._row):
            for x in range(self._col):
                pos = y*self._col  + x
                if self._board[pos] == 1:
                    wcounter += 1
                elif self._board[pos] == -1:
                    bcounter += 1
            if bcounter > (self._col / 2) or wcounter > (self._col / 2) :
                return True
            bcounter = 0
            wcounter = 0
        for x in range(self._col):
            for y in range(self._row):
                pos = y*self._col + x
                if self._board[pos] == 1:
                    wcounter += 1
                elif self._board[pos] == -1:
                    bcounter += 1
            if bcounter > (self._row / 2) or wcounter > (self._row / 2) :
                return True
            bcounter = 0
            wcounter = 0
        for y in range(self._row):
            for x in range(self._col - 2):
                pos = y*self._col+x
                if (self._board[pos] == self._board[pos+1] and self._board[pos] == self._board[pos + 2] and self._board[pos] != 0):
                    return True       
        for x in range(self._col):
            for y in range(self._row - 2):
                pos = y*self._col+x
                if (self._board[pos] == self._board[pos+self._col] and self._board[pos] == self._board[pos + 2*self._col] and self._board[pos] != 0):
                    return True
        return False


    def robothelp(self):
        bcounter = 0
        wcounter = 0
        #Here the algorithm checks if the are cols or rows with half cells of the same color and apply a correction
        for y in range(self._row):
            for x in range(self._col):
                pos = y*self._col+ x
                if self._board[pos] == 1:
                    wcounter += 1
                elif self._board[pos] == -1:
                    bcounter += 1
            if bcounter == (self._col / 2) :
                for x in range(self._col):
                    pos = y*self._col+x
                    if self._board[pos] != -1 and pos not in self._forb:
                        self._board[pos] = 1
            elif wcounter == (self._col / 2):
                for x in range(self._col):
                    pos = y*self._col+x
                    if self._board[pos] != 1 and pos not in self._forb:
                        self._board[pos] = -1
            bcounter = 0
            wcounter = 0
        
        for x in range(self._col):
            for y in range(self._row):
                pos = y*self._col + x
                if self._board[pos] == 1:
                    wcounter += 1
                elif self._board[pos] == -1:
                    bcounter += 1
            if bcounter == (self._row / 2):
                for y in range(self._row):
                    pos = y *self._col+x
                    if self._board[pos] != -1 and pos not in self._forb:
                        self._board[pos] = 1
            elif wcounter == (self._row / 2):
                for y in range(self._row):
                    pos = y*self._col+x
                    if self._board[pos] != 1 and pos not in self._forb:
                        self._board[pos] = -1
            bcounter = 0
            wcounter = 0
        
          #Here the algorithm checks if the are two cells colored in the same way and apply every possible corrections    
        for y in range(self._row):
            for x in range(self._col-2):
                pos = y*self._col + x
                if (self._board[pos] == self._board[pos + 1] and self._board[pos] != 0 and  not pos+2 in self._forb):
                    self._board[pos+2] = -self._board[pos]

        for x in range(self._col):
            for y in range(self._row-2):
                pos = y*self._col + x
                if (self._board[pos] == self._board[pos+self._col] and self._board[pos] != 0 and not pos+(2*self._col) in self._forb):
                    self._board[pos+(2*self._col)] = -self._board[pos]
                    
             
        for y in range(self._row):
            for x in range(2,self._col,1):
                pos = y*self._col + x
                if (self._board[pos] == self._board[pos  - 1] and self._board[pos] != 0 and not pos-2 in self._forb):
                    self._board[pos-2] = -self._board[pos]
           
        for x in range(self._col):
            for y in range(2,self._row,1):
                pos = y*self._col + x
                if (self._board[pos] == self._board[pos-self._col] and self._board[pos] != 0 and not pos-(2*self._col) in self._forb):
                    self._board[pos-(2*self._col)] = -self._board[pos]


              
    def black_ver(self,pos:int) -> bool:
        formerboard = self._board[:]
        self._board[pos] = 1
        for teta in range(3):
            self.robothelp()
        if self.unsolvable():
            self._board = formerboard
            return True
        self._board = formerboard
        return False
    
    def white_ver(self,pos:int) -> bool:
        formerboard = self._board[:]
        self._board[pos] = -1
        for teta in range(3):
            self.robothelp()
        if self.unsolvable():
            self._board = formerboard
            return True
        self._board = formerboard
        return False

    def no_rec_solver(self):
        if not self.unsolvable():
            formerboard = self._board[:]
            for y in range(self._row):
                for x in range(self._col):
                    pos = y*self._col+x
                    if self._board[pos] == 0:
                        if self.black_ver(pos):
                            self._board[pos] = -1
                            return
                        elif self.white_ver(pos):
                            self._board[pos] = 1
                            return
                 


    def solve_recursive(self,i:int) -> bool:
        while i < len(self._board) and self._board[i] != 0 :
            i += 1
        if i < len(self._board):
            saved = self._board[:]  # save current status
            for color in (1,-1):
                self._board[i] = color
                if self.solve_recursive(i + 1):
                    return True
                self._board = saved[:]  # backtracking
        return self.finished()
                        
                
            
            
                        
            
            
                    


class BoardGameGui:
    def __init__(self, g: BoardGame):
        self._game = g
        self._downtime = 0
        self.update_buttons()

    def tick(self):
        if g2d.key_pressed("LeftButton"):
            self._downtime = time()
        elif g2d.key_released("LeftButton"):
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            if time() - self._downtime > LONG_PRESS:
                pass
            else:
                self._game.play_at(x, y)
                pass
        elif g2d.key_pressed("h"):
            self._game.no_rec_solver()
        elif g2d.key_pressed("u"):
            if self._game.unsolvable():
                g2d.alert("Unsolvable")
            else:
                g2d.alert("Solvable")
        elif g2d.key_pressed("a"):
            self._game.robothelp()
        elif g2d.key_pressed("s"):
            self._game.solve_recursive(0)
        self.update_buttons()
        
        
    def update_buttons(self):
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        col, row = self._game.col(), self._game.row()
        for y in range(1, row):
            g2d.draw_line((0, y * H), (col * W, y * H))
        for x in range(1, col):
            g2d.draw_line((x * W, 0), (x * W, row * H))
        for y in range(row):
            for x in range(col):
                value = self._game.value_at(x, y)
                xr,yr = (x*W, y*H)
                if self._game.value_at(x,y) == 0:
                    g2d.set_color((150,160,140))
                    g2d.fill_rect((xr-1,yr-1,W-1,H-1))
                elif self._game.value_at(x,y) == 1:
                    g2d.set_color((250,250,250))
                    g2d.fill_rect((xr-1,yr-1,W-1,H-1))
                else:
                    g2d.set_color((0,0,0))
                    g2d.fill_rect((xr-1,yr-1,W-1,H-1))  
        g2d.update_canvas()
        if self._game.finished():
            g2d.alert(self._game.message())
            g2d.close_canvas()
  
conf = start()
game = Tinr(conf)
gui_play(game)


