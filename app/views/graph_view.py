import tkinter as tk
import logging
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx
import numpy as np

from .theme import (FOND, SIDEBAR, ACCENT, TEXTE, CARTE, BORDURE,
                          SUCCES, ERREUR, AVERT, VIOLET, POLICE)

logger = logging.getLogger(__name__)


class GraphView(tk.Toplevel):
    """Fenêtre de visualisation du réseau électrique."""

    def __init__(self, parent, reseau, chemin=None, acm=None, coloration=None, flot=None,
                 graphe_oriente=None, titre="Réseau Électrique du Maroc"):
        super().__init__(parent)
        self.reseau = reseau
        self.chemin = chemin or []
        self.acm    = acm
        self.coloration = coloration
        self.flot = flot
        self.graphe_oriente = graphe_oriente  # Graphe orienté optionnel
        self.titre  = titre
        self._fig   = None

        self.title(titre)
        self.geometry("950x660")
        self.configure(bg=FOND)
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self._fermer)

        self._creer_interface()
        self._centrer(parent)

    # ------------------------------------------------------------------ #
    def _centrer(self, parent):
        self.update_idletasks()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_x(), parent.winfo_y()
        x = px + (pw - 950) // 2
        y = py + (ph - 660) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    def _fermer(self):
        if self._fig:
            plt.close(self._fig)
        self.destroy()

    # ------------------------------------------------------------------ #
    def _creer_interface(self):
        # En-tête
        header = tk.Frame(self, bg=SIDEBAR, height=52)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header, text=f"  {self.titre}",
            font=(POLICE, 13, 'bold'), bg=SIDEBAR, fg=ACCENT,
        ).pack(side=tk.LEFT, padx=15, pady=10)
        tk.Button(
            header, text='Fermer',
            command=self._fermer,
            font=(POLICE, 9), bg=ERREUR, fg='white',
            relief='flat', cursor='hand2', padx=12, pady=4,
        ).pack(side=tk.RIGHT, padx=15, pady=12)

        self._dessiner_graphe()

    # ------------------------------------------------------------------ #
    def _dessiner_graphe(self):
        # Utiliser le graphe orienté si fourni, sinon le graphe normal
        G = self.graphe_oriente if self.graphe_oriente is not None else self.reseau.graphe
        pos = self.reseau.positions

        self._fig, ax = plt.subplots(figsize=(11, 7.5), facecolor='#1E293B')
        ax.set_facecolor('#1E293B')

        # --- Couleurs des arêtes ---
        chemin_aretes = set()
        acm_aretes    = set()

        if self.chemin and len(self.chemin) > 1:
            for k in range(len(self.chemin) - 1):
                u, v = self.chemin[k], self.chemin[k + 1]
                chemin_aretes.add((u, v))
                # Pour les graphes orientés, ne pas ajouter l'arête inverse
                if not self.graphe_oriente:
                    chemin_aretes.add((v, u))

        if self.acm:
            for u, v in self.acm.edges():
                acm_aretes.add((u, v))
                acm_aretes.add((v, u))

        edge_colors = []
        edge_widths = []
        for u, v in G.edges():
            if (u, v) in chemin_aretes:
                edge_colors.append(AVERT)
                edge_widths.append(4.5)
            elif (u, v) in acm_aretes:
                edge_colors.append(SUCCES)
                edge_widths.append(3.5)
            else:
                edge_colors.append('#475569')
                edge_widths.append(1.8)

        # --- Couleurs des nœuds ---
        node_colors = []
        
        # Si coloration Welsh-Powell
        if self.coloration:
            # Utiliser des couleurs distinctes pour chaque classe de couleur
            couleurs_palette = ['#C084FC', '#4ADE80', '#F59E0B', '#EF4444', '#3B82F6', 
                               '#EC4899', '#8B5CF6', '#10B981', '#F97316', '#6366F1']
            for node in G.nodes():
                couleur_idx = self.coloration.get(node, 0)
                node_colors.append(couleurs_palette[couleur_idx % len(couleurs_palette)])
        # Si chemin
        elif self.chemin:
            for node in G.nodes():
                if node == self.chemin[0] or node == self.chemin[-1]:
                    node_colors.append(ERREUR)
                elif node in self.chemin:
                    node_colors.append(AVERT)
                else:
                    node_colors.append(ACCENT)
        # Sinon couleur par défaut
        else:
            for node in G.nodes():
                node_colors.append(ACCENT)

        # --- Dessin ---
        # Dessiner les arêtes d'abord (sans flèches pour les graphes orientés)
        if self.graphe_oriente:
            # Dessiner les arêtes sans flèches
            nx.draw_networkx_edges(
                G, pos, ax=ax,
                edge_color=edge_colors, width=edge_widths, alpha=0.85,
                arrows=False  # Pas de flèches automatiques
            )
            
            # Ajouter manuellement les flèches au milieu des arêtes
            for i, (u, v) in enumerate(G.edges()):
                x1, y1 = pos[u]
                x2, y2 = pos[v]
                
                # Calculer le point milieu
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                
                # Calculer l'angle de la flèche
                dx, dy = x2 - x1, y2 - y1
                length = np.sqrt(dx*dx + dy*dy)
                if length > 0:
                    # Normaliser la direction
                    dx, dy = dx/length, dy/length
                    
                    # Créer la flèche au milieu (plus grande)
                    arrow = mpatches.FancyArrowPatch(
                        (mx - dx*0.03, my - dy*0.03),  # Point de départ de la flèche
                        (mx + dx*0.03, my + dy*0.03),  # Point d'arrivée de la flèche
                        arrowstyle='->',
                        mutation_scale=18,  # Augmenté de 12 à 18
                        color=edge_colors[i],
                        alpha=0.95,
                        linewidth=2  # Épaisseur de la flèche
                    )
                    ax.add_patch(arrow)
        else:
            nx.draw_networkx_edges(
                G, pos, ax=ax,
                edge_color=edge_colors, width=edge_widths, alpha=0.85,
            )
        nx.draw_networkx_nodes(
            G, pos, ax=ax,
            node_color=node_colors, node_size=900, alpha=0.95,
        )
        nx.draw_networkx_labels(
            G, pos, ax=ax,
            font_size=8, font_color='white', font_weight='bold',
        )

        # Étiquettes distances ou flot
        if self.flot:
            # Afficher le flot au lieu des distances
            flot_labels = {(u, v): f"Flot: {self.flot.get((u, v), 0)}" 
                          for u, v in G.edges()}
            nx.draw_networkx_edge_labels(
                G, pos, edge_labels=flot_labels, ax=ax,
                font_size=7, font_color='#4ADE80', label_pos=0.5,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#0F172A',
                          edgecolor='none', alpha=0.75),
            )
        elif self.graphe_oriente:
            # Pour les graphes orientés, afficher capacités et poids
            if hasattr(list(G.edges(data=True))[0][2], 'get') and 'capacite' in list(G.edges(data=True))[0][2]:
                # Afficher les capacités pour Ford-Fulkerson
                cap_labels = {(u, v): f"C: {d.get('capacite', 0)}" for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(
                    G, pos, edge_labels=cap_labels, ax=ax,
                    font_size=7, font_color='#60A5FA', label_pos=0.3,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#0F172A',
                              edgecolor='none', alpha=0.75),
                )
            
            if hasattr(list(G.edges(data=True))[0][2], 'get') and 'poids' in list(G.edges(data=True))[0][2]:
                # Afficher les poids pour Bellman-Ford
                poids_labels = {(u, v): f"P: {d.get('poids', 0)}" for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(
                    G, pos, edge_labels=poids_labels, ax=ax,
                    font_size=7, font_color='#F59E0B', label_pos=0.7,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#0F172A',
                              edgecolor='none', alpha=0.75),
                )
        else:
            # Afficher les distances et coûts pour les graphes non-orientés
            dist_labels = {(u, v): f"{d['distance']} km" for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(
                G, pos, edge_labels=dist_labels, ax=ax,
                font_size=7, font_color='#CBD5E1', label_pos=0.33,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#0F172A',
                          edgecolor='none', alpha=0.75),
            )

            # Étiquettes coûts
            cout_labels = {(u, v): f"{d['cout']:,} DH" for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(
                G, pos, edge_labels=cout_labels, ax=ax,
                font_size=7, font_color='#FCD34D', label_pos=0.67,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#0F172A',
                          edgecolor='none', alpha=0.75),
            )

        # Légende
        legend = []
        
        if self.coloration:
            # Créer une légende pour chaque couleur utilisée
            couleurs_utilisees = set(self.coloration.values())
            couleurs_palette = ['#C084FC', '#4ADE80', '#F59E0B', '#EF4444', '#3B82F6', 
                               '#EC4899', '#8B5CF6', '#10B981', '#F97316', '#6366F1']
            
            # Compter les nœuds par couleur
            distribution = {}
            for noeud, couleur in self.coloration.items():
                if couleur not in distribution:
                    distribution[couleur] = 0
                distribution[couleur] += 1
            
            # Ajouter chaque couleur à la légende
            for couleur_idx in sorted(couleurs_utilisees):
                nb_noeuds = distribution.get(couleur_idx, 0)
                couleur_visuelle = couleurs_palette[couleur_idx % len(couleurs_palette)]
                legend.append(mpatches.Patch(
                    facecolor=couleur_visuelle, 
                    label=f'Couleur {couleur_idx + 1} ({nb_noeuds} nœuds)'
                ))
        elif self.flot:
            legend.append(mpatches.Patch(facecolor=SUCCES, label='Réseau de flot'))
        else:
            legend.append(mpatches.Patch(facecolor='#475569', label='Liaison électrique'))
        
        if chemin_aretes:
            legend += [
                mpatches.Patch(facecolor=AVERT,  label='Chemin optimal'),
                mpatches.Patch(facecolor=ERREUR, label='Source / Destination'),
            ]
        if acm_aretes:
            legend.append(mpatches.Patch(facecolor=SUCCES, label='Arbre Couvrant Minimal'))

        if legend:
            ax.legend(handles=legend, loc='upper right',
                      facecolor='#0F172A', edgecolor=BORDURE,
                      labelcolor='white', fontsize=8, framealpha=0.9)

        ax.set_title(self.titre, color='white', fontsize=13, fontweight='bold', pad=14)
        ax.axis('off')
        plt.tight_layout(pad=1.0)

        # Intégration dans Tkinter
        canvas = FigureCanvasTkAgg(self._fig, master=self)
        canvas.draw()

        toolbar_frame = tk.Frame(self, bg='#1E293B')
        toolbar_frame.pack(fill=tk.X, side=tk.BOTTOM)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        logger.info(f"GraphView affiché : chemin={self.chemin}, acm={self.acm is not None}")
