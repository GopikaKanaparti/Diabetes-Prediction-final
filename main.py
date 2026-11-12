import streamlit as st
from loader import page_icon
from function.function import *

# ---------------------------------
# Page configuration
# ---------------------------------
st.set_page_config(
    page_title="Diabetes Prediction with AI",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------
# Header
# ---------------------------------
from app.header import app as header_app
header_app()

# ---------------------------------
# Input Section
# ---------------------------------
from app.input import app as input_app
input_data = input_app()

# ---------------------------------
# Prediction Section
# ---------------------------------
from app.predict import app as predict_app
prediction = predict_app(input_data)   # 🔑 capture probability

# ---------------------------------
# Explainability Section (POINT 3)
# ---------------------------------
from app.explainer import app as explainer_app
explainer_app(input_data)

# ---------------------------------
# Risk Categorization Section (POINT 4)
# ---------------------------------
from app.risk_categorization import app as risk_app
risk_app(prediction)

from app.recommendation import app as recommendation_app
recommendation_app(prediction)

# ---------------------------------
# Model Performance
# ---------------------------------
from app.performance import app as performance_app
performance_app()

# ---------------------------------
# Permutation Importance
# ---------------------------------
from app.perm_importance import app as perm_importance_app
perm_importance_app()

# ---------------------------------
# About Section
# ---------------------------------
#from app.about import app as about_app
#about_app()
