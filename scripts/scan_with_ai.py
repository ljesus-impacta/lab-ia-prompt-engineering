import os
import sys
import json
from openai import OpenAI

# Configuração
PROMPT_PATH = 'prompts/v3-schema.md'
OUTPUT_FILE = 'llm_output.json'
# Modelo a ser usado (gpt-4-turbo ou gpt-3.5-turbo-0125 para economizar)
MODEL_NAME = "gpt-3.5-turbo-0125" 

def load_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{filepath}' não encontrado.")
        sys.exit(1)

def main():
    # 1. Verifica API Key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ Erro: Variável de ambiente OPENAI_API_KEY não definida.")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)

    # 2. Identifica qual arquivo analisar (passado via argumento)
    if len(sys.argv) < 2:
        print("Uso: python scripts/scan_with_ai.py <caminho_do_arquivo_tf>")
        sys.exit(1)
    
    target_file = sys.argv[1]
    print(f"🔍 Lendo arquivo alvo: {target_file}...")
    iac_code = load_file(target_file)

    # 3. Prepara o Prompt (Injeta o código no template v3)
    print(f"📖 Lendo prompt base: {PROMPT_PATH}...")
    base_prompt = load_file(PROMPT_PATH)
    
    # Substitui o placeholder {{CODIGO_DO_PR}} pelo código real
    final_prompt = base_prompt.replace("{{CODIGO_DO_PR}}", iac_code)

    # 4. Chamada à API
    print(f"🚀 Enviando para OpenAI ({MODEL_NAME})...")
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a rigid code analysis engine. Output JSON only."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.0, # Temperatura 0 para máxima consistência
            response_format={"type": "json_object"} # Força saída JSON garantida
        )
        
        ai_content = response.choices[0].message.content
        
        # 5. Salva o resultado
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(ai_content)
            
        print(f"✅ Análise concluída. Resultado salvo em '{OUTPUT_FILE}'.")

    except Exception as e:
        print(f"❌ Erro na comunicação com a API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
