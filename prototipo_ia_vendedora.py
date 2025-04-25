"""
Protótipo de IA Vendedora para WhatsApp - Plena Saúde
Desenvolvido para atendimento nas regiões de Francisco Morato, Caieiras e Perus
"""

class IAVendedoraPlena:
    def __init__(self):
        # Inicialização da IA com estados de conversação
        self.estados = {
            "inicio": self.saudacao_inicial,
            "coletar_nome": self.coletar_nome,
            "coletar_telefone": self.coletar_telefone,
            "coletar_email": self.coletar_email,
            "identificar_tipo_plano": self.identificar_tipo_plano,
            "coletar_quantidade_vidas": self.coletar_quantidade_vidas,
            "coletar_idades": self.coletar_idades,
            "coletar_empresa": self.coletar_empresa,
            "verificar_cnpj": self.verificar_cnpj,
            "preferencia_hospital": self.preferencia_hospital,
            "apresentar_cotacao": self.apresentar_cotacao,
            "responder_carencia": self.responder_carencia,
            "responder_documentacao": self.responder_documentacao,
            "responder_inicio_uso": self.responder_inicio_uso,
            "encaminhar_corretor": self.encaminhar_corretor,
            "encerramento": self.encerramento
        }
        
        # Estado atual da conversa
        self.estado_atual = "inicio"
        
        # Dados do cliente
        self.dados_cliente = {
            "nome": "",
            "telefone": "",
            "email": "",
            "tipo_plano": "",
            "quantidade_vidas": 0,
            "idades": [],
            "empresa": "",
            "cnpj_ativo": False,
            "preferencia_hospital": "",
            "cotacao_valor": 0.0
        }
        
        # Perguntas frequentes
        self.perguntas_frequentes = {
            "carencia": ["carência", "carencia", "espera", "quando posso usar"],
            "documentacao": ["documentos", "documentação", "documentacao", "preciso levar", "contratação"],
            "inicio_uso": ["começar", "comecar", "iniciar", "quando posso usar", "quando começa"]
        }
    
    def processar_mensagem(self, mensagem):
        """Processa a mensagem recebida do cliente e retorna uma resposta"""
        # Verificar se é uma pergunta frequente
        for tipo, palavras_chave in self.perguntas_frequentes.items():
            if any(palavra in mensagem.lower() for palavra in palavras_chave):
                if tipo == "carencia":
                    return self.responder_carencia()
                elif tipo == "documentacao":
                    return self.responder_documentacao()
                elif tipo == "inicio_uso":
                    return self.responder_inicio_uso()
        
        # Se não for pergunta frequente, seguir o fluxo normal
        return self.estados[self.estado_atual](mensagem)
    
    # Métodos para cada estado da conversação
    
    def saudacao_inicial(self, mensagem=None):
        self.estado_atual = "coletar_nome"
        return """Olá! Sou a assistente virtual da Plena Saúde. 👋
Estou aqui para ajudar você a encontrar o plano de saúde ideal para você, sua família ou empresa nas regiões de Francisco Morato, Caieiras e Perus.

Para começarmos, poderia me informar seu nome completo?"""
    
    def coletar_nome(self, mensagem):
        self.dados_cliente["nome"] = mensagem
        self.estado_atual = "coletar_telefone"
        return f"Obrigado, {mensagem}. Agora preciso do seu telefone para contato:"
    
    def coletar_telefone(self, mensagem):
        self.dados_cliente["telefone"] = mensagem
        self.estado_atual = "coletar_email"
        return "Perfeito! E qual é o seu e-mail?"
    
    def coletar_email(self, mensagem):
        self.dados_cliente["email"] = mensagem
        self.estado_atual = "identificar_tipo_plano"
        return f"""{self.dados_cliente['nome']}, você está buscando um plano de saúde para:
1. Você (individual)
2. Sua família
3. Sua empresa (plano empresarial/PME)

Responda com o número da opção desejada."""
    
    def identificar_tipo_plano(self, mensagem):
        opcao = mensagem.strip()
        if opcao == "1":
            self.dados_cliente["tipo_plano"] = "individual"
            self.estado_atual = "coletar_quantidade_vidas"
            return "Entendi que você busca um plano individual. Vamos seguir com sua cotação. Quantas pessoas serão incluídas no plano?"
        elif opcao == "2":
            self.dados_cliente["tipo_plano"] = "familiar"
            self.estado_atual = "coletar_quantidade_vidas"
            return "Entendi que você busca um plano familiar. Quantas pessoas serão incluídas no plano?"
        elif opcao == "3":
            self.dados_cliente["tipo_plano"] = "empresarial"
            self.estado_atual = "coletar_empresa"
            return "Entendi que você busca um plano empresarial/PME. Qual é o nome da sua empresa?"
        else:
            return """Desculpe, não entendi sua escolha. Por favor, responda com o número da opção desejada:
1. Você (individual)
2. Sua família
3. Sua empresa (plano empresarial/PME)"""
    
    def coletar_quantidade_vidas(self, mensagem):
        try:
            quantidade = int(mensagem.strip())
            self.dados_cliente["quantidade_vidas"] = quantidade
            self.estado_atual = "coletar_idades"
            return f"Obrigado. Agora preciso saber a idade de cada pessoa. Por favor, informe as {quantidade} idades separadas por vírgula (ex: 30, 25, 2):"
        except ValueError:
            return "Por favor, informe apenas o número de pessoas que serão incluídas no plano."
    
    def coletar_idades(self, mensagem):
        try:
            idades = [int(idade.strip()) for idade in mensagem.split(",")]
            if len(idades) != self.dados_cliente["quantidade_vidas"]:
                return f"O número de idades informadas não corresponde à quantidade de vidas ({self.dados_cliente['quantidade_vidas']}). Por favor, tente novamente."
            
            self.dados_cliente["idades"] = idades
            self.estado_atual = "preferencia_hospital"
            return """Você tem preferência por algum hospital específico na região?
1. Sim
2. Não tenho preferência específica

Se sim, qual hospital?"""
        except ValueError:
            return "Por favor, informe as idades separadas por vírgula (ex: 30, 25, 2)."
    
    def coletar_empresa(self, mensagem):
        self.dados_cliente["empresa"] = mensagem
        self.estado_atual = "verificar_cnpj"
        return "Sua empresa possui CNPJ ativo há mais de 6 meses?"
    
    def verificar_cnpj(self, mensagem):
        if "sim" in mensagem.lower():
            self.dados_cliente["cnpj_ativo"] = True
        else:
            self.dados_cliente["cnpj_ativo"] = False
        
        self.estado_atual = "coletar_quantidade_vidas"
        return "Quantos funcionários/vidas serão incluídos no plano?"
    
    def preferencia_hospital(self, mensagem):
        if mensagem.strip() == "1" or "sim" in mensagem.lower():
            # Cliente tem preferência, aguardar nome do hospital
            return "Por favor, informe qual hospital é de sua preferência:"
        else:
            self.dados_cliente["preferencia_hospital"] = "Sem preferência específica"
            self.estado_atual = "apresentar_cotacao"
            return self.calcular_cotacao()
    
    def calcular_cotacao(self):
        """Calcula a cotação com base nos dados do cliente"""
        # Aqui seria implementada a lógica real de cálculo com base nas tabelas de preços
        # Este é apenas um exemplo simplificado
        
        tipo_plano = self.dados_cliente["tipo_plano"]
        quantidade_vidas = self.dados_cliente["quantidade_vidas"]
        
        # Valores fictícios para exemplo
        if tipo_plano == "individual":
            valor_base = 150.00
        elif tipo_plano == "familiar":
            valor_base = 130.00
        else:  # empresarial
            valor_base = 110.00
        
        # Ajuste por idade (simplificado)
        if "idades" in self.dados_cliente and self.dados_cliente["idades"]:
            fator_idade = sum(1 + (idade / 100) for idade in self.dados_cliente["idades"]) / len(self.dados_cliente["idades"])
        else:
            fator_idade = 1.3  # valor médio para quando não temos idades
        
        # Cálculo final
        valor_total = valor_base * quantidade_vidas * fator_idade
        self.dados_cliente["cotacao_valor"] = round(valor_total, 2)
        
        return self.apresentar_cotacao()
    
    def apresentar_cotacao(self, mensagem=None):
        self.estado_atual = "encaminhar_corretor"
        
        tipo_plano_texto = {
            "individual": "Individual",
            "familiar": "Familiar",
            "empresarial": "Empresarial/PME"
        }.get(self.dados_cliente["tipo_plano"], "")
        
        return f"""Com base nas informações que você me forneceu, preparei uma cotação para o plano {tipo_plano_texto} da Plena Saúde:

Valor mensal: R$ {self.dados_cliente["cotacao_valor"]:.2f}
Cobertura: Consultas, exames, internações, cirurgias, UTI, emergências e urgências
Rede credenciada: Hospitais Previna em Francisco Morato, Caieiras e Perus

Gostaria de receber mais detalhes sobre este plano ou prosseguir com a contratação?"""
    
    def responder_carencia(self, mensagem=None):
        return """Sobre a carência dos planos da Plena Saúde:

- Urgência e emergência: 24 horas
- Consultas e exames simples: 30 dias
- Exames complexos: 90 dias
- Internações e cirurgias: 180 dias
- Parto: 300 dias

Lembrando que estas são condições gerais e podem variar conforme o plano escolhido.

Em que mais posso ajudar?"""
    
    def responder_documentacao(self, mensagem=None):
        return """Para contratação do plano, você precisará dos seguintes documentos:

Para pessoa física:
- RG e CPF de todos os beneficiários
- Comprovante de residência atualizado
- Cartão do SUS

Para empresas (PME):
- Contrato social
- Cartão CNPJ
- Documentos dos sócios (RG e CPF)
- Documentos dos beneficiários (RG e CPF)
- Comprovante de vínculo empregatício

Em que mais posso ajudar?"""
    
    def responder_inicio_uso(self, mensagem=None):
        return """Após a contratação e pagamento do primeiro boleto, o plano estará ativo a partir da data de vigência informada no contrato, geralmente no primeiro dia do mês seguinte à contratação.

Você receberá as carteirinhas digitais por e-mail e poderá utilizar os serviços respeitando os períodos de carência.

Em que mais posso ajudar?"""
    
    def encaminhar_corretor(self, mensagem):
        if "sim" in mensagem.lower() or "prosseguir" in mensagem.lower() or "contratação" in mensagem.lower():
            self.estado_atual = "encerramento"
            return f"""Ótimo, {self.dados_cliente["nome"]}! Para finalizar sua contratação, vou encaminhar suas informações para um de nossos corretores especializados, que entrará em contato com você em breve para concluir o processo.

O pagamento do primeiro boleto será feito diretamente ao corretor.

Tem mais alguma dúvida que eu possa esclarecer?"""
        else:
            return "Entendo. Em que mais posso ajudar você sobre os planos da Plena Saúde?"
    
    def encerramento(self, mensagem=None):
        self.estado_atual = "inicio"  # Reinicia o fluxo para uma nova conversa
        return """Foi um prazer ajudar você! Se surgir qualquer outra dúvida sobre os planos da Plena Saúde, estou à disposição.

Tenha um ótimo dia! 😊"""


