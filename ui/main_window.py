"""
Janela principal da aplicação - Integração completa (RNF01, RNF02, RNF03)
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional
import threading
import time

from database import DatabaseManager
from core import NotificationScheduler, TimeUtils
from .dialogs import AddActivityDialog, EditActivityDialog, ConfirmDialog
from .task_list import TaskListPanel
from .hydration_panel import HydrationPanel


class ConfigDialog(ctk.CTkToplevel):
    """Diálogo de configurações do sistema"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("⚙️ Configurações")
        self.geometry("450x280")
        self.resizable(False, False)
        
        # Centralizar
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 225
        y = (self.winfo_screenheight() // 2) - 140
        self.geometry(f"+{x}+{y}")
        
        # Modal
        self.transient(parent)
        self.grab_set()
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        """Monta interface de configurações"""
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame,
            text="⚙️ Configurações do Sistema",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4ECDC4"
        )
        titulo.pack(pady=(0, 30))
        
        # ============== SEÇÃO: STARTUP ==============
        
        section_startup = ctk.CTkFrame(main_frame, fg_color="#2B2B2B", corner_radius=10)
        section_startup.pack(fill="x", pady=(0, 20))
        
        label_startup = ctk.CTkLabel(
            section_startup,
            text="🚀 Inicialização Automática",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        )
        label_startup.pack(padx=15, pady=(15, 5), fill="x")
        
        desc_startup = ctk.CTkLabel(
            section_startup,
            text="Iniciar automaticamente com o Windows",
            font=ctk.CTkFont(size=11),
            text_color="#A0A0A0",
            anchor="w"
        )
        desc_startup.pack(padx=15, pady=(0, 10), fill="x")
        
        btn_frame_startup = ctk.CTkFrame(section_startup, fg_color="transparent")
        btn_frame_startup.pack(fill="x", padx=15, pady=(0, 15))
        
        self.btn_ativar_startup = ctk.CTkButton(
            btn_frame_startup,
            text="✅ Ativar Startup",
            command=self._ativar_startup,
            fg_color="#28A745",
            hover_color="#218838",
            height=40
        )
        self.btn_ativar_startup.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_desativar_startup = ctk.CTkButton(
            btn_frame_startup,
            text="❌ Desativar Startup",
            command=self._desativar_startup,
            fg_color="#DC3545",
            hover_color="#C82333",
            height=40
        )
        self.btn_desativar_startup.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # Status do startup
        self.label_status_startup = ctk.CTkLabel(
            section_startup,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#4ECDC4"
        )
        self.label_status_startup.pack(padx=15, pady=(0, 10))
        
        # Botão de debug (TEMPORÁRIO - para testar)
        btn_debug = ctk.CTkButton(
            section_startup,
            text="🔍 Ver Caminho Registrado",
            command=self._mostrar_caminho_debug,
            fg_color="#6C757D",
            hover_color="#5A6268",
            height=35
        )
        btn_debug.pack(fill="x", padx=15, pady=(5, 15))
        
        # ============== BOTÃO FECHAR ==============
        
        btn_fechar = ctk.CTkButton(
            main_frame,
            text="✅ Fechar",
            command=self.destroy,
            fg_color="#6C757D",
            hover_color="#5A6268",
            height=45
        )
        btn_fechar.pack(fill="x")
        
        # Verifica status inicial do startup
        self._verificar_status_startup()
    
    def _ativar_startup(self):
        """Ativa inicialização automática"""
        try:
            from startup_manager import StartupManager
            sucesso, mensagem = StartupManager.adicionar_ao_startup()
            
            if sucesso:
                self.label_status_startup.configure(
                    text="✅ Startup ativado com sucesso!",
                    text_color="#28A745"
                )
                messagebox.showinfo("Sucesso", mensagem)
            else:
                messagebox.showerror("Erro", mensagem)
                
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Falha ao ativar startup:\n{e}")
    
    def _desativar_startup(self):
        """Desativa inicialização automática"""
        try:
            from startup_manager import StartupManager
            sucesso, mensagem = StartupManager.remover_do_startup()
            
            if sucesso:
                self.label_status_startup.configure(
                    text="❌ Startup desativado",
                    text_color="#DC3545"
                )
                messagebox.showinfo("Sucesso", mensagem)
            else:
                messagebox.showerror("Erro", mensagem)
                
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Falha ao desativar startup:\n{e}")
    
    def _verificar_status_startup(self):
        """Verifica status atual do startup"""
        try:
            from startup_manager import StartupManager
            if StartupManager.verificar_startup():
                self.label_status_startup.configure(
                    text="✅ Startup está ATIVADO",
                    text_color="#28A745"
                )
            else:
                self.label_status_startup.configure(
                    text="❌ Startup está DESATIVADO",
                    text_color="#DC3545"
                )
        except:
            self.label_status_startup.configure(
                text="⚠️ Não foi possível verificar status",
                text_color="#FFA500"
            )
    
    def _mostrar_caminho_debug(self):
        """Mostra caminho registrado no startup (debug)"""
        try:
            from startup_manager import StartupManager
            caminho = StartupManager.obter_caminho_registrado()
            
            if caminho:
                messagebox.showinfo(
                    "Debug - Caminho Registrado",
                    f"📍 Caminho no registro:\n\n{caminho}\n\n"
                    f"✅ Startup está configurado"
                )
            else:
                messagebox.showinfo(
                    "Debug - Caminho Registrado",
                    "❌ Nenhum caminho registrado\n\nStartup não está ativo"
                )
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro ao verificar:\n{e}")


