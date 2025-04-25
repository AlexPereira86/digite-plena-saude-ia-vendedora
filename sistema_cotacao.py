"""
Sistema de Cotação para Planos de Saúde da Plena Saúde
Implementação detalhada para cálculo de valores de planos nas regiões de Francisco Morato, Caieiras e Perus
"""

class SistemaCotacaoPlena:
    def __init__(self):
        # Tabela de preços por faixa etária para planos individuais/familiares
        # Valores fictícios baseados em médias de mercado (devem ser substituídos pelos valores reais)
        self.tabela_precos_individual = {
            # Faixa etária: valor base
            "0-18": 120.00,
            "19-23": 150.00,
            "24-28": 180.00,
            "29-33": 210.00,
            "34-38": 240.00,
            "39-43": 270.00,
            "44-48": 320.00,
            "49-53": 380.00,
            "54-58": 450.00,
            "59+": 550.00
        }
        
        # Tabela de preços para planos empresariais (PME)
        # Valores por vida, variando conforme quantidade de vidas
        self.tabela_precos_empresarial = {
            # Faixa de vidas: {faixa etária: valor}
            "2-9": {
                "0-18": 100.00,
                "19-23": 130.00,
                "24-28": 160.00,
                "29-33": 190.00,
                "34-38": 220.00,
                "39-43": 250.00,
                "44-48": 290.00,
                "49-53": 340.00,
                "54-58": 410.00,
                "59+": 500.00
            },
            "10-29": {
                "0-18": 90.00,
                "19-23": 120.00,
                "24-28": 150.00,
                "29-33": 180.00,
                "34-38": 210.00,
                "39-43": 240.00,
                "44-48": 280.00,
                "49-53": 330.00,
                "54-58": 390.00,
                "59+": 480.00
            },
            "30+": {
                "0-18": 80.00,
                "19-23": 110.00,
                "24-28": 140.00,
                "29-33": 170.00,
                "34-38": 200.00,
                "39-43": 230.00,
                "44-48": 270.00,
                "49-53": 320.00,
                "54-58": 380.00,
                "59+": 460.00
            }
        }
        
        # Fatores de ajuste para diferentes tipos de planos
        self.fatores_plano = {
            "basico": 1.0,
            "intermediario": 1.3,
            "completo": 1.6
        }
        
        # Fatores de ajuste para coparticipação
        self.fatores_coparticipacao = {
            "sem": 1.0,
            "com": 0.8  # 20% de desconto para planos com coparticipação
        }
        
        # Hospitais disponíveis por região
        self.hospitais_por_regiao = {
            "Francisco Morato": ["Hospital Previna Francisco Morato", "Hospital Municipal de Francisco Morato"],
            "Caieiras": ["Hospital Previna Caieiras", "Hospital Municipal de Caieiras"],
            "Perus": ["Hospital Previna Perus", "Hospital Municipal Dr. Moyses Deutsch"]
        }
        
        # Hospitais premium (com adicional de valor)
        self.hospitais_premium = {
            "Hospital Previna Premium": 1.15,  # 15% adicional
            "Hospital São Camilo": 1.25,       # 25% adicional
            "Hospital Samaritano": 1.30        # 30% adicional
        }
    
    def obter_faixa_etaria(self, idade):
        """Determina a faixa etária com base na idade"""
        if idade <= 18:
            return "0-18"
        elif idade <= 23:
            return "19-23"
        elif idade <= 28:
            return "24-28"
        elif idade <= 33:
            return "29-33"
        elif idade <= 38:
            return "34-38"
        elif idade <= 43:
            return "39-43"
        elif idade <= 48:
            return "44-48"
        elif idade <= 53:
            return "49-53"
        elif idade <= 58:
            return "54-58"
        else:
            return "59+"
    
    def obter_faixa_vidas(self, quantidade_vidas):
        """Determina a faixa de quantidade de vidas para planos empresariais"""
        if quantidade_vidas < 10:
            return "2-9"
        elif quantidade_vidas < 30:
            return "10-29"
        else:
            return "30+"
    
    def calcular_valor_individual(self, idade, tipo_plano="intermediario", coparticipacao="sem", hospital_premium=None):
        """Calcula o valor para um beneficiário individual"""
        faixa_etaria = self.obter_faixa_etaria(idade)
        valor_base = self.tabela_precos_individual[faixa_etaria]
        
        # Aplicar fator do tipo de plano
        valor = valor_base * self.fatores_plano[tipo_plano]
        
        # Aplicar fator de coparticipação
        valor = valor * self.fatores_coparticipacao[coparticipacao]
        
        # Aplicar adicional de hospital premium, se aplicável
        if hospital_premium and hospital_premium in self.hospitais_premium:
            valor = valor * self.hospitais_premium[hospital_premium]
        
        return round(valor, 2)
    
    def calcular_valor_familiar(self, idades, tipo_plano="intermediario", coparticipacao="sem", hospital_premium=None):
        """Calcula o valor para um plano familiar com múltiplos beneficiários"""
        valor_total = 0
        
        # Calcular valor individual para cada beneficiário
        for idade in idades:
            valor_total += self.calcular_valor_individual(idade, tipo_plano, coparticipacao, hospital_premium)
        
        # Aplicar desconto para planos familiares (5% para 3+ vidas, 10% para 5+ vidas)
        if len(idades) >= 5:
            valor_total = valor_total * 0.9  # 10% de desconto
        elif len(idades) >= 3:
            valor_total = valor_total * 0.95  # 5% de desconto
        
        return round(valor_total, 2)
    
    def calcular_valor_empresarial(self, idades, tipo_plano="intermediario", coparticipacao="com", hospital_premium=None):
        """Calcula o valor para um plano empresarial com múltiplos beneficiários"""
        valor_total = 0
        quantidade_vidas = len(idades)
        faixa_vidas = self.obter_faixa_vidas(quantidade_vidas)
        
        # Calcular valor para cada beneficiário com base na tabela empresarial
        for idade in idades:
            faixa_etaria = self.obter_faixa_etaria(idade)
            valor_base = self.tabela_precos_empresarial[faixa_vidas][faixa_etaria]
            
            # Aplicar fator do tipo de plano
            valor = valor_base * self.fatores_plano[tipo_plano]
            
            # Aplicar fator de coparticipação
            valor = valor * self.fatores_coparticipacao[coparticipacao]
            
            # Adicionar ao valor total
            valor_total += valor
        
        # Aplicar adicional de hospital premium, se aplicável
        if hospital_premium and hospital_premium in self.hospitais_premium:
            valor_total = valor_total * self.hospitais_premium[hospital_premium]
        
        return round(valor_total, 2)
    
    def gerar_cotacao(self, tipo_plano_contrato, idades, tipo_cobertura="intermediario", 
                     coparticipacao="sem", hospital_premium=None):
        """Gera uma cotação completa com base nos parâmetros fornecidos"""
        
        if tipo_plano_contrato == "individual" and len(idades) == 1:
            valor = self.calcular_valor_individual(idades[0], tipo_cobertura, coparticipacao, hospital_premium)
            tipo_texto = "Individual"
        elif tipo_plano_contrato in ["individual", "familiar"]:
            valor = self.calcular_valor_familiar(idades, tipo_cobertura, coparticipacao, hospital_premium)
            tipo_texto = "Familiar" if len(idades) > 1 else "Individual"
        elif tipo_plano_contrato == "empresarial":
            valor = self.calcular_valor_empresarial(idades, tipo_cobertura, coparticipacao, hospital_premium)
            tipo_texto = "Empresarial/PME"
        else:
            return {"erro": "Tipo de plano inválido"}
        
        # Determinar nome do plano com base no tipo de cobertura
        nome_plano = {
            "basico": "Plena Essencial",
            "intermediario": "Plena Plus",
            "completo": "Plena Premium"
        }.get(tipo_cobertura, "Plena Plus")
        
        # Determinar texto de coparticipação
        texto_coparticipacao = "Com Coparticipação" if coparticipacao == "com" else "Sem Coparticipação"
        
        # Construir resposta da cotação
        cotacao = {
            "tipo_plano": tipo_texto,
            "nome_plano": nome_plano,
            "coparticipacao": texto_coparticipacao,
            "quantidade_vidas": len(idades),
            "valor_mensal": valor,
            "hospital_premium": hospital_premium if hospital_premium else "Rede padrão Plena Saúde",
            "cobertura": self.obter_cobertura(tipo_cobertura)
        }
        
        return cotacao
    
    def obter_cobertura(self, tipo_cobertura):
        """Retorna a descrição da cobertura com base no tipo de plano"""
        coberturas = {
            "basico": [
                "Consultas em clínicas básicas",
                "Exames de rotina",
                "Internações em enfermaria",
                "Urgência e emergência",
                "Cobertura nos Hospitais Previna"
            ],
            "intermediario": [
                "Consultas em todas as especialidades",
                "Exames simples e complexos",
                "Internações em enfermaria",
                "Cirurgias",
                "Urgência e emergência",
                "Cobertura nos Hospitais Previna e rede credenciada"
            ],
            "completo": [
                "Consultas em todas as especialidades",
                "Exames simples e complexos",
                "Internações em apartamento privativo",
                "Cirurgias de alta complexidade",
                "Urgência e emergência",
                "Cobertura nos Hospitais Previna, rede credenciada e hospitais premium",
                "Reembolso para procedimentos fora da rede"
            ]
        }
        
        return coberturas.get(tipo_cobertura, coberturas["intermediario"])
    
    def listar_hospitais_regiao(self, regiao):
        """Lista os hospitais disponíveis em uma determinada região"""
        if regiao in self.hospitais_por_regiao:
            return self.hospitais_por_regiao[regiao]
        else:
            regioes_disponiveis = list(self.hospitais_por_regiao.keys())
            return f"Região não encontrada. Regiões disponíveis: {', '.join(regioes_disponiveis)}"


