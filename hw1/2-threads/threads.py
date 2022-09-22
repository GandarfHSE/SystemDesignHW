import threading

condvar = threading.Condition()
need_print = 1

def print_num(order, cnt):
    global need_print
    global condvar

    for i in range(cnt):
        with condvar:
            condvar.wait_for(lambda: order == need_print)
            print(order, end = "")
            need_print = need_print % 3 + 1
            condvar.notify_all()

n = int(input())
threads = [threading.Thread(target = print_num, args = (i, n)) for i in range(1, 4)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()