import tkinter as tk
import logging

from algorithms.kruskal import executer_kruskal
from views.theme import (FOND, SIDEBAR, ACCENT, TEXTE, CARTE, BORDURE,
                          SUCCES, ERREUR, AVERT, VIOLET, POLICE,
                          POLICE_MONO, creer_bouton, creer_header, creer_section_config_graphe)

logger = logging.getLogger(__name__)


class KruskalView(tk.Toplevel):
    def __init__(self, parent, reseau):
        super().__init__(parent)
        self.reseau  = reseau
        self._parent = parent

        self.title("Algorithme de Kruskal — Arbre Couvrant Minimal")
        self.geometry("620x700")
        self.configure(bg=FOND)
        self.resizable(True, True)  # Permettre le redimensionnement

        self._creer_interface()
        self._centrer(parent)

    def _centrer(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width()  - 620) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 700) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    # ------------------------------------------------------------------ #
    def _creer_interface(self):
        creer_header(self, "  Algorithme de Kruskal — Arbre Couvrant Minimal")

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

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=16)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        tk.Label(
            outer,
            text=("Construit l'Arbre Couvrant Minimal (ACM) en triant toutes les arêtes "
                  "par coût croissant et en ajoutant celles qui ne forment pas de cycle."),
            font=(POLICE, 10), bg=FOND, fg='#94A3B8', wraplength=560, justify='left',
        ).pack(pady=(0, 14), anchor='w')

        # Section configuration
        self.entry_points, self.entry_densite, self.label_points, self.label_densite = \
            creer_section_config_graphe(outer, self.reseau, self._appliquer_config)

        self._frame_resultat = tk.Frame(outer, bg=FOND)
        self._frame_resultat.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(outer, bg=FOND)
        btn_frame.pack(pady=12)

        creer_bouton(btn_frame, "  Recalculer", self._calculer,
                     couleur_bg=SUCCES, couleur_fg='#0F172A', taille=10).pack(side=tk.LEFT, padx=6)
        creer_bouton(btn_frame, "  Voir Graphe ACM", self._voir_graphe_acm,
                     couleur_bg=VIOLET, taille=10).pack(side=tk.LEFT, padx=6)
        creer_bouton(btn_frame, "  Fermer",     self.destroy,
                     couleur_bg='#334155', taille=10).pack(side=tk.LEFT, padx=6)
        
        # Calculer automatiquement au démarrage
        self.after(100, self._calculer)

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
        
        # Recalculer automatiquement avec la nouvelle configuration
        self._calculer()

    def _calculer(self):
        for w in self._frame_resultat.winfo_children():
            w.destroy()

        res = executer_kruskal(self.reseau.graphe)

        if not res['succes']:
            tk.Label(self._frame_resultat, text=f"  Erreur : {res['erreur']}",
                     font=(POLICE, 10), bg=FOND, fg=ERREUR).pack(anchor='w')
            return

        self._afficher(res)

    def _afficher(self, res):
        liaisons    = res['liaisons']
        cout_total  = res['cout_total']
        dist_totale = res['dist_totale']

        # Résumé
        card_top = tk.Frame(self._frame_resultat, bg=CARTE, padx=18, pady=14)
        card_top.pack(fill=tk.X, pady=(0, 10))

        tk.Label(card_top, text="Résultat Kruskal — ACM",
                 font=(POLICE, 11, 'bold'), bg=CARTE, fg=ACCENT).pack(anchor='w')
        tk.Frame(card_top, bg=BORDURE, height=1).pack(fill=tk.X, pady=8)

        resume = tk.Frame(card_top, bg=CARTE)
        resume.pack(fill=tk.X)
        for col, (lbl, val) in enumerate([
            ("Arêtes retenues",    str(len(liaisons))),
            ("Coût total minimal", f"{cout_total:,} DH"),
            ("Distance totale",    f"{dist_totale:,} km"),
        ]):
            c = tk.Frame(resume, bg='#0F172A', padx=10, pady=8)
            c.grid(row=0, column=col, padx=6, sticky='nsew')
            resume.columnconfigure(col, weight=1)
            tk.Label(c, text=lbl,  font=(POLICE, 8),          bg='#0F172A', fg='#64748B').pack()
            tk.Label(c, text=val,  font=(POLICE, 14, 'bold'),  bg='#0F172A', fg=AVERT).pack()

        # Tableau des liaisons (triées par coût croissant)
        card_table = tk.Frame(self._frame_resultat, bg=CARTE, padx=18, pady=14)
        card_table.pack(fill=tk.BOTH, expand=True)

        tk.Label(card_table, text="Arêtes retenues (ordre croissant de coût)",
                 font=(POLICE, 10, 'bold'), bg=CARTE, fg=TEXTE).pack(anchor='w', pady=(0, 8))

        entete = tk.Frame(card_table, bg='#0F172A')
        entete.pack(fill=tk.X)
        for col, (txt, w) in enumerate([
            ("#",            4),
            ("De",          18),
            ("Vers",        18),
            ("Distance",    12),
            ("Coût (DH)",   12),
        ]):
            tk.Label(entete, text=txt, width=w,
                     font=(POLICE_MONO, 9, 'bold'),
                     bg='#0F172A', fg=ACCENT, anchor='w').grid(row=0, column=col, padx=4, pady=4)

        for idx, liais in enumerate(liaisons):
            bg = CARTE if idx % 2 == 0 else '#243044'
            ligne = tk.Frame(card_table, bg=bg)
            ligne.pack(fill=tk.X)
            vals = [
                str(idx + 1),
                liais['de'],
                liais['vers'],
                f"{liais['distance']} km",
                f"{liais['cout']:,}",
            ]
            widths = [4, 18, 18, 12, 12]
            for col, (v, w) in enumerate(zip(vals, widths)):
                tk.Label(ligne, text=v, width=w,
                         font=(POLICE_MONO, 9),
                         bg=bg, fg=TEXTE, anchor='w').grid(row=0, column=col, padx=4, pady=3)

        creer_bouton(
            self._frame_resultat,
            "  Visualiser l'ACM sur le graphe",
            lambda: self._voir_graphe(res['acm']),
            couleur_bg=VIOLET, taille=10,
        ).pack(pady=10, anchor='w')

    def _voir_graphe(self, acm):
        from .graph_view import GraphView
        GraphView(self._parent, self.reseau, acm=acm,
                  titre="Kruskal — Arbre Couvrant Minimal")

    def _voir_graphe_acm(self):
        """Affiche le graphe complet avant tout calcul"""
        from .graph_view import GraphView
        GraphView(self._parent, self.reseau, titre="Graphe complet — Kruskal")
