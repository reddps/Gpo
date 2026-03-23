"""
Constantes, cores e configurações do aplicativo.
"""

# ──────────────────────────────────────────────────────────────────────────────
# Arquivo de dados
# ──────────────────────────────────────────────────────────────────────────────
DATA_FILE = "cupid_tracker_data.json"

# ──────────────────────────────────────────────────────────────────────────────
# Dados de drops por boss
# ──────────────────────────────────────────────────────────────────────────────
DROPS = {
    "Cupid Queen": [
        ("Cupid's Wand",                    "~2%"),
        ("Cupid's Battleaxe",               "~2%"),
        ("Cupid's Chakram",                 "~2%"),
        ("VCQ Outfit",                      "~2%"),
        ("VCQ Wings",                       "~2%"),
        ("Prestige Cupid's Chakram",        "muito raro"),
        ("Cupid Queen's Maid Outfit",       "muito raro"),
        ("Cupid's All-Seeing Eye",          "muito raro"),
        ("Virtuous Cupid Queen's Outfit",   "~2%"),
        ("Virtuous Cupid Queen's Wings",    "~2%"),
    ],
    "Leo": [
        ("Love Boppers Headband",           "~5%"),
        ("Love Shades",                     "~5%"),
        ("Cupid's Harp",                    "~5%"),
        ("VC Vanguard Outfit",              "~5%"),
        ("VC Vanguard Helmet",              "~5%"),
        ("Wings of Leo",                    "~5%"),
        ("Inferno Hagoromo",                "muito raro"),
    ],
    "Worshipper NPCs": [
        ("Cupid's Mask",                    "~5%"),
        ("Worshipper Cape",                 "~5%"),
        ("Wings of Roses",                  "~5%"),
        ("Cupid Scarf",                     "~5%"),
        ("Love Witch's Hat",                "~5%"),
    ],
    "Raro / Comum": [
        ("Cupid's Headband",                "5%"),
        ("Cupid Boat",                      "15%"),
        ("Dark Root",                       "15%"),
        ("SP Reset Essence",                "15%"),
    ],
}

# ──────────────────────────────────────────────────────────────────────────────
# Cores por raridade e itens
# ──────────────────────────────────────────────────────────────────────────────
RARITY_COLORS = {
    "Cupid Queen":      "#c80a98",
    "Leo":              "#e09128",
    "Worshipper NPCs":  "#7c3aed",
    "Raro / Comum":     "#2277bb",
    "muito raro":       "#ff2255",
    "~2%":              "#c80a98",
    "~5%":              "#e09128",
    "5%":               "#2277bb",
    "15%":              "#22aa66",
}

# ──────────────────────────────────────────────────────────────────────────────
# Tema de cores
# ──────────────────────────────────────────────────────────────────────────────
BG       = "#1a1a2e"
SURFACE  = "#16213e"
CARD     = "#0f3460"
ACCENT   = "#e94560"
TEXT     = "#eaeaea"
MUTED    = "#8899aa"
SUCCESS  = "#2ecc71"
BORDER   = "#243050"
