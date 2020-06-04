from Graphe_Adjacence.Algorithmes_Approches2 import AlgoAdjacence
from Graphe_Adjacence.Graph2 import Graph_A
import numpy as np

class Node:
    def __init__(self,graphe,L,v=""):
        self.graphe_r = graphe
        self.solution_courante = L
        self.v = v


#Fonctions de bornes :
def borne_1(graphe):
    deg_max = max(graphe.degre_graph().values())
    if(graphe.m == 0):
        return np.infty
    return int(np.ceil(deg_max / graphe.m))

def borne_2(graphe, C = None):
    C = [] if C == None else C
    C = AlgoAdjacence.algo_couplage(graphe)
    return len(C)/2

def borne_3(graphe):
    tmp = 2 * graphe.n - 1
    A = tmp - np.sqrt(tmp**2 - 8 * graphe.m)
    return np.ceil(A/2)



def generation_arbre(graph,C = None,best = None,estimateurs_borne = []):
    C = [] if C == None else C
    print(graph.adjacence_list)
    if(max(graph.degre_graph().values()) == 0):
        return [([C],len(C))]

    #Estimation d'une solution réalisable
    R = AlgoAdjacence.algo_glouton(graph)
    print("Solution réalisable",R)
    if(best == None or len(R) < len(best)):
        best = R

    #Calcul des bornes
    bornes = []
    for i in estimateurs_borne:
        bornes.append(i(graph.copier()))
    best_expectation = max(bornes)
    print("Bornes calculees : ",bornes)
    print("Borne inf = ",best_expectation)
    print("Best = ",best)

    #Elagation
    if(len(best) < best_expectation):
        print('ON ELAGE STP')
        return [([C], len(C))]

    #Continuer l'exploration
    s1 = None
    for i in graph.adjacence_list:
        if(len(graph.adjacence_list[i]) >= 1):
            s1=i
            break
    s2 = graph.adjacence_list[s1][0]
    C1 = C + [s1]
    C2 = C + [s2]
    print("Le branchement se fait suivant l'arréte (",s1,",",s2,")")
    print("Branchement en ",s1)
    B1 = generation_arbre(graph.supprimer_sommet(s1),C1,best=best,estimateurs_borne=estimateurs_borne)
    print("Retour ")
    print("Branchement en ",s2)
    B2 = generation_arbre(graph.supprimer_sommet(s2),C2,best=best,estimateurs_borne=estimateurs_borne)
    print("Retour 2")
    return (B1) + (B2)




def parcours_profondeur(G,estimateurs_bornes=[borne_1,borne_2,borne_3]):
    pile = []
    pile.append(Node(G,[]))
    best = G.n*[9]

    #Recherce d'une arréte
    while not (len(pile) == 0):
        print("======")
        N = pile.pop()
        C = N.solution_courante
        print("N = ",C," ",N.graphe_r)
        graph = N.graphe_r

        print("Visite de ",graph.adjacence_list)
        print("M = ", graph.m)
        print("Ensemble courant : ",C)

        #Calcul d'une solution réalisable
        R = AlgoAdjacence.algo_glouton(graph)
        if(len(R) + len(C) < len(best)):
            best = R + C

        #Calcul des bornes
        bornes = []
        for i in estimateurs_bornes:
            bornes.append(i(graph))

        min_expected = max(bornes)

        print("Bornes calculées : ",bornes)
        print("Solution réalisable par gloutonerie : ",R)
        print("Solution réalisable par couplage : ",AlgoAdjacence.algo_couplage(graph))
        print("Meilleur solution : ",best)

        #Tentative d'élagage
        if(len(best) <= min_expected + len(C) and min_expected != np.infty):
            print("Elagage non trivial")
            #On empile pas
            continue

        #Recherche d'un arrête selon laquelle brancher
        e = None
        for i in graph.adjacence_list:
            if(len(graph.adjacence_list[i]) >= 1):
                s1=i
                e = (i,graph.adjacence_list[i][0])
                break

        #MAJ de la pile si arréte il y a :
        if(e != None):
            print("Ajout de ",e[0]," et de ",e[1])
            pile.append(Node(graph.supprimer_sommet(e[1]),C + [e[1]]))
            pile.append(Node(graph.supprimer_sommet(e[0]),C + [e[0]]))

