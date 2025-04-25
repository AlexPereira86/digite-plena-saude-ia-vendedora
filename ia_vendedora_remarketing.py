"""
IA Vendedora Integrada para WhatsApp - Plena Saúde
Versão com Modo de Teste e Funcionalidade de Remarketing
"""

from sistema_cotacao import SistemaCotacaoPlena
import datetime
import os
import time

class IAVendedoraPlenaIntegrada:
    def __init__(self, modo_teste=False):
        # Configuração do modo de teste
        self.modo_teste = modo_teste
        self.log_file = "/home/ubuntu/plena_saude_ia/log_interacoes_teste.txt"
        
        # Configuração de remarketing
        self.remarketing_ativo = True
        self.tempo_inatividade = 24 * 60 * 60  # 24 horas em segundos (ajustável)
        self.max_tentativas_remarketing = 3
        self.intervalo_entre_tentativas = 24 * 60 * 60  # 24 horas em segundos (ajustável)
        
        # Registro de clientes para remarketing
        self.clientes_remarketing = {}
        
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
            "encerramento": self.encerramento,
            "remarketing": self.enviar_remarketing
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
            "cotacao": {},
            "ultima_interacao": time.time(),
            "tentativas_remarketing": 0,
            "conversa_ativa": True
        }
        
        # Perguntas frequentes
        self.perguntas_frequentes = {
            "carencia": ["carência", "carencia", "espera", "quando posso usar"],
            "documentacao": ["documentos", "documentação", "documentacao", "preciso levar", "contratação"],
            "inicio_uso": ["começar", "comecar", "iniciar", "quando posso usar", "quando começa"]
        }
        
        # Inicializar o sistema de cotação
        self.sistema_cotacao = SistemaCotacaoPlena()
        
        # Inicializar arquivo de log se estiver em modo de teste
        if self.modo_teste:
            self.inicializar_log()
    
    def inicializar_log(self):
        """Inicializa o arquivo de log para o modo de teste"""
        with open(self.log_file, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"NOVA SESSÃO DE TESTE - {datetime.datetime.now()}\n")
            f.write(f"{'='*50}\n")
    
    def registrar_log(self, tipo, mensagem, resposta=None):
        """Registra interações no arquivo de log quando em modo de teste"""
        if not self.modo_teste:
            return
            
        with open(self.log_file, 'a') as f:
            f.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] {tipo}:\n")
            f.write(f"- Mensagem: {mensagem}\n")
            if resposta:
                f.write(f"- Resposta: {resposta}\n")
            f.write(f"- Estado atual: {self.estado_atual}\n")
            f.write(f"- Dados do cliente: {str(self.dados_cliente)}\n")
    
    def formatar_resposta(self, resposta):
        """Adiciona prefixo de teste às respostas quando em modo de teste"""
        if self.modo_teste:
            return f"[TESTE] {resposta}"
        return resposta
    
    def processar_mensagem(self, mensagem, telefone_cliente=None):
        """Processa a mensagem recebida do cliente e retorna uma resposta"""
        # Atualizar timestamp da última interação
        self.dados_cliente["ultima_interacao"] = time.time()
        self.dados_cliente["conversa_ativa"] = True
        
        # Se o cliente está retornando após remarketing, registrar
        if telefone_cliente and telefone_cliente in self.clientes_remarketing:
            self.registrar_log("RETORNO_REMARKETING", 
                              f"Cliente retornou após remarketing: {telefone_cliente}", 
                              "Retomando conversa")
            
            # Recuperar dados do cliente se disponíveis
            if "dados_cliente" in self.clientes_remarketing[telefone_cliente]:
                self.dados_cliente = self.clientes_remarketing[telefone_cliente]["dados_cliente"]
                self.estado_atual = self.clientes_remarketing[telefone_cliente]["estado"]
                
                # Mensagem de boas-vindas para cliente que retorna
                if self.dados_cliente["nome"]:
                    resposta = f"Que bom ver você novamente, {self.dados_cliente['nome']}! Vamos continuar de onde paramos. {self.estados[self.estado_atual]('retorno')}"
                    return self.formatar_resposta(resposta)
        
        # Verificar se é uma pergunta frequente
        for tipo, palavras_chave in self.perguntas_frequentes.items():
            if any(palavra in mensagem.lower() for palavra in palavras_chave):
                if tipo == "carencia":
                    resposta = self.responder_carencia()
                    self.registrar_log("PERGUNTA_FREQUENTE", mensagem, resposta)
                    return self.formatar_resposta(resposta)
                elif tipo == "documentacao":
                    resposta = self.responder_documentacao()
                    self.registrar_log("PERGUNTA_FREQUENTE", mensagem, resposta)
                    return self.formatar_resposta(resposta)
                elif tipo == "inicio_uso":
                    resposta = self.responder_inicio_uso()
                    self.registrar_log("PERGUNTA_FREQUENTE", mensagem, resposta)
                    return self.formatar_resposta(resposta)
        
        # Se não for pergunta frequente, seguir o fluxo normal
        resposta = self.estados[self.estado_atual](mensagem)
        self.registrar_log("FLUXO_NORMAL", mensagem, resposta)
        return self.formatar_resposta(resposta)
    
    def verificar_inatividade(self):
        """Verifica clientes inativos e envia mensagens de remarketing quando necessário"""
        if not self.remarketing_ativo:
            return []
            
        mensagens_remarketing = []
        tempo_atual = time.time()
        
        # Verificar cliente atual
        if (self.dados_cliente["telefone"] and 
            not self.dados_cliente["conversa_ativa"] and
            self.dados_cliente["tentativas_remarketing"] < self.max_tentativas_remarketing and
            (tempo_atual - self.dados_cliente["ultima_interacao"]) > self.tempo_inatividade):
            
            # Incrementar tentativas e atualizar timestamp
            self.dados_cliente["tentativas_remarketing"] += 1
            self.dados_cliente["ultima_interacao"] = tempo_atual
            
            # Gerar mensagem de remarketing
            mensagem = self.enviar_remarketing()
            
            # Adicionar à lista de mensagens a enviar
            mensagens_remarketing.append({
                "telefone": self.dados_cliente["telefone"],
                "mensagem": self.formatar_resposta(mensagem)
            })
            
            # Registrar no log
            self.registrar_log("REMARKETING_ENVIADO", 
                              f"Tentativa {self.dados_cliente['tentativas_remarketing']} para {self.dados_cliente['telefone']}", 
                              mensagem)
            
            # Salvar dados do cliente para remarketing
            self.clientes_remarketing[self.dados_cliente["telefone"]] = {
                "dados_cliente": self.dados_cliente.copy(),
                "estado": self.estado_atual,
                "ultima_tentativa": tempo_atual
            }
        
        # Verificar clientes em remarketing
        for telefone, dados in list(self.clientes_remarketing.items()):
            # Pular o cliente atual que já foi tratado
            if telefone == self.dados_cliente["telefone"]:
                continue
                
            # Verificar se é hora de enviar nova tentativa
            if (dados["dados_cliente"]["tentativas_remarketing"] < self.max_tentativas_remarketing and
                (tempo_atual - dados["ultima_tentativa"]) > self.intervalo_entre_tentativas):
                
                # Incrementar tentativas e atualizar timestamp
                dados["dados_cliente"]["tentativas_remarketing"] += 1
                dados["ultima_tentativa"] = tempo_atual
                
                # Gerar mensagem de remarketing
                self.dados_cliente = dados["dados_cliente"]  # Temporariamente usar dados deste cliente
                self.estado_atual = dados["estado"]
                mensagem = self.enviar_remarketing()
                
                # Adicionar à lista de mensagens a enviar
                mensagens_remarketing.append({
                    "telefone": telefone,
                    "mensagem": self.formatar_resposta(mensagem)
                })
                
                # Registrar no log
                self.registrar_log("REMARKETING_ENVIADO", 
                                  f"Tentativa {dados['dados_cliente']['tentativas_remarketing']} para {telefone}", 
                                  mensagem)
                
                # Atualizar dados no dicionário
                self.clientes_remarketing[telefone] = {
                    "dados_cliente": self.dados_cliente.copy(),
                    "estado": self.estado_atual,
                    "ultima_tentativa": tempo_atual
                }
            
            # Remover clientes que atingiram o limite de tentativas
            elif dados["dados_cliente"]["tentativas_remarketing"] >= self.max_tentativas_remarketing:
                self.registrar_log("REMARKETING_ENCERRADO", 
                                  f"Limite de tentativas atingido para {telefone}", 
                                  "Cliente removido da lista de remarketing")
                del self.clientes_remarketing[telefone]
        
        return mensagens_remarketing
    
    def marcar_conversa_inativa(self):
        """Marca a conversa atual como inativa para iniciar o processo de remarketing"""
        if self.dados_cliente["telefone"]:
            self.dados_cliente["conversa_ativa"] = False
            self.registrar_log("CONVERSA_INATIVA", 
                              f"Cliente {self.dados_cliente['telefone']} marcado como inativo", 
                              "Remarketing será iniciado após período de inatividade")
    
    def enviar_remarketing(self, mensagem=None):
        """Gera mensagens de remarketing com base no estado da conversa e número de tentativas"""
        tentativa = self.dados_cliente["tentativas_remarketing"]
        nome = self.dados_cliente["nome"] if self.dados_cliente["nome"] else "Olá"
        
        # Mensagens de remarketing baseadas no estado da conversa
        if self.estado_atual in ["coletar_nome", "coletar_telefone", "coletar_email"]:
            # Cliente abandonou no início do processo
            if tentativa == 1:
                return f"{nome}, notamos que você começou a cotar um plano de saúde da Plena Saúde. Podemos ajudar com alguma informação adicional? Estamos à disposição para continuar o atendimento."
            elif tentativa == 2:
                return f"{nome}, ainda está interessado em conhecer os planos de saúde da Plena Saúde? Temos opções que cabem no seu bolso com excelente cobertura nas regiões de Francisco Morato, Caieiras e Perus."
            else:
                return f"{nome}, última chance! Aproveite condições especiais nos planos da Plena Saúde. Responda esta mensagem para retomar sua cotação com um desconto exclusivo."
                
        elif self.estado_atual in ["identificar_tipo_plano", "coletar_quantidade_vidas", "coletar_idades"]:
            # Cliente forneceu informações básicas mas não completou dados do plano
            if tentativa == 1:
                return f"{nome}, você estava cotando um plano de saúde da Plena Saúde. Faltam apenas alguns dados para concluirmos sua cotação personalizada. Podemos continuar?"
            elif tentativa == 2:
                return f"{nome}, estamos quase finalizando sua cotação do plano Plena Saúde! Responda esta mensagem para continuarmos e você descobrir quanto economizaria com nossos planos."
            else:
                return f"{nome}, última oportunidade! Temos uma oferta especial para você. Conclua sua cotação e ganhe 5% de desconto na primeira mensalidade do seu plano Plena Saúde."
                
        elif self.estado_atual in ["coletar_regiao", "preferencia_hospital", "coletar_tipo_cobertura", "coletar_coparticipacao"]:
            # Cliente forneceu dados principais mas não chegou à cotação
            if tentativa == 1:
                return f"{nome}, você estava muito próximo de receber sua cotação personalizada da Plena Saúde! Falta pouco para concluir. Podemos continuar de onde paramos?"
            elif tentativa == 2:
                return f"{nome}, sua cotação da Plena Saúde está quase pronta! Responda esta mensagem para receber os valores e conhecer todos os benefícios do plano."
            else:
                return f"{nome}, oferta exclusiva! Conclua sua cotação agora e ganhe 10% de desconto na primeira mensalidade do seu plano Plena Saúde. Esta oferta é válida apenas por 24 horas!"
                
        elif self.estado_atual in ["apresentar_cotacao", "encaminhar_corretor"]:
            # Cliente recebeu cotação mas não finalizou
            if tentativa == 1:
                return f"{nome}, notamos que você recebeu uma cotação do plano Plena Saúde. Ficou alguma dúvida que possamos esclarecer? Estamos à disposição!"
            elif tentativa == 2:
                return f"{nome}, que tal agendar uma conversa com um de nossos consultores para esclarecer todas as suas dúvidas sobre o plano Plena Saúde? Responda esta mensagem para agendarmos."
            else:
                return f"{nome}, última chance! Aproveite condições exclusivas na contratação do seu plano Plena Saúde: isenção de carência para consultas e exames simples. Oferta válida por 24 horas!"
        
        # Mensagem genérica caso nenhuma condição seja atendida
        return f"{nome}, sentimos sua falta! Estamos à disposição para continuar o atendimento sobre os planos da Plena Saúde. Podemos ajudar em algo?"
    
    # Métodos para cada estado da conversação
    
    def saudacao_inicial(self, mensagem=None):
        if mensagem == "retorno":
            return "Vamos continuar com sua cotação. Em que posso ajudar?"
            
        self.estado_atual = "coletar_nome"
        return """Olá! Sou a assistente virtual da Plena Saúde. 👋
Estou aqui para ajudar você a encontrar o plano de saúde ideal para você, sua família ou empresa nas regiões de Francisco Morato, Caieiras e Perus.

Para começarmos, poderia me informar seu nome completo?"""
    
    def coletar_nome(self, mensagem):
        if mensagem == "retorno":
            return f"Poderia confirmar seu nome completo?"
            
        self.dados_cliente["nome"] = mensagem
        self.estado_atual = "coletar_telefone"
        return f"Obrigado, {mensagem}. Agora preciso do seu telefone para contato:"
    
    def coletar_telefone(self, mensagem):
        if mensagem == "retorno":
            return f"Poderia confirmar seu telefone para contato?"
            
        self.dados_cliente["telefone"] = mensagem
        self.estado_atual = "coletar_email"
        return "Perfeito! E qual é o seu e-mail?"
    
    def coletar_email(self, mensagem):
        if mensagem == "retorno":
            return f"Poderia confirmar seu e-mail?"
            
        self.dados_cliente["email"] = mensagem
        self.estado_atual = "identificar_tipo_plano"
        return f"""{self.dados_cliente['nome']}, você está buscando um plano de saúde para:
1. Você (individual)
2. Sua família
3. Sua empresa (plano empresarial/PME)

Responda com o número da opção desejada."""
    
    def identificar_tipo_plano(self, mensagem):
        if mensagem == "retorno":
            return f"""Você estava buscando um plano de saúde para:
1. Você (individual)
2. Sua família
3. Sua empresa (plano empresarial/PME)

Responda com o número da opção desejada."""
            
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
        if mensagem == "retorno":
            return f"Você estava informando quantas pessoas serão incluídas no plano. Poderia confirmar esse número?"
            
        try:
            quantidade = int(mensagem.strip())
            self.dados_cliente["quantidade_vidas"] = quantidade
            self.estado_atual = "coletar_idades"
            return f"Obrigado. Agora preciso saber a idade de cada pessoa. Por favor, informe as {quantidade} idades separadas por vírgula (ex: 30, 25, 2):"
        except ValueError:
            return "Por favor, informe apenas o número de pessoas que serão incluídas no plano."
    
    def coletar_idades(self, mensagem):
        if mensagem == "retorno":
            return f"Você estava informando as idades das {self.dados_cliente['quantidade_vidas']} pessoas. Poderia confirmar essas idades separadas por vírgula?"
            
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
        if mensagem == "retorno":
            return """Em qual região você reside ou pretende utilizar mais o plano?
1. Francisco Morato
2. Caieiras
3. Perus
4. Outra região

Responda com o número da opção desejada."""
            
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
        if mensagem == "retorno":
            return f"Você estava informando o nome da sua empresa. Poderia confirmar?"
            
        self.dados_cliente["empresa"] = mensagem
        self.estado_atual = "verificar_cnpj"
        return "Sua empresa possui CNPJ ativo há mais de 6 meses?"
    
    def verificar_cnpj(self, mensagem):
        if mensagem == "retorno":
            return f"Sua empresa possui CNPJ ativo há mais de 6 meses?"
            
        if "sim" in mensagem.lower():
            self.dados_cliente["cnpj_ativo"] = True
        else:
            self.dados_cliente["cnpj_ativo"] = False
        
        self.estado_atual = "coletar_quantidade_vidas"
        return "Quantos funcionários/vidas serão incluídos no plano?"
    
    def preferencia_hospital(self, mensagem):
        if mensagem == "retorno":
            return """Você tem preferência por algum hospital específico na região?
1. Sim
2. Não tenho preferência específica

Se sim, qual hospital?"""
            
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
        if mensagem == "retorno":
            return """Qual tipo de cobertura você está buscando?
1. Básica (Plena Essencial) - Cobertura essencial com menor custo
2. Intermediária (Plena Plus) - Boa cobertura com custo-benefício equilibrado
3. Completa (Plena Premium) - Cobertura ampla com mais benefícios

Responda com o número da opção desejada."""
            
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
        if mensagem == "retorno":
            return """Você prefere um plano com ou sem coparticipação?

Com coparticipação: Mensalidade mais baixa, mas você paga uma pequena parte ao utilizar alguns serviços
Sem coparticipação: Mensalidade um pouco mais alta, mas sem pagamentos adicionais ao utilizar os serviços

1. Com coparticipação
2. Sem coparticipação

Responda com o número da opção desejada."""
            
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
        
        # Se estiver em modo de teste, aplicar desconto fictício
        if self.modo_teste:
            # Salvar cotação original para comparação
            cotacao_original = self.sistema_cotacao.gerar_cotacao(
                self.dados_cliente["tipo_plano"],
                self.dados_cliente["idades"],
                self.dados_cliente["tipo_cobertura"],
                self.dados_cliente["coparticipacao"],
                hospital_premium
            )
            
            # Aplicar desconto de 15% para demonstração
            cotacao = cotacao_original.copy()
            cotacao["valor_mensal"] = round(cotacao["valor_mensal"] * 0.85, 2)
            cotacao["desconto_teste"] = "15% de desconto aplicado (apenas em modo de teste)"
            
            # Registrar no log a diferença
            self.registrar_log(
                "COTACAO_TESTE", 
                f"Valor original: R$ {cotacao_original['valor_mensal']:.2f}", 
                f"Valor com desconto: R$ {cotacao['valor_mensal']:.2f}"
            )
        else:
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
        if mensagem == "retorno":
            cotacao = self.dados_cliente["cotacao"]
            return f"""Você recebeu uma cotação para o plano {cotacao["nome_plano"]} ({cotacao["tipo_plano"]}) da Plena Saúde.
Valor mensal: R$ {cotacao["valor_mensal"]:.2f}

Gostaria de receber mais detalhes sobre este plano ou prosseguir com a contratação?"""
            
        self.estado_atual = "encaminhar_corretor"
        
        cotacao = self.dados_cliente["cotacao"]
        cobertura_texto = "\n".join([f"- {item}" for item in cotacao["cobertura"]])
        
        # Adicionar informação de desconto se estiver em modo de teste
        desconto_info = ""
        if self.modo_teste and "desconto_teste" in cotacao:
            desconto_info = f"\n{cotacao['desconto_teste']}"
            
        # Adicionar desconto de remarketing se for uma tentativa de remarketing
        if self.dados_cliente["tentativas_remarketing"] > 0:
            desconto_remarketing = 5 * self.dados_cliente["tentativas_remarketing"]  # 5% por tentativa
            if desconto_remarketing > 0:
                valor_original = cotacao["valor_mensal"]
                valor_com_desconto = round(valor_original * (1 - desconto_remarketing/100), 2)
                desconto_info += f"\nOFERTA ESPECIAL: {desconto_remarketing}% de desconto na primeira mensalidade!"
                
                # Registrar no log
                self.registrar_log(
                    "DESCONTO_REMARKETING", 
                    f"Desconto de {desconto_remarketing}% aplicado", 
                    f"Valor original: R$ {valor_original:.2f}, Com desconto: R$ {valor_com_desconto:.2f}"
                )
        
        return f"""Com base nas informações que você me forneceu, preparei uma cotação para o plano {cotacao["nome_plano"]} ({cotacao["tipo_plano"]}) da Plena Saúde:

Valor mensal: R$ {cotacao["valor_mensal"]:.2f}{desconto_info}
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
        if mensagem == "retorno":
            return f"""Você estava prestes a ser encaminhado para um corretor para finalizar a contratação.
