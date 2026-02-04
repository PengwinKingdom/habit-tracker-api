from datetime import date, timedelta

def format_date(date_obj: date) -> str:
    """Formatear fecha para la API (YYYY-MM-DD)"""
    return str(date_obj)

def get_date_range(days: int) -> tuple:
    """Obtener rango de fechas desde hoy hacia atrás"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def format_display_date(date_str: str) -> str:
    """Formatear fecha para mostrar al usuario (DD/MM/YYYY)"""
    try:
        date_obj = date.fromisoformat(date_str[:10])
        return date_obj.strftime("%d/%m/%Y")
    except:
        return date_str