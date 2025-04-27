import queue

q = queue.Queue()

list1 = [1, 5, 7]
q.put(list1)
print(list(q.queue))

q.put(2)
print(list(q.queue))

dict1 = {'python': 'rulez', 'second':'entry'}
q.put(dict1)
print(list(q.queue))
