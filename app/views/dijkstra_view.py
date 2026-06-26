import tkinter as tk
from tkinter import ttk, messagebox
import logging

from algorithms.dijkstra import executer_dijkstra
from views.theme import (FOND, SIDEBAR, ACCENT, TEXTE, CARTE, BORDURE,
                          SUCCES, ERREUR, AVERT, VIOLET, POLICE,
                          creer_bouton, creer_header, creer_section_config_graphe)

logger = logging.getLogger(__name__)


class DijkstraView(tk.Toplevel):
    def __init__(self, parent, reseau):
        super().__init__(parent)
        self.reseau  = reseau
        self._parent = parent

        self.title("Algorithme de Dijkstra — Chemin Optimal")
        self.geometry("560x650")
        self.configure(bg=FOND)
        self.resizable(True, True)  # Permettre le redimensionnement
        self.grab_set()

        self._creer_interface()
        self._centrer(parent)

    def _centrer(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width()  - 560) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 650) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    # ------------------------------------------------------------------ #
    def _creer_interface(self):
        creer_header(self, "  Algorithme de Dijkstra")

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
            text="Calcule le chemin de distance minimale entre deux points du réseau.",
            font=(POLICE, 10), bg=FOND, fg='#94A3B8', wraplength=490,
        ).pack(pady=(0, 16))

        # Section configuration
        self.entry_points, self.entry_densite, self.label_points, self.label_densite = \
            creer_section_config_graphe(outer, self.reseau, self._appliquer_config)

        # Formulaire de sélection
        form = tk.Frame(outer, bg=CARTE, padx=22, pady=18)
        form.pack(fill=tk.X)

        self._combo_source = self._ligne_combo(form, "Point de départ :", self.reseau.villes[0] if self.reseau.villes else "V1", 0)
        self._combo_dest   = self._ligne_combo(form, "Point d'arrivée :", self.reseau.villes[1] if len(self.reseau.villes) > 1 else self.reseau.villes[0], 1)

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
        self._combo_dest['values'] = self.reseau.villes
        self._combo_source.set(self.reseau.villes[0] if self.reseau.villes else "V1")
        self._combo_dest.set(self.reseau.villes[1] if len(self.reseau.villes) > 1 else self.reseau.villes[0])
        
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
        dest   = self._combo_dest.get()

        if source == dest:
            messagebox.showwarning(
                "Entrée invalide",
                "Le point de départ et le point d'arrivée doivent être différents.",
                parent=self,
            )
            return

        res = executer_dijkstra(self.reseau.graphe, source, dest)
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

        chemin   = res['chemin']
        distance = res['distance']
        cout     = res['cout']

        card = tk.Frame(self._frame_resultat, bg=CARTE, padx=18, pady=14)
        card.pack(fill=tk.X)

        tk.Label(card, text="Résultat — Chemin Optimal",
                 font=(POLICE, 11, 'bold'), bg=CARTE, fg=ACCENT).pack(anchor='w')
        tk.Frame(card, bg=BORDURE, height=1).pack(fill=tk.X, pady=8)

        chemin_str = "  →  ".join(chemin)
        tk.Label(card, text=chemin_str,
                 font=(POLICE, 10, 'bold'), bg=CARTE, fg=AVERT,
                 wraplength=480, justify='left').pack(anchor='w', pady=4)

        for label, val in [
            ("Distance totale :", f"{distance} km"),
            ("Coût estimé :",     f"{cout:,} DH"),
            ("Nombre d'étapes :", str(len(chemin) - 1)),
        ]:
            row = tk.Frame(card, bg=CARTE)
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=label,    font=(POLICE, 10),          bg=CARTE, fg='#94A3B8').pack(side=tk.LEFT)
            tk.Label(row, text=f"  {val}", font=(POLICE, 10, 'bold'), bg=CARTE, fg=TEXTE).pack(side=tk.LEFT)

        creer_bouton(
            self._frame_resultat,
            "  Voir sur le graphe",
            lambda: self._voir_graphe(chemin),
            couleur_bg=VIOLET, taille=10,
        ).pack(pady=(12, 0), anchor='w')

    def _voir_graphe(self, chemin):
        from .graph_view import GraphView
        GraphView(
            self._parent, self.reseau,
            chemin=chemin,
            titre=f"Dijkstra : {chemin[0]} → {chemin[-1]}",
        )

    def _voir_graphe_complet(self):
        """Affiche le graphe complet du réseau électrique"""
        from .graph_view import GraphView
        GraphView(
            self._parent, self.reseau,
            titre="Réseau Électrique Complet — Dijkstra",
        )
