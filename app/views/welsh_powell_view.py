import tkinter as tk
from tkinter import messagebox
import logging

from algorithms.welsh_powell import executer_welsh_powell
from views.theme import (FOND, SIDEBAR, ACCENT, TEXTE, CARTE, BORDURE,
                          SUCCES, ERREUR, AVERT, VIOLET, POLICE,
                          creer_bouton, creer_header)

logger = logging.getLogger(__name__)


class WelshPowellView(tk.Toplevel):
    def __init__(self, parent, reseau):
        super().__init__(parent)
        self.reseau  = reseau
        self._parent = parent

        self.title("Algorithme de Welsh-Powell — Coloration de Graphe")
        self.geometry("560x680")
        self.configure(bg=FOND)
        self.resizable(True, True)  # Permettre le redimensionnement
        self.grab_set()

        self._creer_interface()
        self._centrer(parent)

    def _centrer(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width()  - 560) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 680) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    # ------------------------------------------------------------------ #
    def _creer_interface(self):
        creer_header(self, "  Algorithme de Welsh-Powell")

        # Container avec scrollbar
        container = tk.Frame(self, bg=FOND)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg=FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        outer = tk.Frame(canvas, bg=FOND)
        outer.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=outer, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=18)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        tk.Label(
            outer,
            text="Coloration de graphe : assigne des couleurs aux nœuds de façon à ce que "
                 "deux nœuds adjacents n'aient jamais la même couleur.",
            font=(POLICE, 10), bg=FOND, fg='#94A3B8', wraplength=490,
        ).pack(pady=(0, 16))

        # Configuration du graphe
        config_card = tk.Frame(outer, bg=CARTE, padx=18, pady=14)
        config_card.pack(fill=tk.X, pady=(0, 16))

        tk.Label(
            config_card,
            text="Configuration du Graphe",
            font=(POLICE, 11, 'bold'),
            bg=CARTE, fg=ACCENT,
        ).pack(anchor='w', pady=(0, 10))

        # Frame pour les deux champs côte à côte
        fields_frame = tk.Frame(config_card, bg=CARTE)
        fields_frame.pack(fill=tk.X)

        # Colonne gauche - Nombre de sommets
        left_col = tk.Frame(fields_frame, bg=CARTE)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(
            left_col,
            text="Nombre de sommets (1-100)",
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

        self.entry_sommets = tk.Entry(
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
        self.entry_sommets.insert(0, str(self.reseau.nb_villes))
        self.entry_sommets.pack(anchor='w', pady=(0, 5))

        self.label_sommets = tk.Label(
            left_col,
            text=f"Valeur actuelle: {self.reseau.nb_villes} sommets",
            font=(POLICE, 9),
            bg=CARTE, fg='#94A3B8',
        )
        self.label_sommets.pack(anchor='w')

        # Colonne droite - Densité
        right_col = tk.Frame(fields_frame, bg=CARTE)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

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
            bg=CARTE, fg='#94A3B8',
        )
        self.label_densite.pack(anchor='w')

        # Validation lors de la perte de focus
        def validate_sommets_range(event):
            try:
                val = int(self.entry_sommets.get())
                if not (1 <= val <= 100):
                    self.entry_sommets.delete(0, tk.END)
                    self.entry_sommets.insert(0, str(max(1, min(100, val))))
                val = int(self.entry_sommets.get())
                self.label_sommets.configure(text=f"Valeur actuelle: {val} sommets")
            except ValueError:
                self.entry_sommets.delete(0, tk.END)
                self.entry_sommets.insert(0, str(self.reseau.nb_villes))
                self.label_sommets.configure(text=f"Valeur actuelle: {self.reseau.nb_villes} sommets")

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

        self.entry_sommets.bind('<FocusOut>', validate_sommets_range)
        self.entry_sommets.bind('<Return>', validate_sommets_range)
        self.entry_densite.bind('<FocusOut>', validate_densite_range)
        self.entry_densite.bind('<Return>', validate_densite_range)

        # Callbacks pour mise à jour des labels en temps réel
        def update_sommets_label(event=None):
            try:
                val = self.entry_sommets.get()
                if val:
                    self.label_sommets.configure(text=f"Valeur saisie: {val} sommets")
            except:
                pass
        
        def update_densite_label(event=None):
            try:
                val = self.entry_densite.get()
                if val:
                    self.label_densite.configure(text=f"Valeur saisie: {val}% de connexions")
            except:
                pass
        
        self.entry_sommets.bind('<KeyRelease>', update_sommets_label)
        self.entry_densite.bind('<KeyRelease>', update_densite_label)

        # Espace avant le bouton
        tk.Label(config_card, text="", bg=CARTE, height=1).pack()

        # Bouton appliquer
        from views.theme import creer_bouton
        creer_bouton(
            config_card,
            "  Appliquer Configuration",
            self._appliquer_config,
            couleur_bg=VIOLET,
            taille=10,
        ).pack(anchor='w')

        # Boutons
        btn_frame = tk.Frame(outer, bg=FOND)
        btn_frame.pack(pady=16)

        creer_bouton(btn_frame, "  Calculer Coloration", self._calculer,
                     couleur_bg=ACCENT, couleur_fg='#0F172A', taille=11).pack(side=tk.LEFT, padx=6)
        creer_bouton(btn_frame, "  Voir Graphe Complet", self._voir_graphe_complet,
                     couleur_bg=VIOLET, taille=11).pack(side=tk.LEFT, padx=6)
        creer_bouton(btn_frame, "  Fermer",   self.destroy,
                     couleur_bg='#334155', taille=11).pack(side=tk.LEFT, padx=6)

        # Zone de résultat
        self._frame_resultat = tk.Frame(outer, bg=FOND)
        self._frame_resultat.pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------ #
    def _appliquer_config(self):
        """Applique la nouvelle configuration du réseau"""
        try:
            nb_sommets = int(self.entry_sommets.get())
            densite = int(self.entry_densite.get())
            
            # Validation des limites
            if not (1 <= nb_sommets <= 100):
                raise ValueError(f"Le nombre de sommets doit être entre 1 et 100 (saisi: {nb_sommets})")
            if not (1 <= densite <= 100):
                raise ValueError(f"La densité doit être entre 1% et 100% (saisi: {densite}%)")
                
        except ValueError as e:
            messagebox.showerror(
                "Erreur de saisie",
                f"Valeur invalide:\n{str(e)}\n\nVeuillez corriger et réessayer.",
                parent=self,
            )
            return
        
        # Reconfigurer le réseau
        self.reseau.reconfigurer(nb_sommets, densite)
        
        # Mettre à jour les labels
        self.label_sommets.configure(text=f"Valeur actuelle: {nb_sommets} sommets")
        self.label_densite.configure(text=f"Valeur actuelle: {densite}% de connexions")
        
        # Effacer les résultats précédents
        for w in self._frame_resultat.winfo_children():
            w.destroy()
        
        messagebox.showinfo(
            "Configuration Appliquée",
            f"Le graphe a été reconfiguré avec :\n\n"
            f"• {nb_sommets} sommets\n"
            f"• Densité de {densite}%\n"
            f"• {self.reseau.get_stats()['nb_liaisons']} liaisons générées\n\n"
            f"Vous pouvez maintenant calculer la coloration.",
            parent=self,
        )
        logger.info(f"Welsh-Powell : configuration appliquée - {nb_sommets} sommets, {densite}% densité")

    def _calculer(self):
        res = executer_welsh_powell(self.reseau.graphe)
        self._afficher_resultat(res)

    def _afficher_resultat(self, res):
        for w in self._frame_resultat.winfo_children():
            w.destroy()

        if not res['succes']:
            tk.Label(
                self._frame_resultat,
                text=f"  {res['erreur']}",
                font=(POLICE, 10), bg=FOND, fg=ERREUR,
            ).pack(anchor='w')
            return

        coloration = res['coloration']
        nb_couleurs = res['nb_couleurs']

        card = tk.Frame(self._frame_resultat, bg=CARTE, padx=18, pady=14)
        card.pack(fill=tk.X)

        tk.Label(card, text="Résultat — Coloration du Graphe",
                 font=(POLICE, 11, 'bold'), bg=CARTE, fg=ACCENT).pack(anchor='w')
        tk.Frame(card, bg=BORDURE, height=1).pack(fill=tk.X, pady=8)

        for label, val in [
            ("Nombre chromatique :", f"{nb_couleurs} couleurs"),
            ("Nombre de sommets :",  str(len(coloration))),
            ("Densité du graphe :",  f"{self.reseau.densite}%"),
        ]:
            row = tk.Frame(card, bg=CARTE)
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=label,    font=(POLICE, 10),          bg=CARTE, fg='#94A3B8').pack(side=tk.LEFT)
            tk.Label(row, text=f"  {val}", font=(POLICE, 10, 'bold'), bg=CARTE, fg=TEXTE).pack(side=tk.LEFT)

        # Afficher la distribution des couleurs
        tk.Label(card, text="\nDistribution des couleurs :",
                 font=(POLICE, 10, 'bold'), bg=CARTE, fg=TEXTE).pack(anchor='w', pady=(8, 4))

        # Compter le nombre de nœuds par couleur
        distribution = {}
        for noeud, couleur in coloration.items():
            if couleur not in distribution:
                distribution[couleur] = []
            distribution[couleur].append(noeud)

        # Afficher chaque couleur
        for couleur in sorted(distribution.keys()):
            noeuds = distribution[couleur]
            noeuds_str = ", ".join(sorted(noeuds)[:10])  # Limiter à 10 nœuds
            if len(noeuds) > 10:
                noeuds_str += f", ... ({len(noeuds) - 10} autres)"
            
            row = tk.Frame(card, bg=CARTE)
            row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=f"Couleur {couleur + 1}:",
                     font=(POLICE, 9), bg=CARTE, fg=AVERT, width=12, anchor='w').pack(side=tk.LEFT)
            tk.Label(row, text=f"{len(noeuds)} nœuds — {noeuds_str}",
                     font=(POLICE, 9), bg=CARTE, fg='#94A3B8', anchor='w').pack(side=tk.LEFT)

        creer_bouton(
            self._frame_resultat,
            "  Voir la coloration sur le graphe",
            lambda: self._voir_graphe_colore(coloration),
            couleur_bg=VIOLET, taille=10,
        ).pack(pady=(12, 0), anchor='w')

    def _voir_graphe_complet(self):
        """Affiche le graphe complet du réseau"""
        from .graph_view import GraphView
        GraphView(
            self._parent, self.reseau,
            titre="Réseau Complet — Welsh-Powell",
        )

    def _voir_graphe_colore(self, coloration):
        """Affiche le graphe avec la coloration"""
        from .graph_view import GraphView
        GraphView(
            self._parent, self.reseau,
            coloration=coloration,
            titre="Coloration de Graphe — Welsh-Powell",
        )
