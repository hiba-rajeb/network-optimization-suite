import tkinter as tk

from views.theme import (FOND, SIDEBAR, ACCENT, TEXTE, CARTE, BORDURE,
                          SUCCES, ERREUR, AVERT, MUTED, POLICE)


class SplashView(tk.Frame):
    """Page d'accueil affichée au lancement de l'application."""

    def __init__(self, parent, on_start):
        super().__init__(parent, bg=FOND)
        self._on_start = on_start
        self._creer_interface()

    # ------------------------------------------------------------------ #
    def _creer_interface(self):
        # Conteneur centré verticalement
        outer = tk.Frame(self, bg=FOND)
        outer.place(relx=0.5, rely=0.5, anchor='center')

        # ---- Logo / icône électrique ----
        tk.Label(
            outer,
            text="⚡",
            font=(POLICE, 64),
            bg=FOND, fg=ACCENT,
        ).pack(pady=(0, 6))

        # ---- Nom de l'école ----
        tk.Label(
            outer,
            text="Mohammadia School of Engineers",
            font=(POLICE, 18, 'bold'),
            bg=FOND, fg=TEXTE,
        ).pack()

        tk.Label(
            outer,
            text="EMI — École Mohammadia d'Ingénieurs",
            font=(POLICE, 11),
            bg=FOND, fg=MUTED,
        ).pack(pady=(2, 0))

        # ---- Séparateur ----
        tk.Frame(outer, bg=ACCENT, height=2, width=480).pack(pady=22)

        # ---- Titre de l'application ----
        tk.Label(
            outer,
            text="Optimisation du Réseau Électrique au Maroc",
            font=(POLICE, 24, 'bold'),
            bg=FOND, fg=TEXTE,
        ).pack(pady=(4, 0))

        tk.Label(
            outer,
            text="Application Desktop — Recherche Opérationnelle et Algorithmes de Graphes",
            font=(POLICE, 11),
            bg=FOND, fg=MUTED,
        ).pack(pady=(6, 0))

        # ---- Séparateur ----
        tk.Frame(outer, bg=BORDURE, height=1, width=480).pack(pady=22)

        # ---- Infos étudiante & encadrante ----
        info_frame = tk.Frame(outer, bg=FOND)
        info_frame.pack()

        self._ligne_info(info_frame, "Étudiante :", "RAJEB HIBA", 0)

        # Séparateur vertical entre les deux infos
        tk.Frame(info_frame, bg=BORDURE, width=1, height=45).pack(side=tk.LEFT, padx=20)

        self._ligne_info(info_frame, "Encadrante :", "Dr. EL MKHALET MOUNA", 0)

        # ---- Bouton Démarrer ----
        btn = tk.Button(
            outer,
            text="  Démarrer l'Application  ",
            command=self._on_start,
            font=(POLICE, 13, 'bold'),
            bg=ACCENT,
            fg='#0F172A',
            activebackground='#0EA5E9',
            activeforeground='#0F172A',
            relief='flat',
            cursor='hand2',
            padx=30, pady=12,
            bd=0,
        )
        btn.pack(pady=(28, 0))

        btn.bind('<Enter>', lambda e: btn.configure(bg='#0EA5E9'))
        btn.bind('<Leave>', lambda e: btn.configure(bg=ACCENT))

        # ---- Version ----
        tk.Label(
            outer,
            text="Python · Tkinter · NetworkX · Matplotlib  —  2026",
            font=(POLICE, 8),
            bg=FOND, fg='#334155',
        ).pack(pady=(20, 0))

    # ------------------------------------------------------------------ #
    def _ligne_info(self, parent, label, valeur, row):
        f = tk.Frame(parent, bg=FOND)
        f.pack(side=tk.LEFT, padx=16)
        tk.Label(f, text=label,  font=(POLICE, 10),         bg=FOND, fg=MUTED).pack()
        tk.Label(f, text=valeur, font=(POLICE, 13, 'bold'),  bg=FOND, fg=TEXTE).pack()
