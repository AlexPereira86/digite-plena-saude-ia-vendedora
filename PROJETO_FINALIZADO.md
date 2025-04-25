# Projeto IA Vendedora para WhatsApp - Plena Saúde

## Visão Geral do Projeto Finalizado

Este projeto implementa uma IA vendedora completa para WhatsApp especializada em planos de saúde da Plena Saúde, com foco nas regiões de Francisco Morato, Caieiras e Perus. A solução inclui todas as funcionalidades necessárias para automatizar o processo de vendas, desde o primeiro contato até o encaminhamento para um corretor.

## Componentes Principais

### 1. Fluxo de Conversação (`fluxo_conversacao.md`)
- Estrutura detalhada do diálogo para atendimento via WhatsApp
- Mensagens para cada etapa do processo de cotação
- Respostas para perguntas frequentes

### 2. Sistema de Cotação (`sistema_cotacao.py`)
- Cálculos para planos individuais, familiares e empresariais
- Consideração de faixas etárias, quantidade de vidas e preferências
- Opções de cobertura e coparticipação
- Informações sobre hospitais por região

### 3. IA Vendedora Básica (`prototipo_ia_vendedora.py`)
- Implementação inicial do fluxo de conversação
- Estrutura básica de estados e transições
- Simulação de conversa simples

### 4. IA Vendedora Integrada (`ia_vendedora_integrada.py`)
- Integração do fluxo de conversação com o sistema de cotação
- Coleta de informações do cliente
- Processamento de perguntas frequentes
- Geração de cotações personalizadas
- Encaminhamento para corretores

### 5. IA Vendedora com Modo de Teste (`ia_vendedora_modo_teste.py`)
- Prefixo "[TESTE]" em todas as mensagens
- Desconto fictício nas cotações para demonstração
- Encaminhamento para corretor de teste
- Sistema de log detalhado para análise

### 6. IA Vendedora com Remarketing (`ia_vendedora_remarketing.py`)
- Detecção de inatividade de clientes
- Mensagens de follow-up personalizadas por estágio
- Escalonamento de ofertas com descontos progressivos
- Limite de tentativas para não incomodar o cliente
- Retomada inteligente da conversa

## Funcionalidades Implementadas

### Atendimento Básico
- Saudação e coleta de informações básicas
- Identificação do tipo de plano desejado
- Coleta de dados específicos (idades, região, preferências)
- Apresentação de cotação personalizada
- Respostas para perguntas frequentes
- Encaminhamento para corretor

### Cotação Avançada
- Cálculos precisos baseados em múltiplos fatores
- Diferentes tipos de planos e coberturas
- Opções com e sem coparticipação
- Consideração de preferências de hospital
- Informações detalhadas sobre cobertura

### Modo de Teste
- Identificação clara de mensagens de teste
- Valores fictícios para demonstração
- Registro detalhado de interações
- Ambiente seguro para treinamento e testes

### Remarketing
- Recuperação de clientes inativos
- Mensagens personalizadas por estágio da conversa
- Ofertas progressivas para incentivar retorno
- Retomada da conversa do ponto onde parou
- Limite de tentativas para respeitar o cliente

## Instruções de Uso

### Requisitos
- Python 3.6 ou superior
- Integração com API de WhatsApp Business ou plataforma de chatbot

### Instalação
1. Clone este repositório
2. Atualize as tabelas de preços no arquivo `sistema_cotacao.py` com valores reais da Plena Saúde
3. Integre o código com sua plataforma de WhatsApp

### Configuração
- Para ambiente de produção: Use `ia_vendedora_remarketing.py` com `modo_teste=False`
- Para ambiente de teste: Use `ia_vendedora_remarketing.py` com `modo_teste=True`
- Ajuste os parâmetros de remarketing conforme necessário:
  - `tempo_inatividade`: Tempo antes de considerar cliente inativo (padrão: 24 horas)
  - `max_tentativas_remarketing`: Número máximo de tentativas (padrão: 3)
  - `intervalo_entre_tentativas`: Tempo entre tentativas (padrão: 24 horas)

## Implementação em Ambiente Real

Para implementar esta solução em um ambiente real de WhatsApp:

1. Integre o código com uma API de WhatsApp Business ou plataforma de chatbot
2. Configure um sistema de agendamento para verificar clientes inativos regularmente
3. Implemente um mecanismo para encaminhar leads qualificados para corretores
4. Atualize regularmente as informações de planos e preços

## Próximos Passos Recomendados

1. **Integração com CRM**: Conectar a IA com um sistema de CRM para rastreamento completo de leads
2. **Análise de Sentimento**: Implementar análise de sentimento para detectar frustração ou satisfação do cliente
3. **Personalização Avançada**: Adicionar mais personalização baseada em histórico do cliente
4. **Expansão Regional**: Adicionar suporte para mais regiões além das três principais
5. **Dashboard de Desempenho**: Criar um painel para monitorar conversões e eficácia do remarketing

## Conclusão

Esta IA vendedora para WhatsApp representa uma solução completa e sofisticada para automatizar o processo de vendas de planos de saúde da Plena Saúde. Com funcionalidades avançadas como cotação personalizada, modo de teste e remarketing, a solução está pronta para aumentar significativamente a eficiência do processo de vendas e a taxa de conversão de leads.

---

Desenvolvido por Manus AI - Abril 2025