# Exemplo de uso do sistema de cotação
if __name__ == "__main__":
    sistema = SistemaCotacaoPlena()
    
    # Exemplo 1: Cotação individual
    print("Exemplo 1: Cotação Individual")
    cotacao_individual = sistema.gerar_cotacao("individual", [35], "intermediario", "sem")
    print(f"Plano: {cotacao_individual['nome_plano']} ({cotacao_individual['tipo_plano']})")
    print(f"Valor mensal: R$ {cotacao_individual['valor_mensal']:.2f}")
    print(f"Coparticipação: {cotacao_individual['coparticipacao']}")
    print("Cobertura:")
    for item in cotacao_individual['cobertura']:
        print(f"- {item}")
    print("-" * 50)
    
    # Exemplo 2: Cotação familiar
    print("Exemplo 2: Cotação Familiar (3 vidas)")
    cotacao_familiar = sistema.gerar_cotacao("familiar", [35, 32, 5], "completo", "com")
    print(f"Plano: {cotacao_familiar['nome_plano']} ({cotacao_familiar['tipo_plano']})")
    print(f"Valor mensal: R$ {cotacao_familiar['valor_mensal']:.2f}")
    print(f"Coparticipação: {cotacao_familiar['coparticipacao']}")
    print("Cobertura:")
    for item in cotacao_familiar['cobertura']:
        print(f"- {item}")
    print("-" * 50)
    
    # Exemplo 3: Cotação empresarial
    print("Exemplo 3: Cotação Empresarial (15 vidas)")
    idades_empresa = [25, 30, 35, 40, 45, 28, 32, 37, 42, 47, 29, 34, 39, 44, 49]
    cotacao_empresarial = sistema.gerar_cotacao("empresarial", idades_empresa, "intermediario", "com")
    print(f"Plano: {cotacao_empresarial['nome_plano']} ({cotacao_empresarial['tipo_plano']})")
    print(f"Valor mensal: R$ {cotacao_empresarial['valor_mensal']:.2f}")
    print(f"Coparticipação: {cotacao_empresarial['coparticipacao']}")
    print("Cobertura:")
    for item in cotacao_empresarial['cobertura']:
        print(f"- {item}")
    print("-" * 50)
    
    # Exemplo 4: Cotação com hospital premium
    print("Exemplo 4: Cotação com Hospital Premium")
    cotacao_premium = sistema.gerar_cotacao("familiar", [40, 38, 10, 8], "completo", "sem", "Hospital São Camilo")
    print(f"Plano: {cotacao_premium['nome_plano']} ({cotacao_premium['tipo_plano']})")
    print(f"Valor mensal: R$ {cotacao_premium['valor_mensal']:.2f}")
    print(f"Hospital: {cotacao_premium['hospital_premium']}")
    print(f"Coparticipação: {cotacao_premium['coparticipacao']}")
    print("Cobertura:")
    for item in cotacao_premium['cobertura']:
        print(f"- {item}")
    print("-" * 50)
    
    # Exemplo 5: Listar hospitais por região
    print("Exemplo 5: Hospitais disponíveis por região")
    for regiao in sistema.hospitais_por_regiao:
        print(f"Região: {regiao}")
        hospitais = sistema.listar_hospitais_regiao(regiao)
        for hospital in hospitais:
            print(f"- {hospital}")
        print()
