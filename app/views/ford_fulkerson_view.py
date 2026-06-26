import tkinter as tk
from tkinter import ttk, messagebox
import logging

from algorithms.ford_fulkerson import executer_ford_fulkerson
from views.theme import (FOND, SIDEBAR, ACCENT, TEXTE, CARTE, BORDURE,
                          SUCCES, ERREUR, AVERT, VIOLET, POLICE,
                          creer_bouton, creer_header, creer_section_config_graphe)

logger = logging.getLogger(__name__)


class FordFulkersonView(tk.Toplevel):
    def __init__(self, parent, reseau):
        super().__init__(parent)
        self.reseau  = reseau
        self._parent = parent

        self.title("Algorithme de Ford-Fulkerson — Flot Maximal")
        self.geometry("560x700")
        self.configure(bg=FOND)
        self.resizable(True, True)  # Permettre le redimensionnement
        self.grab_set()

        self._creer_interface()
        self._centrer(parent)

    def _centrer(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width()  - 560) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 700) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    # ------------------------------------------------------------------ #
    def _creer_interface(self):
        creer_header(self, "  Algorithme de Ford-Fulkerson")

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
            text="Calcule le flot maximal entre une source et un puits dans un réseau.",
            font=(POLICE, 10), bg=FOND, fg='#94A3B8', wraplength=490,
        ).pack(pady=(0, 16))

        # Section configuration
        self.entry_points, self.entry_densite, self.label_points, self.label_densite = \
            creer_section_config_graphe(outer, self.reseau, self._appliquer_config)

        # Formulaire de sélection
        form = tk.Frame(outer, bg=CARTE, padx=22, pady=18)
        form.pack(fill=tk.X)

        self._combo_source = self._ligne_combo(form, "Point source :", self.reseau.villes[0] if self.reseau.villes else "V1", 0)
        self._combo_puits  = self._ligne_combo(form, "Point puits :", self.reseau.villes[-1] if self.reseau.villes else "V1", 1)

        # Boutons
        btn_frame = tk.Frame(outer, bg=FOND)
        btn_frame.pack(pady=16)

        creer_bouton(btn_frame, "  Calculer", self._calculer,
                     couleur_bg=ACCENT, couleur_fg='#0F172A', taille=11).pack(side=tk.LEFT, padx=6)
        creer_bouton(btn_frame, "  Voir Graphe Complet", self._voir_graphe_complet,
                     couleur_bg=VIOLET, taille=11).pack(side=tk.LEFT, padx=6)
        creer_bouton(btn_frame, "  Fermer",   self.destroy,
                     couleur_bg='#334155', taille=11).pack(side=tk.LEFT, padx=6)

        # Zone de résultat
        self._frame_resultat = tk.Frame(outer, bg=FOND)
        self._frame_resultat.pack(fill=tk.BOTH, expand=True)

    def _ligne_combo(self, parent, label, defaut, row):
        tk.Label(parent, text=label, font=(POLICE, 10, 'bold'),
                 bg=CARTE, fg=TEXTE).grid(row=row, column=0, sticky='w', pady=10, padx=(0, 15))
        combo = ttk.Combobox(parent, values=self.reseau.villes, state='readonly',
                              font=(POLICE, 10), width=22)
        combo.set(defaut if defaut in self.reseau.villes else self.reseau.villes[0])
        combo.grid(row=row, column=1, pady=10)
        return combo

    # ------------------------------------------------------------------ #
    def _appliquer_config(self):
        """Applique la nouvelle configuration du réseau"""
        try:
            nb_points = int(self.entry_points.get())
            densite = int(self.entry_densite.get())
            
            # Validation des limites
            if not (1 <= nb_points <= 100):
                raise ValueError(f"Le nombre de points doit être entre 1 et 100 (saisi: {nb_points})")
            if not (1 <= densite <= 100):
                raise ValueError(f"La densité doit être entre 1% et 100% (saisi: {densite}%)")
                
        except ValueError as e:
            from tkinter import messagebox
            messagebox.showerror(
                "Erreur de saisie",
                f"Valeur invalide:\n{str(e)}\n\nVeuillez corriger et réessayer.",
                parent=self,
            )
            return
        
        # Reconfigurer le réseau
        self.reseau.reconfigurer(nb_points, densite)
        
        # Mettre à jour les combos
        self._combo_source['values'] = self.reseau.villes
        self._combo_puits['values'] = self.reseau.villes
        self._combo_source.set(self.reseau.villes[0] if self.reseau.villes else "V1")
        self._combo_puits.set(self.reseau.villes[-1] if self.reseau.villes else "V1")
        
        # Effacer les résultats
        for w in self._frame_resultat.winfo_children():
            w.destroy()
        
        messagebox.showinfo(
            "Configuration Appliquée",
            f"Le graphe a été reconfiguré avec :\n\n"
            f"• {nb_points} points\n"
            f"• Densité de {densite}%\n"
            f"• {self.reseau.get_stats()['nb_liaisons']} liaisons",
            parent=self,
        )

    def _calculer(self):
        source = self._combo_source.get()
        puits  = self._combo_puits.get()

        if source == puits:
            messagebox.showwarning(
                "Entrée invalide",
                "La source et le puits doivent être différents.",
                parent=self,
            )
            return

        res = executer_ford_fulkerson(self.reseau, source, puits)
        self._afficher_resultat(res, source, puits)

    def _afficher_resultat(self, res, source, puits):
        for w in self._frame_resultat.winfo_children():
            w.destroy()

        if not res['succes']:
            tk.Label(
                self._frame_resultat,
                text=f"  {res['erreur']}",
                font=(POLICE, 10), bg=FOND, fg=ERREUR,
            ).pack(anchor='w')
            return

        flot_max = res['flot_max']
        nb_chemins = res['nb_chemins']

        card = tk.Frame(self._frame_resultat, bg=CARTE, padx=18, pady=14)
        card.pack(fill=tk.X)

        tk.Label(card, text="Résultat — Flot Maximal",
                 font=(POLICE, 11, 'bold'), bg=CARTE, fg=ACCENT).pack(anchor='w')
        tk.Frame(card, bg=BORDURE, height=1).pack(fill=tk.X, pady=8)

        tk.Label(card, text=f"{source}  →  {puits}",
                 font=(POLICE, 10, 'bold'), bg=CARTE, fg=AVERT,
                 wraplength=480, justify='left').pack(anchor='w', pady=4)

        for label, val in [
            ("Flot maximal :", f"{flot_max} unités"),
            ("Chemins augmentants :", f"{nb_chemins} trouvés"),
        ]:
            row = tk.Frame(card, bg=CARTE)
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=label,    font=(POLICE, 10),          bg=CARTE, fg='#94A3B8').pack(side=tk.LEFT)
            tk.Label(row, text=f"  {val}", font=(POLICE, 10, 'bold'), bg=CARTE, fg=TEXTE).pack(side=tk.LEFT)

        # Afficher les chemins augmentants
        if res['chemins']:
            tk.Label(card, text="\nChemins augmentants trouvés :",
                     font=(POLICE, 10, 'bold'), bg=CARTE, fg=TEXTE).pack(anchor='w', pady=(8, 4))

            for i, chemin_info in enumerate(res['chemins'][:5], 1):  # Limiter à 5 chemins
                chemin = chemin_info['chemin']
                flot = chemin_info['flot']
                chemin_str = "  →  ".join(chemin)
                
                row = tk.Frame(card, bg=CARTE)
                row.pack(fill=tk.X, pady=2)
                tk.Label(row, text=f"Chemin {i}:",
                         font=(POLICE, 9), bg=CARTE, fg=AVERT, width=10, anchor='w').pack(side=tk.LEFT)
                tk.Label(row, text=f"{chemin_str} (flot: {flot})",
                         font=(POLICE, 9), bg=CARTE, fg='#94A3B8', anchor='w').pack(side=tk.LEFT)

            if len(res['chemins']) > 5:
                tk.Label(card, text=f"... et {len(res['chemins']) - 5} autres chemins",
                         font=(POLICE, 9), bg=CARTE, fg='#64748B').pack(anchor='w', pady=(2, 0))

        creer_bouton(
            self._frame_resultat,
            "  Voir le réseau de flot",
            lambda: self._voir_graphe_flot(res['flot'], source, puits),
            couleur_bg=VIOLET, taille=10,
        ).pack(pady=(12, 0), anchor='w')

    def _voir_graphe_complet(self):
        """Affiche le graphe complet du réseau orienté"""
        from .graph_view import GraphView
        graphe_oriente = self.reseau.creer_graphe_oriente()
        GraphView(
            self._parent, self.reseau,
            graphe_oriente=graphe_oriente,
            titre="Réseau Orienté — Ford-Fulkerson",
        )

    def _voir_graphe_flot(self, flot, source, puits):
        """Affiche le graphe avec le flot"""
        from .graph_view import GraphView
        graphe_oriente = self.reseau.creer_graphe_oriente()
        GraphView(
            self._parent, self.reseau,
            flot=flot,
            graphe_oriente=graphe_oriente,
            titre=f"Réseau de Flot : {source} → {puits}",
        )
