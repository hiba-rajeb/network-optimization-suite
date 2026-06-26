"""
Algorithme de Welsh-Powell pour la coloration de graphe.
Utilisé pour assigner des couleurs aux nœuds de manière à ce que
deux nœuds adjacents n'aient jamais la même couleur.
"""

import logging
import networkx as nx

logger = logging.getLogger(__name__)


def executer_welsh_powell(graphe):
    """
    Applique l'algorithme de Welsh-Powell pour colorier le graphe.
    
    Args:
        graphe: Un graphe NetworkX
    
    Returns:
        dict: Résultat contenant:
            - succes (bool): True si l'algorithme a réussi
            - coloration (dict): Dictionnaire {noeud: couleur}
            - nb_couleurs (int): Nombre de couleurs utilisées
            - chromatique (int): Nombre chromatique (même valeur)
            - erreur (str): Message d'erreur si échec
    """
    try:
        if not graphe or graphe.number_of_nodes() == 0:
            return {
                'succes': False,
                'erreur': "Le graphe est vide",
            }
        
        # Étape 1 : Trier les nœuds par degré décroissant
        noeuds_tries = sorted(graphe.nodes(), 
                             key=lambda n: graphe.degree(n), 
                             reverse=True)
        
        # Étape 2 : Initialiser la coloration
        coloration = {}
        couleur_actuelle = 0
        
        # Étape 3 : Colorier les nœuds
        while len(coloration) < len(noeuds_tries):
            # Trouver tous les nœuds non coloriés qui peuvent prendre la couleur actuelle
            noeuds_a_colorier = []
            
            for noeud in noeuds_tries:
                if noeud in coloration:
                    continue
                
                # Vérifier si ce nœud peut prendre la couleur actuelle
                # Un nœud peut prendre la couleur si aucun de ses voisins déjà colorié n'a cette couleur
                peut_colorier = True
                for voisin in graphe.neighbors(noeud):
                    if voisin in coloration and coloration[voisin] == couleur_actuelle:
                        peut_colorier = False
                        break
                
                if peut_colorier:
                    # On vérifie aussi qu'aucun nœud déjà ajouté à la liste n'est voisin
                    est_compatible = True
                    for noeud_deja_ajoute in noeuds_a_colorier:
                        if graphe.has_edge(noeud, noeud_deja_ajoute):
                            est_compatible = False
                            break
                    
                    if est_compatible:
                        noeuds_a_colorier.append(noeud)
            
            # Assigner la couleur actuelle à tous les nœuds valides
            for noeud in noeuds_a_colorier:
                coloration[noeud] = couleur_actuelle
            
            # Passer à la couleur suivante
            couleur_actuelle += 1
        
        nb_couleurs = couleur_actuelle
        
        logger.info(f"Welsh-Powell : {nb_couleurs} couleurs utilisées pour {len(coloration)} nœuds")
        
        return {
            'succes': True,
            'coloration': coloration,
            'nb_couleurs': nb_couleurs,
            'chromatique': nb_couleurs,
        }
    
    except Exception as e:
        logger.exception("Erreur dans Welsh-Powell")
        return {
            'succes': False,
            'erreur': f"Erreur lors de l'exécution : {str(e)}",
        }
