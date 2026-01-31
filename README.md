# 🤖 Automação de Code Review de IaC (Terraform/CloudFormation)

> Este projeto demonstra a evolução de técnicas de Prompt Engineering aplicadas a DevOps, criando um analisador automático de Pull Requests focado em Segurança e Infraestrutura como Código (IaC).

+ **Contexto:** DevOps Engineering  
+ **Autor:** Luciano Souza de Jesus
+ **MBA:** Arquitetura de Soluções em Cloud Computing
+ **Universidade:** Impacta

---

## 📂 Estrutura do Projeto

```plaintext
.
├── prompts/
│   ├── v1-baseline.md       # Prompt Zero-shot (Generalista)
│   ├── v2-structured.md     # Prompt com Persona e CoT (Organizado)
│   └── v3-schema.md         # Prompt JSON/Anti-Injection (Robusto)
├── resultados/
│   ├── (Simulações de saída dos modelos)
└── README.md
```

---

## 🚀 Raciocínio da Evolução dos Prompts

O objetivo central é sair de uma análise genérica e imprevisível para uma integração de **CI/CD robusta**, segura e automatizável. Abaixo, o detalhamento das três fases de maturidade do projeto.

### 1. v1-baseline (O Generalista)
*Uma abordagem inicial "Zero-shot".*

* **🧠 Lógica:** Prompt básico que apenas fornece as regras ao modelo e pede uma análise, sem contexto profundo.
* **⚠️ Problemas:**
    * **Inconsistência:** A saída varia entre texto corrido e tópicos, sem padrão definido.
    * **Falha de Integração:** Difícil de ser consumido por scripts de CI/CD devido à falta de estrutura.
    * **Alucinações:** Alta suscetibilidade a erros factuais e ignorância de nuances.

### 2. v2-structured (O Organizado)
*Introdução de Role Prompting e Chain of Thought (CoT).*

* **🧠 Lógica:**
    * **Persona:** O modelo assume o papel de um "Senior Cloud Security Engineer".
    * **Delimitadores:** Uso claro de separadores para o código.
    * **Chain of Thought:** Solicita a explicação do raciocínio antes do veredito final.
* **✅ Melhorias:** Aumento significativo na qualidade técnica e consistência da análise.
* **⚠️ Problemas:**
    * **Parsing:** Ainda retorna texto livre (Markdown), dificultando o tratamento programático automatizado.
    * **Segurança:** Vulnerável a *Prompt Injection* via comentários maliciosos no código analisado.

### 3. v3-schema (O Robusto & Seguro)
*Foco total em Automação e Segurança (Sandwich Defense).*

* **🧠 Lógica:** Saída estritamente em **JSON** para consumo direto por ferramentas como `jq` ou Python.
* **🛡️ Segurança (Anti-Injection):**
    * **Sandwich Defense:** Instruções de defesa antes e depois do input do usuário.
    * **XML Tags:** Delimitadores estritos para isolar o input.
    * **Tratamento de Dados:** Instrução explícita para tratar o input apenas como dados, ignorando comandos embutidos.
* **⚙️ Critérios Técnicos:** Uso de *Few-Shot Prompting* e Enums para garantir que campos como "Criticidade" sigam valores padrão.

---

## 📊 Comparativo Técnico

| Característica | v1-baseline | v2-structured | v3-schema |
| :--- | :---: | :---: | :---: |
| **Formato de Saída** | Texto Livre (Aleatório) | Markdown Estruturado | JSON Estrito |
| **Técnica Principal** | Zero-shot | Role Prompting / CoT | Sandwich Defense / Schema |
| **Integrabilidade CI/CD** | 🔴 Baixa | 🟡 Média | 🟢 Alta |
| **Segurança** | 🔴 Vulnerável | 🟡 Moderada | 🟢 Robusta |

---

### Como utilizar

1. **Selecione o prompt:** Copie o conteúdo do arquivo desejado na pasta `prompts/`.
2. **Insira o código:** Substitua o placeholder de código pelo seu Terraform ou CloudFormation.
3. **Execute:** Submeta ao seu LLM de preferência (GPT-4, Claude 3, etc.).
4. **Automatize (v3):** Utilize um script para parsear o JSON de resposta e bloquear a pipeline em caso de erros críticos.
