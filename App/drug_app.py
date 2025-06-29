import gradio as gr
import skops.io as sio

# Tambahkan semua tipe yang kamu percayai secara eksplisit
trusted_types = [
    "sklearn.pipeline.Pipeline",
    "sklearn.tree.DecisionTreeClassifier",
    "numpy.dtype"
]

model_path = "Model/drug_pipeline.skops"
pipe = sio.load(model_path, trusted=trusted_types)

# Fungsi prediksi
def predict_drug(age, sex, blood_pressure, cholesterol, na_to_k_ratio):
    features = [age, sex, blood_pressure, cholesterol, na_to_k_ratio]
    predicted_drug = pipe.predict([features])[0]
    return f"Predicted Drug: {predicted_drug}"

# Input & output komponen
inputs = [
    gr.Slider(15, 74, step=1, label="Age"),
    gr.Radio(["M", "F"], label="Sex"),
    gr.Radio(["HIGH", "LOW", "NORMAL"], label="Blood Pressure"),
    gr.Radio(["HIGH", "NORMAL"], label="Cholesterol"),
    gr.Slider(6.2, 38.2, step=0.1, label="Na_to_K"),
]

outputs = gr.Label()

examples = [
    [30, "M", "HIGH", "NORMAL", 15.4],
    [35, "F", "LOW", "NORMAL", 8],
    [50, "M", "HIGH", "HIGH", 34],
]

title = "Klasifikasi Obat"
description = "Masukkan detail untuk mengidentifikasi jenis obat dengan benar."
article = "Aplikasi ini merupakan contoh CI/CD untuk Machine Learning"

# Jalankan antarmuka
gr.Interface(
    fn=predict_drug,
    inputs=inputs,
    outputs=outputs,
    examples=examples,
    title=title,
    description=description,
    article=article,
    theme=gr.themes.Soft(),
).launch()
