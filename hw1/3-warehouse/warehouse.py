import threading
from random import randint
from time import sleep

whos_taking = 1
goods_access = threading.Lock()
goods = []
cv_num = threading.Condition()
cv_stuff = threading.Condition()

def producer_thread(prod_num):
    global goods
    global goods_access
    global cv_stuff

    stuff_cnt = 0
    while True:
        sleep(randint(10,100) / 25)
        with goods_access:
            with cv_stuff:
                print("Producer ", prod_num, " provided new stuff")
                goods.append("stuff " + str(stuff_cnt) + " from " + str(prod_num))
                cv_stuff.notify()
        stuff_cnt += 1


def consumer_thread(cons_num):
    global whos_taking
    global goods_access
    global goods
    global cv_num
    global cv_stuff
    global cons_n

    while True:
        with cv_num:
            cv_num.wait_for(lambda: cons_num == whos_taking)

            with cv_stuff:
                cv_stuff.wait_for(lambda: len(goods) > 0)

                with goods_access:
                    my_good = goods.pop()
                    print("Consumer ", cons_num, " took ", my_good)
            
            whos_taking = whos_taking % cons_n + 1
            cv_num.notify_all()

prod_n = int(input("Enter number of producers: "))
cons_n = int(input("Enter number of consumers: "))

threads = []
for i in range(1, prod_n + 1):
    threads.append(threading.Thread(target = producer_thread, args = (i, )))
for i in range(1, cons_n + 1):
    threads.append(threading.Thread(target = consumer_thread, args = (i, )))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