Gostaria de prosseguir com a contratação do plano {self.dados_cliente['cotacao']['nome_plano']}?"""
            
        if "sim" in mensagem.lower() or "prosseguir" in mensagem.lower() or "contratação" in mensagem.lower():
            self.estado_atual = "encerramento"
            
            # Definir corretor com base no modo (teste ou produção)
            corretor = "Corretor de Teste (corretor.teste@plenasaude.com.br)" if self.modo_teste else "um de nossos corretores especializados"
            
            # Registrar lead no log se estiver em modo de teste
            if self.modo_teste:
                self.registrar_log(
                    "LEAD_QUALIFICADO", 
                    f"Cliente: {self.dados_cliente['nome']} ({self.dados_cliente['telefone']})", 
                    f"Plano: {self.dados_cliente['cotacao']['nome_plano']} - R$ {self.dados_cliente['cotacao']['valor_mensal']:.2f}"
                )
            
            return f"""Ótimo, {self.dados_cliente["nome"]}! Para finalizar sua contratação, vou encaminhar suas informações para {corretor}, que entrará em contato com você em breve para concluir o processo.

O pagamento do primeiro boleto será feito diretamente ao corretor.

Tem mais alguma dúvida que eu possa esclarecer?"""
        else:
            return "Entendo. Em que mais posso ajudar você sobre os planos da Plena Saúde?"
    
    def encerramento(self, mensagem=None):
        self.estado_atual = "inicio"  # Reinicia o fluxo para uma nova conversa
        
        # Registrar encerramento no log se estiver em modo de teste
        if self.modo_teste:
            self.registrar_log("ENCERRAMENTO", "Conversa finalizada", "Fluxo reiniciado para nova conversa")
        
        return """Foi um prazer ajudar você! Se surgir qualquer outra dúvida sobre os planos da Plena Saúde, estou à disposição.

