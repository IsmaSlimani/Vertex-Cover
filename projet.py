import random
import copy
import time
import matplotlib.pyplot as plt
import numpy as np
import math

def remove_node(graph,node):
    graph_bis = copy.deepcopy(graph)
    if node in graph_bis.keys():
        del graph_bis[node]
        for value in graph_bis.values():
            if node in value:
                value.remove(node)
    return graph_bis

def delete_multiple_nodes(graph, list_nodes):
    graph_bis = copy.deepcopy(graph)
    for i in list_nodes:
        if i in graph_bis.keys():
            del graph_bis[i]
            for value in graph_bis.values():
                if i in value:
                    value.remove(i)
    return graph_bis

def generer_instance(n, p):
    if n>0 and p<1 and p>0:
        graph = {i: [] for i in range(n)}
        for i in range(n):
            for j in range(i+1,n):
                proba = random.random()
                if proba>p:
                    graph[i].append(j)
                    graph[j].append(i)
    else:
        print('Valeur invalide de n ou p')
    return graph

def max_degree_graph(graph):
    max_degree = -1
    for key in graph.keys():
        if len(graph[key])>max_degree:
            max_degree = len(graph[key])
            node = key
    return node, max_degree


def liste_aretes(g):
    aretes = []
    for node in g.keys():
        for voisin in g[node]:
            if (node,voisin) not in aretes and (voisin,node) not in aretes:
                aretes.append((node,voisin))
    return aretes

def algo_couplage(g):
    C = []
    aretes = liste_aretes(g)
    for (node1,node2) in aretes:
        if node1 not in C and node2 not in C:
            C.append(node1)
            C.append(node2)
    return C

def algo_glouton(g):
    C = []
    e = liste_aretes(g)
    graph_bis = copy.deepcopy(g)
    while len(e)>0:
        node_deg_max,max_degree = max_degree_graph(graph_bis)
        C.append(node_deg_max)
        graph_bis = remove_node(graph_bis, node_deg_max)
        for (a,b) in e.copy():
            if (node_deg_max == a or node_deg_max == b) :
                e.remove((a,b))
    return C

def branchement(G):
    #Cas où le graphe est vide
    if len(G) == 0:
        print("Le graphe est vide")
        return None,None
        
    opti_sol = algo_couplage(G)
    e = liste_aretes(G)
    
    #Cas où le graphe n'a pas d'arêtes
    if (e == []):
        return [key for key in G.keys()], 1
    (a,b) = e[0]
    node = []
    noeuds_générés = 2
    
    #Création du noeud droit
    right_child_graph = remove_node(G,b)
    right_child_aretes = liste_aretes(right_child_graph)
    node.insert(0,[[b],right_child_graph,right_child_aretes])
    
    #Création du noeud gauche
    left_child_sommet = a
    left_child_graph = remove_node(G,a)
    left_child_aretes = liste_aretes(left_child_graph)
    node.insert(0,[[a],left_child_graph,left_child_aretes])
    
    while(len(node)>0):
        noeud = node.pop(0)
        if noeud[2] == []:
            if len(opti_sol)>len(noeud[0]):
                opti_sol = noeud[0]
        else:
            (a,b) = noeud[2][0]
            #(a,b) = random.choice(noeud[2])
            #Création du noeud droit
            right_child_graph = remove_node(noeud[1],b)
            right_child_aretes = liste_aretes(right_child_graph)
            right_c = copy.deepcopy(noeud[0])
            right_c.append(b)
            if len(opti_sol)>=len(right_c):
                node.insert(0,[right_c,right_child_graph,right_child_aretes])
                noeuds_générés += 1
                
            #Création du noeud gauche
            left_child_sommet = a
            left_child_graph = remove_node(noeud[1],a)
            left_child_aretes = liste_aretes(left_child_graph)
            left_c = copy.deepcopy(noeud[0])
            left_c.append(a)
            if len(opti_sol)>=len(left_c):  
                node.insert(0,[left_c,left_child_graph,left_child_aretes])
                noeuds_générés += 1
    
    return opti_sol, noeuds_générés

