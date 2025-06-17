import threading
count =0
lock = threading.Lock() # mutex for locking count   

def increase_num():
    global count
    for i in range(1000000):
        with lock: # with - סוגר את הנעול כאשר מגדילים את הסופר ופותח אותו כאשר יוצאים מ ה - :(נקודותיים)
            count+=1
        # אפשר לעשות גם : 
        #lock.acquire() # נועל
        #count +=1
        #lock.release() # פותח
def decrease_num():
    global count
    for i in range(1000000):
        with lock:
            count-=1

t1 = threading.Thread(target=increase_num)
t2 = threading.Thread(target=decrease_num)
# מפעיל את התהליכונים
t1.start()
t2.start()

#מחכה ש ה THREADS יסיימו 
t1.join()
t2.join()

print(count)
