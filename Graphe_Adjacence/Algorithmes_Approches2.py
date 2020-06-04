from Graphe_Adjacence.Graph2 import Graph_A
import numpy as np
import time
import math

class AlgoAdjacence :

    @staticmethod
    def algo_couplage(G):
        C = []
        for i in G.adjacence_list:
            if (i in C):
                continue
            for j in G.adjacence_list[i]:
                if ( j in C ):
                    continue
                C.append(i)
                C.append(j)
                break
        return C

    @staticmethod
    def algo_glouton(G):
        G1 = G.copier()
        C = []
        while ( max(G1.degre_graph().values()) !=  0 ):
            v = G1.degre_max()
            if(max(G1.degre_graph().values()) == 0):
                break
            C.append(v)
            G1 = G1.supprimer_sommet(str(v),copy=False)
        return C

    @staticmethod
    def timeNGeneration(minN,maxN,p,mesure="log(f(n))",moyenne=20):
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
                    g = Graph_A(i,p)
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
                    g = Graph_A(i,p)
                    L.append(time.time() - start_time)
                moy = np.array(L).mean()
                T["n"].append(i)
                T[mesure].append(np.log(moy))
        elif (mesure == "log(f(log(n)))"):
            for i in range(minN, maxN + 1,int(marge)):
                start_time = time.time()
                g = Graph_A(i, p)
                T["n"].append(np.exp(i))
                T[mesure].append( np.log( (time.time() - start_time) ))
        return T
