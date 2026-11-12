import streamlit as st


def categorize_risk(probability):
    """
    Categorize diabetes risk based on prediction probability.

    Parameters:
    probability (float): Diabetes prediction probability (0 to 1)

    Returns:
    tuple: (risk_level, color, description)
    """

    if probability < 0.30:
        return (
            "Low Risk",
            "green",
            "You are at low risk of diabetes. Maintain a healthy lifestyle."
        )

    elif 0.30 <= probability < 0.60:
        return (
            "Medium Risk",
            "orange",
            "You are at moderate risk. Consider lifestyle improvements and monitoring."
        )

    else:
        return (
            "High Risk",
            "red",
            "You are at high risk of diabetes. Medical consultation is recommended."
        )


def app(prediction_probability):
    """
    Streamlit UI for Risk Categorization Module
    """

    st.markdown("## 🩺 Diabetes Risk Categorization")

    # Ensure probability is a float
    if isinstance(prediction_probability, (list, tuple)):
        probability = float(prediction_probability[0])
    else:
        probability = float(prediction_probability)

    risk_level, color, description = categorize_risk(probability)

    st.markdown(
        f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            background-color: rgba(0,0,0,0.03);
            border-left: 6px solid {color};
        ">
            <h3 style="color:{color};">{risk_level}</h3>
            <p><strong>Prediction Confidence:</strong> {(probability * 100):.2f}%</p>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

