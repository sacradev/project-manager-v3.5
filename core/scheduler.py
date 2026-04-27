"""
Sistema de notificações e monitoramento de horários (RF05, RF06)
Usa threading para não bloquear a interface
"""
import threading
import time
import winsound
from datetime import datetime
from typing import Callable, List, Tuple, Optional
from .utils import TimeUtils


class NotificationScheduler:
    """Gerenciador de notificações baseado em tempo"""
    
    def __init__(self, callback_notificacao: Callable[[str, str], None]):
        """
        Args:
            callback_notificacao: Função que exibe popup (titulo, mensagem)
        """
        self.callback_notificacao = callback_notificacao
        self.atividades_monitoradas: List[Tuple[int, str, str]] = []
        self.atividades_notificadas: set = set()
        
        self._thread_monitor: Optional[threading.Thread] = None
        self._thread_hidratacao: Optional[threading.Thread] = None
        self._rodando = False
        
        # Configurações
        self.intervalo_hidratacao = 900  # 15 minutos em segundos (RF06)
        self.frequencia_checagem = 30  # Verifica a cada 30 segundos
    
    def carregar_atividades(self, atividades: List[Tuple]):
        """
        Atualiza lista de atividades a serem monitoradas
        
        Args:
            atividades: Lista de tuplas (id, hora_inicio, hora_fim, descricao)
        """
        self.atividades_monitoradas = atividades
        self.atividades_notificadas.clear()  # Reset ao recarregar
    
    def iniciar(self):
        """Inicia threads de monitoramento (RNF02)"""
        if self._rodando:
            return
        
        self._rodando = True
        
        # Thread 1: Monitor de atividades (RF05)
        self._thread_monitor = threading.Thread(
            target=self._monitorar_atividades,
            daemon=True
        )
        self._thread_monitor.start()
        
        # Thread 2: Lembrete de hidratação (RF06)
        self._thread_hidratacao = threading.Thread(
            target=self._monitorar_hidratacao,
            daemon=True
        )
        self._thread_hidratacao.start()
        
        print("🔔 Scheduler iniciado")
    
    def parar(self):
        """Para todos os monitores"""
        self._rodando = False
        print("🔕 Scheduler parado")
    
    def _monitorar_atividades(self):
        """
        Loop de verificação de horários (RF05)
        Roda em thread separada
        """
        while self._rodando:
            try:
                horario_atual = TimeUtils.obter_horario_atual()
                
                for atividade in self.atividades_monitoradas:
                    id_atividade, hora_inicio, hora_fim, descricao = atividade
                    
                    # Verifica se chegou a hora E ainda não notificou
                    if hora_inicio == horario_atual and id_atividade not in self.atividades_notificadas:
                        self._disparar_notificacao_atividade(descricao, hora_inicio, hora_fim)
                        self.atividades_notificadas.add(id_atividade)
                
                # Reseta notificações à meia-noite (RN01)
                if horario_atual == "00:00":
                    self.atividades_notificadas.clear()
                
                time.sleep(self.frequencia_checagem)
                
            except Exception as e:
                print(f"⚠️ Erro no monitor de atividades: {e}")
                time.sleep(5)
    
    def _monitorar_hidratacao(self):
        """
        Loop de lembrete de hidratação (RF06)
        Roda em thread separada
        """
        while self._rodando:
            try:
                time.sleep(self.intervalo_hidratacao)
                
                if self._rodando:  # Verifica novamente após sleep longo
                    self._disparar_notificacao_agua()
                
            except Exception as e:
                print(f"⚠️ Erro no monitor de hidratação: {e}")
                time.sleep(60)
    
    def _disparar_notificacao_atividade(self, descricao: str, hora_inicio: str, hora_fim: str):
        """
        Dispara popup + som para atividade (RF05)
        
        Args:
            descricao: Nome da atividade
            hora_inicio: Horário de início
            hora_fim: Horário de término
        """
        titulo = "⏰ Hora da Atividade!"
        mensagem = f"{descricao}\n\n🕐 {hora_inicio} - {hora_fim}"
        
        # Toca som do sistema
        self._tocar_som_alerta()
        
        # Chama callback da UI (será implementado na interface)
        self.callback_notificacao(titulo, mensagem)
        
        print(f"🔔 Notificação disparada: {descricao}")
    
    def _disparar_notificacao_agua(self):
        """
        Dispara lembrete de hidratação (RF06)
        """
        titulo = "💧 Lembrete de Hidratação"
        mensagem = "Hora de beber água!\n\nMantenha-se hidratado 😊"
        
        self._tocar_som_alerta()
        self.callback_notificacao(titulo, mensagem)
        
        print("💧 Lembrete de água disparado")
    
    def _tocar_som_alerta(self):
        """
        Reproduz som de notificação do Windows
        """
        try:
            # Som padrão do sistema (Windows)
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except Exception as e:
            print(f"⚠️ Não foi possível tocar som: {e}")
    
    def configurar_intervalo_hidratacao(self, minutos: int):
        """
        Permite ajustar intervalo de lembretes de água
        
        Args:
            minutos: Intervalo em minutos (padrão: 15)
        """
        self.intervalo_hidratacao = minutos * 60
        print(f"⏲️ Intervalo de hidratação ajustado para {minutos} minutos")


class TaskChecker:
    """Utilitário para verificar status de tarefas"""
    
    @staticmethod
    def tarefa_em_andamento(hora_inicio: str, hora_fim: str) -> bool:
        """
        Verifica se uma tarefa está acontecendo agora
        
        Args:
            hora_inicio: Horário de início (HH:MM)
            hora_fim: Horário de fim (HH:MM)
            
        Returns:
            bool: True se estiver no período da tarefa
        """
        agora = TimeUtils.converter_para_segundos(TimeUtils.obter_horario_atual())
        inicio = TimeUtils.converter_para_segundos(hora_inicio)
        fim = TimeUtils.converter_para_segundos(hora_fim)
        
        return inicio <= agora < fim
    
    @staticmethod
    def tarefa_concluida(hora_fim: str) -> bool:
        """
        Verifica se uma tarefa já passou
        
        Args:
            hora_fim: Horário de fim (HH:MM)
            
        Returns:
            bool: True se já passou do horário
        """
        agora = TimeUtils.converter_para_segundos(TimeUtils.obter_horario_atual())
        fim = TimeUtils.converter_para_segundos(hora_fim)
        
        return agora >= fim