"""
Funções utilitárias do sistema
"""
from datetime import datetime, time
from typing import Tuple

class TimeUtils:
    """Utilitários de manipulação de tempo"""
    
    @staticmethod
    def obter_horario_atual() -> str:
        """
        Retorna horário atual no formato HH:MM
        
        Returns:
            str: Horário atual (ex: "14:35")
        """
        return datetime.now().strftime("%H:%M")
    
    @staticmethod
    def obter_data_atual() -> str:
        """
        Retorna data atual no formato YYYY-MM-DD
        
        Returns:
            str: Data atual (ex: "2025-01-23")
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def converter_para_segundos(horario: str) -> int:
        """
        Converte horário HH:MM para segundos desde meia-noite
        
        Args:
            horario: String no formato "HH:MM"
            
        Returns:
            int: Segundos desde 00:00
        """
        h, m = map(int, horario.split(':'))
        return h * 3600 + m * 60
    
    @staticmethod
    def segundos_ate_horario(horario_alvo: str) -> int:
        """
        Calcula quantos segundos faltam até um horário específico
        
        Args:
            horario_alvo: Horário no formato "HH:MM"
            
        Returns:
            int: Segundos até o horário (negativo se já passou)
        """
        agora = TimeUtils.obter_horario_atual()
        
        segundos_alvo = TimeUtils.converter_para_segundos(horario_alvo)
        segundos_agora = TimeUtils.converter_para_segundos(agora)
        
        diferenca = segundos_alvo - segundos_agora
        
        # Se o horário já passou hoje, agenda para amanhã
        if diferenca < 0:
            diferenca += 86400  # +24 horas
        
        return diferenca
    
    @staticmethod
    def formatar_duracao(hora_inicio: str, hora_fim: str) -> str:
        """
        Calcula duração entre dois horários
        
        Args:
            hora_inicio: Horário inicial (HH:MM)
            hora_fim: Horário final (HH:MM)
            
        Returns:
            str: Duração formatada (ex: "2h 30min")
        """
        seg_inicio = TimeUtils.converter_para_segundos(hora_inicio)
        seg_fim = TimeUtils.converter_para_segundos(hora_fim)
        
        duracao_seg = seg_fim - seg_inicio
        
        horas = duracao_seg // 3600
        minutos = (duracao_seg % 3600) // 60
        
        if horas > 0:
            return f"{horas}h {minutos}min"
        return f"{minutos}min"


class FormatUtils:
    """Utilitários de formatação de texto"""
    
    @staticmethod
    def formatar_horario_display(hora_inicio: str, hora_fim: str) -> str:
        """
        Formata intervalo de tempo para exibição
        
        Args:
            hora_inicio: Horário inicial
            hora_fim: Horário final
            
        Returns:
            str: Formato "HH:MM - HH:MM"
        """
        return f"{hora_inicio} - {hora_fim}"
    
    @staticmethod
    def truncar_texto(texto: str, max_chars: int = 40) -> str:
        """
        Trunca texto longo adicionando reticências
        
        Args:
            texto: Texto original
            max_chars: Número máximo de caracteres
            
        Returns:
            str: Texto truncado
        """
        if len(texto) <= max_chars:
            return texto
        return texto[:max_chars-3] + "..."