import pygame
import random
import math as m
from pygame_ui import Button, Slider


HEIGHT = 720
WIDTH = 1280
FPS = 60

WHITE = (223,223,223)
RED = (223,0,0)
GREEN = (0,223,0)
BLACK = (0,0,0)
PURPLE = (255,0,255)
GREY = (150,150,150)



class Array:
    
    def __init__(self, window, number):
        self.window = window
        self.running = False
        self.number = number
        self.pointers = {}
        self.generate_array()
        self.generate_bars()
        self.sort_alg = None


    def draw_array(self):
        for i, (bar, value) in enumerate(zip(self.bars, self.array)):
            bar.height = m.floor(2.1 * value)
            bar.y = HEIGHT - 130 - bar.height
            color = (value, 255 - value, 255)
            pygame.draw.rect(self.window, color, bar)
        for pointer in self.pointers.values():
            pygame.draw.rect(self.window, pointer.color, pointer)
        

    def generate_bars(self):
        self.bars = []
        width = 900 / self.number - 1
        for i, el in enumerate(self.array):
            height = m.floor(2.1 * el)
            y = HEIGHT - 130 - height
            rect = pygame.Rect(330 + i * (width+1), y, width, height)
            self.bars.append(rect)
      
            
    def generate_array(self):
        self.array = [random.randint(0, 255) for i in range(self.number)]

            
    def start_alg(self, sort_alg=None):
        if sort_alg is not None:
            self.sort_alg = sort_alg
        self.running = False
        self.generate_array()
        self.generate_bars()
        
        if self.sort_alg == "merge":
            self.pointers = {
                "r": Pointer(WHITE, self.number),
                "l": Pointer(WHITE, self.number),
                "i": Pointer(RED, self.number),
            }
            sort_iter = merge_sort(self, 0, len(self.array))
            return sort_iter
        
        if self.sort_alg == "quick":
            self.pointers = {
                "pivot": Pointer(WHITE, self.number),
                "m": Pointer(WHITE, self.number),
                "i": Pointer(RED, self.number),
            }
            sort_iter = quick_sort(self, 0, len(self.array))
            return sort_iter
        
        if self.sort_alg == "selection":
            self.pointers = {
                "m": Pointer(WHITE, self.number),
                "i": Pointer(RED, self.number),
            }
            sort_iter = selection_sort(self)
            return sort_iter
        
        if self.sort_alg == "bogo":
            self.pointers = {}
            sort_iter = bogo_sort(self)
            return sort_iter
        
        if self.sort_alg == "radix_msd":
            self.pointers = {
                "pos": Pointer(PURPLE, self.number),
                "i": Pointer(WHITE, self.number),
            }
            sort_iter = MSD_radix_sort(self, 2, 0, len(self.array))
            return sort_iter
        
        if self.sort_alg == "radix_lsd":
            self.pointers = {
                "pos": Pointer(PURPLE, self.number),
                "i": Pointer(WHITE, self.number),
            }
            sort_iter = LSD_radix_sort(self, 2)
            return sort_iter
        
        if self.sort_alg == "insertion":
            self.pointers = {
                "i": Pointer(RED, self.number),
                "j": Pointer(PURPLE, self.number),
            }
            sort_iter = insertion_sort(self)
            return sort_iter
        
        if self.sort_alg == "shuffle":
            self.pointers = {
                "i": Pointer(WHITE, self.number),
                "i+1": Pointer(WHITE, self.number),
            }
            sort_iter = shuffle_sort(self)
            return sort_iter
        
          
  
class Pointer(pygame.Rect):
    
    def __init__(self, color, number_of_bars):
        width = 900 // number_of_bars - 3
        if width < 1:
            width = 1
        super().__init__(330+1, HEIGHT - 120 , width, 10)
        self.color = color
        
    
    def set_pos_from_index(self, i, array):
        self.x = array.bars[i].x + 1
        
            
            
def draw_window(window, array, buttons, sliders):
    window.fill(BLACK)
    array.draw_array()
    for button in buttons.values():
        button.draw_button()
    for slider in sliders.values():
        slider.draw_slider()
    pygame.display.update()
    


def quick_sort(array, left, right):
    if left < right - 1:
        mid = yield from partition(array, left, right)
        yield from quick_sort(array, left, mid)
        yield from quick_sort(array, mid+1, right)

 
        
def partition(a, left, right):
    piv_ind = random.randrange(left, right)
    a.array[piv_ind], a.array[right-1] = a.array[right-1], a.array[piv_ind]
    a.pointers["pivot"].set_pos_from_index(right-1, a)
    pivot = a.array[right-1]
    m = left
    for i in range(left, right-1):
        a.pointers["i"].set_pos_from_index(i, a)
        a.pointers["m"].set_pos_from_index(m, a)
        if a.array[i] < pivot:
            a.array[i], a.array[m] = a.array[m], a.array[i]
            m += 1
        yield None
    a.array[m], a.array[right-1] = a.array[right-1], a.array[m]
    return m



