import numpy as np
import copy


def read_graph(name):
    f = open(name, "r")
    L = f.readlines()
    i = 0
    n = 0
    s = []
    lenght = int(L[1].strip())
    tab = np.zeros((lenght, lenght))
    while i < len(L):
        if (L[i].strip() == "Sommets"):
            i += 1
            while (L[i].strip() != "Nombre d aretes"):
                s.append(L[i].strip())
                i += 1
                n += 1
        elif (L[i].strip() == "Aretes"):
            i += 1
            while (i < len(L)):
                pos = L[i].strip().split(" ")
                tab[int(pos[0]), int(pos[1])] = 1
                tab[int(pos[1]), int(pos[0])] = 1
                i += 1
        else:
            i += 1
    return [s, tab]

def random_graph(n,p):
    s = np.arange(n).astype('str')
    tab = np.random.random((n,n))
    tab = np.where(tab < p,1,0 )
    tab = np.tril(tab,-1)
    tab2 = np.transpose(tab)
    tab += tab2
    return [s,tab]

def liste_arretes(G):
    e = np.where(G[1] == 1)
    E = [(G[0][e[0][i]],G[0][e[1][i]]) for i in range(0, len(e[0])) if e[0][i] < e[1][i]]
    return E

class Graph_A:

    def __init__(self,n=None,p=None,file=None):
        L = []
        self.n = 0
        self.m = 0
        if ((p!=None and n != None) or file != None):
            if(file != None):
                L = read_graph(file)
            else:
                L = random_graph(n,p)
            self.arretes = liste_arretes(L)
            self.m = int(len(self.arretes))
            self.adjacence_list = {}
            self.n = len(L[0])
            for i in L[0]:
                self.adjacence_list[i] = []
            for i in self.arretes:
                if i[1] not in self.adjacence_list[i[0]]:
                    self.adjacence_list[i[0]].append(i[1])
                if i[0] not in self.adjacence_list[i[1]]:
                    self.adjacence_list[i[1]].append(i[0])

        else:
            self.adjacence_list = {}

    def afficher_graph(self):
        print("Liste d'Adjacence : ")
        print(self.adjacence_list)


    def copier(self):
        G = Graph_A()
        G.adjacence_list = copy.deepcopy(self.adjacence_list)
        G.n = self.n
        G.m = self.m
        return G


    def supprimer_sommet(self,sommet,copy = True):
        if(copy):
            G = self.copier()
        else:
            G = self
        G.m = G.m - len(G.adjacence_list[sommet])
        for i in G.adjacence_list:
            if sommet in G.adjacence_list[i]:
                G.adjacence_list[i].remove(sommet)
        del G.adjacence_list[sommet]
        G.n = G.n - 1
        return G



    def supprimer_sommets(self,sommets,copy = True):
        G = None
        if (copy):
            G = self.copier()
        else:
            G = self
        for i in sommets:
            G.supprimer_sommet(i,copy=False)
        return G



    def degre_graph(self):
        L = {}
        for i in self.adjacence_list:
            L[i] = len( self.adjacence_list[i] )
        return L

    def degre_max(self):
        imax = -1
        vmax = -1
        C = self.degre_graph()
        for i in C:
            if C[i] > vmax :
                imax = i
                vmax  = C[i]
        return imax




#G1 = Graph(0,0,file=r"C:\Users\mohamed\PycharmProjects\Projet_Complexe\Graphe_OO\exempleinstance.txt")
#G1.supprimer_sommet("0",copy=False)
#print(G1.degre_graph())
#print(G1.degre_max())

g = Graph_A(5,0.5)
