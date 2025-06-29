# Target untuk menginstal dependensi
install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

# Target untuk menjalankan skrip training
train:
	python train.py

# Target untuk evaluasi dan buat laporan
eval:
	echo "## Model Metrics" > report.md
	cat Results/metrics.txt >> report.md
	echo '\n## Confusion Matrix Plot' >> report.md
	echo '![Confusion Matrix](./Results/model_results.png)' >> report.md
	cml comment create report.md

# Target untuk menyimpan hasil ke branch 'update'
update-branch:
	git config --global user.name $(USER_NAME)
	git config --global user.email $(USER_EMAIL)
	git commit -am "Update with new results"
	git push --force origin HEAD:update

# Target untuk login ke Hugging Face
hf-login:
	git pull origin update
	git switch update
	pip install -U "huggingface_hub[cli]"
	huggingface-cli login --token $(HF) --add-to-git-credential

# Target untuk mengunggah file
push-hub:
	huggingface-cli upload ubaccount-nalendra/MLOpsDrugTest ./App --repo-type=space --commit-message="Sync App files"
	huggingface-cli upload ubaccount-nalendra/MLOpsDrugTest ./Model --repo-type=space --commit-message="Sync Model"
	huggingface-cli upload ubaccount-nalendra/MLOpsDrugTest ./Results --repo-type=space --commit-message="Sync Metrics"

# Target utama untuk deploy
deploy:
	make hf-login
	make push-hub