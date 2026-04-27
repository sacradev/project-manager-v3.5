"""
Gerenciador de conexão e operações do banco SQLite
"""
import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional
from .models import *

class DatabaseManager:
    def __init__(self, db_path: str = "rotina.db"):
        self.db_path = Path(db_path)
        self.conn: Optional[sqlite3.Connection] = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Cria o banco e tabelas se não existirem (RN03)"""
        primeira_execucao = not self.db_path.exists()
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute(SCHEMA_ATIVIDADES)
        self.conn.execute(SCHEMA_REGISTRO_SAUDE)
        self.conn.commit()
        
        if primeira_execucao:
            self._carregar_dados_iniciais()
    
    def _carregar_dados_iniciais(self):
        """Insere a carga padrão na primeira execução"""
        self.conn.executemany(QUERY_INSERIR_ATIVIDADE, CARGA_INICIAL)
        self.conn.commit()
        print("✅ Banco inicializado com dados padrão")
    
    # ==================== CRUD ATIVIDADES ====================
    
    def adicionar_atividade(self, hora_inicio: str, hora_fim: str, descricao: str) -> bool:
        """RF01 - Cadastro com validação"""
        try:
            self.conn.execute(QUERY_INSERIR_ATIVIDADE, (hora_inicio, hora_fim, descricao))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Conflito de horário
    
    def listar_atividades(self) -> List[Tuple]:
        """RF03 - Retorna lista ordenada cronologicamente"""
        cursor = self.conn.execute(QUERY_LISTAR_ATIVIDADES)
        return cursor.fetchall()
    
    def atualizar_atividade(self, id_: int, hora_inicio: str, hora_fim: str, descricao: str) -> bool:
        """RF04 - Edição de atividade existente"""
        try:
            self.conn.execute(QUERY_ATUALIZAR_ATIVIDADE, (hora_inicio, hora_fim, descricao, id_))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def deletar_atividade(self, id_: int):
        """RF04 - Remoção de atividade"""
        self.conn.execute(QUERY_DELETAR_ATIVIDADE, (id_,))
        self.conn.commit()
    
    # ==================== HIDRATAÇÃO ====================
    
    def obter_agua_hoje(self) -> int:
        """RF07 - Retorna quantidade de copos de hoje"""
        cursor = self.conn.execute(QUERY_OBTER_AGUA_HOJE)
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    
    def incrementar_agua(self):
        """RF07 - Adiciona 1 copo ao contador"""
        quantidade_atual = self.obter_agua_hoje()
        nova_quantidade = quantidade_atual + 1
        self.conn.execute(QUERY_ATUALIZAR_AGUA, (nova_quantidade, nova_quantidade))
        self.conn.commit()
        return nova_quantidade
    
    def fechar(self):
        """Encerra conexão ao fechar o app"""
        if self.conn:
            self.conn.close()