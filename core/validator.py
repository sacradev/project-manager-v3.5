"""
Sistema de validações (RN02 - Regras de Negócio)
"""
import re
from datetime import datetime
from typing import Tuple, Optional

class Validator:
    """Validador de dados de entrada"""
    
    REGEX_HORARIO = r'^([01]\d|2[0-3]):([0-5]\d)$'
    
    @staticmethod
    def validar_horario(horario: str) -> bool:
        """
        Valida se o horário está no formato HH:MM (24h)
        
        Args:
            horario: String no formato "HH:MM"
            
        Returns:
            bool: True se válido
        """
        return bool(re.match(Validator.REGEX_HORARIO, horario))
    
    @staticmethod
    def validar_intervalo(hora_inicio: str, hora_fim: str) -> Tuple[bool, str]:
        """
        Valida se o intervalo de tempo é logicamente correto
        
        Args:
            hora_inicio: Horário de início (HH:MM)
            hora_fim: Horário de fim (HH:MM)
            
        Returns:
            Tuple[bool, str]: (é_válido, mensagem_erro)
        """
        # Valida formato individual
        if not Validator.validar_horario(hora_inicio):
            return False, "❌ Horário de início inválido (use HH:MM)"
        
        if not Validator.validar_horario(hora_fim):
            return False, "❌ Horário de fim inválido (use HH:MM)"
        
        # Converte para objetos de tempo para comparação
        try:
            inicio = datetime.strptime(hora_inicio, "%H:%M")
            fim = datetime.strptime(hora_fim, "%H:%M")
        except ValueError:
            return False, "❌ Erro ao processar horários"
        
        # Valida se fim é depois do início
        if fim <= inicio:
            return False, "❌ Horário de fim deve ser posterior ao de início"
        
        return True, ""
    
    @staticmethod
    def validar_descricao(descricao: str) -> Tuple[bool, str]:
        """
        Valida se a descrição não está vazia
        
        Args:
            descricao: Texto da atividade
            
        Returns:
            Tuple[bool, str]: (é_válido, mensagem_erro)
        """
        desc_limpa = descricao.strip()
        
        if not desc_limpa:
            return False, "❌ A descrição não pode estar vazia"
        
        if len(desc_limpa) < 3:
            return False, "❌ A descrição deve ter no mínimo 3 caracteres"
        
        if len(desc_limpa) > 100:
            return False, "❌ A descrição não pode exceder 100 caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_atividade_completa(
        hora_inicio: str, 
        hora_fim: str, 
        descricao: str
    ) -> Tuple[bool, str]:
        """
        Validação completa de uma atividade (RF02 + RN02)
        
        Returns:
            Tuple[bool, str]: (é_válido, mensagem_erro)
        """
        # Valida intervalo de tempo
        valido_intervalo, msg_intervalo = Validator.validar_intervalo(
            hora_inicio, hora_fim
        )
        if not valido_intervalo:
            return False, msg_intervalo
        
        # Valida descrição
        valido_desc, msg_desc = Validator.validar_descricao(descricao)
        if not valido_desc:
            return False, msg_desc
        
        return True, "✅ Atividade válida"