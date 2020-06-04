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

class Graph:
    def __init__(self,n,p,file=None):
        L = []
        if(file):
            L = read_graph(file)
        else:
            L = random_graph(n,p)
        self.etiquettes = L[0]
        self.adjacence = L[1]
        self.arretes = liste_arretes([self.etiquettes,self.adjacence])

    def copy(self):
        G = Graph(0,0)
        G.etiquettes = copy.deepcopy(self.etiquettes)
        G.adjacence = copy.deepcopy(self.adjacence)
        G.arretes = copy.deepcopy(self.arretes)
        return G

    def afficher_graph(self):
        print("Etiquettes : ",self.etiquettes)
        print("Arrétes : ",self.arretes)
        print("Matrice d'Adjacence : ")
        print(self.adjacence)

    def sup_sommet(graph, sommet):
        g = graph.copy()
        i = list(g[0]).index(sommet)
        g[1] = np.delete(g[1], i, 0)
        g[1] = np.delete(g[1], i, 1)
        g[0] = np.delete(g[0], i, 0)
        return g

    def supprimer_sommet(self,sommet,maj = True):
        i = list(self.etiquettes).index(sommet)
        self.adjacence = np.delete(self.adjacence,i,axis=0)
        self.adjacence = np.delete(self.adjacence, i,axis=1)
        self.etiquettes = np.delete(self.etiquettes, i, 0)
        #Discuter de la nécessité de ça :
        if(maj):
            self.arretes = [e for e in self.arretes if ((e[0] != sommet) and (e[1] != sommet)) ]
        #self.arretes = liste_arretes([self.etiquettes, self.adjacence])

        return copy.deepcopy(self)

    def supprimer_sommet_copy(self,sommet,maj = True):
        graph = self.copy()
        i = list(self.etiquettes).index(sommet)
        graph.adjacence = np.delete(graph.adjacence,i,axis=0)
        graph.adjacence = np.delete(graph.adjacence, i,axis=1)
        graph.etiquettes = np.delete(self.etiquettes, i, 0)
        #Discuter de la nécessité de ça :
        if(maj):
            graph.arretes = [e for e in graph.arretes if ((e[0] != sommet) and (e[1] != sommet)) ]
        #self.arretes = liste_arretes([self.etiquettes, self.adjacence])

        return graph

    def supprimer_sommets(self,sommets,maj = True):
        i = [list(self.etiquettes).index(i) for i in sommets]
        self.adjacence = np.delete(self.adjacence,i,axis=0)
        self.adjacence = np.delete(self.adjacence, i,axis=1)
        self.etiquettes = np.delete(self.etiquettes, i, 0)
        #Discuter de la nécessité de ça :
        if (maj):
            for sommet in sommets:
                self.arretes = [i for i in self.arretes if ((i[0] != sommet) and (i[1] != sommet)) ]
        #self.arretes = liste_arretes([self.etiquettes, self.adjacence])


    def degre_graph(self):
        if self.adjacence.size == 0:
            return np.zeros((1))
        return np.sum(self.adjacence, axis=0)

    def degre_max(self):
        return self.etiquettes[np.argmax(self.degre_graph())]
