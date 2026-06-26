import tkinter as tk
from tkinter import ttk

FOND    = '#1A1625'   # deep purple-black background
SIDEBAR = '#211C30'   # dark purple sidebar
ACCENT  = '#C084FC'   # lavender purple accent
TEXTE   = '#EDE9F5'   # near-white with purple tint
CARTE   = '#2A2440'   # dark purple card
BORDURE = '#3D3659'   # muted purple border
SUCCES  = '#4ADE80'
ERREUR  = '#EF4444'
AVERT   = '#F59E0B'
VIOLET  = '#9B5DE5'   # brighter purple for highlights
MUTED   = '#8B87A0'   # muted lavender-gray
POLICE      = 'Segoe UI'
POLICE_MONO = 'Consolas'


def appliquer_style_ttk(root):
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure(
        'TCombobox',
        fieldbackground=CARTE,
        background=CARTE,
        foreground=TEXTE,
        arrowcolor=ACCENT,
        selectbackground='#9B5DE5',
        selectforeground='white',
        bordercolor=BORDURE,
        lightcolor=BORDURE,
        darkcolor=BORDURE,
    )
    style.map('TCombobox',
        fieldbackground=[('readonly', CARTE)],
        foreground=[('readonly', TEXTE)],
        selectbackground=[('readonly', '#9B5DE5')],
    )
    style.configure(
        'TScrollbar',
        background=BORDURE,
        troughcolor=SIDEBAR,
        arrowcolor=MUTED,
        bordercolor=SIDEBAR,
    )


def creer_bouton(parent, texte, commande, couleur_bg=None, couleur_fg=None,
                 taille=10, bold=True, padx=15, pady=7):
    if couleur_bg is None:
        couleur_bg = CARTE
    if couleur_fg is None:
        couleur_fg = TEXTE

    poids = 'bold' if bold else 'normal'
    btn = tk.Button(
        parent,
        text=texte,
        command=commande,
        font=(POLICE, taille, poids),
        bg=couleur_bg,
        fg=couleur_fg,
        activebackground=ACCENT,
        activeforeground='#1A1625',
        relief='flat',
        cursor='hand2',
        padx=padx,
        pady=pady,
        bd=0,
    )

    hover_bg = ACCENT
    hover_fg = '#1A1625'
    orig_bg  = couleur_bg
    orig_fg  = couleur_fg

    btn.bind('<Enter>', lambda e: btn.configure(bg=hover_bg, fg=hover_fg))
    btn.bind('<Leave>', lambda e: btn.configure(bg=orig_bg,  fg=orig_fg))
    return btn


def creer_header(parent, texte, bg=SIDEBAR, fg=ACCENT, hauteur=55):
    frame = tk.Frame(parent, bg=bg, height=hauteur)
    frame.pack(fill=tk.X)
    frame.pack_propagate(False)
    tk.Label(
        frame, text=texte,
        font=(POLICE, 13, 'bold'),
        bg=bg, fg=fg,
    ).pack(side=tk.LEFT, padx=15, pady=12)
    return frame


def creer_separateur_label(parent, texte, bg=SIDEBAR):
    tk.Label(
        parent, text=texte.upper(),
        font=(POLICE, 7, 'bold'),
        bg=bg, fg='#475569',
    ).pack(fill=tk.X, padx=15, pady=(14, 2))
    tk.Frame(parent, bg=BORDURE, height=1).pack(fill=tk.X, padx=15, pady=(0, 4))


def creer_section_config_graphe(parent, reseau, callback_appliquer=None):
    """
    Crée une section de configuration du graphe (nombre de points et densité).
    
    Args:
        parent: Widget parent
        reseau: Instance de ReseauElectrique
        callback_appliquer: Fonction à appeler après application de la config
    
    Returns:
        tuple: (entry_points, entry_densite, label_points, label_densite)
    """
    config_card = tk.Frame(parent, bg=CARTE, padx=18, pady=14)
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

    entry_points = tk.Entry(
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
    entry_points.insert(0, str(reseau.nb_villes))
    entry_points.pack(anchor='w', pady=(0, 5))

    label_points = tk.Label(
        left_col,
        text=f"Valeur actuelle: {reseau.nb_villes}",
        font=(POLICE, 9),
        bg=CARTE, fg='#94A3B8',
    )
    label_points.pack(anchor='w')

    # Colonne droite - Densité
    right_col = tk.Frame(fields_frame, bg=CARTE)
    right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

    tk.Label(
        right_col,
        text="Densité du graphe (1-100%)",
        font=(POLICE, 10, 'bold'),
        bg=CARTE, fg=TEXTE,
    ).pack(anchor='w', pady=(0, 5))

    entry_densite = tk.Entry(
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
    entry_densite.insert(0, str(reseau.densite))
    entry_densite.pack(anchor='w', pady=(0, 5))

    label_densite = tk.Label(
        right_col,
        text=f"Valeur actuelle: {reseau.densite}%",
        font=(POLICE, 9),
        bg=CARTE, fg='#94A3B8',
    )
    label_densite.pack(anchor='w')

    # Validation lors de la perte de focus
    def validate_points_range(event):
        try:
            val = int(entry_points.get())
            if not (1 <= val <= 100):
                entry_points.delete(0, tk.END)
                entry_points.insert(0, str(max(1, min(100, val))))
            label_points.configure(text=f"Valeur actuelle: {entry_points.get()}")
        except ValueError:
            entry_points.delete(0, tk.END)
            entry_points.insert(0, str(reseau.nb_villes))
            label_points.configure(text=f"Valeur actuelle: {reseau.nb_villes}")

    def validate_densite_range(event):
        try:
            val = int(entry_densite.get())
            if not (1 <= val <= 100):
                entry_densite.delete(0, tk.END)
                entry_densite.insert(0, str(max(1, min(100, val))))
            label_densite.configure(text=f"Valeur actuelle: {entry_densite.get()}%")
        except ValueError:
            entry_densite.delete(0, tk.END)
            entry_densite.insert(0, str(reseau.densite))
            label_densite.configure(text=f"Valeur actuelle: {reseau.densite}%")

    entry_points.bind('<FocusOut>', validate_points_range)
    entry_points.bind('<Return>', validate_points_range)
    entry_densite.bind('<FocusOut>', validate_densite_range)
    entry_densite.bind('<Return>', validate_densite_range)

    # Callbacks pour mise à jour des labels en temps réel
    def update_points_label(event=None):
        try:
            val = entry_points.get()
            if val:
                label_points.configure(text=f"Valeur saisie: {val}")
        except:
            pass
    
    def update_densite_label(event=None):
        try:
            val = entry_densite.get()
            if val:
                label_densite.configure(text=f"Valeur saisie: {val}%")
        except:
            pass
    
    entry_points.bind('<KeyRelease>', update_points_label)
    entry_densite.bind('<KeyRelease>', update_densite_label)

    # Bouton appliquer si callback fourni
    if callback_appliquer:
        tk.Label(config_card, text="", bg=CARTE, height=1).pack()  # Espace
        creer_bouton(
            config_card,
            "  Appliquer Configuration",
            callback_appliquer,
            couleur_bg=VIOLET,
            taille=10,
        ).pack(anchor='w')

    return entry_points, entry_densite, label_points, label_densite
