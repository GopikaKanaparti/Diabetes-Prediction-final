import streamlit as st


def get_recommendations(risk_level):
    """
    Returns prevention and precaution recommendations
    based on diabetes risk level.
    """

    if risk_level == "Low Risk":
        return [
            "Maintain a balanced diet with limited sugar intake.",
            "Engage in regular physical activity (30 minutes daily).",
            "Monitor body weight and maintain a healthy BMI.",
            "Undergo routine health checkups annually."
        ]

    elif risk_level == "Medium Risk":
        return [
            "Reduce consumption of refined carbohydrates and sugary foods.",
            "Increase physical activity to at least 45 minutes daily.",
            "Monitor blood glucose levels periodically.",
            "Maintain healthy body weight and reduce stress.",
            "Consult a healthcare professional if symptoms appear."
        ]

    else:  # High Risk
        return [
            "Consult a physician or diabetologist immediately.",
            "Follow a medically prescribed diet plan.",
            "Monitor blood glucose levels regularly.",
            "Avoid sugary beverages and processed foods.",
            "Adopt a strict exercise and weight-management routine."
        ]


def app(prediction_probability):
    """
    Streamlit UI for Prevention & Recommendation Module
    """

    st.markdown("## 🛡️ Prevention & Precaution Recommendations")

    # Ensure probability is a float
    if isinstance(prediction_probability, (list, tuple)):
        probability = float(prediction_probability[0])
    else:
        probability = float(prediction_probability)

    # Determine risk level (same logic as Point 4)
    if probability < 0.30:
        risk_level = "Low Risk"
        color = "green"
    elif 0.30 <= probability < 0.60:
        risk_level = "Medium Risk"
        color = "orange"
    else:
        risk_level = "High Risk"
        color = "red"

    recommendations = get_recommendations(risk_level)

    st.markdown(
        f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            border-left: 6px solid {color};
            background-color: rgba(0,0,0,0.03);
        ">
            <h3 style="color:{color};">{risk_level} – Recommended Actions</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    for rec in recommendations:
        st.write(f"✔ {rec}")