Tenha um ótimo dia! 😊"""


# Exemplo de uso da IA integrada com remarketing
if __name__ == "__main__":
    # Criar instância em modo de teste
    ia = IAVendedoraPlenaIntegrada(modo_teste=True)
    
    print("="*70)
    print("SIMULAÇÃO DA IA VENDEDORA PLENA SAÚDE - MODO DE TESTE COM REMARKETING")
    print("="*70)
    print("Todas as mensagens terão o prefixo [TESTE]")
    print("Cotações terão desconto fictício de 15% para demonstração")
    print("Sistema de remarketing ativado para clientes inativos")
    print("="*70)
    
    # Simulação de conversa
    print("\nSimulação de conversa com a IA Vendedora Integrada da Plena Saúde (MODO TESTE)")
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
    
    # Simular cliente abandonando a conversa
    print("Cliente: [abandona a conversa]")
    print("IA: [aguardando resposta]")
    print("-" * 70)
    
    # Marcar conversa como inativa
    ia.marcar_conversa_inativa()
    print("Sistema: Conversa marcada como inativa")
    print("-" * 70)
    
    # Simular passagem de tempo (para teste)
    print("Sistema: Simulando passagem de tempo...")
    
    # Verificar inatividade e gerar mensagens de remarketing
    mensagens_remarketing = ia.verificar_inatividade()
    
    if mensagens_remarketing:
        print("Sistema: Mensagens de remarketing geradas:")
        for msg in mensagens_remarketing:
            print(f"Para: {msg['telefone']}")
            print(f"Mensagem: {msg['mensagem']}")
    print("-" * 70)
    
    # Simular cliente retornando após remarketing
    print("Cliente: [retorna após remarketing] Olá, ainda estou interessado")
    resposta = ia.processar_mensagem("Olá, ainda estou interessado", "11 98765-4321")
    print(f"IA: {resposta}")
    print("-" * 70)
    
    # Continuar a conversa de onde parou
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
    
    print("\nSimulação concluída. Verifique o arquivo de log para detalhes das interações.")
    print(f"Arquivo de log: {ia.log_file}")
    print("="*70)
