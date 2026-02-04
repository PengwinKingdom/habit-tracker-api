import requests
import streamlit as st
from typing import Optional, Dict, Any, List

class HabitTrackerAPI:
    """Cliente para la API de Habit Tracker"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[Any, Any]]:
        """Realizar petición a la API con manejo de errores"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.request(method, url, **kwargs, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timeout - El servidor no responde")
            return None
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection error - Verifica que el backend esté corriendo")
            return None
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ HTTP Error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            return None
    
    def get_habits(self, user_id: int):
        """Obtener todos los hábitos de un usuario"""
        data=self._make_request("GET",f"/users/{user_id}/habits")
        
        if data is None:
            return[]

        #backend devuelve  {"user_id": 1, "habits": [ ... ]}
        if isinstance(data, dict) and "habits" in data and isinstance(data["habits"], list):
            data = data["habits"]
        
        if not isinstance(data, list):
            return []

        normalized=[]
        for h in data:
            if not isinstance(h,dict):
                continue
            
            habit_id = h.get("HabitId") or h.get("habit_id") or h.get("id")
            title = h.get("Title") or h.get("title") or h.get("name")
            description = h.get("Description") or h.get("description") or ""
            is_active = h.get("IsActive") if "IsActive" in h else h.get("is_active", True)
            created_at = h.get("CreatedAt") or h.get("created_at")

            normalized.append({
                **h,
                "id": habit_id,
                "title":title,
                "description": description,
                "is_active": is_active,
                "created_at": created_at
                })

        return normalized
    

    def create_habit(self, user_id: int, title: str, description: str):
        """Crear un nuevo hábito"""
        return self._make_request("POST", f"/users/{user_id}/habits", json={
            "title": title,
            "description": description
        })
    
    def get_habit_logs(self, habit_id: int, days: int = 7) -> Optional[List[Dict]]:
        return self._make_request("GET", f"/habits/{habit_id}/logs?days={days}")

    def create_log(self, habit_id: int, log_date: str, completed: bool, notes: str = ""):
        return self._make_request("POST", f"/habits/{habit_id}/logs", json={
            "log_date": log_date,
            "completed": completed,
            "notes": notes
            })

    def update_log(self, habit_id: int, log_id: int, completed: bool, notes: str = ""):
        return self._make_request("PUT", f"/habits/{habit_id}/logs/{log_id}", json={
            "completed": completed,
            "notes": notes
            })

    
    def get_analytics(self, user_id: int, days: int = 7) -> Optional[List[Dict]]:
        return self._make_request("GET", f"/users/{user_id}/analytics/completion?days={days}")
    
    def health_check(self) -> bool:
        result = self._make_request("GET", "/openapi.json")
        return result is not None

    def upsert_log(self, habit_id:int,log_date:str,completed:bool,notes:str=""):
        return self._make_request(
            "PUT",
            f"/habits/{habit_id}/logs/{log_date}",
            json={"completed":completed,"notes":notes}
        )