def selection_sort(a):
    length = len(a.array)
    for i in range(length-1):
        m = yield from get_min(a, i+1, length)
        m = m[0]
        a.pointers["i"].set_pos_from_index(i, a)
        if a.array[i] > a.array[m]:
            a.pointers["m"].set_pos_from_index(m, a)
            a.pointers["m"].color = GREEN
            a.array[i], a.array[m] = a.array[m], a.array[i]
            yield None



def get_min(a, left, right):
    a.pointers["m"].color = WHITE
    current_min = a.array[left]
    current_min_ind = left
    for i in range(left + 1, right):
        a.pointers["m"].set_pos_from_index(i, a)
        if a.array[i] < current_min:
            current_min = a.array[i]
            current_min_ind = i
        yield None
    return current_min_ind, current_min



def merge_sort(array, left, right):
    if left < right - 1:
        mid = (left + right)//2
        yield from merge_sort(array, left, mid)
        yield from merge_sort(array, mid, right)
        yield from merge(array, left, right)



def merge(a, left, right):
    a.pointers["i"].color = RED
    a.pointers["l"].color = WHITE
    a.pointers["r"].color = WHITE
    mid = (left + right)//2 
    l = left
    r = mid
    a.pointers["l"].set_pos_from_index(l, a)
    a.pointers["r"].set_pos_from_index(r, a)
    newarray = []
    for i in range(left, right):
        a.pointers["i"].set_pos_from_index(i, a)
        if r == right:
            newarray.append(a.array[l])
            l += 1
            a.pointers["l"].set_pos_from_index(l, a)
        elif l < mid and a.array[l] <= a.array[r]:
            newarray.append(a.array[l])
            l += 1
            a.pointers["l"].set_pos_from_index(l, a)
        else:
            newarray.append(a.array[r])
            r += 1
            if r != right:
                a.pointers["r"].set_pos_from_index(r, a)
        yield None
    a.pointers["l"].color = BLACK
    a.pointers["r"].color = BLACK
    a.pointers["r"].set_pos_from_index(-1, a)
    a.pointers["l"].set_pos_from_index(-1, a)
    for i, el in enumerate(newarray):
        a.pointers["i"].color = PURPLE
        a.array[left+i] = el
        a.pointers["i"].set_pos_from_index(left+i, a)
        yield None



def bogo_sort(array):
    while True:
        random.shuffle(array.array)
        ordered = isordered(array.array)
        yield None
        if ordered:
            break
  
        
  
def isordered(array):
    for i, el in enumerate(array):
        try:
            if array[i+1] < el:
                return False
        except IndexError:
            pass
    return True



def counting_sort(array, max_key=None):
    if max_key is not None:
        max_key = max(array.array)
    count = [0] * (max_key + 1)
    for el in array.array:
        count[el] += 1
    array.array.clear()
    for i, el in enumerate(count):
        array.array += el * [i]
       
        

