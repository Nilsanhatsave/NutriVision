import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
import xgboost as xgb
import joblib
import os
from config import Config

class AnemiaModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.is_trained = False
    
    def prepare_data(self, df):
        feature_columns = [
            'idade_meses', 'peso_kg', 'altura_cm', 'muac_mm',
            'diversidade_alimentar', 'consumo_ferro', 'febre', 'diarreia',
            'suplementacao_ferro', 'suplementacao_vit_a', 'inseguranca_alimentar'
        ]
        self.feature_columns = feature_columns
        X = df[feature_columns].copy()
        X = X.fillna(X.mean())
        for col in ['febre', 'diarreia', 'suplementacao_ferro', 
                    'suplementacao_vit_a', 'inseguranca_alimentar']:
            if col in X.columns:
                X[col] = X[col].astype(int)
        return X
    
    def train(self, df):
        X = self.prepare_data(df)
        # Usar MUAC e diversidade alimentar como proxy para anemia
        y = ((df['muac_mm'] < 125) | (df['diversidade_alimentar'] < 4)).astype(int)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            objective='binary:logistic',
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss'
        )
        
        self.model.fit(X_train_scaled, y_train, verbose=False)
        
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, self.model.predict_proba(X_test_scaled)[:, 1])
        
        self.is_trained = True
        print(f"✅ Modelo de Anemia: Acurácia={accuracy:.2f}, AUC={auc:.2f}")
        
        os.makedirs(Config.MODEL_PATH, exist_ok=True)
        joblib.dump(self.model, f"{Config.MODEL_PATH}anemia_model.pkl")
        joblib.dump(self.scaler, f"{Config.MODEL_PATH}anemia_scaler.pkl")
        joblib.dump(self.feature_columns, f"{Config.MODEL_PATH}anemia_features.pkl")
        
        return {'accuracy': accuracy, 'auc': auc}
    
    def predict(self, patient_data):
        try:
            self.model = joblib.load(f"{Config.MODEL_PATH}anemia_model.pkl")
            self.scaler = joblib.load(f"{Config.MODEL_PATH}anemia_scaler.pkl")
            self.feature_columns = joblib.load(f"{Config.MODEL_PATH}anemia_features.pkl")
        except:
            # Fallback: avaliação baseada em regras simples
            risco = "BAIXO"
            prob = 0.2
            
            if patient_data.get('muac_mm', 0) < 125:
                risco = "ALTO"
                prob = 0.85
            elif patient_data.get('diversidade_alimentar', 0) < 4:
                risco = "MÉDIO"
                prob = 0.65
            elif patient_data.get('consumo_ferro', 0) == 0:
                risco = "MÉDIO"
                prob = 0.55
            
            return {
                'probabilidade': prob * 100,
                'nivel_risco': risco,
                'recomendacao': 'Encaminhar para médico' if risco == 'ALTO' else 'Manter acompanhamento'
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
        
        return {
            'probabilidade': round(prob * 100, 2),
            'nivel_risco': risk,
            'recomendacao': 'Encaminhar para médico' if risk == 'ALTO' else 'Manter acompanhamento'
        }