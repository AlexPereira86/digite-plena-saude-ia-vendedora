# IA Vendedora para WhatsApp - Plena Saúde

Este projeto implementa uma IA vendedora para WhatsApp especializada em planos de saúde da Plena Saúde, com foco nas regiões de Francisco Morato, Caieiras e Perus.

## Estrutura do Projeto

O projeto é composto por três componentes principais:

1. **Fluxo de Conversação** (`fluxo_conversacao.md`):
   - Estrutura detalhada do diálogo para atendimento via WhatsApp
   - Mensagens para cada etapa do processo de cotação
   - Respostas para perguntas frequentes

2. **Sistema de Cotação** (`sistema_cotacao.py`):
   - Cálculos para planos individuais, familiares e empresariais
   - Consideração de faixas etárias, quantidade de vidas e preferências
   - Opções de cobertura e coparticipação
   - Informações sobre hospitais por região

3. **IA Vendedora Integrada** (`ia_vendedora_integrada.py`):
   - Integração do fluxo de conversação com o sistema de cotação
   - Coleta de informações do cliente
   - Processamento de perguntas frequentes
   - Geração de cotações personalizadas
   - Encaminhamento para corretores

## Como Usar

### Requisitos

- Python 3.6 ou superior
- Integração com API de WhatsApp Business ou plataforma de chatbot

### Instalação

1. Clone este repositório
2. Atualize as tabelas de preços no arquivo `sistema_cotacao.py` com valores reais da Plena Saúde
3. Integre o código com sua plataforma de WhatsApp

### Execução

Para testar a IA localmente:

```bash
python3 ia_vendedora_integrada.py
```

## Personalização

### Atualização de Preços

Para atualizar os preços dos planos, modifique as tabelas no arquivo `sistema_cotacao.py`:

```python
self.tabela_precos_individual = {
    "0-18": 120.00,  # Atualize com valores reais
    # ...
}
```

### Adição de Hospitais

Para adicionar ou modificar hospitais disponíveis:

```python
self.hospitais_por_regiao = {
    "Francisco Morato": ["Hospital A", "Hospital B"],
    # ...
}
```

## Implementação em Ambiente Real

Para implementar esta solução em um ambiente real de WhatsApp:

1. Integre o código com uma API de WhatsApp Business ou plataforma de chatbot
2. Configure o sistema para receber e processar mensagens
3. Implemente um mecanismo para encaminhar leads qualificados para corretores
4. Atualize regularmente as informações de planos e preços

## Fluxo de Atendimento

1. Saudação inicial
2. Coleta de informações básicas (nome, telefone, e-mail)
3. Identificação do tipo de plano (individual, familiar, empresarial)
4. Coleta de informações específicas (idades, região, preferências)
5. Apresentação da cotação
6. Resposta a perguntas frequentes
7. Encaminhamento para corretor

## Limitações e Melhorias Futuras

- Implementar integração direta com sistemas da Plena Saúde
- Adicionar autenticação e verificação de dados
- Implementar análise de sentimento para melhorar atendimento
- Adicionar suporte a anexos e documentos