def LSD_radix_sort(a, base, key_length=None):
    digit_place = 0
    if key_length is None:
        maxval = max(a.array)
        key_length = 0
        while maxval:
            maxval //= base
            key_length += 1
    
    while digit_place < key_length:
        output = [None for i in a.array]
        counter = [0] * base
        a.pointers["pos"].color = BLACK
        a.pointers["pos"].set_pos_from_index(-1, a)
        for i, el in enumerate(a.array):
            digit = (el // (base**digit_place)) % base
            counter[digit] += 1
            a.pointers["i"].set_pos_from_index(i, a)
            yield None
            
        #cumulative counter
        for i in range(base-1):
            counter[i+1] += counter[i]
            
        pos_array = []
        for el in reversed(a.array):
            digit = (el // (base**digit_place)) % base
            counter[digit] -= 1
            pos = counter[digit]
            output[pos] = el
            pos_array.append(pos)
            
        a.pointers["pos"].color = PURPLE
        for i in range(len(a.array)):
            a.array[i] = output[i]
            a.pointers["i"].set_pos_from_index(i, a)
            a.pointers["pos"].set_pos_from_index(pos_array[i], a)
            yield None
        digit_place += 1
        
        
        
def MSD_radix_sort(a, base, left, right, digit_place=None, key_length=None):
    if key_length is None:
        maxval = max(a.array)
        key_length = 0
        while maxval:
            maxval //= base
            key_length += 1
    if digit_place is None:
        digit_place = key_length - 1
    
    if digit_place >= 0 and right - left > 1:
        output = a.array[left:right]
        counter = [0] * base
        a.pointers["pos"].color = BLACK
        a.pointers["pos"].set_pos_from_index(-1, a)
        for i, el in enumerate(a.array[left:right]):
            digit = (el // (base**digit_place)) % base
            counter[digit] += 1
            a.pointers["i"].set_pos_from_index(left + i, a)
            yield None
            
        #cumulative counter
        for i in range(base-1):
            counter[i+1] += counter[i]
        counter_copy = counter[:]
        
        pos_array = []
        for el in reversed(a.array[left:right]):
            digit = (el // (base**digit_place)) % base
            counter[digit] -= 1
            pos = counter[digit]
            output[pos] = el
            pos_array.append(pos)
            
        a.pointers["pos"].color = PURPLE
        for i, j in enumerate(range(left, right)):
            a.array[j] = output[i]
            a.pointers["i"].set_pos_from_index(j, a)
            a.pointers["pos"].set_pos_from_index(left + pos_array[i], a)
            yield None
        
        digit_place -= 1
        
        for i in range(base):
            newleft = left + counter_copy[i-1] if i != 0 else left
            newright = left + counter_copy[i] 
            yield from MSD_radix_sort(a, base, newleft, 
                                      newright, digit_place, key_length)      
        
        
        
def insertion_sort(array):
    for i, el in enumerate(array.array[1:]):
        array.pointers["i"].set_pos_from_index(i+1, array)
        count = 0
        for j in range(i+1):
            if array.array[i-j] > el:
                array.array[i-j+1] = array.array[i-j]
                array.pointers["j"].set_pos_from_index(i-j+1, array)
                yield None
            else:
                break
            count += 1
        array.array[i-count+1] = el
        array.pointers["j"].set_pos_from_index(i-count+1, array)
        yield None
        
  
        
def shuffle_sort(array):
    l = 0
    r = len(array.array)
    while True:
        if r - l < 2:
            break
        else:
            temp = l
            for i in range(l, r-1):
                if array.array[i] > array.array[i+1]:
                    array.array[i], array.array[i+1] = array.array[i+1], array.array[i]
                    temp = i + 1
                array.pointers["i"].set_pos_from_index(i, array)
                array.pointers["i+1"].set_pos_from_index(i+1, array)
                yield None
            r = temp 
            
        if r - l < 2:
            break
        else:
            temp = r - 1
            for i in range(r-1, l, -1):
                if array.array[i] < array.array[i-1]:
                    array.array[i], array.array[i-1] = array.array[i-1], array.array[i]
                    temp = i
                array.pointers["i"].set_pos_from_index(i, array)
                array.pointers["i+1"].set_pos_from_index(i-1, array)
                yield None
            l = temp 

    

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    run = True
    clock = pygame.time.Clock()
    pygame.display.set_caption("Sorting Algorithm Visualizer")
    secs_passed = 0
    operations_per_sec = 60
    
    array = Array(window, 100)
    sort_iter = array.start_alg("quick")
    y = [50 + i*80 for i in range(10)]
    buttons = {
        "quick": Button(window, "Quick Sort", pos=(50, y[0]), size=(230,60)),
        "merge": Button(window, "Merge Sort", pos=(50, y[1]), size=(230,60)),
        "selection": Button(window, "Selection Sort", pos=(50, y[2]), size=(230,60)),
        "bogo": Button(window, "Bogo Sort", pos=(50, y[3]), size=(230,60)),
        "insertion": Button(window, "Insertion Sort", pos=(50, y[4]), size=(230,60)),
        "shuffle": Button(window, "Shuffle Sort", pos=(50, y[5]), size=(230,60)),
                "radix_lsd": Button(window, "LSD Radix Sort", pos=(50, y[6]), size=(230,60)),
        "radix_msd": Button(window, "MSD Radix Sort", pos=(50, y[7]), size=(230,60)),
        "start": Button(window, "Start", pos=(330, HEIGHT - 90),
                        size=(110, 60), color=GREEN),
        "stop": Button(window, "Stop", pos=(450, HEIGHT - 90),
                       size=(110, 60), color=RED),
        "new": Button(window, "New", pos=(570, HEIGHT - 90),
                          size=(110, 60), color=WHITE),
    }
    algorithms = [key for key in buttons.keys() if key not in ("start", "stop", "new")]
    
    sliders = {
        "speed": Slider(window, "Speed", values=(1,1000), pos=(730, HEIGHT - 90),
                          size=(225, 60), val=60),
        "number": Slider(window, "Bars", values=(2,450), pos=(1005, HEIGHT - 90),
                          size=(225, 60), val=100)
    }
    
    while run:
        
        time = clock.tick(FPS)
        secs_passed += (time/1000)
        num_operations = m.floor(secs_passed*operations_per_sec)
        secs_passed -= 1/operations_per_sec * num_operations
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
            
            for name, button in buttons.items():
                if button.check_clicked(event) is True:
                    if name in algorithms:
                        sort_iter = array.start_alg(name)
                    if name == "start":
                        array.running = True
                    if name == "stop":
                        array.running = False
                    if name == "new":
                        sort_iter = array.start_alg()
                        
            sliders["speed"].on_clicked(event)
            operations_per_sec = sliders["speed"].val
            sliders["number"].on_clicked(event)
            number = sliders["number"].val
            if number != array.number:
                array.number = number
                sort_iter = array.start_alg()
                
        if array.running is True:
            try:
                for i in range(num_operations):
                    next(sort_iter)
            except StopIteration:
                array.running = False
                for pointer in array.pointers.values():
                    pointer.x = 330+1
        draw_window(window, array, buttons, sliders)
    
    pygame.quit()



if __name__ == "__main__":
    main()