# Import semua library yang dibutuhkan
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import skops.io as sio

# 1. Muat Dataset
drug_df = pd.read_csv("Data/drug200.csv")
drug_df = drug_df.sample(frac=1)

# 2. Pisahkan Data
X = drug_df.drop("Drug", axis=1).values
y = drug_df.Drug.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=125)

# 3. Bangun Pipeline
cat_col = [1, 2, 3]
num_col = [0, 4]
transform = ColumnTransformer([
    ("num_imputer", SimpleImputer(strategy="median"), num_col),
    ("encoder", OrdinalEncoder(), cat_col),
    ("num_scaler", StandardScaler(), num_col),
])
pipe = Pipeline(
    steps=[
        ("preprocessing", transform),
        ("model", RandomForestClassifier(n_estimators=100, random_state=125)),
    ]
)
pipe.fit(X_train, y_train)

# 4. Evaluasi
predictions = pipe.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
f1 = f1_score(y_test, predictions, average="macro")
print("Accuracy:", str(round(accuracy, 2) * 100) + "%", "F1:", round(f1, 2))

# 5. Simpan Hasil
with open("Results/metrics.txt", "w") as outfile:
    outfile.write(f"Accuracy: {round(accuracy, 2)}, F1 Score = {round(f1,2)}.")

cm = confusion_matrix(y_test, predictions, labels=pipe.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=pipe.classes_)
disp.plot()
plt.savefig("Results/model_results.png", dpi=120)

# 6. Simpan Model
sio.dump(pipe, "Model/drug_pipeline.skops")
print("Training, evaluation, and saving artifacts complete.")