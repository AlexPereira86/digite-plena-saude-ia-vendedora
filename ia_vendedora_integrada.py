"""
IA Vendedora Integrada para WhatsApp - Plena Saúde
Integração do protótipo da IA vendedora com o sistema de cotação detalhado
"""

from sistema_cotacao import SistemaCotacaoPlena

class IAVendedoraPlenaIntegrada:
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
            "coletar_regiao": self.coletar_regiao,
            "preferencia_hospital": self.preferencia_hospital,
            "coletar_tipo_cobertura": self.coletar_tipo_cobertura,
            "coletar_coparticipacao": self.coletar_coparticipacao,
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
            "regiao": "",
            "preferencia_hospital": "",
            "tipo_cobertura": "intermediario",
            "coparticipacao": "sem",
            "cotacao": {}
        }
        
        # Perguntas frequentes
        self.perguntas_frequentes = {
            "carencia": ["carência", "carencia", "espera", "quando posso usar"],
            "documentacao": ["documentos", "documentação", "documentacao", "preciso levar", "contratação"],
            "inicio_uso": ["começar", "comecar", "iniciar", "quando posso usar", "quando começa"]
        }
        
        # Inicializar o sistema de cotação
        self.sistema_cotacao = SistemaCotacaoPlena()
    
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
            self.estado_atual = "coletar_regiao"
            return """Em qual região você reside ou pretende utilizar mais o plano?
1. Francisco Morato
2. Caieiras
3. Perus
4. Outra região

Responda com o número da opção desejada."""
        except ValueError:
            return "Por favor, informe as idades separadas por vírgula (ex: 30, 25, 2)."
    
    def coletar_regiao(self, mensagem):
        opcao = mensagem.strip()
        regioes = {
            "1": "Francisco Morato",
            "2": "Caieiras",
            "3": "Perus",
            "4": "Outra região"
        }
        
        if opcao in regioes:
            self.dados_cliente["regiao"] = regioes[opcao]
            
            if opcao == "4":
                # Se for outra região, informar sobre limitações
                self.estado_atual = "preferencia_hospital"
                return """A Plena Saúde tem foco de atendimento nas regiões de Francisco Morato, Caieiras e Perus. 
Em outras regiões, o atendimento pode ser limitado.

Você tem preferência por algum hospital específico na região?
1. Sim
2. Não tenho preferência específica

Se sim, qual hospital?"""
            else:
                # Mostrar hospitais disponíveis na região selecionada
                hospitais = self.sistema_cotacao.listar_hospitais_regiao(regioes[opcao])
                hospitais_texto = "\n".join([f"- {hospital}" for hospital in hospitais])
                
                self.estado_atual = "preferencia_hospital"
                return f"""Na região de {regioes[opcao]}, temos os seguintes hospitais disponíveis:

{hospitais_texto}

Você tem preferência por algum desses hospitais?
1. Sim
2. Não tenho preferência específica

Se sim, qual hospital?"""
        else:
            return """Por favor, escolha uma das opções disponíveis:
1. Francisco Morato
2. Caieiras
3. Perus
4. Outra região"""
    
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
            self.estado_atual = "coletar_tipo_cobertura"
            return """Qual tipo de cobertura você está buscando?
1. Básica (Plena Essencial) - Cobertura essencial com menor custo
2. Intermediária (Plena Plus) - Boa cobertura com custo-benefício equilibrado
3. Completa (Plena Premium) - Cobertura ampla com mais benefícios

Responda com o número da opção desejada."""
    
    def coletar_tipo_cobertura(self, mensagem):
        opcao = mensagem.strip()
        coberturas = {
            "1": "basico",
            "2": "intermediario",
            "3": "completo"
        }
        
        if opcao in coberturas:
            self.dados_cliente["tipo_cobertura"] = coberturas[opcao]
            self.estado_atual = "coletar_coparticipacao"
            return """Você prefere um plano com ou sem coparticipação?

Com coparticipação: Mensalidade mais baixa, mas você paga uma pequena parte ao utilizar alguns serviços
Sem coparticipação: Mensalidade um pouco mais alta, mas sem pagamentos adicionais ao utilizar os serviços

1. Com coparticipação
2. Sem coparticipação

Responda com o número da opção desejada."""
        else:
            return """Por favor, escolha uma das opções disponíveis:
1. Básica (Plena Essencial)
2. Intermediária (Plena Plus)
3. Completa (Plena Premium)"""
    
    def coletar_coparticipacao(self, mensagem):
        opcao = mensagem.strip()
        if opcao == "1":
            self.dados_cliente["coparticipacao"] = "com"
        elif opcao == "2":
            self.dados_cliente["coparticipacao"] = "sem"
        else:
            return """Por favor, escolha uma das opções disponíveis:
1. Com coparticipação
2. Sem coparticipação"""
        
        self.estado_atual = "apresentar_cotacao"
        return self.calcular_cotacao()
    
    def calcular_cotacao(self):
        """Calcula a cotação com base nos dados do cliente usando o sistema de cotação"""
        hospital_premium = None
        if self.dados_cliente["preferencia_hospital"] in self.sistema_cotacao.hospitais_premium:
            hospital_premium = self.dados_cliente["preferencia_hospital"]
        
        cotacao = self.sistema_cotacao.gerar_cotacao(
            self.dados_cliente["tipo_plano"],
            self.dados_cliente["idades"],
            self.dados_cliente["tipo_cobertura"],
            self.dados_cliente["coparticipacao"],
            hospital_premium
        )
        
        self.dados_cliente["cotacao"] = cotacao
        return self.apresentar_cotacao()
    
    def apresentar_cotacao(self, mensagem=None):
        self.estado_atual = "encaminhar_corretor"
        
        cotacao = self.dados_cliente["cotacao"]
        cobertura_texto = "\n".join([f"- {item}" for item in cotacao["cobertura"]])
        
        return f"""Com base nas informações que você me forneceu, preparei uma cotação para o plano {cotacao["nome_plano"]} ({cotacao["tipo_plano"]}) da Plena Saúde:

Valor mensal: R$ {cotacao["valor_mensal"]:.2f}
{cotacao["coparticipacao"]}
Quantidade de vidas: {cotacao["quantidade_vidas"]}
Rede hospitalar: {cotacao["hospital_premium"]}

Cobertura:
{cobertura_texto}

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


# Exemplo de uso da IA integrada
if __name__ == "__main__":
    ia = IAVendedoraPlenaIntegrada()
    
    # Simulação de conversa
    print("Simulação de conversa com a IA Vendedora Integrada da Plena Saúde")
    print("-" * 70)
    
    # Primeira mensagem (saudação)
    resposta = ia.processar_mensagem("Olá")
    print("Cliente: Olá")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Coleta de nome
    resposta = ia.processar_mensagem("Maria Silva")
    print("Cliente: Maria Silva")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Coleta de telefone
    resposta = ia.processar_mensagem("11 98765-4321")
    print("Cliente: 11 98765-4321")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Coleta de email
    resposta = ia.processar_mensagem("maria.silva@email.com")
    print("Cliente: maria.silva@email.com")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Tipo de plano
    resposta = ia.processar_mensagem("2")
    print("Cliente: 2")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Quantidade de vidas
    resposta = ia.processar_mensagem("4")
    print("Cliente: 4")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Idades
    resposta = ia.processar_mensagem("35, 32, 5, 3")
    print("Cliente: 35, 32, 5, 3")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Região
    resposta = ia.processar_mensagem("2")
    print("Cliente: 2")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Preferência de hospital
    resposta = ia.processar_mensagem("2")
    print("Cliente: 2")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Tipo de cobertura
    resposta = ia.processar_mensagem("2")
    print("Cliente: 2")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Coparticipação
    resposta = ia.processar_mensagem("1")
    print("Cliente: 1")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Pergunta sobre carência
    resposta = ia.processar_mensagem("Como funciona a carência?")
    print("Cliente: Como funciona a carência?")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Prosseguir com contratação
    resposta = ia.processar_mensagem("Sim, quero contratar")
    print("Cliente: Sim, quero contratar")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Encerramento
    resposta = ia.processar_mensagem("Não, obrigado")
    print("Cliente: Não, obrigado")
    print(f"IA: {resposta}")
    print("-" * 70)