def calcul_borne_inf(G):
    _, max_degree = max_degree_graph(G)
    couplage = algo_couplage(G)
    n = len(list(G.keys()))
    m = len(liste_aretes(G))

    b1 = math.ceil(m/max_degree)
    b2 = len(couplage)/2
    b3 = ((2*n)-1-(np.sqrt(((2*n)-1)**2 - 8*m)))/2
    return np.max([b1,b2,b3])


#Fonction branchement (avec ajout de bornes)
def branchement_couplage(G):
    #Cas où le graphe est vide
    if len(G) == 0:
        print("Le graphe est vide")
        return None,None
    
    #Cas où le graphe n'a pas d'arêtes
    e = liste_aretes(G)
    if (e == []):
        return [key for key in G.keys()], 1
    
    opti_sol = algo_couplage(G)
    borneInf = calcul_borne_inf(G)
    borneSup = len(algo_couplage(G))
    #Si la borne inférieure est supérieure ou égale à la borne supérieure
    #Retourner directement la solution obtenue avec l'algo couplage
    if borneInf >= borneSup:
        return opti_sol, 1
    
    (a,b) = e[0]
    node = []
    noeuds_générés = 2
    
    #Création du noeud droit
    right_child_graph = remove_node(G,b)
    right_child_aretes = liste_aretes(right_child_graph)
    if len(right_child_aretes) != 0:
        newBorneInf_r = calcul_borne_inf(right_child_graph)
        newBorneSup_r = len(algo_couplage(right_child_graph))
    else:
        newBorneInf_r = None
        newBorneSup_r = None
            
      
    #On élague si borne_sup < borne_inf ou si borne_inf > taille de la solution optimale
    #Avant d'insérer le noeud dans la pile on vérifie si les deux condition ne sont pas vérifiées
    if (newBorneInf_r != None and not(newBorneSup_r < newBorneInf_r or newBorneInf_r > len(opti_sol))):
        node.insert(0,[[b],right_child_graph,right_child_aretes,newBorneInf_r,newBorneSup_r])
    elif len(opti_sol)>1:
        opti_sol = [b]
        noeuds_générés = 1
    #Création du noeud gauche
    left_child_sommet = a
    left_child_graph = remove_node(G,a)
    left_child_aretes = liste_aretes(left_child_graph)
    if len(left_child_aretes) != 0:
        newBorneInf_l = calcul_borne_inf(left_child_graph)
        newBorneSup_l = len(algo_couplage(left_child_graph))
    else:
        newBorneInf_l = None
        newBorneSup_l = None
        
    if (newBorneInf_l != None and not(newBorneSup_l < newBorneInf_l or newBorneInf_l > len(opti_sol))):
        node.insert(0,[[a],left_child_graph,left_child_aretes,newBorneInf_l,newBorneSup_l])
    elif len(opti_sol)>1:
        opti_sol = [a]
        noeuds_générés = 1
        
    while(len(node)>0):
        noeud = node.pop(0)
        if noeud[2] != []:
            (a,b) = noeud[2][0]
            #Création du noeud droit
            right_child_graph = remove_node(noeud[1],b)
            right_child_aretes = liste_aretes(right_child_graph)
            right_c = copy.deepcopy(noeud[0])
            right_c.append(b)
            if len(right_child_aretes) != 0:
                newBorneInf_r = calcul_borne_inf(right_child_graph)
                newBorneSup_r = len(algo_couplage(right_child_graph))
            else:
                newBorneInf_r = None
                newBorneSup_r = None
            if (newBorneInf_r != None and not(newBorneSup_r < newBorneInf_r or newBorneInf_r > len(opti_sol))):
                if len(opti_sol)>=len(right_c):
                    node.insert(0,[right_c,right_child_graph,right_child_aretes,newBorneInf_r,newBorneSup_r])
                    noeuds_générés += 1
            
            elif len(opti_sol)>len(right_c):
                opti_sol = right_c

            #Création du noeud gauche
            left_child_sommet = a
            left_child_graph = remove_node(noeud[1],a)
            left_child_aretes = liste_aretes(left_child_graph)
            left_c = copy.deepcopy(noeud[0])
            left_c.append(a)
            if len(left_child_aretes) != 0:
                newBorneInf_l = calcul_borne_inf(left_child_graph)
                newBorneSup_l = len(algo_couplage(left_child_graph))
            else:
                newBorneInf_l = None
                newBorneSup_l = None
            if (newBorneInf_l != None and not(newBorneSup_l < newBorneInf_l or newBorneInf_l > len(opti_sol))):
                if len(opti_sol)>=len(left_c):
                    node.insert(0,[left_c,left_child_graph,left_child_aretes,newBorneInf_l,newBorneSup_l])
                    noeuds_générés += 1
            elif len(opti_sol)>len(left_c):
                opti_sol = left_c

    return opti_sol, noeuds_générés

