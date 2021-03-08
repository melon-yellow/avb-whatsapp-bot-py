
import Miscellaneous
misc = Miscellaneous.Miscellaneous()

@misc.threading.Async
def theworld(stop, continues):
    print(stop)
    misc.time.sleep(6)
    print(continues)

print("")
stop = theworld("The World!", "And now time goes again...")
print("...")
stop.wait()
print("")

series1 = misc.threading.serial()
series2 = misc.threading.serial()
for i in range(6):
    series1.add(lambda: print("ora"))
    series2.add(lambda: print("muda"))

misc.keepalive()