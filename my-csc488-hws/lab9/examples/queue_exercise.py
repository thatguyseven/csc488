import queue

q = queue.Queue()
# 1. Enqueue 5 
q.put(5)
print(list(q.queue))

# 2. Enqueue 7 
q.put(7)
print(list(q.queue))

# 3. Enqueue A 
q.put('A')
print(list(q.queue))

# 4. Dequeue 
out = q.get()
print(list(q.queue))

# 5. Enqueue 1 
q.put(1)
print(list(q.queue))

# 6. Enqueue 4 
q.put(4)
print(list(q.queue))

# 7. Dequeue 
out = q.get()
print(list(q.queue))

# 8. Dequeue 
out = q.get()
print(list(q.queue))