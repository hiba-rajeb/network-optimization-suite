import networkx as nx
import logging

logger = logging.getLogger(__name__)


def executer_bellman_ford(reseau, source, destination):
    """
    Exécute l'algorithme Bellman-Ford sur un graphe orienté.
    
    Args:
        reseau: Instance de ReseauElectrique
        source: Nœud source
        destination: Nœud destination
        
    Returns:
        dict: Résultat avec chemin, distance et coût
    """
    try:
        # Créer un graphe orienté pour Bellman-Ford
        graphe_oriente = reseau.creer_graphe_oriente()
        
        # Utiliser les poids comme poids pour l'algorithme (peut contenir des valeurs négatives)
        dist, chemin = nx.single_source_bellman_ford(
            graphe_oriente, source, target=destination, weight='poids'
        )

        # Calculer le coût total et la distance réelle
        cout_total = 0
        distance_totale = 0
        for i in range(len(chemin) - 1):
            arrete = graphe_oriente[chemin[i]][chemin[i + 1]]
            cout_total += arrete['cout']
            distance_totale += arrete['distance']

        logger.info(f"Bellman-Ford {source}→{destination}: {chemin}, poids: {dist}, distance: {distance_totale} km, coût: {cout_total} DH")
        return {
            'succes': True, 
            'chemin': chemin, 
            'poids': dist,
            'distance': distance_totale, 
            'cout': cout_total,
            'graphe_oriente': graphe_oriente
        }

    except nx.NetworkXNoPath:
        msg = f"Aucun chemin entre {source} et {destination}"
        logger.warning(msg)
        return {'succes': False, 'erreur': msg}
    except nx.NodeNotFound as e:
        msg = f"Ville non trouvée : {e}"
        logger.error(msg)
        return {'succes': False, 'erreur': msg}
    except nx.NetworkXUnbounded:
        msg = "Cycle de poids négatif détecté dans le réseau"
        logger.error(msg)
        return {'succes': False, 'erreur': msg}
    except Exception as e:
        logger.exception("Erreur inattendue Bellman-Ford")
        return {'succes': False, 'erreur': str(e)}
