import multiprocessing as mp

def add_process(queue, numbers_to_add):
    for number in numbers_to_add:
        queue.put(number)

class AllNumsClass:
    def __init__(self):
        self.queue = mp.Queue()
    def get_queue(self):
        return self.queue

if __name__ == '__main__':

    all_nums_class = AllNumsClass()

    processes = []
    p1 = mp.Process(target=add_process, args=(all_nums_class.get_queue(), [1,3,5]))
    p2 = mp.Process(target=add_process, args=(all_nums_class.get_queue(), [2,4,6]))

    processes.append(p1)
    processes.append(p2)
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    output = [] 
    while all_nums_class.get_queue().qsize() > 0:
        output.append(all_nums_class.get_queue().get())
    print(output)
