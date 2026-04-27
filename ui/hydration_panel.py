"""
Painel de controle de hidratação (RF07, RF08)
"""
import customtkinter as ctk
from typing import Callable


class HydrationPanel(ctk.CTkFrame):
    """Painel de acompanhamento de consumo de água"""
    
    def __init__(self, parent, on_add_copo: Callable, on_change_intervalo: Callable):
        """
        Args:
            on_add_copo: Callback executado ao clicar no botão de adicionar
            on_change_intervalo: Callback ao mudar intervalo (recebe minutos)
        """
        super().__init__(parent, fg_color="#1E1E1E", corner_radius=10)
        
        self.on_add_copo = on_add_copo
        self.on_change_intervalo = on_change_intervalo
        self.quantidade_atual = 0
        self.intervalo_atual = 15  # Padrão
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        """Monta interface do painel"""
        
        # Container principal com padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ============== TÍTULO ==============
        
        titulo = ctk.CTkLabel(
            main_container,
            text="💧 Hidratação",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4ECDC4"
        )
        titulo.pack(pady=(0, 15))
        
        # ============== DISPLAY PRINCIPAL ==============
        
        display_frame = ctk.CTkFrame(main_container, fg_color="#2B2B2B", corner_radius=10)
        display_frame.pack(fill="x", pady=(0, 15))
        
        # Ícone de copo
        icone_copo = ctk.CTkLabel(
            display_frame,
            text="🥤",
            font=ctk.CTkFont(size=60)
        )
        icone_copo.pack(pady=(20, 10))
        
        # Contador numérico
        self.label_contador = ctk.CTkLabel(
            display_frame,
            text="0",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="#4ECDC4"
        )
        self.label_contador.pack(pady=(0, 5))
        
        # Texto descritivo
        self.label_descricao = ctk.CTkLabel(
            display_frame,
            text="copos de água hoje",
            font=ctk.CTkFont(size=13),
            text_color="#A0A0A0"
        )
        self.label_descricao.pack(pady=(0, 20))
        
        # ============== BOTÃO PRINCIPAL ==============
        
        self.btn_adicionar = ctk.CTkButton(
            main_container,
            text="➕ Beber Água",
            command=self._adicionar_copo,
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#28A745",
            hover_color="#218838"
        )
        self.btn_adicionar.pack(fill="x", pady=(10, 0))
        
        # ============== SEPARADOR ==============
        
        separador = ctk.CTkFrame(main_container, height=2, fg_color="#3B3B3B")
        separador.pack(fill="x", pady=20)
        
        # ============== CONFIGURAÇÃO DE INTERVALO ==============
        
        config_frame = ctk.CTkFrame(main_container, fg_color="#2B2B2B", corner_radius=10)
        config_frame.pack(fill="x", pady=(0, 15))
        
        # Título da seção
        label_config_titulo = ctk.CTkLabel(
            config_frame,
            text="⏱️ Intervalo de Lembretes",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFA500"
        )
        label_config_titulo.pack(pady=(15, 5), padx=15, anchor="w")
        
        # Descrição
        label_config_desc = ctk.CTkLabel(
            config_frame,
            text="Tempo entre notificações",
            font=ctk.CTkFont(size=11),
            text_color="#A0A0A0"
        )
        label_config_desc.pack(pady=(0, 10), padx=15, anchor="w")
        
        # Display do intervalo atual
        self.label_intervalo_atual = ctk.CTkLabel(
            config_frame,
            text="15 minutos",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4ECDC4"
        )
        self.label_intervalo_atual.pack(pady=(5, 10))
        
        # Slider de intervalo
        slider_container = ctk.CTkFrame(config_frame, fg_color="transparent")
        slider_container.pack(fill="x", padx=15, pady=(0, 10))
        
        self.slider_intervalo = ctk.CTkSlider(
            slider_container,
            from_=5,
            to=120,
            number_of_steps=23,  # Intervalos de 5 em 5
            command=self._atualizar_intervalo_slider,
            progress_color="#4ECDC4",
            button_color="#4ECDC4",
            button_hover_color="#3DBDB4"
        )
        self.slider_intervalo.set(15)  # Valor padrão
        self.slider_intervalo.pack(fill="x", pady=(0, 5))
        
        # Labels de referência
        ref_frame = ctk.CTkFrame(slider_container, fg_color="transparent")
        ref_frame.pack(fill="x")
        
        ctk.CTkLabel(
            ref_frame,
            text="5min",
            font=ctk.CTkFont(size=9),
            text_color="#6C757D"
        ).pack(side="left")
        
        ctk.CTkLabel(
            ref_frame,
            text="120min",
            font=ctk.CTkFont(size=9),
            text_color="#6C757D"
        ).pack(side="right")
        
        # Botões rápidos
        btn_rapidos_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        btn_rapidos_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        ctk.CTkLabel(
            btn_rapidos_frame,
            text="Atalhos:",
            font=ctk.CTkFont(size=10),
            text_color="#A0A0A0"
        ).pack(side="left", padx=(0, 10))
        
        for minutos in [15, 30, 60]:
            btn = ctk.CTkButton(
                btn_rapidos_frame,
                text=f"{minutos}min",
                width=60,
                height=30,
                command=lambda m=minutos: self._definir_intervalo_rapido(m),
                fg_color="#3B3B3B",
                hover_color="#4B4B4B",
                font=ctk.CTkFont(size=11)
            )
            btn.pack(side="left", padx=2)
        
        # ============== DICA DE SAÚDE ==============
        
        info_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        info_frame.pack(fill="x", pady=(10, 0))
        
        self.label_dica = ctk.CTkLabel(
            info_frame,
            text="💡 Mantenha-se hidratado!\nBeba água regularmente.",
            font=ctk.CTkFont(size=11),
            text_color="#6C757D",
            justify="center"
        )
        self.label_dica.pack()
    
    def _adicionar_copo(self):
        """Handler do botão de adicionar (RF07)"""
        self.on_add_copo()
    
    def _atualizar_intervalo_slider(self, valor):
        """Atualiza label e notifica mudança de intervalo"""
        minutos = int(valor)
        self.intervalo_atual = minutos
        self.label_intervalo_atual.configure(text=f"{minutos} minutos")
        
        # Notifica a janela principal
        self.on_change_intervalo(minutos)
    
    def _definir_intervalo_rapido(self, minutos: int):
        """Define intervalo através dos botões rápidos"""
        self.slider_intervalo.set(minutos)
        self.intervalo_atual = minutos
        self.label_intervalo_atual.configure(text=f"{minutos} minutos")
        self.on_change_intervalo(minutos)
    
    def set_intervalo(self, minutos: int):
        """Define intervalo programaticamente (usado ao carregar)"""
        self.slider_intervalo.set(minutos)
        self.intervalo_atual = minutos
        self.label_intervalo_atual.configure(text=f"{minutos} minutos")
    
    def atualizar_display(self, quantidade: int):
        """
        Atualiza interface com nova quantidade (RF08)
        
        Args:
            quantidade: Número de copos consumidos
        """
        self.quantidade_atual = quantidade
        
        # Atualiza contador
        self.label_contador.configure(text=str(quantidade))
        
        # Mensagens motivacionais
        if quantidade == 0:
            self.label_dica.configure(text="💡 Mantenha-se hidratado!\nBeba água regularmente.")
        elif quantidade < 4:
            self.label_dica.configure(text="💪 Bom começo! Continue assim!")
        elif quantidade < 8:
            self.label_dica.configure(text="🔥 Excelente! Você está se hidratando bem!")
        else:
            self.label_dica.configure(text="🏆 Incrível! Você está super hidratado!")
    
    def resetar_dia(self):
        """
        Reseta contador para novo dia (RN01)
        Chamado automaticamente à meia-noite
        """
        self.atualizar_display(0)