#Branchement avec ajout de bornes et voisins
def branchement_couplage_voisins(G):
    #Cas où le graphe est vide
    if len(G) == 0:
        print("Le graphe est vide")
        return None,None
   
    #Cas où le graphe n'a pas d'arêtes
    e = liste_aretes(G)
    if (e == []):
        return [key for key in G.keys()], 1
   
    opti_sol = algo_couplage(G)
    borneInf = calcul_borne_inf(G)
    borneSup = len(algo_couplage(G))
    #Si la borne inférieure est supérieure ou égale à la borne supérieure
    #Retourner directement la solution obtenue avec l'algo couplage
    if borneInf >= borneSup:
        return opti_sol, 1
   
    (a,b) = e[0]
    node = []
    noeuds_générés = 2
   
    #Création du noeud droit
    right_child_graph = remove_node(G,b)
    right_child_aretes = liste_aretes(right_child_graph)
    right_c = [b]
   
    #supprimer les voisins du sommet a de l'arete (a,b):
    if len(right_child_aretes) != 0:
        voisins_right_child = right_child_graph[a]
        right_child_graph = remove_node(right_child_graph,a)
        for voisin in voisins_right_child:
            if voisin in right_child_graph:
                right_child_graph = remove_node(right_child_graph,voisin)
                #actualiser la liste d'aretes du graphe du noeud droit:
                right_child_aretes = liste_aretes(right_child_graph)
                right_c.append(voisin)
     
   
    if len(right_child_aretes) != 0:  
        newBorneInf_r = calcul_borne_inf(right_child_graph)
        newBorneSup_r = len(algo_couplage(right_child_graph))
    else:
        newBorneInf_r = None
        newBorneSup_r = None
       
    #On élague si borne_sup < borne_inf ou si borne_inf > taille de la solution optimale
    #Avant d'insérer le noeud dans la pile on vérifie si les deux condition ne sont pas vérifiées
    if (newBorneInf_r != None and not(newBorneSup_r < newBorneInf_r or newBorneInf_r > len(opti_sol))):
        node.insert(0,[right_c,right_child_graph,right_child_aretes,newBorneInf_r,newBorneSup_r])
    elif len(opti_sol)> len(right_c):
        opti_sol = right_c
        noeuds_générés = 1
       
    #Création du noeud gauche
    left_child_sommet = a
    left_child_graph = remove_node(G,a)
    left_child_aretes = liste_aretes(left_child_graph)
    if len(left_child_aretes) != 0:
        newBorneInf_l = calcul_borne_inf(left_child_graph)
        newBorneSup_l = len(algo_couplage(left_child_graph))
    else:
        newBorneInf_l = None
        newBorneSup_l = None
       
    if (newBorneInf_l != None and not(newBorneSup_l < newBorneInf_l or newBorneInf_l > len(opti_sol))):
        node.insert(0,[[a],left_child_graph,left_child_aretes,newBorneInf_l,newBorneSup_l])
    elif len(opti_sol)>1:
        opti_sol = [a]
        noeuds_générés = 1
       
       
    while(len(node)>0):
        noeud = node.pop(0)
        #si le graphe en tete de pile n'a pas d'aretes:
        if len(noeud[2])==0 :
            if len(opti_sol)>len(noeud[0]):
                opti_sol = noeud[0]
        else:
            (a,b) = noeud[2][0] #recuperer la premiere arete
            #Création du noeud droit
            right_child_graph = remove_node(noeud[1],b)
            right_child_aretes = liste_aretes(right_child_graph)
            right_c = copy.deepcopy(noeud[0])
            right_c.append(b)
           
            if len(right_child_aretes) != 0:
                voisins_right_child = right_child_graph[a]
                #comme nous allons prendre dans la couverture tous les voisins
                #de (a) autant supprimer (a)
                right_child_graph = remove_node(right_child_graph,a)
                for voisin in voisins_right_child:
                    if voisin in right_child_graph:
                        #supprimer les voisins de (a) du graphe du noeud droit:
                        right_child_graph = remove_node(right_child_graph,voisin)
                        right_child_aretes = liste_aretes(right_child_graph)
                        #ajouter les voisins à la couverture:
                        right_c.append(voisin)
           
           
            if len(right_child_aretes) != 0:
                newBorneInf_r = calcul_borne_inf(right_child_graph)
                newBorneSup_r = len(algo_couplage(right_child_graph))
            else:
                newBorneInf_r = None
                newBorneSup_r = None
            if (newBorneInf_r != None and not(newBorneSup_r < newBorneInf_r or newBorneInf_r > len(opti_sol))):
                if len(opti_sol)>=len(right_c):
                    node.insert(0,[right_c,right_child_graph,right_child_aretes,newBorneInf_r,newBorneSup_r])
                    noeuds_générés += 1
           
            elif len(opti_sol)>len(right_c):
                opti_sol = right_c
           
           
            #Création du noeud gauche
            left_child_sommet = a
            left_child_graph = remove_node(noeud[1],a)
            left_child_aretes = liste_aretes(left_child_graph)
            left_c = copy.deepcopy(noeud[0])
            left_c.append(a)
            if len(left_child_aretes) != 0:
                newBorneInf_l = calcul_borne_inf(left_child_graph)
                newBorneSup_l = len(algo_couplage(left_child_graph))
            else:
                newBorneInf_l = None
                newBorneSup_l = None
            if (newBorneInf_l != None and not(newBorneSup_l < newBorneInf_l or newBorneInf_l > len(opti_sol))):
                if len(opti_sol)>=len(left_c):
                    node.insert(0,[left_c,left_child_graph,left_child_aretes,newBorneInf_l,newBorneSup_l])
                    noeuds_générés += 1
            elif len(opti_sol)>len(left_c):
                opti_sol = left_c

    return opti_sol, noeuds_générés


