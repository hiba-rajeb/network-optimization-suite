import tkinter as tk
from tkinter import messagebox
import logging

from views.theme import (FOND, SIDEBAR, ACCENT, TEXTE, CARTE, BORDURE,
                          SUCCES, ERREUR, AVERT, VIOLET, MUTED, POLICE,
                          appliquer_style_ttk, creer_separateur_label, creer_bouton)

logger = logging.getLogger(__name__)


class MainWindow(tk.Frame):
    """Fenêtre principale de l'application."""

    def __init__(self, parent, reseau):
        super().__init__(parent, bg=FOND)
        self.reseau = reseau
        appliquer_style_ttk(parent)
        self._creer_interface()

    # ================================================================== #
    #  CONSTRUCTION DE L'INTERFACE                                        #
    # ================================================================== #

    def _creer_interface(self):
        self._creer_header()
        corps = tk.Frame(self, bg=FOND)
        corps.pack(fill=tk.BOTH, expand=True)
        self._creer_sidebar(corps)
        self._creer_contenu(corps)

    # ------------------------------------------------------------------ #
    def _creer_header(self):
        header = tk.Frame(self, bg=SIDEBAR, height=68)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Titres empilés à gauche
        titles = tk.Frame(header, bg=SIDEBAR)
        titles.pack(side=tk.LEFT, padx=20, pady=8)

        tk.Label(
            titles,
            text="Optimisation du Réseau Électrique au Maroc",
            font=(POLICE, 15, 'bold'),
            bg=SIDEBAR, fg=ACCENT,
            anchor='w',
        ).pack(anchor='w')

        tk.Label(
            titles,
            text="Recherche Opérationnelle & Algorithmes de Graphes",
            font=(POLICE, 9),
            bg=SIDEBAR, fg='#64748B',
            anchor='w',
        ).pack(anchor='w', pady=(1, 0))

        # EMI à droite
        tk.Label(
            header,
            text="EMI — 2026",
            font=(POLICE, 9),
            bg=SIDEBAR, fg='#334155',
        ).pack(side=tk.RIGHT, padx=20)

    # ------------------------------------------------------------------ #
    def _creer_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=SIDEBAR, width=230)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Canvas scrollable pour la sidebar
        cvs = tk.Canvas(sidebar, bg=SIDEBAR, highlightthickness=0, width=210)
        vbar = tk.Scrollbar(sidebar, orient='vertical', command=cvs.yview, 
                           bg=SIDEBAR, troughcolor=SIDEBAR, 
                           activebackground=ACCENT, width=18)
        frame = tk.Frame(cvs, bg=SIDEBAR)

        frame.bind('<Configure>',
                   lambda e: cvs.configure(scrollregion=cvs.bbox('all')))
        cvs.create_window((0, 0), window=frame, anchor='nw')
        cvs.configure(yscrollcommand=vbar.set)
        
        cvs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel pour le scroll
        def _on_mousewheel(event):
            cvs.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        
        cvs.bind_all('<MouseWheel>', _on_mousewheel)

        self._remplir_sidebar(frame)

    def _btn_sidebar(self, parent, icone, texte, commande, couleur_accent=None):
        if couleur_accent is None:
            couleur_accent = ACCENT
        f = tk.Frame(parent, bg=SIDEBAR)
        f.pack(fill=tk.X, padx=10, pady=2)

        btn = tk.Button(
            f,
            text=f"{icone}  {texte}",
            command=commande,
            font=(POLICE, 10),
            bg=CARTE,
            fg=TEXTE,
            activebackground=couleur_accent,
            activeforeground='#0F172A' if couleur_accent != ERREUR else 'white',
            relief='flat',
            cursor='hand2',
            anchor='w',
            padx=12, pady=7,
            bd=0,
        )
        btn.pack(fill=tk.X)

        orig_bg = CARTE
        btn.bind('<Enter>', lambda e: btn.configure(
            bg=couleur_accent,
            fg='#1A1625' if couleur_accent != ERREUR else 'white'))
        btn.bind('<Leave>', lambda e: btn.configure(bg=orig_bg, fg=TEXTE))
        return btn

    def _remplir_sidebar(self, frame):
        tk.Label(frame, text='', bg=SIDEBAR).pack(pady=6)

        # RÉGÉNÉRER
        self._btn_sidebar(
            frame, '⟳', 'RÉGÉNÉRER', self._demarrer, SUCCES
        )

        # Algorithmes de graphes
        creer_separateur_label(frame, 'Algorithmes de Graphes')

        self._btn_sidebar(frame, '📍', 'Dijkstra',     self._ouvrir_dijkstra)
        self._btn_sidebar(frame, '📍', 'Bellman-Ford', self._ouvrir_bellman_ford)
        self._btn_sidebar(frame, '🌲', 'Prim (ACM)',   self._ouvrir_prim)
        self._btn_sidebar(frame, '🌲', 'Kruskal (ACM)',self._ouvrir_kruskal)
        self._btn_sidebar(frame, '🎨', 'Welsh-Powell', self._ouvrir_welsh_powell, AVERT)
        self._btn_sidebar(frame, '💧', 'Ford-Fulkerson', self._ouvrir_ford_fulkerson, SUCCES)

        creer_separateur_label(frame, '')
        self._btn_sidebar(frame, '🗺', 'Afficher Graphe', self._afficher_graphe, VIOLET)

        # Recherche opérationnelle
        creer_separateur_label(frame, 'Recherche Opérationnelle')

        self._btn_sidebar(frame, '🚚', 'Méthode Nord-Ouest', self._ouvrir_nord_ouest, AVERT)
        self._btn_sidebar(frame, '📊', 'Simplexe',           self._ouvrir_simplexe,   AVERT)

        creer_separateur_label(frame, '')

        tk.Label(frame, text='', bg=SIDEBAR).pack(pady=4)
        self._btn_sidebar(frame, '✖', 'Quitter', self._quitter, ERREUR)
        tk.Label(frame, text='', bg=SIDEBAR).pack(pady=8)

    # ------------------------------------------------------------------ #
    def _creer_contenu(self, parent):
        # Container principal pour le contenu avec scrollbar
        container = tk.Frame(parent, bg=FOND)
        container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Canvas pour le scroll
        canvas = tk.Canvas(container, bg=FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        self._contenu = tk.Frame(canvas, bg=FOND)
        self._contenu.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self._contenu, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=24, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel pour le scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # --- Titre section ---
        tk.Label(
            self._contenu,
            text="Tableau de Bord",
            font=(POLICE, 18, 'bold'),
            bg=FOND, fg=TEXTE,
        ).pack(anchor='w')

        tk.Label(
            self._contenu,
            text="Optimisation du Réseau Électrique au Maroc",
            font=(POLICE, 10),
            bg=FOND, fg=MUTED,
        ).pack(anchor='w', pady=(2, 18))

        # ===== SECTION CONFIGURATION =====
        self._creer_section_config()
        
        # Séparateur
        tk.Frame(self._contenu, bg=BORDURE, height=1).pack(fill=tk.X, pady=(15, 18))

        # Cartes de statistiques
        tk.Label(
            self._contenu,
            text="Statistiques du Réseau",
            font=(POLICE, 12, 'bold'),
            bg=FOND, fg=TEXTE,
        ).pack(anchor='w', pady=(0, 10))
        
        self._stats_frame = tk.Frame(self._contenu, bg=FOND)
        self._stats_frame.pack(fill=tk.X, pady=(0, 18))
        self._creer_cartes_stats()

        # Séparateur
        tk.Frame(self._contenu, bg=BORDURE, height=1).pack(fill=tk.X, pady=(0, 16))

        # Description / Guide
        self._creer_guide()

    def _creer_section_config(self):
        """Crée la section de configuration du réseau"""
        config_card = tk.Frame(self._contenu, bg=CARTE, padx=20, pady=16)
        config_card.pack(fill=tk.X, pady=(0, 0))

        # Titre
        header_frame = tk.Frame(config_card, bg=CARTE)
        header_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(
            header_frame,
            text="⚙  Configuration du Réseau",
            font=(POLICE, 12, 'bold'),
            bg=CARTE, fg=ACCENT,
        ).pack(side=tk.LEFT)

        # Frame principal avec deux colonnes
        main_frame = tk.Frame(config_card, bg=CARTE)
        main_frame.pack(fill=tk.X)

        # Colonne gauche - Nombre de points
        left_col = tk.Frame(main_frame, bg=CARTE)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        tk.Label(
            left_col,
            text="Nombre de points (1-100)",
            font=(POLICE, 10, 'bold'),
            bg=CARTE, fg=TEXTE,
        ).pack(anchor='w', pady=(0, 5))

        # Validation pour les nombres entiers
        def validate_number(action, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
            if action != '1':  # '1' = insertion
                return True
            try:
                if value_if_allowed == "":
                    return True
                val = int(value_if_allowed)
                return True  # On valide à la saisie, les limites seront vérifiées au focus out
            except ValueError:
                return False

        vcmd = (config_card.register(validate_number), '%d', '%P', '%s', '%S', '%v', '%i', '%W')

        self.entry_villes = tk.Entry(
            left_col,
            font=(POLICE, 11),
            bg=SIDEBAR, fg=TEXTE,
            insertbackground=ACCENT,
            relief='solid', bd=1,
            highlightcolor=ACCENT,
            highlightthickness=2,
            validate='key',
            validatecommand=vcmd,
            width=8,
        )
        self.entry_villes.insert(0, str(self.reseau.nb_villes))
        self.entry_villes.pack(anchor='w', pady=(0, 5))

        self.label_villes = tk.Label(
            left_col,
            text=f"Valeur actuelle: {self.reseau.nb_villes} points (V1 à V{self.reseau.nb_villes})",
            font=(POLICE, 9),
            bg=CARTE, fg=MUTED,
        )
        self.label_villes.pack(anchor='w')

        # Colonne droite - Densité
        right_col = tk.Frame(main_frame, bg=CARTE)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0))

        tk.Label(
            right_col,
            text="Densité du graphe (1-100%)",
            font=(POLICE, 10, 'bold'),
            bg=CARTE, fg=TEXTE,
        ).pack(anchor='w', pady=(0, 5))

        self.entry_densite = tk.Entry(
            right_col,
            font=(POLICE, 11),
            bg=SIDEBAR, fg=TEXTE,
            insertbackground=SUCCES,
            relief='solid', bd=1,
            highlightcolor=SUCCES,
            highlightthickness=2,
            validate='key',
            validatecommand=vcmd,
            width=8,
        )
        self.entry_densite.insert(0, str(self.reseau.densite))
        self.entry_densite.pack(anchor='w', pady=(0, 5))

        self.label_densite = tk.Label(
            right_col,
            text=f"Valeur actuelle: {self.reseau.densite}% de connexions",
            font=(POLICE, 9),
            bg=CARTE, fg=MUTED,
        )
        self.label_densite.pack(anchor='w')

        # Validation lors de la perte de focus
        def validate_points_range(event):
            try:
                val = int(self.entry_villes.get())
                if not (1 <= val <= 100):
                    self.entry_villes.delete(0, tk.END)
                    self.entry_villes.insert(0, str(max(1, min(100, val))))
                val = int(self.entry_villes.get())
                self.label_villes.configure(text=f"Valeur actuelle: {val} points (V1 à V{val})")
            except ValueError:
                self.entry_villes.delete(0, tk.END)
                self.entry_villes.insert(0, str(self.reseau.nb_villes))
                self.label_villes.configure(text=f"Valeur actuelle: {self.reseau.nb_villes} points (V1 à V{self.reseau.nb_villes})")

        def validate_densite_range(event):
            try:
                val = int(self.entry_densite.get())
                if not (1 <= val <= 100):
                    self.entry_densite.delete(0, tk.END)
                    self.entry_densite.insert(0, str(max(1, min(100, val))))
                val = int(self.entry_densite.get())
                self.label_densite.configure(text=f"Valeur actuelle: {val}% de connexions")
            except ValueError:
                self.entry_densite.delete(0, tk.END)
                self.entry_densite.insert(0, str(self.reseau.densite))
                self.label_densite.configure(text=f"Valeur actuelle: {self.reseau.densite}% de connexions")

        self.entry_villes.bind('<FocusOut>', validate_points_range)
        self.entry_villes.bind('<Return>', validate_points_range)
        self.entry_densite.bind('<FocusOut>', validate_densite_range)
        self.entry_densite.bind('<Return>', validate_densite_range)

        # Callbacks pour mise à jour des labels en temps réel
        def update_points_label(event=None):
            try:
                val = self.entry_villes.get()
                if val:
                    self.label_villes.configure(text=f"Valeur saisie: {val} points")
            except:
                pass
        
        def update_densite_label(event=None):
            try:
                val = self.entry_densite.get()
                if val:
                    self.label_densite.configure(text=f"Valeur saisie: {val}% de connexions")
            except:
                pass
        
        self.entry_villes.bind('<KeyRelease>', update_points_label)
        self.entry_densite.bind('<KeyRelease>', update_densite_label)

        # Bouton Appliquer
        btn_frame = tk.Frame(config_card, bg=CARTE)
        btn_frame.pack(fill=tk.X, pady=(12, 0))

        creer_bouton(
            btn_frame, "  Appliquer Configuration", self._appliquer_config,
            couleur_bg=ACCENT, couleur_fg='#0F172A', taille=10
        ).pack(side=tk.LEFT)

    def _creer_cartes_stats(self):
        stats = self.reseau.get_stats()
        donnees = [
            ("Points",            str(stats['nb_villes']),         "nœuds du réseau",  ACCENT),
            ("Liaisons",          str(stats['nb_liaisons']),       "lignes HT",         SUCCES),
            ("Distance Totale",   f"{stats['dist_totale']:,}",     "km",                AVERT),
            ("Coût du Réseau",    f"{stats['cout_total']:,}",      "DH",                '#EF4444'),
        ]
        self._labels_stats = []

        for col, (titre, valeur, unite, couleur) in enumerate(donnees):
            carte = tk.Frame(self._stats_frame, bg=CARTE, padx=14, pady=14)
            carte.grid(row=0, column=col, padx=8, pady=4, sticky='nsew')
            self._stats_frame.columnconfigure(col, weight=1)

            tk.Label(carte, text=titre,  font=(POLICE, 9),          bg=CARTE, fg=MUTED).pack()
            lbl = tk.Label(carte, text=valeur, font=(POLICE, 20, 'bold'), bg=CARTE, fg=couleur)
            lbl.pack()
            tk.Label(carte, text=unite,  font=(POLICE, 8),          bg=CARTE, fg='#64748B').pack()
            self._labels_stats.append((lbl, couleur))

    def _actualiser_stats(self):
        stats = self.reseau.get_stats()
        valeurs = [
            str(stats['nb_villes']),
            str(stats['nb_liaisons']),
            f"{stats['dist_totale']:,}",
            f"{stats['cout_total']:,}",
        ]
        for (lbl, _), val in zip(self._labels_stats, valeurs):
            lbl.configure(text=val)

    def _creer_guide(self):
        guide = tk.Frame(self._contenu, bg=CARTE, padx=20, pady=16)
        guide.pack(fill=tk.BOTH, expand=True)

        tk.Label(guide, text="Guide d'utilisation",
                 font=(POLICE, 12, 'bold'), bg=CARTE, fg=TEXTE).pack(anchor='w', pady=(0, 10))

        lignes = [
            ("⟳  RÉGÉNÉRER",        "Régénère le réseau avec de nouvelles distances et coûts aléatoires."),
            ("📍 Dijkstra",         "Chemin de distance minimale entre deux points (algorithme glouton)."),
            ("📍 Bellman-Ford",     "Chemin minimal — tolère les arêtes à poids négatifs."),
            ("🌲 Prim / Kruskal",   "Arbre Couvrant Minimal (ACM) : infrastructure électrique optimale."),
            ("🎨 Welsh-Powell",     "Coloration de graphe : assigne des couleurs aux nœuds adjacents."),
            ("💧 Ford-Fulkerson",   "Flot maximal : calcule le flux maximum entre source et puits."),
            ("🗺  Afficher Graphe", "Visualisation du réseau complet avec distances et coûts."),
            ("🚚 Méthode Nord-Ouest","Transport d'énergie : allocation initiale depuis le coin NW."),
            ("📊 Simplexe",         "Maximisation de la distribution électrique par programmation linéaire."),
        ]

        for cmd, desc in lignes:
            row = tk.Frame(guide, bg=CARTE)
            row.pack(fill=tk.X, pady=3)

            tk.Label(row, text=cmd, width=22, anchor='w',
                     font=(POLICE, 10, 'bold'), bg=CARTE, fg=ACCENT).pack(side=tk.LEFT)
            tk.Label(row, text=desc, anchor='w',
                     font=(POLICE, 10), bg=CARTE, fg='#CBD5E1').pack(side=tk.LEFT, padx=(8, 0))

    # ================================================================== #
    #  ACTIONS DES BOUTONS                                               #
    # ================================================================== #

    def _appliquer_config(self):
        """Applique la nouvelle configuration du réseau"""
        try:
            nb_villes = int(self.entry_villes.get())
            densite = int(self.entry_densite.get())
            
            # Validation des limites
            if not (1 <= nb_villes <= 100):
                raise ValueError(f"Le nombre de points doit être entre 1 et 100 (saisi: {nb_villes})")
            if not (1 <= densite <= 100):
                raise ValueError(f"La densité doit être entre 1% et 100% (saisi: {densite}%)")
            
        except ValueError as e:
            messagebox.showerror(
                "Erreur de saisie",
                f"Valeur invalide:\n{str(e)}\n\nVeuillez corriger et réessayer.",
                parent=self.winfo_toplevel(),
            )
            return
        
        # Reconfigurer le réseau
        self.reseau.reconfigurer(nb_villes, densite)
        self._actualiser_stats()
        
        # Mettre à jour les labels
        self.label_villes.configure(text=f"Valeur actuelle: {nb_villes} points (V1 à V{nb_villes})")
        self.label_densite.configure(text=f"Valeur actuelle: {densite}% de connexions")
        
        messagebox.showinfo(
            "Configuration Appliquée",
            f"Le réseau a été reconfiguré avec :\n\n"
            f"• {nb_villes} points (V1 à V{nb_villes})\n"
            f"• Densité de {densite}%\n"
            f"• {self.reseau.get_stats()['nb_liaisons']} liaisons générées",
            parent=self.winfo_toplevel(),
        )
        logger.info(f"Configuration appliquée : {nb_villes} points, {densite}% densité")

    def _configurer(self):
        """Ouvre la fenêtre de configuration du réseau"""
        try:
            from views.config_view import ConfigView
            ConfigView(self.winfo_toplevel(), self.reseau, self._actualiser_stats)
        except Exception as e:
            logger.exception("Erreur ouverture configuration")
            messagebox.showerror("Erreur", str(e), parent=self.winfo_toplevel())

    def _demarrer(self):
        self.reseau.reinitialiser()
        self._actualiser_stats()
        messagebox.showinfo(
            "Réseau Régénéré",
            "Le réseau électrique a été régénéré.\n\n"
            "Toutes les distances et les coûts ont été recalculés aléatoirement.",
            parent=self.winfo_toplevel(),
        )
        logger.info("Réseau réinitialisé par l'utilisateur")

    def _ouvrir_dijkstra(self):
        try:
            from views.dijkstra_view import DijkstraView
            DijkstraView(self.winfo_toplevel(), self.reseau)
        except Exception as e:
            logger.exception("Erreur ouverture Dijkstra")
            messagebox.showerror("Erreur", str(e), parent=self.winfo_toplevel())

    def _ouvrir_bellman_ford(self):
        try:
            from views.bellman_ford_view import BellmanFordView
            BellmanFordView(self.winfo_toplevel(), self.reseau)
        except Exception as e:
            logger.exception("Erreur ouverture Bellman-Ford")
            messagebox.showerror("Erreur", str(e), parent=self.winfo_toplevel())

    def _ouvrir_prim(self):
        try:
            from views.prim_view import PrimView
            PrimView(self.winfo_toplevel(), self.reseau)
        except Exception as e:
            logger.exception("Erreur ouverture Prim")
            messagebox.showerror("Erreur", str(e), parent=self.winfo_toplevel())

    def _ouvrir_kruskal(self):
        try:
            from views.kruskal_view import KruskalView
            KruskalView(self.winfo_toplevel(), self.reseau)
        except Exception as e:
            logger.exception("Erreur ouverture Kruskal")
            messagebox.showerror("Erreur", str(e), parent=self.winfo_toplevel())

    def _ouvrir_welsh_powell(self):
        try:
            from views.welsh_powell_view import WelshPowellView
            WelshPowellView(self.winfo_toplevel(), self.reseau)
        except Exception as e:
            logger.exception("Erreur ouverture Welsh-Powell")
            messagebox.showerror("Erreur", str(e), parent=self.winfo_toplevel())

    def _ouvrir_ford_fulkerson(self):
        try:
            from views.ford_fulkerson_view import FordFulkersonView
            FordFulkersonView(self.winfo_toplevel(), self.reseau)
        except Exception as e:
            logger.exception("Erreur ouverture Ford-Fulkerson")
            messagebox.showerror("Erreur", str(e), parent=self.winfo_toplevel())

    def _afficher_graphe(self):
        try:
            from .graph_view import GraphView
            GraphView(self.winfo_toplevel(), self.reseau,
                      titre="Réseau Électrique du Maroc")
        except Exception as e:
            logger.exception("Erreur affichage graphe")
            messagebox.showerror("Erreur", str(e), parent=self.winfo_toplevel())

    def _ouvrir_nord_ouest(self):
        try:
            from views.nord_ouest_view import NordOuestView
            NordOuestView(self.winfo_toplevel(), self.reseau)
        except Exception as e:
            logger.exception("Erreur ouverture Nord-Ouest")
            messagebox.showerror("Erreur", str(e), parent=self.winfo_toplevel())

    def _ouvrir_simplexe(self):
        try:
            from views.simplexe_view import SimplexeView
            SimplexeView(self.winfo_toplevel(), self.reseau)
        except Exception as e:
            logger.exception("Erreur ouverture Simplexe")
            messagebox.showerror("Erreur", str(e), parent=self.winfo_toplevel())

    def _quitter(self):
        if messagebox.askyesno(
            "Quitter l'application",
            "Êtes-vous sûr de vouloir quitter ?",
            parent=self.winfo_toplevel(),
        ):
            logger.info("Application fermée par l'utilisateur")
            self.winfo_toplevel().destroy()
