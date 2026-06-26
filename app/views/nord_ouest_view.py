import tkinter as tk
import logging

from algorithms.nord_ouest import (
    generer_donnees, methode_nord_ouest
)
from views.theme import (FOND, SIDEBAR, ACCENT, TEXTE, CARTE, BORDURE,
                          SUCCES, ERREUR, AVERT, VIOLET, POLICE,
                          POLICE_MONO, creer_bouton, creer_header)

logger = logging.getLogger(__name__)


class NordOuestView(tk.Toplevel):
    def __init__(self, parent, reseau):
        super().__init__(parent)
        self.reseau = reseau
        self.nb_sources = 3
        self.nb_destinations = 4
        self.sources = []
        self.destinations = []

        self.title("Méthode du Coin Nord-Ouest — Transport d'Énergie")
        self.geometry("780x740")
        self.configure(bg=FOND)
        self.resizable(True, True)

        self._creer_interface()
        self._centrer(parent)
        self._calculer()

    def _centrer(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width()  - 780) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 740) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    # ------------------------------------------------------------------ #
    def _creer_interface(self):
        creer_header(self, "  Méthode du Coin Nord-Ouest")

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

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=14)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        tk.Label(
            outer,
            text=("Résout le problème de transport d'énergie électrique depuis les points producteurs "
                  "vers les points consommateurs. L'allocation débute depuis le coin supérieur gauche (Nord-Ouest)."),
            font=(POLICE, 10), bg=FOND, fg='#94A3B8', wraplength=720, justify='left',
        ).pack(pady=(0, 12), anchor='w')

        # Section configuration
        config_card = tk.Frame(outer, bg=CARTE, padx=18, pady=14)
        config_card.pack(fill=tk.X, pady=(0, 16))

        tk.Label(
            config_card,
            text="Configuration du Problème de Transport",
            font=(POLICE, 11, 'bold'),
            bg=CARTE, fg=ACCENT,
        ).pack(anchor='w', pady=(0, 10))

        # Frame pour les deux champs côte à côte
        fields_frame = tk.Frame(config_card, bg=CARTE)
        fields_frame.pack(fill=tk.X)

        # Colonne gauche - Nombre de points
        left_col = tk.Frame(fields_frame, bg=CARTE)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

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

        self.entry_points = tk.Entry(
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
        self.entry_points.insert(0, "7")  # 3 sources + 4 destinations par défaut
        self.entry_points.pack(anchor='w', pady=(0, 5))

        self.label_points = tk.Label(
            left_col,
            text=f"Valeur actuelle: 7 points",
            font=(POLICE, 9),
            bg=CARTE, fg='#94A3B8',
        )
        self.label_points.pack(anchor='w')

        # Colonne droite - Densité
        right_col = tk.Frame(fields_frame, bg=CARTE)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(
            right_col,
            text="Densité (1-100%)",
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
        self.entry_densite.insert(0, "50")  # Densité par défaut 50%
        self.entry_densite.pack(anchor='w', pady=(0, 5))

        self.label_densite = tk.Label(
            right_col,
            text=f"Valeur actuelle: 50%",
            font=(POLICE, 9),
            bg=CARTE, fg='#94A3B8',
        )
        self.label_densite.pack(anchor='w')

        # Validation lors de la perte de focus
        def validate_points_range(event):
            try:
                val = int(self.entry_points.get())
                if not (1 <= val <= 100):
                    self.entry_points.delete(0, tk.END)
                    self.entry_points.insert(0, str(max(1, min(100, val))))
                val = int(self.entry_points.get())
                self.label_points.configure(text=f"Valeur actuelle: {val} points")
            except ValueError:
                self.entry_points.delete(0, tk.END)
                self.entry_points.insert(0, "7")
                self.label_points.configure(text=f"Valeur actuelle: 7 points")

        def validate_densite_range(event):
            try:
                val = int(self.entry_densite.get())
                if not (1 <= val <= 100):
                    self.entry_densite.delete(0, tk.END)
                    self.entry_densite.insert(0, str(max(1, min(100, val))))
                val = int(self.entry_densite.get())
                self.label_densite.configure(text=f"Valeur actuelle: {val}%")
            except ValueError:
                self.entry_densite.delete(0, tk.END)
                self.entry_densite.insert(0, "50")
                self.label_densite.configure(text=f"Valeur actuelle: 50%")

        self.entry_points.bind('<FocusOut>', validate_points_range)
        self.entry_points.bind('<Return>', validate_points_range)
        self.entry_densite.bind('<FocusOut>', validate_densite_range)
        self.entry_densite.bind('<Return>', validate_densite_range)

        # Callbacks pour mise à jour des labels en temps réel
        def update_points_label(event=None):
            try:
                val = self.entry_points.get()
                if val:
                    self.label_points.configure(text=f"Valeur saisie: {val} points")
            except:
                pass
        
        def update_densite_label(event=None):
            try:
                val = self.entry_densite.get()
                if val:
                    self.label_densite.configure(text=f"Valeur saisie: {val}%")
            except:
                pass
        
        self.entry_points.bind('<KeyRelease>', update_points_label)
        self.entry_densite.bind('<KeyRelease>', update_densite_label)

        # Espace avant le bouton
        tk.Label(config_card, text="", bg=CARTE, height=1).pack()

        # Bouton appliquer
        creer_bouton(
            config_card,
            "  Appliquer Configuration",
            self._appliquer_config,
            couleur_bg=VIOLET,
            taille=10,
        ).pack(anchor='w')

        self._frame_resultat = tk.Frame(outer, bg=FOND)
        self._frame_resultat.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(outer, bg=FOND)
        btn_frame.pack(pady=10)

        creer_bouton(btn_frame, "  Nouvelles données", self._calculer,
                     couleur_bg=ACCENT, couleur_fg='#0F172A', taille=10).pack(side=tk.LEFT, padx=6)
        creer_bouton(btn_frame, "  Fermer",            self.destroy,
                     couleur_bg='#334155', taille=10).pack(side=tk.LEFT, padx=6)

    # ------------------------------------------------------------------ #
    def _appliquer_config(self):
        """Applique la nouvelle configuration du transport"""
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
        
        # Calculer le nombre de sources et destinations basé sur les points et densité
        # Plus de points = plus de sources, densité détermine la répartition
        if nb_points <= 5:
            nb_sources = max(1, nb_points // 2)
            nb_destinations = nb_points - nb_sources
        elif nb_points <= 20:
            nb_sources = max(2, nb_points // 3)
            nb_destinations = nb_points - nb_sources
        else:
            # Pour des graphes plus grands, ajuster selon la densité
            ratio_sources = 0.2 + (densite / 500)  # Entre 0.2 et 0.4
            nb_sources = max(3, int(nb_points * ratio_sources))
            nb_destinations = nb_points - nb_sources
        
        # S'assurer qu'on a au moins 1 source et 1 destination
        nb_sources = max(1, nb_sources)
        nb_destinations = max(1, nb_destinations)
        
        # Mettre à jour les paramètres
        self.nb_sources = nb_sources
        self.nb_destinations = nb_destinations
        
        # Mettre à jour les labels
        self.label_points.configure(text=f"Valeur actuelle: {nb_points} points")
        self.label_densite.configure(text=f"Valeur actuelle: {densite}%")
        
        # Recalculer avec la nouvelle configuration
        self._calculer()

    def _calculer(self):
        for w in self._frame_resultat.winfo_children():
            w.destroy()

        try:
            self.sources, self.destinations, offres, demandes, couts = generer_donnees(self.nb_sources, self.nb_destinations)
            allocation, cout_total  = methode_nord_ouest(offres, demandes, couts)
            self._afficher(offres, demandes, couts, allocation, cout_total)
        except Exception as e:
            logger.exception("Erreur Nord-Ouest")
            tk.Label(self._frame_resultat, text=f"Erreur : {e}",
                     font=(POLICE, 10), bg=FOND, fg=ERREUR).pack(anchor='w')

    # ------------------------------------------------------------------ #
    def _afficher(self, offres, demandes, couts, allocation, cout_total):
        # ---------- Tableau des coûts ----------
        self._tableau(
            self._frame_resultat,
            "Tableau des Coûts Unitaires (DH/MWh)",
            offres, demandes, couts,
            allocation=None,
        )

        tk.Frame(self._frame_resultat, bg=FOND, height=10).pack()

        # ---------- Tableau d'allocation ----------
        self._tableau(
            self._frame_resultat,
            "Tableau d'Allocation — Méthode Nord-Ouest",
            offres, demandes, couts,
            allocation=allocation,
        )

        tk.Frame(self._frame_resultat, bg=FOND, height=10).pack()

        # ---------- Résumé ----------
        card = tk.Frame(self._frame_resultat, bg=CARTE, padx=18, pady=14)
        card.pack(fill=tk.X)

        tk.Label(card, text="Résumé de la Solution",
                 font=(POLICE, 11, 'bold'), bg=CARTE, fg=ACCENT).pack(anchor='w')
        tk.Frame(card, bg=BORDURE, height=1).pack(fill=tk.X, pady=6)

        # Informations sur la configuration
        info_frame = tk.Frame(card, bg=CARTE)
        info_frame.pack(fill=tk.X, pady=(0, 8))
        
        nb_points_total = int(self.entry_points.get()) if hasattr(self, 'entry_points') else self.nb_sources + self.nb_destinations
        densite_config = int(self.entry_densite.get()) if hasattr(self, 'entry_densite') else 50
        
        tk.Label(info_frame, text=f"Points: {nb_points_total} • Densité: {densite_config}% • Sources: {self.nb_sources} • Destinations: {self.nb_destinations}",
                 font=(POLICE, 10), bg=CARTE, fg='#94A3B8').pack(anchor='w')

        cout_frame = tk.Frame(card, bg=CARTE)
        cout_frame.pack(anchor='w')
        tk.Label(cout_frame, text="Coût total de transport :",
                 font=(POLICE, 11), bg=CARTE, fg='#94A3B8').pack(side=tk.LEFT)
        tk.Label(cout_frame, text=f"  {cout_total:,} DH",
                 font=(POLICE, 14, 'bold'), bg=CARTE, fg=SUCCES).pack(side=tk.LEFT)

    # ------------------------------------------------------------------ #
    def _tableau(self, parent, titre, offres, demandes, couts, allocation):
        card = tk.Frame(parent, bg=CARTE, padx=16, pady=12)
        card.pack(fill=tk.X)

        tk.Label(card, text=titre, font=(POLICE, 10, 'bold'),
                 bg=CARTE, fg=ACCENT).pack(anchor='w', pady=(0, 8))

        grid = tk.Frame(card, bg=CARTE)
        grid.pack(anchor='w')

        C_W = 14   # cell width
        H_W = 18   # header width

        # Ligne d'en-tête colonnes
        tk.Label(grid, text="", width=H_W, bg='#0F172A', fg=TEXTE,
                 font=(POLICE_MONO, 8, 'bold')).grid(row=0, column=0, padx=2, pady=2)

        for j, dest in enumerate(self.destinations):
            bg = '#0F172A'
            tk.Label(grid, text=dest, width=C_W, bg=bg, fg=ACCENT,
                     font=(POLICE_MONO, 8, 'bold'), wraplength=100).grid(row=0, column=j+1, padx=2, pady=2)

        tk.Label(grid, text="OFFRE", width=C_W, bg='#0F172A', fg=AVERT,
                 font=(POLICE_MONO, 8, 'bold')).grid(row=0, column=len(self.destinations)+1, padx=2, pady=2)

        # Lignes sources
        for i, src in enumerate(self.sources):
            row_bg = CARTE if i % 2 == 0 else '#243044'

            tk.Label(grid, text=src, width=H_W, bg='#0F172A', fg=TEXTE,
                     font=(POLICE_MONO, 8, 'bold'), anchor='w').grid(row=i+1, column=0, padx=2, pady=2)

            for j in range(len(self.destinations)):
                if allocation is None:
                    txt = str(couts[i][j])
                    fg  = TEXTE
                    bg  = row_bg
                else:
                    val = allocation[i][j]
                    txt = str(val) if val > 0 else "—"
                    fg  = SUCCES if val > 0 else '#475569'
                    bg  = '#0D2818' if val > 0 else row_bg

                tk.Label(grid, text=txt, width=C_W, bg=bg, fg=fg,
                         font=(POLICE_MONO, 9, 'bold' if (allocation and allocation[i][j] > 0) else 'normal'),
                         relief='ridge', bd=1).grid(row=i+1, column=j+1, padx=2, pady=2)

            tk.Label(grid, text=str(offres[i]), width=C_W, bg='#0F172A', fg=AVERT,
                     font=(POLICE_MONO, 8, 'bold')).grid(
                row=i+1, column=len(self.destinations)+1, padx=2, pady=2)

        # Ligne DEMANDE
        tk.Label(grid, text="DEMANDE", width=H_W, bg='#0F172A', fg=AVERT,
                 font=(POLICE_MONO, 8, 'bold')).grid(
            row=len(self.sources)+1, column=0, padx=2, pady=2)

        for j, dem in enumerate(demandes):
            tk.Label(grid, text=str(dem), width=C_W, bg='#0F172A', fg=AVERT,
                     font=(POLICE_MONO, 8, 'bold')).grid(
                row=len(self.sources)+1, column=j+1, padx=2, pady=2)

        tk.Label(grid, text=str(sum(offres)), width=C_W, bg='#0F172A', fg='#64748B',
                 font=(POLICE_MONO, 8)).grid(
            row=len(self.sources)+1, column=len(self.destinations)+1, padx=2, pady=2)
