import random
import logging

logger = logging.getLogger(__name__)


def generer_sources_destinations(nb_sources=3, nb_destinations=4):
    """Génère les listes de sources et destinations selon les paramètres"""
    sources = [f"V{i+1} (Centrale)" for i in range(nb_sources)]
    destinations = [f"V{i+nb_sources+1}" for i in range(nb_destinations)]
    return sources, destinations


def generer_donnees(nb_sources=3, nb_destinations=4):
    """Génère les données pour la méthode Nord-Ouest avec des paramètres variables"""
    sources, destinations = generer_sources_destinations(nb_sources, nb_destinations)
    
    offres   = [random.randint(100, 500) for _ in range(nb_sources)]
    demandes = [random.randint(80,  400) for _ in range(nb_destinations)]
    couts    = [[random.randint(5, 50) for _ in range(nb_destinations)] for _ in range(nb_sources)]

    # Équilibrage offre/demande
    total_offre   = sum(offres)
    total_demande = sum(demandes)
    diff = total_offre - total_demande
    if diff > 0:
        demandes[-1] += diff
    elif diff < 0:
        offres[-1] += (-diff)

    logger.info(f"Nord-Ouest généré: {nb_sources} sources, {nb_destinations} destinations, offres={offres}, demandes={demandes}")
    return sources, destinations, offres, demandes, couts


def methode_nord_ouest(offres_init, demandes_init, couts):
    m = len(offres_init)
    n = len(demandes_init)
    offres   = list(offres_init)
    demandes = list(demandes_init)

    allocation = [[0] * n for _ in range(m)]
    i, j = 0, 0

    while i < m and j < n:
        q = min(offres[i], demandes[j])
        allocation[i][j] = q
        offres[i]   -= q
        demandes[j] -= q

        if offres[i] == 0 and demandes[j] == 0:
            i += 1
            j += 1
        elif offres[i] == 0:
            i += 1
        else:
            j += 1

    cout_total = sum(
        allocation[i][j] * couts[i][j]
        for i in range(m)
        for j in range(n)
    )

    logger.info(f"Nord-Ouest coût total = {cout_total}")
    return allocation, cout_total
