"""
Algorithme de Ford-Fulkerson pour calculer le flot maximal dans un réseau.
Utilisé pour trouver le flux maximum entre une source et un puits.
"""

import logging
import networkx as nx
from collections import deque

logger = logging.getLogger(__name__)


def executer_ford_fulkerson(reseau, source, puits):
    """
    Applique l'algorithme de Ford-Fulkerson pour calculer le flot maximal sur un graphe orienté.
    
    Args:
        reseau: Instance de ReseauElectrique
        source: Nœud source
        puits: Nœud puits
    
    Returns:
        dict: Résultat contenant:
            - succes (bool): True si l'algorithme a réussi
            - flot_max (int): Valeur du flot maximal
            - flot (dict): Flot sur chaque arête {(u,v): flot}
            - chemins (list): Liste des chemins augmentants trouvés
            - erreur (str): Message d'erreur si échec
    """
    try:
        # Créer un graphe orienté pour Ford-Fulkerson
        graphe_oriente = reseau.creer_graphe_oriente()
        
        if source not in graphe_oriente.nodes():
            return {
                'succes': False,
                'erreur': f"Le nœud source '{source}' n'existe pas dans le graphe",
            }
        
        if puits not in graphe_oriente.nodes():
            return {
                'succes': False,
                'erreur': f"Le nœud puits '{puits}' n'existe pas dans le graphe",
            }
        
        if source == puits:
            return {
                'succes': False,
                'erreur': "La source et le puits doivent être différents",
            }
        
        # Créer un graphe résiduel avec les capacités du graphe orienté
        graphe_residuel = nx.DiGraph()
        
        for u, v, data in graphe_oriente.edges(data=True):
            capacite = data.get('capacite', 50)  # Utiliser la capacité définie dans le graphe orienté
            graphe_residuel.add_edge(u, v, capacite=capacite, flot=0)
            # Ajouter l'arête inverse avec capacité 0 pour le graphe résiduel
            if not graphe_residuel.has_edge(v, u):
                graphe_residuel.add_edge(v, u, capacite=0, flot=0)
        
        def bfs_chemin_augmentant(graphe_res, s, t, parent):
            """Trouve un chemin augmentant en utilisant BFS"""
            visite = {s}
            queue = deque([s])
            
            while queue:
                u = queue.popleft()
                
                for v in graphe_res.neighbors(u):
                    capacite = graphe_res[u][v]['capacite']
                    flot = graphe_res[u][v]['flot']
                    
                    if v not in visite and capacite > flot:
                        visite.add(v)
                        queue.append(v)
                        parent[v] = u
                        
                        if v == t:
                            return True
            
            return False
        
        # Algorithme Ford-Fulkerson
        parent = {}
        flot_max = 0
        chemins_augmentants = []
        
        while bfs_chemin_augmentant(graphe_residuel, source, puits, parent):
            # Trouver le flot minimum le long du chemin
            flot_chemin = float('inf')
            v = puits
            chemin = []
            
            while v != source:
                u = parent[v]
                chemin.append((u, v))
                capacite = graphe_residuel[u][v]['capacite']
                flot_actuel = graphe_residuel[u][v]['flot']
                flot_chemin = min(flot_chemin, capacite - flot_actuel)
                v = u
            
            chemin.reverse()
            chemins_augmentants.append({
                'chemin': [source] + [v for u, v in chemin],
                'flot': flot_chemin
            })
            
            # Mettre à jour les flots
            v = puits
            while v != source:
                u = parent[v]
                graphe_residuel[u][v]['flot'] += flot_chemin
                graphe_residuel[v][u]['flot'] -= flot_chemin
                v = u
            
            flot_max += flot_chemin
            parent = {}
        
        # Extraire le flot final sur chaque arête
        flot_aretes = {}
        for u, v in graphe_oriente.edges():
            if graphe_residuel.has_edge(u, v):
                flot_aretes[(u, v)] = graphe_residuel[u][v]['flot']
        
        logger.info(f"Ford-Fulkerson : flot maximal = {flot_max} de {source} à {puits}")
        
        return {
            'succes': True,
            'flot_max': flot_max,
            'flot': flot_aretes,
            'chemins': chemins_augmentants,
            'nb_chemins': len(chemins_augmentants),
        }
    
    except Exception as e:
        logger.exception("Erreur dans Ford-Fulkerson")
        return {
            'succes': False,
            'erreur': f"Erreur lors de l'exécution : {str(e)}",
        }
