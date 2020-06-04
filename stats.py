import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

def stat_algo(algo,graph,p,mesure,fileName):

    Nmax = limit(algo,graph,1.5)
    print("Nmax : " + str(Nmax))


    results1 = tenPoints(algo,graph,Nmax,0.5,mesure)

    r=pd.DataFrame()
    r['n']=results1['n']
    r[mesure]=results1[mesure]

    a = sns.lineplot(x=r["n"],y=r[mesure],
                 palette=sns.color_palette("pastel", 2))

    plt.title("Nmax : " + str(Nmax))
    plt.show()

    a.get_figure().savefig(fileName.replace(" ","_"))

def approximation(algo,optimal,graph,n,p):

    T = {}
    T["n"] = []
    T["approximation"] = []

    for i in range(n):
        g = graph(n,p)
        ra = len(algo(g))
        ro = len(optimal(g))
        T["n"].append(i)
        T["approximation"].append(ra/ro)

    return T

def limit(algo,graph,n):
    i = 5
    startTime = time.time()
    while time.time()-startTime < n:
        startTime = time.time()
        i+=1
        g = graph(i,0.5)
        algo(g)
        print(time.time()- startTime,end='\r')

    print("                                                  ")
    return i

def tenPoints(algo,graph,Nmax,p,mesure="log(N)",moyenne=10):
    T = {}
    T["n"] = []
    T[mesure] = []
    print('avant execution ',mesure)
    lastn = 0
    lastt = 0
    for q in range(1,11):
        L = []
        n = np.floor((q*Nmax)/10).astype("int")
        for i in range(0,moyenne):
            g = graph(n,p)
            start_time = time.time()
            algo(g)
            L.append(time.time() - start_time)
        if(mesure == "f(n)"):
            moy = np.array(L).mean()
            T["n"].append(n)
            T[mesure].append(moy)
        elif(mesure == "log(f(n))"):
            moy = np.array(L).mean()
            T["n"].append(n)
            T[mesure].append(np.log(moy))
        elif (mesure == "log(f(log(n)))"):
            moy = np.array(L).mean()
            T["n"].append(np.log(n))
            T[mesure].append(np.log(moy))
            print(np.log(moy)-np.log(lastt)/np.log(n)-np.log(lastn))
            lastn = n
            lastt = moy
    return T

def timeN(algo,graph,minN,maxN,p,mesure="log(N)",moyenne=20):
    T = {}
    T["n"] = []
    T[mesure] = []
    print('avant execution ',mesure)
    nbpas = 10
    marge = (maxN - minN)/nbpas
    for i in range(minN,maxN+1,int(marge)):
        L = []
        for i in range(0,moyenne):
            g = graph(i,p)
            start_time = time.time()
            algo(g)
            L.append(time.time() - start_time)
        moy = np.array(L).mean()
        print("Moyenne  = ",moy)
        if(mesure == "f(n)"):
            T["n"].append(i)
            T[mesure].append(moy)
        elif(mesure == "log(f(n))"):
            T["n"].append(i)
            T[mesure].append(np.log(moy))
        elif (mesure == "log(f(log(n)))"):
            T["n"].append(np.log(i))
            T[mesure].append(np.log(moy))
    return T
