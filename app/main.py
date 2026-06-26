"""
Application Desktop - Recherche Opérationnelle et Algorithmes de Graphes
Mohammadia School of Engineers (EMI)
Étudiante : RAJEB HIBA

Point d'entrée principal.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.logger import configurer_logger
from models.reseau import ReseauElectrique
from views.splash_view import SplashView
from views.main_window import MainWindow


def main():
    configurer_logger()

    root = tk.Tk()
    root.title("Application Desktop - Recherche Opérationnelle et Algorithmes de Graphes")
    root.geometry("1150x700")
    root.minsize(900, 600)
    root.configure(bg='#1A1625')

    # Icône (optionnelle)
    try:
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception:
        pass

    # Centrer la fenêtre
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x  = (sw - 1150) // 2
    y  = (sh - 700)  // 2
    root.geometry(f"1150x700+{max(0, x)}+{max(0, y)}")

    # Modèle (initialisé une seule fois)
    try:
        reseau = ReseauElectrique()
    except Exception as e:
        messagebox.showerror("Erreur critique",
                              f"Impossible d'initialiser le réseau :\n{e}")
        root.destroy()
        return

    # ------------------------------------------------------------------ #
    # Gestion de la transition Splash → Application principale
    # ------------------------------------------------------------------ #
    current_view = [None]   # liste pour permettre la mutation dans la closure

    def lancer_application():
        """Détruit la page d'accueil et affiche la fenêtre principale."""
        if current_view[0]:
            current_view[0].destroy()
        app = MainWindow(root, reseau)
        app.pack(fill=tk.BOTH, expand=True)
        current_view[0] = app

    # Affichage initial : page d'accueil
    splash = SplashView(root, on_start=lancer_application)
    splash.pack(fill=tk.BOTH, expand=True)
    current_view[0] = splash

    # Fermeture propre
    def on_close():
        import matplotlib.pyplot as plt
        plt.close('all')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
