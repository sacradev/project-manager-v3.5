"""
Gerenciador de inicialização automática com o Windows
"""
import os
import sys
from pathlib import Path
import winreg


class StartupManager:
    """Adiciona/remove programa do startup do Windows"""
    
    APP_NAME = "ProjectManagerV35"
    
    @staticmethod
    def adicionar_ao_startup():
        """Adiciona ao registro do Windows para iniciar automaticamente"""
        try:
            # Detecta caminho do executável ou script
            if getattr(sys, 'frozen', False):
                # Se for .exe compilado (PyInstaller)
                caminho_exe = sys.executable
            else:
                # Se for script .py
                python_exe = sys.executable
                script_path = Path(__file__).parent / "main.py"
                
                # Verifica se main.py existe
                if not script_path.exists():
                    return False, f"❌ Arquivo main.py não encontrado em: {script_path}"
                
                # Comando com pythonw.exe (executa sem console)
                python_dir = Path(python_exe).parent
                pythonw_exe = python_dir / "pythonw.exe"
                
                if pythonw_exe.exists():
                    caminho_exe = f'"{pythonw_exe}" "{script_path}"'
                else:
                    caminho_exe = f'"{python_exe}" "{script_path}"'
            
            # Abre chave do registro
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Define valor
            winreg.SetValueEx(key, StartupManager.APP_NAME, 0, winreg.REG_SZ, caminho_exe)
            winreg.CloseKey(key)
            
            print(f"✅ Startup configurado: {caminho_exe}")
            return True, f"✅ Programa configurado para iniciar com o Windows!\n\nComando registrado:\n{caminho_exe}"
            
        except PermissionError:
            return False, "❌ Sem permissão para modificar o registro.\n\nTente executar como Administrador."
        except Exception as e:
            return False, f"❌ Erro ao configurar startup:\n{str(e)}"
    
    @staticmethod
    def remover_do_startup():
        """Remove do startup do Windows"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            winreg.DeleteValue(key, StartupManager.APP_NAME)
            winreg.CloseKey(key)
            
            print("✅ Startup removido")
            return True, "✅ Programa removido do startup!"
            
        except FileNotFoundError:
            return True, "ℹ️ Programa já não estava no startup"
        except PermissionError:
            return False, "❌ Sem permissão para modificar o registro."
        except Exception as e:
            return False, f"❌ Erro ao remover startup:\n{str(e)}"
    
    @staticmethod
    def verificar_startup():
        """Verifica se está no startup"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            
            valor, _ = winreg.QueryValueEx(key, StartupManager.APP_NAME)
            winreg.CloseKey(key)
            
            print(f"✅ Startup ativo: {valor}")
            return True
            
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"⚠️ Erro ao verificar startup: {e}")
            return False
    
    @staticmethod
    def obter_caminho_registrado():
        """Retorna o caminho configurado no registro"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            
            valor, _ = winreg.QueryValueEx(key, StartupManager.APP_NAME)
            winreg.CloseKey(key)
            
            return valor
            
        except:
            return None