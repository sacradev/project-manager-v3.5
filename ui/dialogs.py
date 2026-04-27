"""
Janelas de diálogo para CRUD de atividades (RF01, RF04)
"""
import customtkinter as ctk
from typing import Optional, Tuple, Callable
from core import Validator


class BaseDialog(ctk.CTkToplevel):
    """Classe base para diálogos modais"""
    
    def __init__(self, parent, title: str, width: int = 450, height: int = 400):
        super().__init__(parent)
        
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        
        # Centralizar na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Modal
        self.transient(parent)
        self.grab_set()
        
        self.resultado: Optional[Tuple] = None
    
    def get_resultado(self):
        """Retorna resultado do diálogo"""
        return self.resultado


class AddActivityDialog(BaseDialog):
    """Diálogo para adicionar nova atividade (RF01)"""
    
    def __init__(self, parent):
        super().__init__(parent, "➕ Nova Atividade", width=500, height=450)
        
        self._criar_widgets()
        
        # Foco no primeiro campo
        self.after(100, lambda: self.entry_hora_inicio.focus())
    
    def _criar_widgets(self):
        """Monta formulário"""
        
        # Frame principal com padding
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame,
            text="📝 Cadastrar Nova Atividade",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4ECDC4"
        )
        titulo.pack(pady=(0, 25))
        
        # Campo: Hora de Início
        label_inicio = ctk.CTkLabel(
            main_frame, 
            text="🕐 Horário de Início:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label_inicio.pack(fill="x", pady=(0, 5))
        
        self.entry_hora_inicio = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ex: 14:30",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entry_hora_inicio.pack(fill="x", pady=(0, 20))
        
        # Campo: Hora de Fim
        label_fim = ctk.CTkLabel(
            main_frame, 
            text="🕐 Horário de Término:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label_fim.pack(fill="x", pady=(0, 5))
        
        self.entry_hora_fim = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ex: 16:00",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entry_hora_fim.pack(fill="x", pady=(0, 20))
        
        # Campo: Descrição
        label_desc = ctk.CTkLabel(
            main_frame, 
            text="📄 Descrição da Atividade:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label_desc.pack(fill="x", pady=(0, 5))
        
        self.entry_descricao = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ex: Estudar Python Avançado",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entry_descricao.pack(fill="x", pady=(0, 20))
        
        # Label de erro (inicialmente vazio)
        self.label_erro = ctk.CTkLabel(
            main_frame,
            text="",
            text_color="#FF6B6B",
            font=ctk.CTkFont(size=12),
            wraplength=450
        )
        self.label_erro.pack(pady=(0, 15))
        
        # Frame de botões
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        # Botão Cancelar
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=self._cancelar,
            fg_color="#6C757D",
            hover_color="#5A6268",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_cancelar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botão Salvar
        btn_salvar = ctk.CTkButton(
            btn_frame,
            text="✅ Salvar Atividade",
            command=self._salvar,
            fg_color="#28A745",
            hover_color="#218838",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_salvar.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        # Atalhos de teclado
        self.bind("<Return>", lambda e: self._salvar())
        self.bind("<Escape>", lambda e: self._cancelar())
    
    def _salvar(self):
        """Valida e retorna dados (RN02)"""
        hora_inicio = self.entry_hora_inicio.get().strip()
        hora_fim = self.entry_hora_fim.get().strip()
        descricao = self.entry_descricao.get().strip()
        
        # Validação completa
        valido, mensagem = Validator.validar_atividade_completa(
            hora_inicio, hora_fim, descricao
        )
        
        if not valido:
            self.label_erro.configure(text=mensagem)
            # Piscar o label de erro
            self.label_erro.configure(text_color="#FF4444")
            self.after(100, lambda: self.label_erro.configure(text_color="#FF6B6B"))
            return
        
        self.resultado = (hora_inicio, hora_fim, descricao)
        self.destroy()
    
    def _cancelar(self):
        """Fecha sem salvar"""
        self.resultado = None
        self.destroy()


class EditActivityDialog(BaseDialog):
    """Diálogo para editar atividade existente (RF04)"""
    
    def __init__(self, parent, atividade: Tuple):
        """
        Args:
            atividade: Tupla (id, hora_inicio, hora_fim, descricao)
        """
        super().__init__(parent, "✏️ Editar Atividade", width=500, height=450)
        
        self.id_atividade = atividade[0]
        self.dados_originais = atividade[1:]
        
        self._criar_widgets()
        self._preencher_campos()
    
    def _criar_widgets(self):
        """Monta formulário"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        titulo = ctk.CTkLabel(
            main_frame,
            text="✏️ Editar Atividade",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFA500"
        )
        titulo.pack(pady=(0, 25))
        
        # Campo: Hora de Início
        ctk.CTkLabel(
            main_frame, 
            text="🕐 Horário de Início:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.entry_hora_inicio = ctk.CTkEntry(
            main_frame,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entry_hora_inicio.pack(fill="x", pady=(0, 20))
        
        # Campo: Hora de Fim
        ctk.CTkLabel(
            main_frame, 
            text="🕐 Horário de Término:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.entry_hora_fim = ctk.CTkEntry(
            main_frame,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entry_hora_fim.pack(fill="x", pady=(0, 20))
        
        # Campo: Descrição
        ctk.CTkLabel(
            main_frame, 
            text="📄 Descrição da Atividade:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.entry_descricao = ctk.CTkEntry(
            main_frame,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entry_descricao.pack(fill="x", pady=(0, 20))
        
        self.label_erro = ctk.CTkLabel(
            main_frame,
            text="",
            text_color="#FF6B6B",
            font=ctk.CTkFont(size=12),
            wraplength=450
        )
        self.label_erro.pack(pady=(0, 15))
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=self._cancelar,
            fg_color="#6C757D",
            hover_color="#5A6268",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_cancelar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_salvar = ctk.CTkButton(
            btn_frame,
            text="💾 Atualizar",
            command=self._salvar,
            fg_color="#FFA500",
            hover_color="#FF8C00",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_salvar.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        self.bind("<Return>", lambda e: self._salvar())
        self.bind("<Escape>", lambda e: self._cancelar())
    
    def _preencher_campos(self):
        """Carrega dados existentes"""
        hora_inicio, hora_fim, descricao = self.dados_originais
        
        self.entry_hora_inicio.insert(0, hora_inicio)
        self.entry_hora_fim.insert(0, hora_fim)
        self.entry_descricao.insert(0, descricao)
        
        # Foco no primeiro campo
        self.after(100, lambda: self.entry_hora_inicio.focus())
    
    def _salvar(self):
        """Valida e retorna dados atualizados"""
        hora_inicio = self.entry_hora_inicio.get().strip()
        hora_fim = self.entry_hora_fim.get().strip()
        descricao = self.entry_descricao.get().strip()
        
        valido, mensagem = Validator.validar_atividade_completa(
            hora_inicio, hora_fim, descricao
        )
        
        if not valido:
            self.label_erro.configure(text=mensagem)
            return
        
        self.resultado = (self.id_atividade, hora_inicio, hora_fim, descricao)
        self.destroy()
    
    def _cancelar(self):
        self.resultado = None
        self.destroy()


class ConfirmDialog(BaseDialog):
    """Diálogo de confirmação genérico"""
    
    def __init__(self, parent, titulo: str, mensagem: str):
        super().__init__(parent, titulo, width=400, height=200)
        
        self._criar_widgets(mensagem)
    
    def _criar_widgets(self, mensagem: str):
        """Monta diálogo de confirmação"""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        label = ctk.CTkLabel(
            main_frame,
            text=mensagem,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        label.pack(pady=30, expand=True)
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        btn_nao = ctk.CTkButton(
            btn_frame,
            text="❌ Não",
            command=self._nao,
            fg_color="#6C757D",
            hover_color="#5A6268",
            height=40,
            width=150
        )
        btn_nao.pack(side="left", expand=True, padx=5)
        
        btn_sim = ctk.CTkButton(
            btn_frame,
            text="✅ Sim",
            command=self._sim,
            fg_color="#DC3545",
            hover_color="#C82333",
            height=40,
            width=150
        )
        btn_sim.pack(side="right", expand=True, padx=5)
        
        self.bind("<Return>", lambda e: self._sim())
        self.bind("<Escape>", lambda e: self._nao())
    
    def _sim(self):
        self.resultado = True
        self.destroy()
    
    def _nao(self):
        self.resultado = False
        self.destroy()