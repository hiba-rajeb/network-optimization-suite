import networkx as nx
import logging

logger = logging.getLogger(__name__)


def executer_dijkstra(graphe, source, destination):
    try:
        chemin = nx.dijkstra_path(graphe, source, destination, weight='distance')
        dist   = nx.dijkstra_path_length(graphe, source, destination, weight='distance')

        cout = sum(
            graphe[chemin[i]][chemin[i + 1]]['cout']
            for i in range(len(chemin) - 1)
        )

        logger.info(f"Dijkstra {source}→{destination}: {chemin}, {dist} km, {cout} DH")
        return {'succes': True, 'chemin': chemin, 'distance': dist, 'cout': cout}

    except nx.NetworkXNoPath:
        msg = f"Aucun chemin entre {source} et {destination}"
        logger.warning(msg)
        return {'succes': False, 'erreur': msg}
    except nx.NodeNotFound as e:
        msg = f"Ville non trouvée : {e}"
        logger.error(msg)
        return {'succes': False, 'erreur': msg}
    except Exception as e:
        logger.exception("Erreur inattendue Dijkstra")
        return {'succes': False, 'erreur': str(e)}
