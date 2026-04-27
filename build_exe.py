"""
Script para compilar o Project Manager em executável
"""
import PyInstaller.__main__
import shutil
from pathlib import Path

# Limpa builds anteriores
if Path('dist').exists():
    shutil.rmtree('dist')
if Path('build').exists():
    shutil.rmtree('build')

# Configuração do PyInstaller
PyInstaller.__main__.run([
    'main.py',
    '--name=ProjectManager',
    '--onefile',  # Um único arquivo
    '--windowed',  # Sem console
    '--icon=icon.ico',  # Ícone customizado
    '--add-data=rotina.db;.',  # Inclui banco (se já existir)
    '--hidden-import=customtkinter',
    '--hidden-import=PIL',
    '--clean',
])

print("\n" + "="*50)
print("✅ COMPILAÇÃO CONCLUÍDA!")
print("="*50)
print(f"\n📦 Executável criado em: dist/ProjectManager.exe")
print(f"📊 Tamanho aproximado: ~50-70 MB")
print("\n🚀 Para testar: dist/ProjectManager.exe")