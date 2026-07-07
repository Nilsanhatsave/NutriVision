class RecommendationEngine:
    def generate_lacuna_analysis(self, patient_data, community_data):
        lacunas = []
        recomendacoes = []
        
        if patient_data.get('diversidade_alimentar', 0) < 4:
            lacunas.append("Baixa diversidade alimentar")
        
        if patient_data.get('consumo_ferro', 0) == 0:
            lacunas.append("Défice de alimentos ricos em ferro")
            recomendacoes.extend(['Feijão', 'Amendoim', 'Folhas verdes'])
        
        if community_data.get('producao_leguminosas', 0) < 10:
            lacunas.append("Baixa produção de leguminosas")
            recomendacoes.append("Aumentar produção de feijão")
        
        return {
            'lacunas_identificadas': lacunas,
            'recomendacoes_agricolas': list(set(recomendacoes)),
            'nivel_prioridade': 'ALTO' if len(lacunas) >= 2 else 'MÉDIO'
        }