#Branchement avec ajout de bornes, voisins et degré max.
def branchement_couplage_voisins_2(G):
    #Cas où le graphe est vide
    if len(G) == 0:
        print("Le graphe est vide")
        return None,None
   
    #Cas où le graphe n'a pas d'arêtes
    e = liste_aretes(G)
    if (e == []):
        return [key for key in G.keys()], 1
   
    opti_sol = algo_couplage(G)
    borneInf = calcul_borne_inf(G)
    borneSup = len(algo_couplage(G))
    #Si la borne inférieure est supérieure ou égale à la borne supérieure
    #Retourner directement la solution obtenue avec l'algo couplage
    if borneInf >= borneSup:
        return opti_sol, 1
   
    sommet_degree_max ,_ = max_degree_graph(G)
    graph_degree_max = dict()
    graph_degree_max[sommet_degree_max] = G[sommet_degree_max] 
    (a,b) = liste_aretes(graph_degree_max)[0]
    node = []
    noeuds_générés = 2
   
    #Création du noeud droit
    right_child_graph = remove_node(G,b)
    right_child_aretes = liste_aretes(right_child_graph)
    right_c = [b]
   
    #supprimer les voisins du sommet a de l'arete (a,b):
    if len(right_child_aretes) != 0:
        voisins_right_child = right_child_graph[a]
        right_child_graph = remove_node(right_child_graph,a)
        for voisin in voisins_right_child:
            if voisin in right_child_graph:
                right_child_graph = remove_node(right_child_graph,voisin)
                #actualiser la liste d'aretes du graphe du noeud droit:
                right_child_aretes = liste_aretes(right_child_graph)
                right_c.append(voisin)
     
   
    if len(right_child_aretes) != 0:  
        newBorneInf_r = calcul_borne_inf(right_child_graph)
        newBorneSup_r = len(algo_couplage(right_child_graph))
    else:
        newBorneInf_r = None
        newBorneSup_r = None
       
    #On élague si borne_sup < borne_inf ou si borne_inf > taille de la solution optimale
    #Avant d'insérer le noeud dans la pile on vérifie si les deux condition ne sont pas vérifiées
    if (newBorneInf_r != None and not(newBorneSup_r < newBorneInf_r or newBorneInf_r > len(opti_sol))):
        node.insert(0,[right_c,right_child_graph,right_child_aretes,newBorneInf_r,newBorneSup_r])
    elif len(opti_sol)> len(right_c):
        opti_sol = right_c
        noeuds_générés = 1
       
    #Création du noeud gauche
    left_child_sommet = a
    left_child_graph = remove_node(G,a)
    left_child_aretes = liste_aretes(left_child_graph)
    if len(left_child_aretes) != 0:
        newBorneInf_l = calcul_borne_inf(left_child_graph)
        newBorneSup_l = len(algo_couplage(left_child_graph))
    else:
        newBorneInf_l = None
        newBorneSup_l = None
       
    if (newBorneInf_l != None and not(newBorneSup_l < newBorneInf_l or newBorneInf_l > len(opti_sol))):
        node.insert(0,[[a],left_child_graph,left_child_aretes,newBorneInf_l,newBorneSup_l])
    elif len(opti_sol)>1:
        opti_sol = [a]
        noeuds_générés = 1
       
       
    while(len(node)>0):
        noeud = node.pop(0)
        #si le graphe en tete de pile n'a pas d'aretes:
        if len(noeud[2])==0 :
            if len(opti_sol)>len(noeud[0]):
                opti_sol = noeud[0]
        else:
            sommet_degree_max ,_ = max_degree_graph(noeud[1])
            graph_degree_max = dict()
            graph_degree_max[sommet_degree_max] = noeud[1][sommet_degree_max] 
            (a,b) = liste_aretes(graph_degree_max)[0] #recuperer l'arete qui possède le sommet de degré max
            #Création du noeud droit
            right_child_graph = remove_node(noeud[1],b)
            right_child_aretes = liste_aretes(right_child_graph)
            right_c = copy.deepcopy(noeud[0])
            right_c.append(b)
           
            if len(right_child_aretes) != 0:
                voisins_right_child = right_child_graph[a]
                #comme nous allons prendre dans la couverture tous les voisins
                #de (a) autant supprimer (a)
                right_child_graph = remove_node(right_child_graph,a)
                for voisin in voisins_right_child:
                    if voisin in right_child_graph:
                        #supprimer les voisins de (a) du graphe du noeud droit:
                        right_child_graph = remove_node(right_child_graph,voisin)
                        right_child_aretes = liste_aretes(right_child_graph)
                        #ajouter les voisins à la couverture:
                        right_c.append(voisin)
           
           
            if len(right_child_aretes) != 0:
                newBorneInf_r = calcul_borne_inf(right_child_graph)
                newBorneSup_r = len(algo_couplage(right_child_graph))
            else:
                newBorneInf_r = None
                newBorneSup_r = None
            if (newBorneInf_r != None and not(newBorneSup_r < newBorneInf_r or newBorneInf_r > len(opti_sol))):
                if len(opti_sol)>=len(right_c):
                    node.insert(0,[right_c,right_child_graph,right_child_aretes,newBorneInf_r,newBorneSup_r])
                    noeuds_générés += 1
           
            elif len(opti_sol)>len(right_c):
                opti_sol = right_c
           
           
            #Création du noeud gauche
            left_child_sommet = a
            left_child_graph = remove_node(noeud[1],a)
            left_child_aretes = liste_aretes(left_child_graph)
            left_c = copy.deepcopy(noeud[0])
            left_c.append(a)
            if len(left_child_aretes) != 0:
                newBorneInf_l = calcul_borne_inf(left_child_graph)
                newBorneSup_l = len(algo_couplage(left_child_graph))
            else:
                newBorneInf_l = None
                newBorneSup_l = None
            if (newBorneInf_l != None and not(newBorneSup_l < newBorneInf_l or newBorneInf_l > len(opti_sol))):
                if len(opti_sol)>=len(left_c):
                    node.insert(0,[left_c,left_child_graph,left_child_aretes,newBorneInf_l,newBorneSup_l])
                    noeuds_générés += 1
            elif len(opti_sol)>len(left_c):
                opti_sol = left_c

    return opti_sol, noeuds_générés