def parcours_profondeur_NB_lite(G):
    pile = []
    pile.append(Node(G,[]))
    best = G.n*[9]
    total = G.n
    #Recherce d'une arréte
    while not (len(pile) == 0):
        N = pile.pop()
        C = N.solution_courante
        graph = N.graphe_r

        #Recherche d'un arrête selon laquelle brancher
        e = None
        for i in graph.adjacence_list:
            if(len(graph.adjacence_list[i]) >= 1):
                s1=i
                e = (i,graph.adjacence_list[i][0])
                break

        #MAJ de la pile si arréte il y a :
        if(e != None):
            pile.append(Node(graph.supprimer_sommet(e[1]),C + [e[1]]))
            pile.append(Node(graph.supprimer_sommet(e[0]),C + [e[0]]))
            continue

        if len(C)<len(best):
            best = C

    return best


def parcours_profondeur_lite(G,estimateurs_bornes=[borne_1,borne_2,borne_3]):
    pile = []
    pile.append(Node(G,[]))
    best = G.n*[9]
    total = G.n
    cpt = 0
    #Recherce d'une arréte
    while not (len(pile) == 0):
        N = pile.pop()
        C = N.solution_courante
        graph = N.graphe_r

        #Calcul d'une solution réalisable
        R = AlgoAdjacence.algo_couplage(graph)

        if(len(R) + len(C) < len(best)):
            best = R + C

        #Calcul des bornes
        bornes = []
        for i in estimateurs_bornes:
            bornes.append(i(graph))

        min_expected = max(bornes)

        #Tentative d'élagage
        if(len(best) <= min_expected + len(C) and min_expected != np.infty):
            cpt += 2 ** (total - len(C))
            #On empile pas
            continue

        #Recherche d'un arrête selon laquelle brancher
        e = None
        for i in graph.adjacence_list:
            if(len(graph.adjacence_list[i]) >= 1):
                s1=i
                e = (i,graph.adjacence_list[i][0])
                break

        #MAJ de la pile si arréte il y a :
        if(e != None):
            pile.append(Node(graph.supprimer_sommet(e[1]),C + [e[1]]))
            pile.append(Node(graph.supprimer_sommet(e[0]),C + [e[0]]))

    return best

def parcours_profondeur_lite_glouton(G,estimateurs_bornes=[borne_1,borne_2,borne_3]):
    pile = []
    pile.append(Node(G,[]))
    best = G.n*[9]
    total = G.n
    cpt = 0
    #Recherce d'une arréte
    while not (len(pile) == 0):
        N = pile.pop()
        C = N.solution_courante
        graph = N.graphe_r

        #Calcul d'une solution réalisable
        R = AlgoAdjacence.algo_glouton(graph)

        if(len(R) + len(C) < len(best)):
            best = R + C

        #Calcul des bornes
        bornes = []
        for i in estimateurs_bornes:
            bornes.append(i(graph))

        min_expected = max(bornes)

        #Tentative d'élagage
        if(len(best) <= min_expected + len(C) and min_expected != np.infty):
            cpt += 2 ** (total - len(C))
            #On empile pas
            continue

        #Recherche d'un arrête selon laquelle brancher
        e = None
        for i in graph.adjacence_list:
            if(len(graph.adjacence_list[i]) >= 1):
                s1=i
                e = (i,graph.adjacence_list[i][0])
                break

        #MAJ de la pile si arréte il y a :
        if(e != None):
            pile.append(Node(graph.supprimer_sommet(e[1]),C + [e[1]]))
            pile.append(Node(graph.supprimer_sommet(e[0]),C + [e[0]]))

    return best

