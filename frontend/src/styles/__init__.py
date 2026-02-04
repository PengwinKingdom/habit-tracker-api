
from pathlib import Path
import streamlit as st

def load_css_file(css_file_path: Path):
    """Cargar un archivo CSS individual"""
    if css_file_path.exists():
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_all_styles():
    """Cargar todos los archivos CSS en orden"""
    styles_dir = Path(__file__).parent
    
    # Orden de carga (importante para la cascada CSS)
    css_files = [
        # Base styles primero
        "themes/colors.css",
        "base/reset.css",
        "base/typography.css",
        "base/layout.css",
        
        # Componentes
        "components/buttons.css",
        "components/forms.css",
        "components/cards.css",
        "components/badges.css",
        "components/metrics.css",
        
        # Pages
        "pages/habits.css",
        "pages/today.css",
        "pages/analytics.css",
        
        # Theme overrides al final
        "themes/sidebar.css",
    ]
    
    for css_file in css_files:
        css_path = styles_dir / css_file
        load_css_file(css_path)

def load_page_specific_css(page_name: str):
    """Cargar CSS específico de una página"""
    styles_dir = Path(__file__).parent
    css_path = styles_dir / "pages" / f"{page_name.lower()}.css"
    load_css_file(css_path)