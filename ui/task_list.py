"""
Componente de lista de atividades com CRUD visual (RF03, RF04)
"""
import customtkinter as ctk
from typing import List, Tuple, Callable, Optional
from core import TimeUtils, FormatUtils, TaskChecker


class TaskItem(ctk.CTkFrame):
    """Item individual de atividade na lista"""
    
    def __init__(
        self, 
        parent, 
        atividade: Tuple,
        on_edit: Callable,
        on_delete: Callable
    ):
        """
        Args:
            atividade: (id, hora_inicio, hora_fim, descricao)
            on_edit: Callback para edição
            on_delete: Callback para exclusão
        """
        super().__init__(parent, fg_color="#2B2B2B", corner_radius=8)
        
        self.atividade = atividade
        self.id_atividade = atividade[0]
        self.hora_inicio = atividade[1]
        self.hora_fim = atividade[2]
        self.descricao = atividade[3]
        
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self._criar_widgets()
        self._atualizar_status()
    
    def _criar_widgets(self):
        """Monta layout do item"""
        
        # Container principal com padding
        self.configure(height=70)
        self.pack_propagate(False)
        
        # Frame esquerdo: Checkbox + Horários + Descrição
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        # Checkbox de conclusão
        self.checkbox = ctk.CTkCheckBox(
            left_frame,
            text="",
            width=20,
            checkbox_width=20,
            checkbox_height=20
        )
        self.checkbox.pack(side="left", padx=(0, 15))
        
        # Frame de informações
        info_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Linha 1: Horários
        horario_texto = FormatUtils.formatar_horario_display(
            self.hora_inicio, self.hora_fim
        )
        duracao = TimeUtils.formatar_duracao(self.hora_inicio, self.hora_fim)
        
        self.label_horario = ctk.CTkLabel(
            info_frame,
            text=f"🕐 {horario_texto} ({duracao})",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4ECDC4",
            anchor="w"
        )
        self.label_horario.pack(fill="x")
        
        # Linha 2: Descrição
        self.label_descricao = ctk.CTkLabel(
            info_frame,
            text=self.descricao,
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.label_descricao.pack(fill="x", pady=(3, 0))
        
        # Frame direito: Botões de ação
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)
        
        # Botão Editar
        btn_editar = ctk.CTkButton(
            btn_frame,
            text="✏️",
            width=40,
            height=40,
            command=self._editar,
            fg_color="#FFA500",
            hover_color="#FF8C00"
        )
        btn_editar.pack(side="left", padx=3)
        
        # Botão Deletar
        btn_deletar = ctk.CTkButton(
            btn_frame,
            text="🗑️",
            width=40,
            height=40,
            command=self._deletar,
            fg_color="#DC3545",
            hover_color="#C82333"
        )
        btn_deletar.pack(side="left", padx=3)
    
    def _atualizar_status(self):
        """Atualiza aparência baseado no status da tarefa"""
        
        if TaskChecker.tarefa_concluida(self.hora_fim):
            # Tarefa já passou
            self.label_horario.configure(text_color="#6C757D")
            self.label_descricao.configure(text_color="#6C757D")
            
        elif TaskChecker.tarefa_em_andamento(self.hora_inicio, self.hora_fim):
            # Tarefa em andamento
            self.configure(border_color="#4ECDC4", border_width=2)
            self.label_descricao.configure(text_color="#4ECDC4")
    
    def _editar(self):
        """Dispara callback de edição"""
        self.on_edit(self.atividade)
    
    def _deletar(self):
        """Dispara callback de exclusão"""
        self.on_delete(self.id_atividade, self.descricao)


class TaskListPanel(ctk.CTkFrame):
    """Painel completo de listagem de atividades"""
    
    def __init__(
        self, 
        parent,
        on_add: Callable,
        on_edit: Callable,
        on_delete: Callable
    ):
        super().__init__(parent, fg_color="#1E1E1E", corner_radius=10)
        
        self.on_add = on_add
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        """Monta estrutura do painel"""
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        header_frame.pack_propagate(False)
        
        # Título
        titulo = ctk.CTkLabel(
            header_frame,
            text="📋 Atividades do Dia",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4ECDC4"
        )
        titulo.pack(side="left")
        
        # Botão Adicionar
        btn_add = ctk.CTkButton(
            header_frame,
            text="➕ Nova Atividade",
            command=self.on_add,
            height=40,
            fg_color="#28A745",
            hover_color="#218838"
        )
        btn_add.pack(side="right")
        
        # Separador
        separador = ctk.CTkFrame(self, height=2, fg_color="#4ECDC4")
        separador.pack(fill="x", padx=15)
        
        # Frame scrollável para lista
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="#4ECDC4",
            scrollbar_button_hover_color="#3DBDB4"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    def carregar_atividades(self, atividades: List[Tuple]):
        """
        Renderiza lista de atividades (RF03 - ordenação automática)
        
        Args:
            atividades: Lista de tuplas (id, hora_inicio, hora_fim, descricao)
        """
        # Limpa lista atual
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not atividades:
            # Mensagem de lista vazia
            label_vazio = ctk.CTkLabel(
                self.scrollable_frame,
                text="📭 Nenhuma atividade cadastrada\n\nClique em '➕ Nova Atividade' para começar",
                font=ctk.CTkFont(size=14),
                text_color="#6C757D"
            )
            label_vazio.pack(pady=50)
            return
        
        # Renderiza cada atividade
        for atividade in atividades:
            item = TaskItem(
                self.scrollable_frame,
                atividade,
                on_edit=self.on_edit,
                on_delete=self.on_delete
            )
            item.pack(fill="x", pady=5)
    
    def atualizar_status(self):
        """
        Atualiza status visual das tarefas (chamado periodicamente)
        """
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, TaskItem):
                widget._atualizar_status()