def parcours_profondeur_lite_ameliore_1(G,estimateurs_bornes=[borne_1,borne_2,borne_3]):
    pile = []
    pile.append(Node(G,[]))
    best = G.n*[9]
    total = G.n
    cpt = 0
    #Recherce d'une arréte
    while not (len(pile) == 0):
        N = pile.pop()
        C = N.solution_courante
        graph = N.graphe_r

        if N.v != "":
            for s in graph.adjacence_list[N.v]:
                C.append(s)
                graph.supprimer_sommet(s)

        #Calcul d'une solution réalisable
        R = AlgoAdjacence.algo_couplage(graph)

        if(len(R) + len(C) < len(best)):
            best = R + C

        #Calcul des bornes
        bornes = []
        for i in estimateurs_bornes:
            bornes.append(i(graph))

        min_expected = max(bornes)

        #Tentative d'élagage
        if(len(best) <= min_expected + len(C) and min_expected != np.infty):
            cpt += 2 ** (total - len(C))
            #On empile pas
            continue

        #Recherche d'un arrête selon laquelle brancher
        e = None
        for i in graph.adjacence_list:
            if(len(graph.adjacence_list[i]) >= 1):
                s1=i
                e = (i,graph.adjacence_list[i][0])
                break

        #MAJ de la pile si arréte il y a :
        if(e != None):
            pile.append(Node(graph.supprimer_sommet(e[1]),C + [e[1]]))
            pile.append(Node(graph.supprimer_sommet(e[0]),C + [e[0]],e[1]))

    return best

def parcours_profondeur_lite_ameliore_1_glouton(G,estimateurs_bornes=[borne_1,borne_2,borne_3]):
    pile = []
    pile.append(Node(G,[]))
    best = G.n*[9]
    total = G.n
    cpt = 0
    #Recherce d'une arréte
    while not (len(pile) == 0):
        N = pile.pop()
        C = N.solution_courante
        graph = N.graphe_r

        if N.v != "":
            for s in graph.adjacence_list[N.v]:
                C.append(s)
                graph.supprimer_sommet(s)

        #Calcul d'une solution réalisable
        R = AlgoAdjacence.algo_glouton(graph)

        if(len(R) + len(C) < len(best)):
            best = R + C

        #Calcul des bornes
        bornes = []
        for i in estimateurs_bornes:
            bornes.append(i(graph))

        min_expected = max(bornes)

        #Tentative d'élagage
        if(len(best) <= min_expected + len(C) and min_expected != np.infty):
            cpt += 2 ** (total - len(C))
            #On empile pas
            continue

        #Recherche d'un arrête selon laquelle brancher
        e = None
        for i in graph.adjacence_list:
            if(len(graph.adjacence_list[i]) >= 1):
                s1=i
                e = (i,graph.adjacence_list[i][0])
                break

        #MAJ de la pile si arréte il y a :
        if(e != None):
            pile.append(Node(graph.supprimer_sommet(e[1]),C + [e[1]]))
            pile.append(Node(graph.supprimer_sommet(e[0]),C + [e[0]],e[1]))

    return best


def parcours_profondeur_lite_ameliore_2(G,estimateurs_bornes=[borne_1,borne_2,borne_3]):
    pile = []
    pile.append(Node(G,[]))
    best = G.n*[9]
    total = G.n
    cpt = 0
    #Recherce d'une arréte
    while not (len(pile) == 0):
        N = pile.pop()
        C = N.solution_courante
        graph = N.graphe_r

        if N.v != "":
            for s in graph.adjacence_list[N.v]:
                C.append(s)
                graph.supprimer_sommet(s)

        #Calcul d'une solution réalisable
        R = AlgoAdjacence.algo_couplage(graph)

        if(len(R) + len(C) < len(best)):
            best = R + C

        #Calcul des bornes
        bornes = []
        for i in estimateurs_bornes:
            bornes.append(i(graph))

        min_expected = max(bornes)

        #Tentative d'élagage
        if(len(best) <= min_expected + len(C) and min_expected != np.infty):
            cpt += 2 ** (total - len(C))
            #On empile pas
            continue

        #Recherche d'un arrête selon laquelle brancher
        e = None
        if graph.m != 0:
            u = graph.degre_max()
            e = [u,graph.adjacence_list[u][0]]

        #MAJ de la pile si arréte il y a :
        if(e != None):
            pile.append(Node(graph.supprimer_sommet(e[1]),C + [e[1]]))
            pile.append(Node(graph.supprimer_sommet(e[0]),C + [e[0]],e[1]))

    return best

#L = generation_arbre(G1,estimateurs_borne=[borne_1,borne_2,borne_3])
#parcours_profondeur(G1,estimateurs_bornes=[borne_1,borne_2,borne_3])
#print(L)