# Exemplo de uso da IA
if __name__ == "__main__":
    ia = IAVendedoraPlena()
    
    # Simulação de conversa
    print("Simulação de conversa com a IA Vendedora da Plena Saúde")
    print("-" * 50)
    
    # Primeira mensagem (saudação)
    resposta = ia.processar_mensagem("Olá")
    print("Cliente: Olá")
    print(f"IA: {resposta}")
    print("-" * 50)
    
    # Coleta de nome
    resposta = ia.processar_mensagem("João Silva")
    print("Cliente: João Silva")
    print(f"IA: {resposta}")
    print("-" * 50)
    
    # Coleta de telefone
    resposta = ia.processar_mensagem("11 98765-4321")
    print("Cliente: 11 98765-4321")
    print(f"IA: {resposta}")
    print("-" * 50)
    
    # Coleta de email
    resposta = ia.processar_mensagem("joao.silva@email.com")
    print("Cliente: joao.silva@email.com")
    print(f"IA: {resposta}")
    print("-" * 50)
    
    # Tipo de plano
    resposta = ia.processar_mensagem("2")
    print("Cliente: 2")
    print(f"IA: {resposta}")
    print("-" * 50)
    
    # Quantidade de vidas
    resposta = ia.processar_mensagem("3")
    print("Cliente: 3")
    print(f"IA: {resposta}")
    print("-" * 50)
    
    # Idades
    resposta = ia.processar_mensagem("35, 32, 5")
    print("Cliente: 35, 32, 5")
    print(f"IA: {resposta}")
    print("-" * 50)
    
    # Preferência de hospital
    resposta = ia.processar_mensagem("2")
    print("Cliente: 2")
    print(f"IA: {resposta}")
    print("-" * 50)
    
    # Pergunta sobre carência
    resposta = ia.processar_mensagem("Como funciona a carência?")
    print("Cliente: Como funciona a carência?")
    print(f"IA: {resposta}")
    print("-" * 50)
    
    # Prosseguir com contratação
    resposta = ia.processar_mensagem("Sim, quero contratar")
    print("Cliente: Sim, quero contratar")
    print(f"IA: {resposta}")
    print("-" * 50)
    
    # Encerramento
    resposta = ia.processar_mensagem("Não, obrigado")
    print("Cliente: Não, obrigado")
    print(f"IA: {resposta}")
    print("-" * 50)
