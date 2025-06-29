# Menginstal dependensi
install:
    pip install --upgrade pip &&\
    pip install -r requirements.txt

# Menjalankan skrip training
train:
    python train.py

# Evaluasi dan buat laporan
eval:
    echo "## Model Metrics" > report.md
    cat Results/metrics.txt >> report.md
    echo '\n## Confusion Matrix Plot' >> report.md
    echo '![Confusion Matrix](./Results/model_results.png)' >> report.md
    cml comment create report.md

# --- BAGIAN BARU UNTUK CI/CD ---

# Target untuk menyimpan hasil ke branch 'update' [cite: 874-885]
update-branch:
    git config --global user.name $(USER_NAME)
    git config --global user.email $(USER_EMAIL)
    git commit -am "Update with new results"
    git push --force origin HEAD:update

# Target untuk login ke Hugging Face [cite: 1150-1163]
hf-login:
    git pull origin update
    git switch update
    pip install -U "huggingface_hub[cli]"
    huggingface-cli login --token $(HF) --add-to-git-credential

# Target untuk mengunggah file [cite: 1164-1177]
push-hub:
    huggingface-cli upload ubaccount-nalendra/MLOpsDrugTest ./App --repo-type=space --commit-message="Sync App files"
    huggingface-cli upload ubaccount-nalendra/MLOpsDrugTest ./Model --repo-type=space --commit-message="Sync Model"
    huggingface-cli upload ubaccount-nalendra/MLOpsDrugTest ./Results --repo-type=space --commit-message="Sync Metrics"

# Target utama untuk deploy [cite: 1178]
deploy: hf-login push-hub