def test_temps_glouton_vs_couplage_sommets():
    times_n_couplage = [] #Tableau dans lequel les résultats des temps d'exécution seront placés pour couplage
    times_n_glouton = [] #Tableau dans lequel les résultats des temps d'exécution seront placés pour glouton
    nb_sommets = []
    for i in range(50,100):
        nb_sommets.append(i) #Garder les sommets pour placer les valeurs après dans l'axe x dans le graphe
        delta1 = 0
        delta2 = 0
        for j in range(30): #Boucle pour refaire le test 50 fois à chaque fois pour chaque taille
            graph = generer_instance(i,0.5) #Générer le graphe à chaque fois
            #Tester l'algo couplage avec le graphe courant
            start_time1 = time.time()
            graph_bis = algo_couplage(graph)
            end_time1 = time.time()
            delta1 += end_time1 - start_time1
            #Tester l'algo glouton avec le test courant
            start_time2 = time.time()
            graph_bis = algo_glouton(graph)
            end_time2 = time.time()
            delta2 += end_time2 - start_time2
        #Faire le calcul de la moyenne pour les deux algo
        moy1 = delta1/30
        moy2 = delta2/30
        #Ajouter le résultat pour la taille n dans les tableaux
        times_n_couplage.append(moy1)
        times_n_glouton.append(moy2)


    plt.plot(nb_sommets, times_n_couplage, label='Couplage') #Plot la ligne pour l'algo couplage
    plt.plot(nb_sommets, times_n_glouton, label='Glouton') #Plot la ligne pour l'algo glouton
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Temps d'exécution")
    plt.legend()
    plt.title("Temps d'exécution en fonction du nombre de sommets")
    plt.show()
    
