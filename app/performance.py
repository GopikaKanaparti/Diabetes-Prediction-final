import streamlit as st
from function.function import make_donut

# ---------------------------------
# Stored model performance metrics
# (From train_compare_models.py)
# ---------------------------------
ACCURACY = 75.32
PRECISION = 64.81
RECALL = 64.81
F1_SCORE = 64.81
ROC_AUC = 75.10


def app():
    st.markdown("### 📊 Model Performance (XGBoost)")

    cols = st.columns(5)
    color = "blue"

    # Accuracy
    cols[0].markdown("**Accuracy**\n\nOverall correct predictions.")
    cols[0].altair_chart(
        make_donut(
            ACCURACY,
            "Accuracy",
            input_color=color,
            R=140,
            innerRadius=40,
            cornerRadius=10
        )
    )

    # F1 Score
    cols[1].markdown("**F1 Score**\n\nBalance between Precision & Recall.")
    cols[1].altair_chart(
        make_donut(
            F1_SCORE,
            "F1 Score",
            input_color=color,
            R=140,
            innerRadius=40,
            cornerRadius=10
        )
    )

    # Recall
    cols[2].markdown("**Recall**\n\nAbility to detect diabetic patients.")
    cols[2].altair_chart(
        make_donut(
            RECALL,
            "Recall",
            input_color=color,
            R=140,
            innerRadius=40,
            cornerRadius=10
        )
    )

    # Precision
    cols[3].markdown("**Precision**\n\nCorrectness of positive predictions.")
    cols[3].altair_chart(
        make_donut(
            PRECISION,
            "Precision",
            input_color=color,
            R=140,
            innerRadius=40,
            cornerRadius=10
        )
    )

    # ROC AUC
    cols[4].markdown("**ROC-AUC**\n\nClass separation capability.")
    cols[4].altair_chart(
        make_donut(
            ROC_AUC,
            "ROC-AUC",
            input_color=color,
            R=140,
            innerRadius=40,
            cornerRadius=10
        )
    )

    st.info(
        "Metrics were computed on the test dataset. "
        "XGBoost achieved the best overall performance and was selected."
    )
