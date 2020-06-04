from Graphe_OO.Graph import Graph
import numpy as np
import time
import math

class AlgoMatrice :

    @staticmethod
    def algo_couplage(G):
        C = []
        E = G.arretes
        for e in E:
            if (e[0] in C) or (e[1] in C):
                continue
            C.append(e[0])
            C.append(e[1])
        return C

    @staticmethod
    def algo_glouton(G):
        G1 = G.copy()
        C = []
        while (G1.degre_graph().max() !=  0):
            v = G1.degre_max()
            C.append(v)
            G1.supprimer_sommet(v)
        return C

    @staticmethod
    def branchement(G,C = None):

    	C = [] if C == None else C
    	E = G.arretes

    	if len(E) == 0:
    		return C

    	s1 = E[0][0]
    	s2 = E[0][1]

    	C1 = C + [s1]
    	C2 = C + [s2]

    	B1 = AlgoMatrice.branchement(G.supprimer_sommet_copy(s1),C1)
    	B2 = AlgoMatrice.branchement(G.supprimer_sommet_copy(s2),C2)

    	if len(B1) < len(B2) :
    		return B1
    	else :
    		return B2

    @staticmethod
    def timeN(algo,minN,maxN,p,mesure="log(N)",moyenne=10):
        T = {}
        T["n"] = []
        T[mesure] = []
        print('avant execution ',mesure)
        nbpas = 10
        marge = (maxN - minN)/nbpas
        if(mesure == "f(n)"):
            for i in range(minN,maxN+1,int(marge)):
                L = []
                for i in range(0,moyenne):
                    g = Graph(i,p)
                    start_time = time.time()
                    algo(g)
                    L.append(time.time() - start_time)
                moy = np.array(L).mean()
                print("Moyenne  = ",moy)
                T["n"].append(i)
                T[mesure].append(moy)
        elif(mesure == "log(f(n))"):
            for i in range(minN,maxN+1,int(marge)):
                L = []
                for j in range(0, moyenne):
                    g = Graph(n=i, p=p)
                    start_time = time.time()
                    algo(g)
                    L.append(time.time() - start_time)
                moy = np.array(L).mean()
                T["n"].append(i)
                T[mesure].append(np.log(moy))
        elif (mesure == "log(f(log(n)))"):
            for i in range(minN, maxN + 1,int(marge)):
                g = Graph(i, p)
                start_time = time.time()
                algo(g)
                T["n"].append(np.exp(i))
                T[mesure].append( np.log( (time.time() - start_time) ))
        return T

    @staticmethod
    def timeNGeneration(minN,maxN,p,mesure="log(f(n))",moyenne=10):
        T = {}
        T["n"] = []
        T[mesure] = []
        print('avant execution ',mesure)
        nbpas = 10
        marge = (maxN - minN)/nbpas
        if(mesure == "f(n)"):
            for i in range(minN,maxN+1,int(marge)):
                L = []
                for i in range(0,moyenne):
                    start_time = time.time()
                    g = Graph(i,p)
                    L.append(time.time() - start_time)
                moy = np.array(L).mean()
                print("Moyenne  = ",moy)
                T["n"].append(i)
                T[mesure].append(moy)
        elif(mesure == "log(f(n))"):
            for i in range(minN,maxN+1,int(marge)):
                L = []
                for j in range(0, moyenne):
                    start_time = time.time()
                    g = Graph(i,p)
                    L.append(time.time() - start_time)
                moy = np.array(L).mean()
                T["n"].append(i)
                T[mesure].append(np.log(moy))
        elif (mesure == "log(f(log(n)))"):
            for i in range(minN, maxN + 1,int(marge)):
                start_time = time.time()
                g = Graph(i, p)
                T["n"].append(np.exp(i))
                T[mesure].append( np.log( (time.time() - start_time) ))
        return T
