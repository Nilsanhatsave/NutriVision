import os

class Config:
    APP_NAME = "NutriVision"
    APP_VERSION = "1.0.0"
    
    MODEL_PATH = "data/trained_models/"
    ANEMIA_THRESHOLD = 11.0
    
    RISK_THRESHOLDS = {
        'anemia': {'low': 0.3, 'medium': 0.6, 'high': 0.8},
        'nutrition': {'low': 0.3, 'medium': 0.6, 'high': 0.8},
        'food_security': {'low': 0.3, 'medium': 0.6, 'high': 0.8}
    }
    
    FOOD_GROUPS = [
        'Cereais', 'Leguminosas', 'Laticínios', 'Carnes', 'Ovos',
        'Frutas', 'Verduras', 'Óleos', 'Açúcares'
    ]
    
    CROP_RECOMMENDATIONS = {
        'ferro': ['Feijão', 'Amendoim', 'Folhas verdes escuras', 'Batata-doce biofortificada'],
        'vitamina_a': ['Cenoura', 'Abóbora', 'Manga', 'Batata-doce biofortificada'],
        'zinco': ['Feijão', 'Milho', 'Arroz'],
        'proteinas': ['Feijão', 'Amendoim', 'Ovos', 'Frango']
    }