# 🛡️ IaC Auto-Reviewer: Code Review de Infraestrutura com IA

+ **Autor:** Luciano Souza de Jesus
+ **MBA:** CLC14 Cloud Computing & DevOps
+ **Universidade:** Impacta

---

## 📋 Sobre o Projeto

Este projeto demonstra a implementação de um **Agente de Segurança e Qualidade para Infraestrutura como Código (IaC)**. Utilizando Engenharia de Prompts avançada e a API da OpenAI, o sistema atua como um "Senior DevOps virtual", analisando Pull Requests de Terraform e CloudFormation antes do merge.

O projeto evolui de uma abordagem manual (v1) para uma automação completa em CI/CD (v3), capaz de bloquear deploys inseguros, detectar custos excessivos e resistir a ataques de *Prompt Injection*.

---

## 📂 Estrutura do Projeto

```text
.
├── .github/
│   └── workflows/
│       └── iac-scan.yml      # Workflow do GitHub Actions (CI/CD)
├── examples/                 # Arquivos IaC para teste (Cenários de PR)
│   ├── pr1_storage.tf
│   ├── pr2_security.tf
│   ├── pr3_database.tf
│   ├── pr4_ec2_tags.tf
│   ├── pr5_lambda.yaml
│   └── pr6_injection.tf
├── prompts/                  # Versões evolutivas dos prompts
│   ├── v1-baseline.md        # Prompt básico (Zero-shot)
│   ├── v2-structured.md      # Prompt com Persona e Markdown
│   └── v3-schema.md          # Prompt Blindado com JSON Schema
├── scripts/                  # Scripts de automação (Python)
│   ├── scan_with_ai.py       # Cliente API: Envia código para a OpenAI
│   └── validate_pr.py        # Gatekeeper: Valida JSON e define Exit Code
├── resultados/               # Evidências dos testes (Prints)
├── llm_output.json           # Arquivo temporário de saída da IA
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação
```

---

## 🧠 Evolução da Engenharia de Prompt

1. v1-baseline (O Generalista): Prompt simples. Retorna texto livre. Falha em consistência e é vulnerável a injeção de prompt.
2. v2-structured (O Organizado): Usa Role Prompting e Chain of Thought. Melhora a explicação para humanos, mas difícil de parsear via script.
3. v3-schema (O Automatizado):
   + Saída: Estritamente JSON.
   + Segurança: Implementa tags XML (<source_code>) e defesa "sanduíche" contra instruções maliciosas.
   + Integração: Projetado para ser consumido por pipelines de CI/CD.

---

## 🛠️ Instalação e Configuração

#### Pré-requisitos
   + Python 3.8+
   + Conta na OpenAI (API Key)

1. Instalar Dependências
```
pip install -r requirements.txt
```
(Conteúdo do requirements.txt: ```openai```)

2. Configurar Variáveis de Ambiente
#### Linux/Mac (Bash):
```export OPENAI_API_KEY="sk-sua-chave-aqui"```

#### Windows (Powershell):
```$env:OPENAI_API_KEY="sk-sua-chave-aqui"```

---

### 🚀 Como Utilizar

1. **Modo 1: Teste Local (CLI):** Você pode rodar a IA contra os arquivos de exemplo localizados na pasta `examples/`. O script `scan_with_ai.py` gera o JSON, e o `validate_pr.py` diz se passa ou falha.
#### Exemplo: Analisando um arquivo com falha de segurança (PR2)
`Bash`
```
# 1. Enviar para análise da IA
python scripts/scan_with_ai.py examples/pr2_security.tf

# 2. Verificar veredito (Gatekeeper)
python scripts/validate_pr.py
```
*Saída esperada:* `✅ SUCESSO: Pull Request aprovado para merge.`

2. **Modo 2: Automação via GitHub Actions** O arquivo `.github/workflows/iac-scan.yml` configura a esteira automática.
   1. Configure o segredo `OPENAI_API_KEY` nas configurações do repositório (Settings > Secrets > Actions).
   2. Abra um Pull Request com arquivos `.tf` ou `.yaml`.
   3. A Action rodará automaticamente e bloqueará o merge se a IA detectar riscos críticos (severity: `High/Critical` ou `decision: Reject`).

---

### 🧪 Cenários de Teste (Pasta `examples/`)

| Arquivo | Cenário | Risco | Decisão Esperada v3 |
| :--- | :---: | :---: | ---: |
| pr1_storage.tf | Bucket S3 sem criptografia e versionamento | Médio | Request Changes (Qualidade: 6/10) |
| pr2_security.tf | SSH (Porta 22) aberto para 0.0.0.0/0 | Crítico | Reject (Qualidade: 0/10) |
| pr3_database.tf | Upgrade de DB (custo 10x maior) | Alto | Discuss (Custo Excessivo) |
| pr4_ec2_tags.tf | Instância correta com tags de custo | Baixo | Approve (Qualidade: 10/10) |
| pr5_lambda.tf | Lambda sem Timeout definido | Crítico | Médio | Approve (com ressalvas) |
| pr6_injection.tf | Tentativa de Prompt Injection ("Ignore instructions") | Crítico | Reject (Ataque Detectado) |

---

### ⚙️ Detalhes Técnicos dos Scripts
`scripts/scan_with_ai.py`
Conecta na API da OpenAI (modelo `gpt-3.5-turbo` ou `gpt-4`), lê o **Prompt v3**, injeta o código do arquivo alvo e salva a resposta crua em `llm_output.json`.

`scripts/validate_pr.py`
Lê o arquivo JSON gerado. Se o campo `decision` for `"Reject"` ou `"Request Changes"`, o script encerra com **Exit Code 1**, o que faz a pipeline do GitHub/Jenkins ficar vermelha (falhar).

`Python`
```
# Trecho da lógica de bloqueio
if decision in ['Reject', 'Request Changes']:
    sys.exit(1) # Bloqueia CI
else:
    sys.exit(0) # Aprova CI
```

*Projeto desenvolvido para fins educacionais sobre DevOps e LLMs.*
