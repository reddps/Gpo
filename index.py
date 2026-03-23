"""
Importa e executa a aplicação Cupid Dungeon Tracker.
Mantém compatibilidade com o antigo arquivo index.py.
"""

from main import *

if __name__ == "__main__":
    from tracker import CupidTracker
    app = CupidTracker()
    app.mainloop()
