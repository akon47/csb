import re
from multiprocessing import Process, Manager
import threading
from threading import Thread
import math
import random
import sys

class ThreadVariable():
    def __init__(self):
        self.lock = threading.Lock()
        self.value = 0
 
    def add(self, _value):
        
        result = 0;
        
        self.lock.acquire()
        try:
            self.value += _value
            result = self.value;
        finally:
            self.lock.release()
            
        return result
    
class ThreadResult():
    def __init__(self):
        self.lock = threading.Lock()
 
    def show(self, bag):
        self.lock.acquire()
        try:
            print('\n\n-----------------------------')
            for i in range(0, len(bag)):
                print(bag[i].name, end='')
                if (i + 1) % 8 != 0:
                    print(', ', end='')
                else:
                    print('')
        finally:
            self.lock.release()

total_count = ThreadVariable()
result_printer = ThreadResult()
            
class Tree:
    def __init__(self, name, index, x, y):
        self.name=name
        self.x=int(x)
        self.y=int(y)
        self.index=int(index)
        
    def distance(self, other):
        return math.sqrt(pow(other.x - self.x, 2) + pow(other.y - self.y, 2))
    
def find_all_mt(distance, count, max_result, trees, bag, start, above):
    global total_count
    
    if max_result <= total_count.value:
        return True
    
    if(len(bag) == count):
        if total_count.add(1) <= max_result:
            bag.sort(key=lambda tree: tree.index)
            result_printer.show(bag)
        return
    
    for i in range(start, len(trees)):
        is_valid = True
        for value in bag:
            if above:
                if(trees[i].distance(value) < distance):
                    is_valid = False
                    break
            else:
                if(trees[i].distance(value) > distance):
                    is_valid = False
                    break
        if is_valid:
            new_bag = list(bag)
            new_bag.append(trees[i])
            if len(new_bag) > 20:
                #print(len(new_bag))
                #proc = Process(target=find_all_mt, args=(distance, count, trees, new_bag, i + 1,))
                #proc.start()
                thread = Thread(target=find_all_mt, args=(distance, count, max_result, trees, new_bag, i + 1, above,))
                thread.start()
            else:
                find_all_mt(distance, count, max_result, trees, new_bag, i + 1, above)
        new_bag = list(bag)
    
    return
    
def find_all(distance, count, max_result, trees, bag, start):
    global total_count
    
    if(len(bag) == count):
        if total_count.add(1) <= max_result:
            print('\n-----------------------------')
            for i in range(0, len(bag)):
                print(bag[i].name, end='')
                if (i + 1) % 8 != 0:
                    print(', ', end='')
                else:
                    print('')
        return
    
    for i in range(start, len(trees)):
        is_valid = True
        for value in bag:
            if(trees[i].distance(value) < distance):
                is_valid = False
                break
        if is_valid:
            new_bag = list(bag)
            new_bag.append(trees[i])
            find_all(distance, count, max_result, trees, new_bag, i + 1)
        new_bag = list(bag)
    
    return
            

def main():    
    
    #file = open('xy.txt', 'r')
    #file = open('xy2.txt', 'r')
    #file = open('xy3.txt', 'r')
    #lines = file.readlines()
    #file.close();

    file = open(sys.argv[1], 'r')
    lines = file.readlines()
    file.close();

    m = re.compile('(.+)\s+(\d+)\s+(\d+)$')

    count = 0
    trees = []
    for line in lines:
        p = m.findall(line)
        trees.append(Tree(p[0][0], count, p[0][1], p[0][2]))
        count += 1
        
    distance = 15
    number_of_trees = 20
    max_result = 30
    rand = False
    above = True
    shuffle = False
    
    if len(sys.argv) > 2:
        distance = int(sys.argv[2])
    if len(sys.argv) > 3:
        number_of_trees = int(sys.argv[3])
    if len(sys.argv) > 4:
        max_result = int(sys.argv[4])
    if len(sys.argv) > 5:
        if sys.argv[5] == 'y':
            shuffle = True
    if len(sys.argv) > 6:
        if sys.argv[6] == 'b':
            above = False

    procs = []
    
    if shuffle:
        for value in range(max_result):
            random.shuffle(trees)
            proc = Process(target=find_all_mt, args=(distance, number_of_trees, 1, trees, [], 0, above))
            proc.start()
            procs.append(proc)
        for p in procs:
            p.join()
    else:
        find_all_mt(distance, number_of_trees, max_result, trees, [], 0, above)
    
if __name__ == "__main__":
    main()
