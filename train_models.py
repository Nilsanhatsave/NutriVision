import pandas as pd
import numpy as np
from models.anemia_model import AnemiaModel
from models.nutrition_model import NutritionModel
from models.food_security_model import FoodSecurityModel
import os

def generate_sample_data(n=500):
    np.random.seed(42)
    
    data = {
        'idade_meses': np.random.randint(0, 60, n),
        'peso_kg': np.random.normal(10, 2, n),
        'altura_cm': np.random.normal(85, 10, n),
        'muac_mm': np.random.normal(140, 15, n),
        'hemoglobina': np.random.normal(11.5, 1.5, n),
        'febre': np.random.choice([0, 1], n, p=[0.8, 0.2]),
        'diarreia': np.random.choice([0, 1], n, p=[0.85, 0.15]),
        'diversidade_alimentar': np.random.randint(1, 9, n),
        'consumo_ferro': np.random.choice([0, 1], n, p=[0.4, 0.6]),
        'consumo_vit_a': np.random.choice([0, 1], n, p=[0.45, 0.55]),
        'consumo_proteinas': np.random.choice([0, 1], n, p=[0.35, 0.65]),
        'suplementacao_ferro': np.random.choice([0, 1], n, p=[0.5, 0.5]),
        'suplementacao_vit_a': np.random.choice([0, 1], n, p=[0.5, 0.5]),
        'producao_leguminosas': np.random.normal(10, 5, n),
        'producao_hortalicas': np.random.normal(20, 10, n),
        'diversidade_agricola': np.random.randint(1, 8, n),
        'producao_total': np.random.normal(1000, 300, n),
        'preco_alimentos': np.random.normal(50, 15, n),
        'precipitacao': np.random.normal(700, 200, n),
        'temperatura': np.random.normal(28, 3, n),
        'seca_frequencia': np.random.poisson(2, n),
        'duracao_epoca': np.random.normal(120, 20, n),
        'inseguranca_alimentar': np.random.choice([0, 1], n, p=[0.6, 0.4]),
        'disponibilidade_alimentos': np.random.normal(50, 15, n)
    }
    
    # Corrigir relação com MUAC e diversidade
    idx = (data['muac_mm'] < 125) | (data['diversidade_alimentar'] < 4)
    data['hemoglobina'][idx] = np.random.normal(9.5, 1.0, sum(idx))
    
    return pd.DataFrame(data)

def main():
    print("=" * 60)
    print("🌿 NutriVision - Treinamento de Modelos")
    print("=" * 60)
    
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/trained_models', exist_ok=True)
    
    print("\n📊 Gerando dados de exemplo...")
    df = generate_sample_data(800)
    df.to_csv('data/sample_data.csv', index=False)
    print(f"   {len(df)} registos gerados")
    
    print("\n" + "=" * 60)
    AnemiaModel().train(df)
    
    print("\n" + "=" * 60)
    NutritionModel().train(df)
    
    print("\n" + "=" * 60)
    FoodSecurityModel().train(df)
    
    print("\n" + "=" * 60)
    print("✅ TREINAMENTO CONCLUÍDO!")
    print("=" * 60)

if __name__ == "__main__":
    main()