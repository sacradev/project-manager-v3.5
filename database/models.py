"""
Schemas e queries SQL do sistema
"""

SCHEMA_ATIVIDADES = """
CREATE TABLE IF NOT EXISTS atividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hora_inicio TEXT NOT NULL, 
    hora_fim TEXT NOT NULL,
    descricao TEXT NOT NULL,
    UNIQUE(hora_inicio, hora_fim)
);
"""

SCHEMA_REGISTRO_SAUDE = """
CREATE TABLE IF NOT EXISTS registro_saude (
    data DATE PRIMARY KEY,
    quantidade_copos INTEGER DEFAULT 0
);
"""

# Carga inicial padrão (RN03)
CARGA_INICIAL = [
    ("06:00", "07:00", "🚴 Pedal Matinal"),
    ("07:00", "08:00", "☕ Café da Manhã"),
    ("09:00", "12:00", "💼 Estudos Cisco"),
    ("14:00", "17:00", "📚 Bootcamp DIO"),
    ("19:00", "22:00", "🎓 SENAI - Aulas"),
]

# Queries parametrizadas
QUERY_INSERIR_ATIVIDADE = """
INSERT INTO atividades (hora_inicio, hora_fim, descricao) 
VALUES (?, ?, ?)
"""

QUERY_LISTAR_ATIVIDADES = """
SELECT id, hora_inicio, hora_fim, descricao 
FROM atividades 
ORDER BY hora_inicio ASC
"""

QUERY_ATUALIZAR_ATIVIDADE = """
UPDATE atividades 
SET hora_inicio = ?, hora_fim = ?, descricao = ? 
WHERE id = ?
"""

QUERY_DELETAR_ATIVIDADE = "DELETE FROM atividades WHERE id = ?"

QUERY_OBTER_AGUA_HOJE = """
SELECT quantidade_copos FROM registro_saude 
WHERE data = DATE('now')
"""

QUERY_ATUALIZAR_AGUA = """
INSERT INTO registro_saude (data, quantidade_copos) 
VALUES (DATE('now'), ?) 
ON CONFLICT(data) DO UPDATE SET quantidade_copos = ?
"""