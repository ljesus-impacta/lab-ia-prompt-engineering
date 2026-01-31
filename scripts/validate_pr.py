import json
import sys
import os

# Define o caminho do arquivo que contém a resposta da IA.
# Em uma pipeline real, isso poderia vir via argumento (sys.argv)
INPUT_FILE = 'llm_output.json'

def main():
    print(f"🔄 Iniciando validação do arquivo: {INPUT_FILE}...")

    # 1. Verifica se o arquivo existe
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Erro Crítico: O arquivo '{INPUT_FILE}' não foi encontrado.")
        print("Certifique-se de que o passo anterior (chamada à IA) gerou o arquivo corretamente.")
        sys.exit(1) # Falha na pipeline

    # 2. Tenta carregar e fazer o parse do JSON
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Erro de Formatação: A saída da IA não é um JSON válido.")
        print(f"Detalhe do erro: {e}")
        sys.exit(1)

    # 3. Extração segura dos dados (usando .get para evitar crash se faltar chave)
    summary = analysis.get('summary', {})
    
    # Normaliza a decisão para evitar erros de caixa (upper/lower case)
    decision = summary.get('decision', 'Reject').strip()
    severity = summary.get('severity', 'High')
    findings = analysis.get('findings', [])

    # 4. Exibição do Relatório no Console (Logs do CI)
    print(f"\n📊 **RELATÓRIO DE ANÁLISE DE IaC**")
    print(f"===================================")
    print(f"🛡️  Gravidade Global: {severity}")
    print(f"⚖️  Decisão da IA:    {decision}")
    print(f"===================================\n")

    if findings:
        print("📋 **ACHADOS TÉCNICOS:**")
        for i, finding in enumerate(findings, 1):
            # Escolhe ícone baseado na severidade implícita ou categoria
            icon = "🔴" if severity in ['Critical', 'High'] else "⚠️"
            
            cat = finding.get('category', 'Geral')
            line = finding.get('line_number', 'N/A')
            desc = finding.get('description', 'Sem descrição')
            action = finding.get('suggested_action', 'Verificar manualmente')

            print(f"{icon} #{i} [{cat}] (Linha {line})")
            print(f"   Desc: {desc}")
            print(f"   Ação: {action}")
            print("   ---")
    else:
        print("✅ Nenhum problema específico listado no array de 'findings'.")

    # 5. Lógica de Gatekeeper (Bloqueio)
    # Lista de decisões que impedem o merge
    BLOCKING_DECISIONS = ['Reject', 'Request Changes', 'Rejeitar', 'Pedir Mudanças']

    print(f"\n🏁 **VEREDITO FINAL:**")
    
    if decision in BLOCKING_DECISIONS:
        print(f"⛔ **FALHA**: O Pull Request foi bloqueado pela política de segurança.")
        sys.exit(1) # Retorna erro para o Github Actions/Jenkins parar o processo
        
    elif decision == 'Discuss':
        print(f"⚠️ **ALERTA**: Necessário discussão humana, mas não bloqueante automaticamente.")
        # Aqui você decide: sys.exit(0) deixa passar, sys.exit(1) bloqueia.
        # Geralmente 'Discuss' não deve quebrar a build, mas notificar.
        sys.exit(0) 
        
    else:
        print(f"✅ **SUCESSO**: Pull Request aprovado para merge.")
        sys.exit(0)

if __name__ == "__main__":
    main()