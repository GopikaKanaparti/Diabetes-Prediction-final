import streamlit as st
import pandas as pd
import io
import re
try:
    from PyPDF2 import PdfReader
    PDF_READER_AVAILABLE = True
except Exception:
    PdfReader = None
    PDF_READER_AVAILABLE = False


def _normalize_columns(cols):
    return [c.strip().lower().replace(' ', '_') for c in cols]


def app():
    st.sidebar.header("Input Parameters")

    uploaded_file = st.sidebar.file_uploader(
        "Upload report (CSV / Excel / JSON / PDF)", type=["csv", "xlsx", "xls", "json", "pdf"]
    )

    required = ['pregnancies', 'glucose', 'insulin', 'bmi', 'age']

    if uploaded_file is not None:
        try:
            if uploaded_file.name.lower().endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.lower().endswith('.json'):
                df = pd.read_json(uploaded_file)
            elif uploaded_file.name.lower().endswith('.pdf'):
                if not PDF_READER_AVAILABLE:
                    raise ImportError('PyPDF2 is not installed')

                # parse PDF text and extract required fields
                def parse_pdf_for_fields(uploaded):
                    raw = uploaded.read()
                    reader = PdfReader(io.BytesIO(raw))
                    text = []
                    for page in reader.pages:
                        try:
                            page_text = page.extract_text() or ""
                        except Exception:
                            page_text = ""
                        text.append(page_text)
                    full = "\n".join(text).lower()

                    patterns = {
                        'pregnancies': r'pregnanc(?:y|ies)[:\s]*([0-9]+(?:\.[0-9]+)?)',
                        'glucose': r'glucose[:\s]*([0-9]+(?:\.[0-9]+)?)',
                        'insulin': r'insulin[:\s]*([0-9]+(?:\.[0-9]+)?)',
                        'bmi': r'bm[iI][:\s]*([0-9]+(?:\.[0-9]+)?)',
                        'age': r'age[:\s]*([0-9]+(?:\.[0-9]+)?)',
                    }

                    results = {}
                    for key, pat in patterns.items():
                        m = re.search(pat, full, flags=re.IGNORECASE)
                        if m:
                            results[key] = m.group(1)
                        else:
                            keypat = rf'{key}[^\d\n\r\-]{{0,20}}([0-9]+(?:\.[0-9]+)?)'
                            m2 = re.search(keypat, full, flags=re.IGNORECASE)
                            if m2:
                                results[key] = m2.group(1)
                    return results

                parsed = parse_pdf_for_fields(uploaded_file)
                if parsed and all(k in parsed for k in required):
                    df = pd.DataFrame([{ 
                        'Pregnancies': float(parsed['pregnancies']),
                        'Glucose': float(parsed['glucose']),
                        'Insulin': float(parsed['insulin']),
                        'BMI': float(parsed['bmi']),
                        'Age': float(parsed['age']),
                    }])
                else:
                    raise ValueError('PDF missing required fields')
            else:
                df = pd.read_excel(uploaded_file)

            cols_norm = _normalize_columns(df.columns)
            mapping = {}
            for r in required:
                if r in cols_norm:
                    mapping[r] = df.columns[cols_norm.index(r)]

            if all(k in mapping for k in required):
                df_selected = df[[mapping[c] for c in required]].copy()
                df_selected.columns = ['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age']
                st.sidebar.success("Report loaded — using uploaded values for prediction.")
                st.sidebar.markdown('---')
                return df_selected.iloc[[0]].reset_index(drop=True)
            else:
                st.sidebar.error(
                    "Uploaded file is missing required columns. Falling back to manual input."
                )
        except Exception as e:
            st.sidebar.error(f"Could not read uploaded file: {e}. Falling back to manual input.")

    # Manual inputs (fallback)
    pregnancies_value = st.sidebar.number_input(
        'Enter value for `Pregnancies`',
        min_value=0,
        max_value=20,
        value=1
    )

    glucose_value = st.sidebar.number_input(
        'Enter value for `Glucose`',
        min_value=0,
        max_value=250,
        value=100
    )

    insulin_value = st.sidebar.number_input(
        'Enter value for `Insulin`',
        min_value=0,
        max_value=1000,
        value=100
    )

    bmi_value = st.sidebar.number_input(
        'Enter value for `BMI`',
        min_value=0.0,
        max_value=100.0,
        value=37.0,
        format="%.1f"
    )

    age_value = st.sidebar.number_input(
        'Enter value for `Age`',
        min_value=0,
        max_value=100,
        value=25
    )

    st.sidebar.markdown('---')
    return pd.DataFrame([[pregnancies_value, glucose_value, insulin_value, bmi_value, age_value]],
                        columns=['Pregnancies', 'Glucose', 'Insulin', 'BMI', 'Age'])