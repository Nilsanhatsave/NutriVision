import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import xgboost as xgb
import joblib
import os
from config import Config

class FoodSecurityModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.is_trained = False
    
    def prepare_data(self, df):
        feature_columns = [
            'producao_total', 'diversidade_agricola', 'producao_leguminosas',
            'producao_hortalicas', 'preco_alimentos', 'precipitacao',
            'temperatura', 'seca_frequencia', 'duracao_epoca'
        ]
        self.feature_columns = feature_columns
        X = df[feature_columns].copy()
        X = X.fillna(X.mean())
        return X
    
    def train(self, df):
        X = self.prepare_data(df)
        y = df['inseguranca_alimentar'].astype(int)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = xgb.XGBClassifier(
            n_estimators=100, max_depth=5, learning_rate=0.1,
            objective='binary:logistic', random_state=42,
            use_label_encoder=False, eval_metric='logloss'
        )
        
        self.model.fit(X_train_scaled, y_train, verbose=False)
        accuracy = accuracy_score(y_test, self.model.predict(X_test_scaled))
        
        self.is_trained = True
        print(f"✅ Modelo de Insegurança Alimentar: Acurácia={accuracy:.2f}")
        
        os.makedirs(Config.MODEL_PATH, exist_ok=True)
        joblib.dump(self.model, f"{Config.MODEL_PATH}food_security_model.pkl")
        joblib.dump(self.scaler, f"{Config.MODEL_PATH}food_security_scaler.pkl")
        joblib.dump(self.feature_columns, f"{Config.MODEL_PATH}food_security_features.pkl")
        
        return {'accuracy': accuracy}
    
    def predict(self, community_data):
        try:
            self.model = joblib.load(f"{Config.MODEL_PATH}food_security_model.pkl")
            self.scaler = joblib.load(f"{Config.MODEL_PATH}food_security_scaler.pkl")
            self.feature_columns = joblib.load(f"{Config.MODEL_PATH}food_security_features.pkl")
        except:
            return {
                'probabilidade': 65.0,
                'nivel_risco': 'MÉDIO',
                'risco_climatico': 'MÉDIO'
            }
        
        X = pd.DataFrame([community_data])[self.feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        prob = self.model.predict_proba(X_scaled)[0, 1]
        
        if prob >= 0.8:
            risk = 'ALTO'
        elif prob >= 0.6:
            risk = 'MÉDIO'
        else:
            risk = 'BAIXO'
        
        climate = 'ALTO' if community_data.get('seca_frequencia', 0) > 2 else 'MÉDIO' if community_data.get('seca_frequencia', 0) > 0 else 'BAIXO'
        
        return {
            'probabilidade': round(prob * 100, 2),
            'nivel_risco': risk,
            'risco_climatico': climate
        }