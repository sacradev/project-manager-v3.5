# 📑 Project Manager v3.5

> Sistema de Gestão de Rotina, Foco e Saúde

![Python](https://img.shields.io/badge/Python-3.13-blue)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2-teal)
![SQLite](https://img.shields.io/badge/SQLite-3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Visão Geral

O **Project Manager v3.5** é uma aplicação desktop desenvolvida para auxiliar no controle diário de atividades e saúde. Diferente de scripts voláteis, utiliza um banco de dados local (SQLite) para persistir configurações, garantindo que sua rotina permaneça inalterada até que você decida modificá-la.

### **Características Principais:**
- ✅ **Gestão de Atividades** com horários definidos
- ✅ **Notificações Automáticas** de início de tarefas
- ✅ **Controle de Hidratação** com lembretes configuráveis
- ✅ **Interface Moderna** (Tema Teal/Dark)
- ✅ **Persistência Total** de dados

---

## 🛠️ Stack Tecnológica

- **Python 3.13** - Linguagem base
- **CustomTkinter** - Interface gráfica moderna
- **SQLite3** - Banco de dados local
- **Threading** - Sistema assíncrono de notificações

---

## 📋 Contrato de Especificação Técnica

Este projeto foi desenvolvido seguindo um **contrato técnico rigoroso**, documentando:
- Requisitos Funcionais (RF01-RF08)
- Requisitos Não Funcionais (RNF01-RNF03)
- Regras de Negócio (RN01-RN03)


---

## 🚀 Como Usar

### **Opção 1: Executável (Recomendado)**

### **Opção 2: Código Fonte**
```
# Baixe ProjectManager.exe
# Execute com duplo clique
# 1. Clone o repositório
git clone https://github.com/sacradev/project-manager.git
cd project-manager

# 2. Instale dependências
pip install -r requirements.txt

# 3. Execute
python main.py
```

## 📖 Funcionalidades Detalhadas]

1. Gestão de Atividades
- Adicione tarefas com horário de início, fim e descrição
- Edite ou delete atividades existentes
- Visualização cronológica automática
- Indicação visual de tarefas em andamento
2. Sistema de Notificações
- Alertas automáticos no horário exato de cada tarefa
- Som do sistema + popup visual
- Notificações de hidratação em intervalos configuráveis
3. Controle de Hidratação
- Contador de copos de água
- Intervalo de lembretes ajustável (5-120 minutos)
- Mensagens motivacionais por progresso
- Reset automático à meia-noite

## 🏗️ Arquitetura

```
project-manager/
│
├── main.py              # Ponto de entrada
├── database/            # Camada de dados (SQLite)
├── core/                # Lógica de negócio
├── ui/                  # Interface gráfica
└── rotina.db            # Banco de dados

```

### Princípios Aplicados:

- Separação de responsabilidades
- Padrão MVC adaptado
- Threading para operações assíncronas

# 🧪 Compilação

Para gerar o executável:
```
python build_exe.py
```
O arquivo ProjectManager.exe será criado em dist/.

# 📄 Licença

MIT License - Sinta-se livre para usar e modificar.

# 🙏 Agradecimentos

Projeto desenvolvido durante estudos de:

- Análise e Desenvolvimento de Sistemas
- Cisco CCNA
- Bootcamp DIO
- Técnico SENAI 2026


### 📊 Evolução Técnica
Este projeto marca um marco importante no meu desenvolvimento:

- Antes: Ideias brutas sem documentação
- Agora: Contratos técnicos + UML + Especificação completa