class CompactHydrationWidget(ctk.CTkFrame):
    """Versão compacta do painel (para layout alternativo)"""
    
    def __init__(self, parent, on_add_copo: Callable):
        super().__init__(parent, fg_color="#2B2B2B", corner_radius=8)
        
        self.on_add_copo = on_add_copo
        self.quantidade_atual = 0
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        """Layout horizontal compacto"""
        
        # Padding interno
        self.configure(height=60)
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Ícone
        icone = ctk.CTkLabel(
            container,
            text="💧",
            font=ctk.CTkFont(size=24)
        )
        icone.pack(side="left", padx=(0, 10))
        
        # Contador
        self.label_contador = ctk.CTkLabel(
            container,
            text="0 copos",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_contador.pack(side="left", fill="x", expand=True)
        
        # Botão
        btn = ctk.CTkButton(
            container,
            text="➕",
            width=40,
            command=self.on_add_copo,
            fg_color="#28A745",
            hover_color="#218838"
        )
        btn.pack(side="right")
    
    def atualizar_display(self, quantidade: int):
        """Atualiza versão compacta"""
        self.quantidade_atual = quantidade
        
        if quantidade >= 8:
            self.label_contador.configure(
                text=f"✅ {quantidade} copos",
                text_color="#28A745"
            )
        else:
            self.label_contador.configure(
                text=f"{quantidade} copos",
                text_color="#FFFFFF"
            )