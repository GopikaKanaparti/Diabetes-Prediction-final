import numpy as np

def explain_prediction(model, feature_names, input_data=None, top_k=5):
    """
    Generates feature-based explanation for a prediction.

    Parameters:
    model : trained ML model
    feature_names : list of feature names
    input_data : optional, not required for importance-based explanation
    top_k : number of top features to return

    Returns:
    dict : sorted feature importance explanation
    """

    # Detect model type and extract importance
    if hasattr(model, 'coef_'):  
        # Logistic Regression
        importance = np.abs(model.coef_[0])

    elif hasattr(model, 'feature_importances_'):  
        # Tree-based models
        importance = model.feature_importances_

    else:
        return {
            "Error": "Explainability not supported for this model type"
        }

    # Normalize importance values
    importance = importance / np.sum(importance)

    # Map features to importance scores
    explanation = {
        feature: round(score * 100, 2)
        for feature, score in zip(feature_names, importance)
    }

    # Sort features by importance (descending)
    explanation = dict(
        sorted(explanation.items(), key=lambda x: x[1], reverse=True)
    )

    # Return only top-k features
    return dict(list(explanation.items())[:top_k])
