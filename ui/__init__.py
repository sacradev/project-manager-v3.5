"""
Módulo de interface gráfica
Expõe componentes da UI
"""
from .main_window import MainWindow
from .dialogs import AddActivityDialog, EditActivityDialog, ConfirmDialog
from .task_list import TaskListPanel, TaskItem
from .hydration_panel import HydrationPanel, CompactHydrationWidget

__all__ = [
    'MainWindow',
    'AddActivityDialog',
    'EditActivityDialog', 
    'ConfirmDialog',
    'TaskListPanel',
    'TaskItem',
    'HydrationPanel',
    'CompactHydrationWidget'
]