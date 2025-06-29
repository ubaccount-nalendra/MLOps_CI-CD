# Menginstal semua dependensi
install:
    pip install --upgrade pip &&\
    pip install -r requirements.txt

# Memformat kode
format:
    pip install black
    black *.py

# Menjalankan skrip training
train:
    python train.py

# Perintah untuk evaluasi
eval:
    echo "## Model Metrics" > report.md
    cat Results/metrics.txt >> report.md
    echo '\n## Confusion Matrix Plot' >> report.md
    echo '![Confusion Matrix](./Results/model_results.png)' >> report.md
    # cml comment create report.md # Baris ini dinonaktifkan untuk lokal