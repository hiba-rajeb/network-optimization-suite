import networkx as nx
import logging

logger = logging.getLogger(__name__)


def executer_prim(graphe):
    try:
        acm = nx.minimum_spanning_tree(graphe, algorithm='prim', weight='cout')

        liaisons    = []
        cout_total  = 0
        dist_totale = 0

        for u, v, data in sorted(acm.edges(data=True), key=lambda x: x[2].get('cout', 0)):
            liaisons.append({
                'de':       u,
                'vers':     v,
                'distance': data.get('distance', 0),
                'cout':     data.get('cout', 0),
            })
            cout_total  += data.get('cout', 0)
            dist_totale += data.get('distance', 0)

        logger.info(f"Prim ACM: {len(liaisons)} arêtes, coût={cout_total} DH, dist={dist_totale} km")
        return {
            'succes':     True,
            'acm':        acm,
            'liaisons':   liaisons,
            'cout_total': cout_total,
            'dist_totale': dist_totale,
        }
    except Exception as e:
        logger.exception("Erreur Prim")
        return {'succes': False, 'erreur': str(e)}
