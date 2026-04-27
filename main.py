"""
Project Manager v3.5
Sistema de Gestão de Rotina, Foco e Saúde

Autor: Victor Sacramento (Sacradev)
Stack: Python 3.13, CustomTkinter, SQLite3
"""
import sys
from ui import MainWindow


def main():
    """Ponto de entrada da aplicação"""
    try:
        app = MainWindow()
        app.mainloop()
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()