class MainWindow(ctk.CTk):
    """Janela principal do Project Manager v3.5"""
    
    def __init__(self):
        super().__init__()
        
        # ============== CONFIGURAÇÕES DA JANELA ==============
        self.title("Project Manager v3.5 - Sacradev")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # Tema Teal/Dark (RNF03)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Centralizar na tela
        self._centralizar_janela()
        
        # ============== INICIALIZAÇÃO DO BANCO ==============
        self.db = DatabaseManager()
        
        # ============== SCHEDULER DE NOTIFICAÇÕES ==============
        self.scheduler = NotificationScheduler(
            callback_notificacao=self._mostrar_notificacao
        )
        
        # ============== CONSTRUÇÃO DA UI ==============
        self._criar_widgets()
        
        # ============== CARREGAMENTO INICIAL ==============
        self._carregar_dados_iniciais()
        
        # ============== INICIA MONITORAMENTO ==============
        self.scheduler.iniciar()
        
        # ============== ATUALIZAÇÃO PERIÓDICA ==============
        self._iniciar_atualizacao_periodica()
        
        # ============== CLEANUP AO FECHAR ==============
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)
    
    def _centralizar_janela(self):
        """Centraliza janela na tela"""
        self.update_idletasks()
        largura = 1000
        altura = 700
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")
    
    def _criar_widgets(self):
        """Monta layout principal"""
        
        # ============== BARRA SUPERIOR ==============
        header = ctk.CTkFrame(self, height=80, fg_color="#1A1A1A", corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        # Logo/Título
        titulo_frame = ctk.CTkFrame(header, fg_color="transparent")
        titulo_frame.pack(side="left", padx=30, pady=20)
        
        titulo = ctk.CTkLabel(
            titulo_frame,
            text="⚡ Project Manager v3.5",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4ECDC4"
        )
        titulo.pack(anchor="w")
        
        subtitulo = ctk.CTkLabel(
            titulo_frame,
            text="Gestão de Rotina, Foco e Saúde",
            font=ctk.CTkFont(size=12),
            text_color="#A0A0A0"
        )
        subtitulo.pack(anchor="w")
        
        # Botão de configurações
        btn_config = ctk.CTkButton(
            header,
            text="⚙️",
            command=self._abrir_configuracoes,
            width=50,
            height=50,
            font=ctk.CTkFont(size=20),
            fg_color="#2B2B2B",
            hover_color="#3B3B3B"
        )
        btn_config.pack(side="right", padx=(0, 20))
        
        # Relógio em tempo real
        self.label_relogio = ctk.CTkLabel(
            header,
            text=TimeUtils.obter_horario_atual(),
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#4ECDC4"
        )
        self.label_relogio.pack(side="right", padx=10)
        
        # ============== CONTAINER PRINCIPAL ==============
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ============== PAINEL ESQUERDO (Lista de Tarefas) ==============
        self.task_panel = TaskListPanel(
            main_container,
            on_add=self._adicionar_atividade,
            on_edit=self._editar_atividade,
            on_delete=self._deletar_atividade
        )
        self.task_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # ============== PAINEL DIREITO (Hidratação) ==============
        self.hydration_panel = HydrationPanel(
            main_container,
            on_add_copo=self._adicionar_copo_agua,
            on_change_intervalo=self._mudar_intervalo_hidratacao
        )
        self.hydration_panel.pack(side="right", fill="y", ipadx=20, padx=(5, 0))
        
        # ============== BARRA INFERIOR (Status) ==============
        footer = ctk.CTkFrame(self, height=40, fg_color="#1A1A1A", corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        self.label_status = ctk.CTkLabel(
            footer,
            text=f"✅ Sistema iniciado | 📅 {TimeUtils.obter_data_atual()}",
            font=ctk.CTkFont(size=11),
            text_color="#A0A0A0"
        )
        self.label_status.pack(side="left", padx=20)
        
        # Autor
        autor = ctk.CTkLabel(
            footer,
            text="Desenvolvido por Sacradev 🚀",
            font=ctk.CTkFont(size=10),
            text_color="#6C757D"
        )
        autor.pack(side="right", padx=20)
    
    # ============== CONFIGURAÇÕES ==============
    
    def _abrir_configuracoes(self):
        """Abre janela de configurações"""
        dialog = ConfigDialog(self)
        self.wait_window(dialog)
    
    # ============== CARREGAMENTO DE DADOS ==============
    
    def _carregar_dados_iniciais(self):
        """Carrega dados do banco (RNF01 - Persistência)"""
        # Carrega atividades
        atividades = self.db.listar_atividades()
        self.task_panel.carregar_atividades(atividades)
        
        # Atualiza scheduler com atividades
        self.scheduler.carregar_atividades(atividades)
        
        # Carrega hidratação do dia
        quantidade_agua = self.db.obter_agua_hoje()
        self.hydration_panel.atualizar_display(quantidade_agua)
        
        self._atualizar_status(f"✅ {len(atividades)} atividades carregadas")
    
    # ============== OPERAÇÕES CRUD ==============
    
    def _adicionar_atividade(self):
        """Handler: Adicionar nova atividade (RF01)"""
        dialog = AddActivityDialog(self)
        self.wait_window(dialog)
        
        resultado = dialog.get_resultado()
        if resultado:
            hora_inicio, hora_fim, descricao = resultado
            
            sucesso = self.db.adicionar_atividade(hora_inicio, hora_fim, descricao)
            
            if sucesso:
                self._recarregar_atividades()
                self._atualizar_status(f"✅ Atividade '{descricao}' adicionada")
            else:
                messagebox.showerror(
                    "Erro",
                    "❌ Conflito de horário!\n\nJá existe uma atividade nesse período."
                )
    
    def _editar_atividade(self, atividade: tuple):
        """Handler: Editar atividade existente (RF04)"""
        dialog = EditActivityDialog(self, atividade)
        self.wait_window(dialog)
        
        resultado = dialog.get_resultado()
        if resultado:
            id_atividade, hora_inicio, hora_fim, descricao = resultado
            
            sucesso = self.db.atualizar_atividade(
                id_atividade, hora_inicio, hora_fim, descricao
            )
            
            if sucesso:
                self._recarregar_atividades()
                self._atualizar_status(f"✏️ Atividade '{descricao}' atualizada")
            else:
                messagebox.showerror(
                    "Erro",
                    "❌ Conflito de horário ao atualizar!"
                )
    
    def _deletar_atividade(self, id_atividade: int, descricao: str):
        """Handler: Deletar atividade (RF04)"""
        dialog = ConfirmDialog(
            self,
            "⚠️ Confirmar Exclusão",
            f"Deseja realmente excluir a atividade:\n\n'{descricao}'?"
        )
        self.wait_window(dialog)
        
        if dialog.get_resultado():
            self.db.deletar_atividade(id_atividade)
            self._recarregar_atividades()
            self._atualizar_status(f"🗑️ Atividade '{descricao}' removida")
    
    def _recarregar_atividades(self):
        """Recarrega lista de atividades (RF03 - Ordenação)"""
        atividades = self.db.listar_atividades()
        self.task_panel.carregar_atividades(atividades)
        self.scheduler.carregar_atividades(atividades)
    
    # ============== HIDRATAÇÃO ==============
    
    def _adicionar_copo_agua(self):
        """Handler: Adicionar copo de água (RF07, RF08)"""
        nova_quantidade = self.db.incrementar_agua()
        self.hydration_panel.atualizar_display(nova_quantidade)
        self._atualizar_status(f"💧 Água registrada ({nova_quantidade} copos)")
    
    def _mudar_intervalo_hidratacao(self, minutos: int):
        """Handler: Altera intervalo de lembretes de hidratação"""
        self.scheduler.configurar_intervalo_hidratacao(minutos)
        self._atualizar_status(f"⏱️ Intervalo ajustado para {minutos} minutos")
    
    # ============== NOTIFICAÇÕES ==============
    
    def _mostrar_notificacao(self, titulo: str, mensagem: str):
        """
        Callback do scheduler para exibir notificações (RF05, RF06)
        Thread-safe usando after()
        """
        def mostrar():
            # Cria janela de notificação
            notif = ctk.CTkToplevel(self)
            notif.title(titulo)
            notif.geometry("400x200")
            notif.resizable(False, False)
            
            # Centralizar na tela
            notif.update_idletasks()
            x = (notif.winfo_screenwidth() // 2) - 200
            y = 80
            notif.geometry(f"+{x}+{y}")
            
            # Sempre no topo e com foco
            notif.attributes("-topmost", True)
            notif.focus_force()
            
            # Efeito visual mais chamativo
            if "Hidratação" in titulo or "água" in mensagem.lower():
                cor_destaque = "#4ECDC4"
                emoji_extra = "💧"
                # Som duplo para água
                try:
                    import winsound
                    winsound.Beep(800, 200)
                    notif.after(300, lambda: winsound.Beep(1000, 200))
                except:
                    pass
            else:
                cor_destaque = "#FFA500"
                emoji_extra = "⏰"
            
            # Conteúdo
            frame = ctk.CTkFrame(notif, fg_color="#2B2B2B", border_width=3, border_color=cor_destaque)
            frame.pack(fill="both", expand=True, padx=3, pady=3)
            
            # Ícone grande
            label_icone = ctk.CTkLabel(
                frame,
                text=emoji_extra,
                font=ctk.CTkFont(size=40)
            )
            label_icone.pack(pady=(15, 5))
            
            # Título
            label_titulo = ctk.CTkLabel(
                frame,
                text=titulo,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=cor_destaque
            )
            label_titulo.pack(pady=(0, 10))
            
            # Mensagem
            label_msg = ctk.CTkLabel(
                frame,
                text=mensagem,
                font=ctk.CTkFont(size=14),
                wraplength=350
            )
            label_msg.pack(pady=(0, 15))
            
            # Botão OK
            btn_ok = ctk.CTkButton(
                frame,
                text="✅ Entendido",
                command=notif.destroy,
                fg_color=cor_destaque,
                hover_color="#3DBDB4" if "água" in mensagem.lower() else "#FF8C00",
                height=45,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            btn_ok.pack(pady=(0, 15), padx=20, fill="x")
            
            # TEMPO: 30 segundos
            notif.after(30000, notif.destroy)
        
        # Executa na thread principal
        self.after(0, mostrar)
    
    # ============== ATUALIZAÇÕES PERIÓDICAS ==============
    
    def _iniciar_atualizacao_periodica(self):
        """Inicia loop de atualização da UI (RNF02)"""
        def loop_atualizacao():
            while True:
                try:
                    # Atualiza relógio
                    self.after(0, self._atualizar_relogio)
                    
                    # Atualiza status das tarefas
                    self.after(0, self._atualizar_status_tarefas)
                    
                    # Verifica reset de dia (RN01)
                    self.after(0, self._verificar_reset_dia)
                    
                    time.sleep(30)  # Atualiza a cada 30 segundos
                    
                except Exception as e:
                    print(f"⚠️ Erro no loop de atualização: {e}")
                    time.sleep(5)
        
        thread = threading.Thread(target=loop_atualizacao, daemon=True)
        thread.start()
    
    def _atualizar_relogio(self):
        """Atualiza display do relógio"""
        self.label_relogio.configure(text=TimeUtils.obter_horario_atual())
    
    def _atualizar_status_tarefas(self):
        """Atualiza indicadores visuais das tarefas"""
        self.task_panel.atualizar_status()
    
    def _verificar_reset_dia(self):
        """Verifica se deve resetar dados do dia (RN01)"""
        if TimeUtils.obter_horario_atual() == "00:00":
            self.hydration_panel.resetar_dia()
            self._atualizar_status("🌙 Novo dia iniciado - Dados resetados")
    
    def _atualizar_status(self, mensagem: str):
        """Atualiza barra de status"""
        self.label_status.configure(text=mensagem)
    
    # ============== ENCERRAMENTO ==============
    
    def _ao_fechar(self):
        """Cleanup ao fechar aplicação"""
        self.scheduler.parar()
        self.db.fechar()
        self.destroy()