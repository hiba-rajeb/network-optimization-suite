import random
import networkx as nx

class ReseauElectrique:
    def __init__(self, nb_villes=100, densite=30):
        """
        Initialise un réseau électrique.
        
        Args:
            nb_villes (int): Nombre de villes (1 à 100)
            densite (int): Pourcentage de densité du graphe (1 à 100)
                          - 1% = graphe très peu connecté
                          - 50% = graphe moyennement connecté
                          - 100% = graphe complet
        """
        self.nb_villes = max(1, min(100, nb_villes))
        self.densite = max(1, min(100, densite))
        
        self.villes = [f"V{i}" for i in range(1, self.nb_villes + 1)]
        self.graphe = nx.Graph()
        self.positions = {}
        
        self.initialiser()

    def initialiser(self):
        """Génère le réseau avec les paramètres actuels"""
        self.graphe.clear()
        self.positions.clear()
        
        # Générer les positions
        random.seed(42)
        for ville in self.villes:
            x = random.uniform(0.10, 0.90)
            y = random.uniform(0.10, 0.90)
            self.positions[ville] = (x, y)
        
        # Ajouter les nœuds
        for ville in self.villes:
            self.graphe.add_node(ville)
        
        # Calculer le nombre de liaisons selon la densité
        # Pour un graphe complet : n*(n-1)/2 arêtes
        nb_max_liaisons = (self.nb_villes * (self.nb_villes - 1)) // 2
        nb_liaisons_cible = max(self.nb_villes - 1, int(nb_max_liaisons * self.densite / 100))
        
        liaisons = set()
        
        # Étape 1 : Créer un graphe connexe (arbre couvrant)
        # Relier chaque ville à la précédente
        for i in range(1, self.nb_villes):
            v1 = f"V{i}"
            v2 = f"V{i+1}"
            liaisons.add((min(v1, v2), max(v1, v2)))
        
        # Étape 2 : Ajouter des liaisons aléatoires jusqu'à atteindre la densité
        random.seed(42)
        tentatives = 0
        max_tentatives = nb_liaisons_cible * 10
        
        while len(liaisons) < nb_liaisons_cible and tentatives < max_tentatives:
            v1_idx = random.randint(1, self.nb_villes)
            v2_idx = random.randint(1, self.nb_villes)
            
            if v1_idx != v2_idx:
                v1 = f"V{v1_idx}"
                v2 = f"V{v2_idx}"
                liaison = (min(v1, v2), max(v1, v2))
                liaisons.add(liaison)
            
            tentatives += 1
        
        # Ajouter les arêtes au graphe avec distances et coûts aléatoires
        for v1, v2 in liaisons:
            distance = random.randint(50, 500)
            cout = random.randint(1000, 10000)
            self.graphe.add_edge(v1, v2, distance=distance, cout=cout)

    def reinitialiser(self):
        """Régénère le réseau avec de nouvelles distances/coûts aléatoires"""
        self.initialiser()
    
    def reconfigurer(self, nb_villes, densite):
        """
        Reconfigure le réseau avec de nouveaux paramètres.
        
        Args:
            nb_villes (int): Nouveau nombre de villes
            densite (int): Nouvelle densité (en pourcentage)
        """
        self.nb_villes = max(1, min(100, nb_villes))
        self.densite = max(1, min(100, densite))
        self.villes = [f"V{i}" for i in range(1, self.nb_villes + 1)]
        self.initialiser()

    def creer_graphe_oriente(self):
        """Crée un graphe orienté pour les algorithmes Ford-Fulkerson et Bellman-Ford"""
        graphe_oriente = nx.DiGraph()
        
        # Ajouter les nœuds
        for ville in self.villes:
            graphe_oriente.add_node(ville)
        
        # Calculer le nombre de liaisons selon la densité (pour graphe orienté)
        # Pour un graphe complet orienté : n*(n-1) arêtes
        nb_max_liaisons = self.nb_villes * (self.nb_villes - 1)
        nb_liaisons_cible = max(self.nb_villes - 1, int(nb_max_liaisons * self.densite / 100))
        
        liaisons = set()
        
        # Étape 1 : Créer un chemin orienté pour assurer la connexité
        for i in range(1, self.nb_villes):
            v1 = f"V{i}"
            v2 = f"V{i+1}"
            liaisons.add((v1, v2))
        
        # Étape 2 : Ajouter des liaisons orientées aléatoires
        random.seed(42)
        tentatives = 0
        max_tentatives = nb_liaisons_cible * 10
        
        while len(liaisons) < nb_liaisons_cible and tentatives < max_tentatives:
            v1_idx = random.randint(1, self.nb_villes)
            v2_idx = random.randint(1, self.nb_villes)
            
            if v1_idx != v2_idx:
                v1 = f"V{v1_idx}"
                v2 = f"V{v2_idx}"
                # Ajouter l'arête orientée (v1 -> v2)
                liaisons.add((v1, v2))
            
            tentatives += 1
        
        # Ajouter les arêtes orientées au graphe
        for v1, v2 in liaisons:
            distance = random.randint(50, 500)
            cout = random.randint(1000, 10000)
            capacite = random.randint(10, 100)  # Capacité pour Ford-Fulkerson
            poids = random.randint(-50, 200)    # Poids (parfois négatifs) pour Bellman-Ford
            
            graphe_oriente.add_edge(v1, v2, 
                                  distance=distance, 
                                  cout=cout,
                                  capacite=capacite,
                                  poids=poids)
        
        return graphe_oriente

    def get_stats(self):
        """Retourne les statistiques du réseau"""
        dist_totale = sum(d['distance'] for _, _, d in self.graphe.edges(data=True))
        cout_total  = sum(d['cout']     for _, _, d in self.graphe.edges(data=True))
        return {
            'nb_villes':  self.graphe.number_of_nodes(),
            'nb_liaisons': self.graphe.number_of_edges(),
            'dist_totale': dist_totale,
            'cout_total':  cout_total,
        }

# Pour la compatibilité avec l'ancien code
VILLES = [f"V{i}" for i in range(1, 101)]  # Liste par défaut de V1 à V100
