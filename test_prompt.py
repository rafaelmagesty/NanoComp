#!/usr/bin/env python3
"""
Script de teste para os novos prompts simplificados.
Uso: python test_prompt.py
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from models import OllamaClient


def test_prompt(tipo: str, nivel: str, circuito: str, model_version: str = "llama3"):
    """
    Testa um prompt específico.
    
    Args:
        tipo: "tipo1_codigo", "tipo2_documentacao", ou "tipo3_passoapasso"
        nivel: "facil", "medio", ou "dificil"
        circuito: "adicao", "multiplicacao", "ativacao", ou "perceptron"
        model_version: versão do modelo Ollama (padrão: "llama3")
    """
    # Nome do template (sem extensão .txt)
    template_name = f"{tipo}_{nivel}_{circuito}"
    
    print(f"\n{'='*60}")
    print(f"Testando: {template_name}")
    print(f"{'='*60}\n")
    
    try:
        # Inicializa o cliente
        client = OllamaClient(model_version=model_version)
        
        # Prepara os parâmetros
        # Para tipo2, você pode adicionar a documentação aqui
        params = {
            "PROMPT": template_name
        }
        
        # Se for tipo2, adicione a documentação do dnaR
        if tipo == "tipo2_documentacao":
            # Você pode substituir isso pela documentação real do git
            params["DNAR_DOCUMENTATION"] = """
            Documentação da biblioteca DNAr:
            - react(species, ci, reactions, ki, t): função principal para simulação
            - species: vetor de strings com nomes das espécies
            - ci: vetor numérico com concentrações iniciais
            - reactions: vetor de strings com reações no formato 'A -> B'
            - ki: vetor numérico com constantes cinéticas
            - t: vetor numérico com intervalos de tempo
            - plot_behavior(): função para visualizar resultados
            """
        
        # Processa o prompt
        print("Enviando prompt para o modelo...")
        response = client.process(**params)
        
        print("\nResposta do modelo:")
        print("-" * 60)
        print(response)
        print("-" * 60)
        
        return response
        
    except FileNotFoundError as e:
        print(f"Erro: Template não encontrado - {e}")
        print(f"Verifique se o arquivo templates/{template_name}.txt existe")
        return None
    except Exception as e:
        print(f"Erro ao processar: {e}")
        return None


def main():
    """Função principal para testes."""
    
    print("=" * 60)
    print("Teste dos Prompts Simplificados")
    print("=" * 60)
    
    # Exemplo 1: Tipo 1 - Fácil - Adição
    print("\n>>> Exemplo 1: Tipo 1 (Código) - Fácil (Adição)")
    test_prompt("tipo1_codigo", "facil", "adicao")
    
    # Exemplo 2: Tipo 2 - Médio - Multiplicação
    print("\n>>> Exemplo 2: Tipo 2 (Documentação) - Médio (Multiplicação)")
    test_prompt("tipo2_documentacao", "medio", "multiplicacao")
    
    # Exemplo 3: Tipo 3 - Difícil - Perceptron
    print("\n>>> Exemplo 3: Tipo 3 (Passo a Passo) - Difícil (Perceptron)")
    test_prompt("tipo3_passoapasso", "dificil", "perceptron")
    
    print("\n" + "=" * 60)
    print("Testes concluídos!")
    print("=" * 60)


if __name__ == "__main__":
    # Você pode testar um prompt específico passando argumentos
    if len(sys.argv) > 1:
        tipo = sys.argv[1] if len(sys.argv) > 1 else "tipo1_codigo"
        nivel = sys.argv[2] if len(sys.argv) > 2 else "facil"
        circuito = sys.argv[3] if len(sys.argv) > 3 else "adicao"
        model = sys.argv[4] if len(sys.argv) > 4 else "llama3"
        
        test_prompt(tipo, nivel, circuito, model)
    else:
        main()

