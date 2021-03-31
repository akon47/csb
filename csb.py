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
            
result_printer = ThreadResult()
            
class Tree:
    def __init__(self, name, index, x, y):
        self.name=name
        self.x=int(x)
        self.y=int(y)
        self.index=int(index)
        
    def distance(self, other):
        return math.sqrt(pow(other.x - self.x, 2) + pow(other.y - self.y, 2))

def getValidByMode(mode,v,range1,range2):
    if mode =='a':
          return True if v >= range1 else False
    elif mode =='b':
          return True if v <= range1 else False
    else:
        return True if range1 <= v and v <= range2 else False
    
def find_all_mt(thread_value, count, max_result, trees, bag, start, mode, range1, range2):
    if max_result <= thread_value.value:
        return True
    
    if(len(bag) == count):
        if thread_value.add(1) <= max_result:
            bag.sort(key=lambda tree: tree.index)
            result_printer.show(bag)
        return
    
    for i in range(start, len(trees)):
        is_valid = True
        for value in bag:
            isCondition = getValidByMode(mode,trees[i].distance(value),range1,range2)
            if not isCondition :
                is_valid = False
                break
        if is_valid:
            new_bag = list(bag)
            new_bag.append(trees[i])
            if len(new_bag) > 20:
                thread = Thread(target=find_all_mt, args=(thread_value, count, max_result, trees, new_bag, i + 1, mode, range1, range2,))
                thread.start()
            else:
                find_all_mt(thread_value, count, max_result, trees, new_bag, i + 1, mode, range1, range2)
        new_bag = list(bag)
    
    return            

def main():    
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
        
    mode = input("모드 이상-a, 이하-b , 범위-c: ")
    range1 = 0
    range2 = 0
    if mode =='a':
        range1 = int(input("이상: "))
    elif mode =='b':
        range1 = int(input("이하: "))
    elif mode =="c":
        range1= int(input("이상: "))
        range2= int(input("이하: "))

    number_of_trees = int(input("위 조건을 만족하는 나무의 개수: "))
    max_result = int(input("최대 몇 개의 결과를 출력할까요? "))

    threads = []
    
    for value in range(max_result):
        random.shuffle(trees)
        thread = Thread(target=find_all_mt, args=(ThreadVariable(), number_of_trees, 1, trees, [], 0, mode, range1, range2))
        thread.start()
        threads.append(thread)
        
    for t in threads:
        t.join()
    
if __name__ == "__main__":
    main()
