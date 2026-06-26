import tkinter as tk
from tkinter import messagebox
import logging

from algorithms.simplexe import creer_probleme, executer_simplexe
from views.theme import (FOND, SIDEBAR, ACCENT, TEXTE, CARTE, BORDURE,
                          SUCCES, ERREUR, AVERT, VIOLET, MUTED, POLICE,
                          POLICE_MONO, creer_bouton, creer_header)

logger = logging.getLogger(__name__)

# Constraint labels used in the editor
_CTR_LABELS = ["Capacité réseau Nord", "Capacité réseau Centre", "Capacité réseau Sud"]


class SimplexeView(tk.Toplevel):
    def __init__(self, parent, reseau):
        super().__init__(parent)
        self.reseau = reseau
        self._current_pb = None   # None → use default from creer_probleme()

        self.title("Méthode du Simplexe — Optimisation Énergétique")
        self.geometry("840x680")
        self.configure(bg=FOND)
        self.resizable(True, True)

        self._creer_interface()
        self._centrer(parent)
        self._calculer()

    def _centrer(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width()  - 840) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 680) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

    # ------------------------------------------------------------------ #
    def _creer_interface(self):
        creer_header(self, "  Méthode du Simplexe — Programmation Linéaire")

        self._outer = tk.Frame(self, bg=FOND, padx=20, pady=12)
        self._outer.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self._outer, bg=FOND)
        btn_frame.pack(pady=(0, 10))

        creer_bouton(btn_frame, "  Modifier le Problème", self._ouvrir_editeur,
                     couleur_bg=VIOLET, couleur_fg=TEXTE, taille=10).pack(side=tk.LEFT, padx=6)
        creer_bouton(btn_frame, "  Fermer", self.destroy,
                     couleur_bg='#334155', taille=10).pack(side=tk.LEFT, padx=6)

        # Scrollable zone
        container = tk.Frame(self._outer, bg=FOND)
        container.pack(fill=tk.BOTH, expand=True)

        vbar = tk.Scrollbar(container, orient='vertical', bg=FOND)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._canvas = tk.Canvas(container, bg=FOND, highlightthickness=0,
                                  yscrollcommand=vbar.set)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vbar.config(command=self._canvas.yview)

        self._scroll_frame = tk.Frame(self._canvas, bg=FOND)
        self._canvas_win = self._canvas.create_window(
            (0, 0), window=self._scroll_frame, anchor='nw'
        )
        self._scroll_frame.bind('<Configure>', self._on_frame_configure)
        self._canvas.bind('<Configure>', self._on_canvas_configure)
        self._canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _on_frame_configure(self, _):
        self._canvas.configure(scrollregion=self._canvas.bbox('all'))

    def _on_canvas_configure(self, event):
        self._canvas.itemconfig(self._canvas_win, width=event.width)

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    # ------------------------------------------------------------------ #
    def _calculer(self):
        for w in self._scroll_frame.winfo_children():
            w.destroy()

        try:
            pb = self._current_pb if self._current_pb else creer_probleme()
            self._current_pb = pb   # keep a reference for the editor
            solution, val_opt, iterations, headers = executer_simplexe(
                pb['c'], pb['A'], pb['b']
            )
            self._afficher(pb, solution, val_opt, iterations, headers)
        except Exception as e:
            logger.exception("Erreur Simplexe")
            tk.Label(self._scroll_frame, text=f"Erreur : {e}",
                     font=(POLICE, 10), bg=FOND, fg=ERREUR).pack(anchor='w')

    # ------------------------------------------------------------------ #
    def _ouvrir_editeur(self):
        pb = self._current_pb
        n  = len(pb['c'])
        m  = len(pb['b'])

        dlg = tk.Toplevel(self)
        dlg.title("Modifier le Problème d'Optimisation")
        dlg.configure(bg=FOND)
        dlg.geometry("640x520")
        dlg.resizable(False, False)
        dlg.grab_set()

        dlg.update_idletasks()
        x = self.winfo_x() + (self.winfo_width()  - 640) // 2
        y = self.winfo_y() + (self.winfo_height() - 520) // 2
        dlg.geometry(f"+{max(0, x)}+{max(0, y)}")

        outer = tk.Frame(dlg, bg=FOND, padx=22, pady=16)
        outer.pack(fill=tk.BOTH, expand=True)

        tk.Label(outer, text="Modifier le Problème d'Optimisation",
                 font=(POLICE, 12, 'bold'), bg=FOND, fg=ACCENT).pack(anchor='w', pady=(0, 14))

        # ---- Objective function ----------------------------------------
        card_obj = tk.Frame(outer, bg=CARTE, padx=16, pady=14)
        card_obj.pack(fill=tk.X, pady=(0, 10))

        tk.Label(card_obj, text="Fonction objectif  —  Maximiser Z",
                 font=(POLICE, 10, 'bold'), bg=CARTE, fg=ACCENT).pack(anchor='w', pady=(0, 10))

        row_obj = tk.Frame(card_obj, bg=CARTE)
        row_obj.pack(anchor='w')

        tk.Label(row_obj, text="Z  =", font=(POLICE_MONO, 11),
                 bg=CARTE, fg=TEXTE).pack(side=tk.LEFT, padx=(0, 6))

        c_entries = []
        SUBS = ['₁', '₂', '₃', '₄', '₅', '₆']
        for i in range(n):
            e = _entry(row_obj, str(_fmt(pb['c'][i])), width=5)
            e.pack(side=tk.LEFT, padx=2)
            tk.Label(row_obj, text=f"x{SUBS[i] if i < len(SUBS) else i+1}",
                     font=(POLICE_MONO, 11), bg=CARTE, fg=SUCCES).pack(side=tk.LEFT)
            if i < n - 1:
                tk.Label(row_obj, text="  +", font=(POLICE_MONO, 11),
                         bg=CARTE, fg=TEXTE).pack(side=tk.LEFT, padx=(2, 4))
            c_entries.append(e)

        # ---- Constraints -----------------------------------------------
        card_ctr = tk.Frame(outer, bg=CARTE, padx=16, pady=14)
        card_ctr.pack(fill=tk.X, pady=(0, 10))

        tk.Label(card_ctr, text="Contraintes  ( ≤ )",
                 font=(POLICE, 10, 'bold'), bg=CARTE, fg=ACCENT).pack(anchor='w', pady=(0, 10))

        grid = tk.Frame(card_ctr, bg=CARTE)
        grid.pack(anchor='w')

        # Header
        tk.Label(grid, text="", width=20, bg=CARTE).grid(row=0, column=0)
        for j in range(n):
            tk.Label(grid, text=f"x{SUBS[j] if j < len(SUBS) else j+1}", width=7,
                     font=(POLICE_MONO, 9, 'bold'), bg=CARTE, fg=SUCCES,
                     anchor='center').grid(row=0, column=j + 1)
        tk.Label(grid, text="≤", width=3, font=(POLICE_MONO, 9),
                 bg=CARTE, fg=MUTED).grid(row=0, column=n + 1)
        tk.Label(grid, text="b", width=7, font=(POLICE_MONO, 9, 'bold'),
                 bg=CARTE, fg=AVERT, anchor='center').grid(row=0, column=n + 2)

        A_entries = []
        b_entries = []
        for i in range(m):
            lbl = _CTR_LABELS[i] if i < len(_CTR_LABELS) else f"Contrainte {i+1}"
            tk.Label(grid, text=lbl, width=20, anchor='w',
                     font=(POLICE, 9), bg=CARTE, fg=MUTED).grid(row=i + 1, column=0, pady=4)

            row_a = []
            for j in range(n):
                e = _entry(grid, str(_fmt(pb['A'][i][j])), width=7)
                e.grid(row=i + 1, column=j + 1, padx=3, pady=4)
                row_a.append(e)

            tk.Label(grid, text="≤", width=3, font=(POLICE_MONO, 9),
                     bg=CARTE, fg=MUTED).grid(row=i + 1, column=n + 1)

            eb = _entry(grid, str(_fmt(pb['b'][i])), width=7)
            eb.grid(row=i + 1, column=n + 2, padx=3, pady=4)

            A_entries.append(row_a)
            b_entries.append(eb)

        # Non-negativity hint
        subs_str = ", ".join(f"x{SUBS[i] if i < len(SUBS) else i+1}" for i in range(n))
        tk.Label(card_ctr, text=f"   {subs_str}  ≥  0",
                 font=(POLICE_MONO, 9), bg=CARTE, fg=MUTED).pack(anchor='w', pady=(6, 0))

        # ---- Error label -----------------------------------------------
        err_lbl = tk.Label(outer, text="", font=(POLICE, 9), bg=FOND, fg=ERREUR)
        err_lbl.pack(anchor='w', pady=(0, 4))

        # ---- Action buttons --------------------------------------------
        def appliquer():
            try:
                new_c = [float(e.get().strip()) for e in c_entries]
                new_A = [[float(e.get().strip()) for e in row] for row in A_entries]
                new_b = [float(e.get().strip()) for e in b_entries]
            except ValueError:
                err_lbl.configure(text="Erreur : tous les champs doivent être des nombres valides.")
                return

            if any(v < 0 for v in new_b):
                err_lbl.configure(text="Erreur : les valeurs b doivent être ≥ 0.")
                return

            # Rebuild problem dict with new values
            var_names = pb['variables'][:n]
            ctr_strs  = []
            for i in range(m):
                terms = "  +  ".join(
                    f"{_fmt(new_A[i][j])}x{SUBS[j] if j < len(SUBS) else j+1}"
                    for j in range(n)
                )
                lbl = _CTR_LABELS[i] if i < len(_CTR_LABELS) else f"Contrainte {i+1}"
                ctr_strs.append(f"{terms}  ≤  {_fmt(new_b[i])}   ({lbl})")
            ctr_strs.append(f"{subs_str}  ≥  0")

            coefs_obj = "  +  ".join(
                f"{_fmt(new_c[i])}x{SUBS[i] if i < len(SUBS) else i+1}"
                for i in range(n)
            )

            self._current_pb = {
                'variables':   var_names,
                'objectif':    f'Maximiser  Z = {coefs_obj}   (MWh distribués)',
                'contraintes': ctr_strs,
                'c': new_c,
                'A': new_A,
                'b': new_b,
            }

            dlg.destroy()
            self._calculer()

        btn_row = tk.Frame(outer, bg=FOND)
        btn_row.pack(anchor='e', pady=(4, 0))

        creer_bouton(btn_row, "Annuler", dlg.destroy,
                     couleur_bg='#334155').pack(side=tk.LEFT, padx=(0, 8))
        creer_bouton(btn_row, "  Calculer", appliquer,
                     couleur_bg=VIOLET, couleur_fg=TEXTE).pack(side=tk.LEFT)

    # ------------------------------------------------------------------ #
    def _afficher(self, pb, solution, val_opt, iterations, headers):
        sf = self._scroll_frame

        # --- Problème ---
        card = tk.Frame(sf, bg=CARTE, padx=18, pady=14)
        card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(card, text="Problème d'Optimisation",
                 font=(POLICE, 11, 'bold'), bg=CARTE, fg=ACCENT).pack(anchor='w')
        tk.Frame(card, bg=BORDURE, height=1).pack(fill=tk.X, pady=6)

        tk.Label(card, text=pb['objectif'],
                 font=(POLICE_MONO, 10, 'bold'), bg=CARTE, fg=SUCCES).pack(anchor='w', pady=4)

        tk.Label(card, text="Sous contraintes :",
                 font=(POLICE, 9, 'bold'), bg=CARTE, fg='#94A3B8').pack(anchor='w', pady=(6, 2))
        for ctr in pb['contraintes']:
            tk.Label(card, text=f"   {ctr}",
                     font=(POLICE_MONO, 9), bg=CARTE, fg=TEXTE).pack(anchor='w')

        # --- Tableaux itératifs ---
        tk.Label(sf, text="Tableaux du Simplexe",
                 font=(POLICE, 11, 'bold'), bg=FOND, fg=ACCENT).pack(anchor='w', pady=(8, 4))

        n = len(pb['c'])
        m = len(pb['b'])
        VAR_NAMES   = [f'x{i+1}' for i in range(n)]
        SLACK_NAMES = [f's{i+1}' for i in range(m)]
        ALL_NAMES   = VAR_NAMES + SLACK_NAMES + ['b']

        for it_idx, snap in enumerate(iterations):
            tableau = snap['tableau']
            basic   = snap['basic']

            label_it = "Tableau Initial" if it_idx == 0 else f"Itération {it_idx}"
            card_it  = tk.Frame(sf, bg=CARTE, padx=14, pady=10)
            card_it.pack(fill=tk.X, pady=3)

            tk.Label(card_it, text=label_it,
                     font=(POLICE, 9, 'bold'), bg=CARTE, fg=AVERT).pack(anchor='w', pady=(0, 6))

            entete = tk.Frame(card_it, bg='#0F172A')
            entete.pack(anchor='w')

            tk.Label(entete, text="Base", width=10,
                     font=(POLICE_MONO, 8, 'bold'), bg='#0F172A', fg=ACCENT,
                     relief='ridge', bd=1).grid(row=0, column=0, padx=1, pady=1)

            for j, hdr in enumerate(ALL_NAMES):
                fg = AVERT if hdr == 'b' else (ACCENT if not hdr.startswith('s') else '#94A3B8')
                tk.Label(entete, text=hdr, width=8,
                         font=(POLICE_MONO, 8, 'bold'), bg='#0F172A', fg=fg,
                         relief='ridge', bd=1).grid(row=0, column=j + 1, padx=1, pady=1)

            for i in range(m):
                base_idx  = basic[i] if i < len(basic) else -1
                base_name = ALL_NAMES[base_idx] if 0 <= base_idx < len(ALL_NAMES) else '?'
                row_bg    = CARTE if i % 2 == 0 else '#243044'

                tk.Label(entete, text=base_name, width=10,
                         font=(POLICE_MONO, 8, 'bold'), bg='#0F172A', fg=SUCCES,
                         relief='ridge', bd=1).grid(row=i + 1, column=0, padx=1, pady=1)

                for j, val in enumerate(tableau[i]):
                    txt = f"{val:8.2f}" if abs(val) < 9999 else f"{val:.1e}"
                    tk.Label(entete, text=txt.strip(), width=8,
                             font=(POLICE_MONO, 8), bg=row_bg, fg=TEXTE,
                             relief='ridge', bd=1).grid(row=i + 1, column=j + 1, padx=1, pady=1)

            tk.Label(entete, text="Z", width=10,
                     font=(POLICE_MONO, 8, 'bold'), bg='#0F172A', fg=ERREUR,
                     relief='ridge', bd=1).grid(row=m + 1, column=0, padx=1, pady=1)

            for j, val in enumerate(tableau[m]):
                txt = f"{val:8.2f}" if abs(val) < 9999 else f"{val:.1e}"
                tk.Label(entete, text=txt.strip(), width=8,
                         font=(POLICE_MONO, 8, 'bold'), bg='#0F172A',
                         fg=ERREUR if j < len(ALL_NAMES) - 1 else SUCCES,
                         relief='ridge', bd=1).grid(row=m + 1, column=j + 1, padx=1, pady=1)

        # --- Solution optimale ---
        card_sol = tk.Frame(sf, bg=CARTE, padx=18, pady=16)
        card_sol.pack(fill=tk.X, pady=(10, 0))

        tk.Label(card_sol, text="Solution Optimale",
                 font=(POLICE, 11, 'bold'), bg=CARTE, fg=ACCENT).pack(anchor='w')
        tk.Frame(card_sol, bg=BORDURE, height=1).pack(fill=tk.X, pady=8)

        for nom, val in zip(pb['variables'], solution):
            row = tk.Frame(card_sol, bg=CARTE)
            row.pack(fill=tk.X, pady=3)
            tk.Label(row, text=f"{nom} =",
                     font=(POLICE, 10), bg=CARTE, fg='#94A3B8').pack(side=tk.LEFT)
            tk.Label(row, text=f"  {val:.2f} MWh",
                     font=(POLICE, 12, 'bold'), bg=CARTE, fg=SUCCES).pack(side=tk.LEFT)

        tk.Frame(card_sol, bg=BORDURE, height=1).pack(fill=tk.X, pady=8)

        val_row = tk.Frame(card_sol, bg=CARTE)
        val_row.pack(fill=tk.X)
        tk.Label(val_row, text="Valeur optimale  Z =",
                 font=(POLICE, 11, 'bold'), bg=CARTE, fg='#94A3B8').pack(side=tk.LEFT)
        tk.Label(val_row, text=f"  {val_opt:.2f} MWh",
                 font=(POLICE, 16, 'bold'), bg=CARTE, fg=AVERT).pack(side=tk.LEFT)

        tk.Label(card_sol, text=f"Nombre d'itérations : {len(iterations) - 1}",
                 font=(POLICE, 9), bg=CARTE, fg='#64748B').pack(anchor='w', pady=(8, 0))


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #

def _fmt(v):
    """Return int if value is a whole number, else float."""
    return int(v) if float(v) == int(float(v)) else round(v, 4)


def _entry(parent, value, width=6):
    e = tk.Entry(
        parent,
        width=width,
        bg='#3D3659',
        fg=TEXTE,
        insertbackground=ACCENT,
        font=(POLICE_MONO, 10),
        relief='flat',
        bd=4,
        justify='center',
    )
    e.insert(0, value)
    return e