def test_temps_glouton_vs_couplage_proba():
    times_p_couplage = []
    times_p_glouton = []
    p = [0.1,0.3,0.5,0.7,0.9]
    for i in p:
        delta1 = 0
        delta2 = 0
        for j in range(50):
            graph = generer_instance(50,i)
            start_time1 = time.time()
            graph_bis_couplage = algo_couplage(graph)
            end_time1 = time.time()
            delta1 += end_time1 - start_time1
            start_time2 = time.time()
            graph_bis_glouton = algo_glouton(graph)
            end_time2 = time.time()
            delta2 += end_time2 - start_time2
        moy1 = delta1/50
        moy2 = delta2/50
        times_p_couplage.append(moy1)
        times_p_glouton.append(moy2)
        
    plt.plot(p, times_p_couplage, label='Couplage')
    plt.plot(p, times_p_glouton, label='Glouton')
    plt.xlabel("Probabilité")
    plt.ylabel("Temps d'exécution")
    plt.legend()
    plt.title("Temps d'exécution en fonction de la probabilité p")
    plt.show()

def test_qualité_glouton_vs_couplage_sommets():
    len_n_couplage = [] #Tableau dans lequel les résultats des temps d'exécution seront placés pour couplage
    len_n_glouton = [] #Tableau dans lequel les résultats des temps d'exécution seront placés pour glouton
    nb_sommets = []
    for i in range(50,100):
        nb_sommets.append(i) #Garder les sommets pour placer les valeurs après dans l'axe x dans le graphe
        delta1 = 0
        delta2 = 0
        for j in range(30): #Boucle pour refaire le test 50 fois à chaque fois pour chaque taille
            graph = generer_instance(i,0.5) #Générer le graphe à chaque fois
            #Tester l'algo couplage avec le graphe courant
            graph_bis_couplage = algo_couplage(graph)
            delta1 += len(graph_bis_couplage)
            #Tester l'algo glouton avec le test courant
            graph_bis_glouton = algo_glouton(graph)
            delta2 += len(graph_bis_glouton)
        #Faire le calcul de la moyenne pour les deux algo
        moy1 = delta1/30
        moy2 = delta2/30
        #Ajouter le résultat pour la taille n dans les tableaux
        len_n_couplage.append(moy1)
        len_n_glouton.append(moy2)
    plt.plot(nb_sommets, len_n_couplage, label='Couplage') #Plot la ligne pour l'algo couplage
    plt.plot(nb_sommets, len_n_glouton, label='Glouton') #Plot la ligne pour l'algo glouton
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Qualité de la solution")
    plt.legend()
    plt.title("Qualité de la solution en fonction du nombre de sommets")
    plt.show()
    
