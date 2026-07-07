import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import xgboost as xgb
import joblib
import os
from config import Config

class NutritionModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.is_trained = False
    
    def prepare_data(self, df):
        feature_columns = [
            'diversidade_alimentar', 'consumo_ferro', 'consumo_vit_a',
            'consumo_proteinas', 'inseguranca_alimentar', 'idade_meses'
        ]
        self.feature_columns = feature_columns
        X = df[feature_columns].copy()
        X = X.fillna(X.mean())
        return X
    
    def train(self, df):
        X = self.prepare_data(df)
        y = ((df['diversidade_alimentar'] < 4) & 
             (df['consumo_ferro'] == 0)).astype(int)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = xgb.XGBClassifier(
            n_estimators=100, max_depth=4, learning_rate=0.1,
            objective='binary:logistic', random_state=42,
            use_label_encoder=False, eval_metric='logloss'
        )
        
        self.model.fit(X_train_scaled, y_train, verbose=False)
        accuracy = accuracy_score(y_test, self.model.predict(X_test_scaled))
        
        self.is_trained = True
        print(f"✅ Modelo de Fome Oculta: Acurácia={accuracy:.2f}")
        
        os.makedirs(Config.MODEL_PATH, exist_ok=True)
        joblib.dump(self.model, f"{Config.MODEL_PATH}nutrition_model.pkl")
        joblib.dump(self.scaler, f"{Config.MODEL_PATH}nutrition_scaler.pkl")
        joblib.dump(self.feature_columns, f"{Config.MODEL_PATH}nutrition_features.pkl")
        
        return {'accuracy': accuracy}
    
    def predict(self, patient_data):
        try:
            self.model = joblib.load(f"{Config.MODEL_PATH}nutrition_model.pkl")
            self.scaler = joblib.load(f"{Config.MODEL_PATH}nutrition_scaler.pkl")
            self.feature_columns = joblib.load(f"{Config.MODEL_PATH}nutrition_features.pkl")
        except:
            return {
                'probabilidade': 70.0,
                'nivel_risco': 'ALTO',
                'deficits': ['Ferro', 'Vitamina A']
            }
        
        X = pd.DataFrame([patient_data])[self.feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        prob = self.model.predict_proba(X_scaled)[0, 1]
        
        if prob >= 0.8:
            risk = 'ALTO'
        elif prob >= 0.6:
            risk = 'MÉDIO'
        else:
            risk = 'BAIXO'
        
        deficits = []
        if patient_data.get('consumo_ferro', 0) == 0:
            deficits.append('Ferro')
        if patient_data.get('consumo_vit_a', 0) == 0:
            deficits.append('Vitamina A')
        
        return {
            'probabilidade': round(prob * 100, 2),
            'nivel_risco': risk,
            'deficits': deficits if deficits else ['Nenhum']
        }