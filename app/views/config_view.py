import tkinter as tk
from tkinter import ttk, messagebox
import logging

from views.theme import (FOND, SIDEBAR, ACCENT, TEXTE, CARTE, BORDURE,
                          SUCCES, ERREUR, AVERT, VIOLET, POLICE,
                          creer_bouton, creer_header)

logger = logging.getLogger(__name__)


class ConfigView(tk.Toplevel):
    """Fenêtre de configuration du réseau électrique."""

    def __init__(self, parent, reseau, callback):
        super().__init__(parent)
        self.reseau = reseau
        self.callback = callback
        
        self.title("Configuration du Réseau")
        self.geometry("520x580")
        self.configure(bg=FOND)
        self.resizable(True, True)  # Permettre le redimensionnement
        self.grab_set()

        self._creer_interface()
        self._centrer(parent)

    def _centrer(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width()  - 520) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 580) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    def _creer_interface(self):
        creer_header(self, "  Configuration du Réseau Électrique")

        outer = tk.Frame(self, bg=FOND, padx=25, pady=18)
        outer.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            outer,
            text="Configurez les paramètres du réseau électrique avant de commencer.",
            font=(POLICE, 10), bg=FOND, fg='#94A3B8', wraplength=450,
        ).pack(pady=(0, 20))

        # Formulaire
        form = tk.Frame(outer, bg=CARTE, padx=25, pady=20)
        form.pack(fill=tk.X)

        # Nombre de points
        tk.Label(
            form,
            text="Nombre de points",
            font=(POLICE, 11, 'bold'),
            bg=CARTE, fg=TEXTE,
        ).pack(anchor='w', pady=(0, 5))
        
        tk.Label(
            form,
            text="Choisissez entre 1 et 100 points pour votre réseau",
            font=(POLICE, 9),
            bg=CARTE, fg='#94A3B8',
        ).pack(anchor='w', pady=(0, 8))

        frame_villes = tk.Frame(form, bg=CARTE)
        frame_villes.pack(fill=tk.X, pady=(0, 20))

        self.scale_villes = tk.Scale(
            frame_villes,
            from_=1, to=100,
            orient=tk.HORIZONTAL,
            font=(POLICE, 10, 'bold'),
            bg=CARTE, fg=ACCENT,
            troughcolor=SIDEBAR,
            highlightthickness=0,
            sliderlength=30,
            length=400,
            command=self._update_villes_label,
        )
        self.scale_villes.set(self.reseau.nb_villes)
        self.scale_villes.pack(fill=tk.X)

        self.label_villes = tk.Label(
            frame_villes,
            text=f"Valeur actuelle : {self.reseau.nb_villes} points",
            font=(POLICE, 9),
            bg=CARTE, fg=AVERT,
        )
        self.label_villes.pack(anchor='w', pady=(5, 0))

        # Séparateur
        tk.Frame(form, bg=BORDURE, height=1).pack(fill=tk.X, pady=15)

        # Densité
        tk.Label(
            form,
            text="Densité du graphe",
            font=(POLICE, 11, 'bold'),
            bg=CARTE, fg=TEXTE,
        ).pack(anchor='w', pady=(0, 5))
        
        tk.Label(
            form,
            text="Pourcentage de liaisons entre les villes (10% = faible, 100% = complet)",
            font=(POLICE, 9),
            bg=CARTE, fg='#94A3B8',
        ).pack(anchor='w', pady=(0, 8))

        frame_densite = tk.Frame(form, bg=CARTE)
        frame_densite.pack(fill=tk.X, pady=(0, 0))

        self.scale_densite = tk.Scale(
            frame_densite,
            from_=10, to=100,
            orient=tk.HORIZONTAL,
            font=(POLICE, 10, 'bold'),
            bg=CARTE, fg=SUCCES,
            troughcolor=SIDEBAR,
            highlightthickness=0,
            sliderlength=30,
            length=400,
            command=self._update_densite_label,
        )
        self.scale_densite.set(self.reseau.densite)
        self.scale_densite.pack(fill=tk.X)

        self.label_densite = tk.Label(
            frame_densite,
            text=f"Valeur actuelle : {self.reseau.densite}%",
            font=(POLICE, 9),
            bg=CARTE, fg=AVERT,
        )
        self.label_densite.pack(anchor='w', pady=(5, 0))

        # Explication densité
        info_frame = tk.Frame(outer, bg=FOND)
        info_frame.pack(fill=tk.X, pady=(15, 0))

        tk.Label(
            info_frame,
            text="💡 Conseil",
            font=(POLICE, 10, 'bold'),
            bg=FOND, fg=VIOLET,
        ).pack(anchor='w')

        tk.Label(
            info_frame,
            text="• Densité faible (10-30%) : graphe peu connecté, plus rapide à calculer\n"
                 "• Densité moyenne (30-60%) : bon équilibre\n"
                 "• Densité élevée (60-100%) : graphe très connecté, calculs plus longs",
            font=(POLICE, 9),
            bg=FOND, fg='#94A3B8',
            justify='left',
        ).pack(anchor='w', pady=(5, 0))

        # Boutons
        btn_frame = tk.Frame(outer, bg=FOND)
        btn_frame.pack(pady=(20, 0))

        creer_bouton(
            btn_frame, "  Appliquer", self._appliquer,
            couleur_bg=ACCENT, couleur_fg='#0F172A', taille=11
        ).pack(side=tk.LEFT, padx=6)
        
        creer_bouton(
            btn_frame, "  Annuler", self.destroy,
            couleur_bg='#334155', taille=11
        ).pack(side=tk.LEFT, padx=6)

    def _update_villes_label(self, val):
        """Met à jour le label du nombre de points"""
        self.label_villes.configure(text=f"Valeur actuelle : {int(float(val))} points")

    def _update_densite_label(self, val):
        """Met à jour le label de la densité"""
        self.label_densite.configure(text=f"Valeur actuelle : {int(float(val))}%")

    def _appliquer(self):
        """Applique la configuration et ferme la fenêtre"""
        nb_villes = int(self.scale_villes.get())
        densite = int(self.scale_densite.get())
        
        # Reconfigurer le réseau
        self.reseau.reconfigurer(nb_villes, densite)
        
        logger.info(f"Configuration appliquée : {nb_villes} points, {densite}% densité")
        
        messagebox.showinfo(
            "Configuration Appliquée",
            f"Le réseau a été configuré avec :\n\n"
            f"• {nb_villes} points (V1 à V{nb_villes})\n"
            f"• Densité de {densite}%\n"
            f"• {self.reseau.get_stats()['nb_liaisons']} liaisons générées",
            parent=self,
        )
        
        # Appeler le callback pour mettre à jour l'interface principale
        if self.callback:
            self.callback()
        
        self.destroy()
