import rubato.utils.proc_timer as pt

pt.start()
for i in range(1, 10000):
    pass
pt.endthenstart("1")
for i in range(1, 10000):
    pass
pt.endthenstart("2")
pt.printall()
