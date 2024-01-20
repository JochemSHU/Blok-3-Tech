from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Lees de dataset in
df = pd.read_csv('Benchpress_Progressie2022.csv')

# Onnodige kolommen verwijderen
df.drop(['birthdate', 'exercise', 'date_of_workout', 'id'], axis=1, inplace=True)

# Vervang 'm' door 1 en 'f' door 0 in de kolom 'Geslacht'
df['gender'] = df['gender'].replace({' m': 1, ' f': 0})

# Itereer over alle kolommen in de dataset
for col in df.columns:
    # Controleer of de kolom een datatype 'object' heeft (tekst)
    if df[col].dtype == 'O':
        # Verwijder spaties uit de tekst in de kolom
        df[col] = df[col].str.replace(' ', '')

# Selecteer de relevante kolommen
features = ['months_of_experience', 'gender', 'weight_kg_rep_1', 'weight_kg_rep_2', 'weight_kg_rep_3', 'weight_kg']
target = 'reps'

# Data splitsen in x en y
y = df[target]
x = df[features]

# Data splitsen in trainings- en testsets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=100)

# Normaliseer de gegevens met StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Haal de feature namen op die zijn gebruikt tijdens het trainen
feature_names = X_train.columns

# Model bouwen met Ridge regressie (lineaire regressie met regularisatie)
lr = Ridge(alpha=0.1)
lr.fit(X_train_scaled, y_train)

# Model bouwen met random forest regressie
rf = RandomForestRegressor(max_depth=5, n_estimators=100, random_state=100)
rf.fit(X_train_scaled, y_train)

# Vraag input aan de gebruiker
months_of_experience = int(input("Voer het aantal maanden ervaring in: "))
gender = int(input("Voer het geslacht in (1 voor man, 0 voor vrouw): "))
weight_kg_rep_1 = float(input("Voer het gewicht voor set 1 in (kg): "))
reps_rep_1 = int(input("Voer het aantal herhalingen voor set 1 in: "))
weight_kg_rep_2 = float(input("Voer het gewicht voor set 2 in (kg): "))
reps_rep_2 = int(input("Voer het aantal herhalingen voor set 2 in: "))
weight_kg_rep_3 = float(input("Voer het gewicht voor set 3 in (kg): "))
reps_rep_3 = int(input("Voer het aantal herhalingen voor set 3 in: "))
weight_kg = float(input("Wat is je lichaamsgewicht(kg): "))

# Vraag aan de gebruiker welk gewicht hij wil voorspellen
Predict = float(input("Voer het gewicht in waarvoor je het aantal herhalingen wilt voorspellen: "))

# Voorspellingen maken voor gebruiker
user_data = {
    'months_of_experience': months_of_experience,
    'gender': gender,
    'weight_kg_rep_1': weight_kg_rep_1,
    'reps_rep_1': reps_rep_1,
    'weight_kg_rep_2': weight_kg_rep_2,
    'reps_rep_2': reps_rep_2,
    'weight_kg_rep_3': weight_kg_rep_3,
    'reps_rep_3': reps_rep_3,
    'weight_kg': weight_kg,
}

# Voeg het specifieke gewicht toe aan de user_data
user_data['Predict_Weight'] = Predict

user_df = pd.DataFrame([user_data], columns=feature_names)

# Voer preprocessing uit op de user input
user_df_scaled = scaler.transform(user_df)

# Voorspel het aantal herhalingen met het Ridge regressiemodel
user_lr_pred = lr.predict(user_df_scaled)
print(f"Voorspeld aantal herhalingen (Ridge Regressie): {user_lr_pred[0]}")

# Voorspel het aantal herhalingen met het random forest model
user_rf_pred = rf.predict(user_df_scaled)
print(f"Voorspeld aantal herhalingen (Random Forest): {user_rf_pred[0]}")

# Voorspellingen maken voor trainings- en testdatasets
y_lr_train_pred = lr.predict(X_train_scaled)
y_lr_test_pred = lr.predict(X_test_scaled)

y_rf_train_pred = rf.predict(X_train_scaled)
y_rf_test_pred = rf.predict(X_test_scaled)

# Bereken MSE en R2 voor Ridge regressie op zowel trainings- als testdatasets
lr_train_mse = mean_squared_error(y_train, y_lr_train_pred)
lr_train_r2 = r2_score(y_train, y_lr_train_pred)

lr_test_mse = mean_squared_error(y_test, y_lr_test_pred)
lr_test_r2 = r2_score(y_test, y_lr_test_pred)

# Bereken MSE en R2 voor random forest op zowel trainings- als testdatasets
rf_train_mse = mean_squared_error(y_train, y_rf_train_pred)
rf_train_r2 = r2_score(y_train, y_rf_train_pred)

rf_test_mse = mean_squared_error(y_test, y_rf_test_pred)
rf_test_r2 = r2_score(y_test, y_rf_test_pred)

# Print de resultaten
print('Ridge Regression MSE (Train): ', lr_train_mse)
print('Ridge Regression R2 (Train): ', lr_train_r2)
print('Ridge Regression MSE (Test): ', lr_test_mse)
print('Ridge Regression R2 (Test): ', lr_test_r2)

print('Random Forest MSE (Train): ', rf_train_mse)
print('Random Forest R2 (Train): ', rf_train_r2)
print('Random Forest MSE (Test): ', rf_test_mse)
print('Random Forest R2 (Test): ', rf_test_r2)


# Bereken de lineaire regressielijn
z = np.polyfit(y_train, y_lr_train_pred, 1)
p = np.poly1d(z)

# Scatterplot met regressielijn
plt.figure(figsize=(5, 5))
plt.scatter(x=y_train, y=y_lr_train_pred, c="#7CAE00", alpha=0.3)
plt.plot(y_train, p(y_train), '#F8766D')

plt.ylabel('Predicted Repetitions')
plt.xlabel('Actual Repetitions')
plt.title('Linear Regression - Training Data')
plt.show()
