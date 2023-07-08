import threading
from queue import Queue

def boo():
    print('This sucks')

t = threading.Thread(target = boo)
t2 = threading.Thread(target = boo)
t.start()
t2.start()

#t.join()
'''
def threader():
    while True:
        worker = q.get()
        print(f"Worker: {worker}")
        #portscan(worker)
        boo()
        q.task_done()
      
q = Queue()
     
for x in range(1): 
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()

for worker in range(1, 5): # How many thread workers
    q.put(worker)
q.join()
'''