def test_qualité_glouton_vs_couplage_proba():
    len_p_couplage = []
    len_p_glouton = []
    p = [0.1,0.3,0.5,0.7,0.9]
    for i in p:
        delta1 = 0
        delta2 = 0
        for j in range(50):
            graph = generer_instance(50,i)
            graph_bis_couplage = algo_couplage(graph)
            delta1 += len(graph_bis_couplage)
            graph_bis_glouton = algo_glouton(graph)
            delta2 += len(graph_bis_glouton)
        moy1 = delta1/50
        moy2 = delta2/50
        len_p_couplage.append(moy1)
        len_p_glouton.append(moy2)
    plt.plot(p, len_p_couplage, label='Couplage')
    plt.plot(p, len_p_glouton, label='Glouton')
    plt.xlabel("Probabilité")
    plt.ylabel("Qualité de la solution")
    plt.legend()
    plt.title("Qualité de la solution en fonction de la probabilité p")
    plt.show()
    
def test_branchements():
    times_n_branchement = [] #Tableau dans lequel les résultats des temps d'exécution seront placés pour branchement
    times_n_branchement_couplage = []
    times_n_branchement_voisins = []
    times_n_branchement_voisins_2 = []
    nb_sommets = []
    nb_noeuds_générés_branchement = []
    nb_noeuds_générés_branchement_couplage = []
    nb_noeuds_générés_branchement_voisins = []
    nb_noeuds_générés_branchement_voisins_2 = []
    for i in range(2,16):
        nb_sommets.append(i) #Garder les sommets pour placer les valeurs après dans l'axe x dans le graphe
        delta1 = 0
        delta2 = 0
        delta3 = 0
        delta4 = 0
        delta_bis1 = 0
        delta_bis2 = 0
        delta_bis3 = 0
        delta_bis4 = 0
        for j in range(30): #Boucle pour refaire le test 30 fois à chaque fois pour chaque taille
            graph = generer_instance(i,0.5) #Générer le graphe à chaque fois
            #Tester l'algo branchement avec le graphe courant
            start_time1 = time.time()
            graph_bis_b1,nb_noeuds_générés_b1 = branchement(graph)
            end_time1 = time.time()
            delta1 += end_time1 - start_time1
            delta_bis1 += nb_noeuds_générés_b1
            #Tester l'algo branchement couplage avec le test courant
            start_time2 = time.time()
            graph_bis_b2,nb_noeuds_générés_b2 = branchement_couplage(graph)
            end_time2 = time.time()
            delta2 += end_time2 - start_time2
            delta_bis2 += nb_noeuds_générés_b2

            #Tester l'algo branchement couplage voisins avec le test courant
            start_time3 = time.time()
            graph_bis_b3,nb_noeuds_générés_b3 = branchement_couplage_voisins(graph)
            end_time3 = time.time()
            delta3 += end_time3 - start_time3
            delta_bis3 += nb_noeuds_générés_b3

            #Tester l'algo branchement couplage voisins avec degré max avec le test courant
            start_time4 = time.time()
            graph_bis_b4,nb_noeuds_générés_b4 = branchement_couplage_voisins_2(graph)
            end_time4 = time.time()
            delta4 += end_time4 - start_time4
            delta_bis4 += nb_noeuds_générés_b4

        #Faire le calcul de la moyenne pour les quatres algo
        moy1 = delta1/30
        moy2 = delta2/30
        moy3 = delta3/30
        moy4 = delta4/30
        moy_bis1 = delta_bis1/30
        moy_bis2 = delta_bis2/30
        moy_bis3 = delta_bis3/30
        moy_bis4 = delta_bis4/30

        #Ajouter le résultat pour la taille n dans les tableaux
        times_n_branchement.append(moy1)
        times_n_branchement_couplage.append(moy2)
        times_n_branchement_voisins.append(moy3)
        times_n_branchement_voisins_2.append(moy4)
        nb_noeuds_générés_branchement.append(moy_bis1)
        nb_noeuds_générés_branchement_couplage.append(moy_bis2)
        nb_noeuds_générés_branchement_voisins.append(moy_bis3)
        nb_noeuds_générés_branchement_voisins_2.append(moy_bis4)
    
    times_p_branchement = []
    p = [0.1,0.3,0.5,0.7,0.9]
    for i in p:
        delta1 = 0
        for j in range(50):
            graph = generer_instance(10,i)
            start_time1 = time.time()
            graph_bis_b1,nb_noeuds_générés_b1 = branchement(graph)
            end_time1 = time.time()
            delta1 += end_time1 - start_time1
        moy1 = delta1/50
        times_p_branchement.append(moy1)
        
    #Graphique qui étudie l'évolution du temps de calcul pour l'algorithme de branchement en fonction du nombre de sommets
    plt.plot(nb_sommets, times_n_branchement, label='Branchement')
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Temps d'exécution")
    plt.legend()
    plt.title("Temps de calcul en fonction du nombre de sommets")
    plt.show()
    
    #Graphique qui étudie l'évolution du temps de calcul pour l'algorithme de branchement en fonction de la proba p
    plt.plot(p, times_p_branchement, label='Branchement')
    plt.xlabel("Probabilité")
    plt.ylabel("Temps d'exécution")
    plt.legend()
    plt.title("Temps de calcul en fonction de la probabilité p")
    plt.show()
    
    #Graphique qui compare les quatres fonctions branchement (temps de calcul)
    plt.plot(nb_sommets, times_n_branchement, label='Branchement')
    plt.plot(nb_sommets, times_n_branchement_couplage, label='Branchement couplage')
    plt.plot(nb_sommets, times_n_branchement_voisins, label='Branchement voisins')
    plt.plot(nb_sommets, times_n_branchement_voisins_2, label='Branchement voisins degré max')
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Temps de calcul")
    plt.legend()
    plt.title("Temps de calcul en fonction du nombre de sommets")
    plt.show()
    
    #Graphique qui compare les quatres fonctions branchement (nombre de noeuds générés)
    plt.plot(nb_sommets, nb_noeuds_générés_branchement, label='Branchement')
    plt.plot(nb_sommets, nb_noeuds_générés_branchement_couplage, label='Branchement couplage')
    plt.plot(nb_sommets, nb_noeuds_générés_branchement_voisins, label='Branchement voisins')
    plt.plot(nb_sommets, nb_noeuds_générés_branchement_voisins_2, label='Branchement voisins degré max')
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Noeuds générés")
    plt.legend()
    plt.title("Nombre de noeuds générés en fonction du nombre de sommets")
    plt.show()
  


  

def rapport_approxim(algo1,algo2,algo3,nmax,p):
    x=[]
    y1=[]
    y2=[]
    N=nmax*(np.arange(10)+1)/10
    if(nmax>1):
        for i in (N):
            print(i)
            i=int(i)+1
            x.append(i)
            rcumul1=0
            rcumul2=0
            for j in range(20):
                g=generer_instance(i,p)
                while(len(g)==0):
                    g=generer_instance(i,p)
                C,nb_n=algo1(g)
                c1=len(C)
                c2=len(algo2(g))
                c3=len(algo3(g))
                rcumul1+=c2/c1
                rcumul2+=c3/c1
            y1.append(rcumul1/20)
            y2.append(rcumul2/20)
    else:
        print('nmax doit etre supérieur à 1')
    
    plt.xlabel('Nombre de sommets')
    plt.ylabel('Rapport d''approximation')
    plt.plot(x,y1,"r",label = 'Couplage')
    plt.plot(x,y2,"b",label='Glouton')
    plt.legend()
    plt.show()
   
