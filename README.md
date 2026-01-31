Autor: Luciano Souza de Jesus Contexto: DevOps Engineering - Automação de Code Review de IaC

Raciocínio da Evolução dos Prompts
O objetivo deste projeto é criar um analisador automático de Pull Requests focado em Terraform/CloudFormation, evoluindo da análise genérica para uma análise estruturada e segura.

v1-baseline (O Generalista):

Lógica: É um prompt "zero-shot" básico. Ele apenas joga as regras no modelo e pede uma análise.

Problemas: A saída é inconsistente. Às vezes retorna texto corrido, às vezes tópicos. É difícil de integrar em uma pipeline de CI/CD (o script falharia ao tentar ler o resultado). É altamente suscetível a alucinações e ignora nuances de contexto.

v2-structured (O Organizado):

Lógica: Introduzimos "Persona" (Role Prompting) e "Delimitadores". Definimos claramente a estrutura de saída (Markdown com seções) e usamos Chain of Thought (pedindo para o modelo explicar o raciocínio antes de dar o veredito).

Melhoria: Aumenta a consistência e a qualidade da análise técnica. O modelo entende que age como um "Senior Cloud Security Engineer".

Problemas: Ainda retorna texto livre, difícil de parsear programaticamente. Ainda vulnerável a injeção se o código contiver comentários maliciosos.

v3-schema (O Robusto & Seguro):

Lógica: Focado em automação total. A saída é estritamente JSON (para consumo via jq ou scripts Python na pipeline).

Segurança (Anti-Injection): Utilizamos a técnica de "Sandwich Defense" e delimitadores claros (XML tags). Instruímos explicitamente o modelo a tratar o input do usuário apenas como dados e ignorar comandos embutidos nele.

Critérios: Usamos Few-Shot Prompting (exemplos) ou definições estritas de esquema para garantir que "Criticidade" seja apenas um dos valores permitidos (enum).
