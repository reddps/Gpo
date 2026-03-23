"""
Aplicação principal: Cupid Dungeon Tracker.
Gerencia o registro de kills e drops do evento de Valentine em GPO.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from constants import DATA_FILE, DROPS, RARITY_COLORS, BG, SURFACE, CARD, ACCENT, TEXT, MUTED, SUCCESS, BORDER
from data_manager import load_data, save_data


class CupidTracker(tk.Tk):
    """Aplicação principal para rastrear kills e drops do Cupid Dungeon."""

    def __init__(self):
        """Inicializa a aplicação."""
        super().__init__()
        self.title("GPO — Cupid Dungeon Tracker 2026")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(820, 600)

        # Carrega dados e inicializa variáveis
        self.data = load_data()
        self.drop_vars = {}   # item_name -> BooleanVar (checkboxes da kill atual)
        self.fruit_var = tk.StringVar(value="")

        # Métricas em cache para evitar loop repetido
        self.total_kills = self.data.get("total_kills", 0)
        self.total_drops = self.data.get("total_drops", 0)
        self.unique_items = set(self.data.get("unique_items", []))

        # Mapa item -> cor para lookup O(1)
        self.item_color = {
            item: RARITY_COLORS.get(rarity, TEXT)
            for rarity, items in DROPS.items()
            for item, _ in items
        }

        # Constrói a UI
        self._build_ui()
        self._refresh_stats()
        self._refresh_history()

    # ──────────────────────────────────────────────────────────────────────────
    # LAYOUT PRINCIPAL
    # ──────────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        """Constrói a interface principal."""
        self._build_header()
        self._build_body()

    def _build_header(self):
        """Constrói o cabeçalho da aplicação."""
        hdr = tk.Frame(self, bg=SURFACE, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Virtuous Cupid Queen",
                 font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=SURFACE).pack()
        tk.Label(hdr, text="Cupid Dungeon 2026  ·  Valentine's Event",
                 font=("Segoe UI", 10), fg=MUTED, bg=SURFACE).pack()

    def _build_body(self):
        """Constrói o corpo principal com seções esquerda e direita."""
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=14, pady=10)

        left  = tk.Frame(body, bg=BG)
        right = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        right.pack(side="right", fill="both", expand=True, padx=(8, 0))

        self._build_stats(left)
        self._build_drop_form(left)
        self._build_history(right)

    # ──────────────────────────────────────────────────────────────────────────
    # SEÇÃO DE ESTATÍSTICAS
    # ──────────────────────────────────────────────────────────────────────────

    def _build_stats(self, parent):
        """Constrói o painel de estatísticas."""
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="x", pady=(0, 10))

        cards = [
            ("Total de Kills",    "stat_kills",    ACCENT),
            ("Total de Drops",    "stat_drops",    TEXT),
            ("Drops / Kill",      "stat_avg",      SUCCESS),
            ("Itens Únicos",      "stat_unique",   "#a0c4ff"),
        ]
        for i, (label, attr, color) in enumerate(cards):
            c = tk.Frame(frame, bg=CARD, padx=12, pady=8,
                         highlightbackground=BORDER, highlightthickness=1)
            c.grid(row=0, column=i, padx=4, sticky="ew")
            frame.columnconfigure(i, weight=1)
            tk.Label(c, text=label, font=("Segoe UI", 8), fg=MUTED, bg=CARD).pack()
            lbl = tk.Label(c, text="0", font=("Segoe UI", 20, "bold"),
                           fg=color, bg=CARD)
            lbl.pack()
            setattr(self, attr, lbl)

    def _refresh_stats(self):
        """Atualiza os valores exibidos nas estatísticas."""
        kills = self.total_kills
        total = self.total_drops
        unique = len(self.unique_items)
        avg = f"{total/kills:.1f}" if kills else "0.0"
        
        self.stat_kills.config(text=str(kills))
        self.stat_drops.config(text=str(total))
        self.stat_avg.config(text=avg)
        self.stat_unique.config(text=str(unique))

    # ──────────────────────────────────────────────────────────────────────────
    # SEÇÃO DE REGISTRO DE KILL
    # ──────────────────────────────────────────────────────────────────────────

    def _build_drop_form(self, parent):
        """Constrói o formulário para registrar uma nova kill."""
        tk.Label(parent, text="Registrar nova kill",
                 font=("Segoe UI", 11, "bold"), fg=TEXT, bg=BG).pack(anchor="w", pady=(4, 6))

        self._build_drops_list(parent)
        self._build_fruit_field(parent)
        self._build_form_buttons(parent)

    def _build_drops_list(self, parent):
        """Constrói a lista scrollável de checkboxes para itens."""
        outer = tk.Frame(parent, bg=SURFACE, highlightbackground=BORDER,
                         highlightthickness=1)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=SURFACE, highlightthickness=0)
        scroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=SURFACE)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def on_canvas_resize(e):
            canvas.itemconfig(win_id, width=e.width)

        inner.bind("<Configure>", on_configure)
        canvas.bind("<Configure>", on_canvas_resize)
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        # Checkboxes por raridade
        for rarity, items in DROPS.items():
            color = RARITY_COLORS[rarity]
            header = tk.Frame(inner, bg=SURFACE)
            header.pack(fill="x", padx=10, pady=(10, 2))
            tk.Label(header, text="●", font=("Segoe UI", 9), fg=color,
                     bg=SURFACE).pack(side="left")
            tk.Label(header, text=f"  {rarity}",
                     font=("Segoe UI", 9, "bold"), fg=color, bg=SURFACE).pack(side="left")

            grid = tk.Frame(inner, bg=SURFACE)
            grid.pack(fill="x", padx=16, pady=(0, 4))

            for idx, (item, rate) in enumerate(items):
                var = tk.BooleanVar(value=False)
                self.drop_vars[item] = var
                row = idx // 2
                col = idx % 2
                cell = tk.Frame(grid, bg=SURFACE)
                cell.grid(row=row, column=col, sticky="w", padx=4, pady=1)
                grid.columnconfigure(col, weight=1)

                cb = tk.Checkbutton(cell, variable=var, bg=SURFACE,
                                    activebackground=SURFACE,
                                    selectcolor=CARD, fg=TEXT,
                                    activeforeground=TEXT,
                                    highlightthickness=0, bd=0)
                cb.pack(side="left")
                tk.Label(cell, text=item, font=("Segoe UI", 9), fg=TEXT,
                         bg=SURFACE).pack(side="left")
                tk.Label(cell, text=f" {rate}", font=("Segoe UI", 8),
                         fg=MUTED, bg=SURFACE).pack(side="left")

    def _build_fruit_field(self, parent):
        """Constrói o campo para registrar Fruta do Diabo (MVP)."""
        fruit_outer = tk.Frame(parent, bg=SURFACE, highlightbackground=BORDER,
                               highlightthickness=1)
        fruit_outer.pack(fill="x", pady=(8, 0))

        fruit_header = tk.Frame(fruit_outer, bg=SURFACE)
        fruit_header.pack(fill="x", padx=10, pady=(8, 4))
        tk.Label(fruit_header, text="🍎", font=("Segoe UI", 11),
                 bg=SURFACE).pack(side="left")
        tk.Label(fruit_header, text="  Fruta do Diabo dropada (MVP)",
                 font=("Segoe UI", 9, "bold"), fg="#2ecc71", bg=SURFACE).pack(side="left")
        tk.Label(fruit_header, text=" — deixe em branco se não foi MVP",
                 font=("Segoe UI", 8), fg=MUTED, bg=SURFACE).pack(side="left")

        fruit_row = tk.Frame(fruit_outer, bg=SURFACE)
        fruit_row.pack(fill="x", padx=10, pady=(0, 10))

        self.fruit_entry = tk.Entry(fruit_row, textvariable=self.fruit_var,
                                    font=("Segoe UI", 10), bg=CARD, fg=TEXT,
                                    insertbackground=TEXT, relief="flat",
                                    highlightbackground=BORDER,
                                    highlightthickness=1)
        self.fruit_entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 6))
        self.fruit_entry.insert(0, "Ex: Paw Paw, Rumble Rumble, Dough...")

        def on_focus_in(e):
            if self.fruit_var.get().startswith("Ex:"):
                self.fruit_entry.delete(0, "end")
                self.fruit_entry.config(fg=TEXT)

        def on_focus_out(e):
            if not self.fruit_var.get().strip():
                self.fruit_entry.insert(0, "Ex: Paw Paw, Rumble Rumble, Dough...")
                self.fruit_entry.config(fg=MUTED)

        self.fruit_entry.config(fg=MUTED)
        self.fruit_entry.bind("<FocusIn>", on_focus_in)
        self.fruit_entry.bind("<FocusOut>", on_focus_out)
        self.fruit_entry.bind("<Return>", lambda e: self._save_kill())

        tk.Button(fruit_row, text="✕", font=("Segoe UI", 9),
                  bg=CARD, fg=MUTED, activebackground=BORDER,
                  activeforeground=TEXT, relief="flat", padx=8, pady=5,
                  cursor="hand2",
                  command=self._clear_fruit).pack(side="left")

    def _build_form_buttons(self, parent):
        """Constrói os botões de ação do formulário."""
        btn_frame = tk.Frame(parent, bg=BG)
        btn_frame.pack(fill="x", pady=8)

        tk.Button(btn_frame, text="⚔️  Salvar Kill",
                  font=("Segoe UI", 11, "bold"),
                  bg=ACCENT, fg="white", activebackground="#c73550",
                  activeforeground="white", relief="flat", pady=8,
                  cursor="hand2", command=self._save_kill).pack(
                      side="left", fill="x", expand=True, padx=(0, 6))

        tk.Button(btn_frame, text="Limpar seleção",
                  font=("Segoe UI", 9), bg=CARD, fg=MUTED,
                  activebackground=BORDER, activeforeground=TEXT,
                  relief="flat", pady=8, cursor="hand2",
                  command=self._clear_checks).pack(side="left")

    def _save_kill(self):
        """Salva uma nova kill com os itens selecionados."""
        selected = [item for item, var in self.drop_vars.items() if var.get()]
        raw_fruit = self.fruit_var.get().strip()
        fruit = raw_fruit if raw_fruit and not raw_fruit.startswith("Ex:") else ""
        
        entry = {
            "kill_num": self.data["total_kills"] + 1,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "drops": selected,
            "fruit": fruit,
        }
        
        self.data["kills"].append(entry)
        self.total_kills += 1
        self.total_drops += len(selected)
        self.unique_items.update(selected)

        self.data["total_kills"] = self.total_kills
        self.data["total_drops"] = self.total_drops
        self.data["unique_items"] = sorted(self.unique_items)

        save_data(self.data)
        self._clear_checks()
        self._clear_fruit()
        self._refresh_stats()
        self._refresh_history()

    def _clear_checks(self):
        """Limpa todos os checkboxes de itens."""
        for var in self.drop_vars.values():
            var.set(False)

    def _clear_fruit(self):
        """Limpa o campo de Fruta do Diabo."""
        self.fruit_var.set("")
        self.fruit_entry.delete(0, "end")
        self.fruit_entry.insert(0, "Ex: Paw Paw, Rumble Rumble, Dough...")
        self.fruit_entry.config(fg=MUTED)

    # ──────────────────────────────────────────────────────────────────────────
    # SEÇÃO DE HISTÓRICO
    # ──────────────────────────────────────────────────────────────────────────

    def _build_history(self, parent):
        """Constrói o painel de histórico de kills."""
        hdr = tk.Frame(parent, bg=BG)
        hdr.pack(fill="x", pady=(0, 6))
        tk.Label(hdr, text="Histórico de kills",
                 font=("Segoe UI", 11, "bold"), fg=TEXT, bg=BG).pack(side="left")
        tk.Button(hdr, text="Apagar tudo", font=("Segoe UI", 8),
                  bg=BG, fg="#e05050", activebackground=BG,
                  activeforeground=ACCENT, relief="flat", cursor="hand2",
                  command=self._reset_all).pack(side="right")

        # Frame com scroll
        outer = tk.Frame(parent, bg=SURFACE, highlightbackground=BORDER,
                         highlightthickness=1)
        outer.pack(fill="both", expand=True)

        self.hist_canvas = tk.Canvas(outer, bg=SURFACE, highlightthickness=0)
        scroll = ttk.Scrollbar(outer, orient="vertical",
                               command=self.hist_canvas.yview)
        self.hist_canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.hist_canvas.pack(side="left", fill="both", expand=True)

        self.hist_inner = tk.Frame(self.hist_canvas, bg=SURFACE)
        self._hist_win = self.hist_canvas.create_window(
            (0, 0), window=self.hist_inner, anchor="nw")

        def on_cfg(e):
            self.hist_canvas.configure(
                scrollregion=self.hist_canvas.bbox("all"))
        def on_resize(e):
            self.hist_canvas.itemconfig(self._hist_win, width=e.width)

        self.hist_inner.bind("<Configure>", on_cfg)
        self.hist_canvas.bind("<Configure>", on_resize)
        self.hist_canvas.bind_all("<MouseWheel>",
            lambda e: self.hist_canvas.yview_scroll(-1*(e.delta//120), "units"))

    def _refresh_history(self):
        """Atualiza o histórico de kills exibido."""
        for w in self.hist_inner.winfo_children():
            w.destroy()

        kills = list(reversed(self.data["kills"]))
        if not kills:
            tk.Label(self.hist_inner, text="Nenhuma kill registrada ainda. Vai caçar! 🎯",
                     font=("Segoe UI", 10), fg=MUTED, bg=SURFACE,
                     wraplength=280).pack(pady=30)
            return

        for k in kills:
            self._build_kill_card(k)

    def _build_kill_card(self, kill_entry):
        """Constrói um card para uma kill individual."""
        card = tk.Frame(self.hist_inner, bg=CARD,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", padx=8, pady=4)

        # Cabeçalho do card
        top = tk.Frame(card, bg=CARD)
        top.pack(fill="x", padx=10, pady=(7, 2))
        tk.Label(top, text=f"Kill #{kill_entry['kill_num']}",
                 font=("Segoe UI", 10, "bold"), fg=ACCENT, bg=CARD).pack(side="left")
        tk.Label(top, text=kill_entry["timestamp"],
                 font=("Segoe UI", 8), fg=MUTED, bg=CARD).pack(side="right")

        # Fruta do Diabo (se houver)
        fruit = kill_entry.get("fruit", "")
        if fruit:
            fruit_frame = tk.Frame(card, bg=CARD)
            fruit_frame.pack(fill="x", padx=10, pady=(0, 2))
            tk.Label(fruit_frame,
                     text=f"  🍎 Fruta: {fruit}",
                     font=("Segoe UI", 8, "bold"), fg="#2ecc71", bg=CARD,
                     anchor="w").pack(fill="x")

        # Drops
        drops = kill_entry["drops"]
        if drops:
            drop_frame = tk.Frame(card, bg=CARD)
            drop_frame.pack(fill="x", padx=10, pady=(0, 7))
            for item in drops:
                rarity_color = self._get_rarity_color(item)
                tk.Label(drop_frame,
                         text=f"  ● {item}",
                         font=("Segoe UI", 8), fg=rarity_color, bg=CARD,
                         anchor="w").pack(fill="x")
        else:
            tk.Label(card, text="  Nenhum drop",
                     font=("Segoe UI", 8, "italic"), fg=MUTED, bg=CARD,
                     anchor="w").pack(padx=10, pady=(0, 7))

    def _get_rarity_color(self, item_name):
        """Retorna a cor associada a um item."""
        return self.item_color.get(item_name, TEXT)

    def _reset_all(self):
        """Apaga todo o histórico de kills."""
        if not messagebox.askyesno("Apagar tudo?",
                "Isso vai apagar todo o histórico de kills.\nTem certeza?"):
            return
        self.data = {"kills": [], "total_kills": 0, "total_drops": 0, "unique_items": []}
        self.total_kills = 0
        self.total_drops = 0
        self.unique_items = set()
        save_data(self.data)
        self._refresh_stats()
        self._refresh_history()
