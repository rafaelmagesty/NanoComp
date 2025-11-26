#!/usr/bin/env python3
"""
Script para gerar código R usando DNAr através de prompts.
Permite escolher modelo LLM, tipo de prompt e salvar resultado em CSV.

Uso:
    python gerar_codigo.py --modelo llama3 --tipo tipo1_codigo --nivel facil --circuito adicao --saida resultado.csv
    python gerar_codigo.py -m llama3 -t tipo1_codigo -n facil -c adicao -s resultado.csv
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from models import OllamaClient


# Documentação do DNAr extraída do repositório GitHub
DNAR_DOCUMENTATION = """
DNAr - Simulate Chemical Reaction Networks based on DNA on R

FUNÇÕES PRINCIPAIS:

1. react(species, ci, reactions, ki, t)
   Simula uma Rede de Reações Químicas (CRN) formal.
   
   Parâmetros:
   - species: vetor de strings com os nomes de todas as espécies químicas
   - ci: vetor numérico com as concentrações iniciais (mesma ordem de species)
   - reactions: vetor de strings com as reações no formato 'A -> B' ou 'A + B -> C + Waste'
   - ki: vetor numérico com as constantes cinéticas para cada reação
   - t: vetor numérico com os intervalos de tempo para a simulação
   
   Retorna: data.frame com o comportamento temporal de todas as espécies

2. react_4domain(species, ci, reactions, ki, t, cmax, qmax, alpha, beta)
   Simula uma CRN baseada em DNA usando o modelo de 4 domínios.
   
   Parâmetros adicionais:
   - cmax: concentração máxima para normalização
   - qmax: taxa máxima para normalização
   - alpha: parâmetro de escala (padrão: 1)
   - beta: parâmetro de escala (padrão: 1)
   
   Retorna: lista com 'behavior' (data.frame) e 'dsd' (código Visual DSD)

3. plot_behavior(behavior, species=None, x_label="Time", y_label="Concentration", legend_name="Species")
   Visualiza o comportamento das espécies ao longo do tempo.
   
   Parâmetros:
   - behavior: data.frame retornado por react() ou react_4domain()$behavior
   - species: vetor de strings com nomes das espécies a plotar (opcional)
   - x_label, y_label, legend_name: labels para o gráfico

EXEMPLO BÁSICO:

library(DNAr)
library(ggplot2)
library(dplyr)

# Definir espécies
species <- c("InputA", "InputB", "Output", "Waste")

# Definir reações
reactions <- c("InputA + InputB -> Output + Waste")

# Concentrações iniciais
ci <- c(10, 5, 0, 0)  # InputA=10, InputB=5, Output=0, Waste=0

# Constantes cinéticas
ki <- c(0.1)

# Intervalo de tempo
t <- seq(0, 100, 0.1)

# Executar simulação
result <- react(species, ci, reactions, ki, t)

# Visualizar
plot_behavior(result, species = c("InputA", "InputB", "Output"))

FORMATO DE REAÇÕES:
- Reação simples: 'A -> B'
- Reação com múltiplos reagentes: 'A + B -> C'
- Reação com múltiplos produtos: 'A -> B + C + Waste'
- Reação completa: 'A + B -> C + D + Waste'

NOTAS IMPORTANTES:
- Todas as espécies devem estar definidas no vetor 'species'
- O vetor 'ci' deve ter o mesmo tamanho e ordem de 'species'
- O vetor 'ki' deve ter o mesmo tamanho de 'reactions'
- Use 'Waste' para espécies que são resíduos da reação
"""


def obter_documentacao():
    """Retorna a documentação do DNAr."""
    return DNAR_DOCUMENTATION


def gerar_codigo(modelo: str, tipo: str, nivel: str, circuito: str, saida: str):
    """
    Gera código R usando um prompt específico e salva em CSV.
    
    Args:
        modelo: Nome do modelo Ollama (ex: llama3)
        tipo: Tipo de prompt (tipo1_codigo, tipo2_documentacao, tipo3_passoapasso)
        nivel: Nível de dificuldade (facil, medio, dificil)
        circuito: Tipo de circuito (adicao, multiplicacao, ativacao, perceptron)
        saida: Nome do arquivo CSV de saída
    """
    # Nome do template
    template_name = f"{tipo}_{nivel}_{circuito}"
    
    print(f"\n{'='*70}")
    print(f"Gerando código R com DNAr")
    print(f"{'='*70}")
    print(f"Modelo: {modelo}")
    print(f"Template: {template_name}")
    print(f"Arquivo de saída: {saida}")
    print(f"{'='*70}\n")
    
    try:
        # Inicializa o cliente
        client = OllamaClient(model_version=modelo)
        
        # Prepara os parâmetros
        params = {
            "PROMPT": template_name
        }
        
        # Se for tipo2, adiciona a documentação
        if tipo == "tipo2_documentacao":
            params["DNAR_DOCUMENTATION"] = obter_documentacao()
            print("Incluindo documentação do DNAr no prompt...")
        
        # Processa o prompt
        print(f"Enviando prompt para o modelo {modelo}...")
        codigo_gerado = client.process(**params)
        
        # Prepara dados para CSV
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dados_csv = [
            {
                "timestamp": timestamp,
                "modelo": modelo,
                "tipo_prompt": tipo,
                "nivel": nivel,
                "circuito": circuito,
                "template": template_name,
                "codigo_r": codigo_gerado
            }
        ]
        
        # Salva em CSV
        arquivo_saida = Path(saida)
        arquivo_existe = arquivo_saida.exists()
        
        with open(arquivo_saida, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=dados_csv[0].keys())
            if not arquivo_existe:
                writer.writeheader()
            writer.writerows(dados_csv)
        
        print(f"\n{'='*70}")
        print(f"Código gerado com sucesso!")
        print(f"Salvo em: {arquivo_saida.absolute()}")
        print(f"{'='*70}\n")
        
        return codigo_gerado
        
    except FileNotFoundError as e:
        print(f"\n❌ Erro: Template não encontrado - {e}")
        print(f"Verifique se o arquivo templates/{template_name}.txt existe")
        return None
    except Exception as e:
        print(f"\n❌ Erro ao processar: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Função principal com parser de argumentos."""
    parser = argparse.ArgumentParser(
        description="Gera código R usando DNAr através de prompts LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python gerar_codigo.py -m llama3 -t tipo1_codigo -n facil -c adicao -s resultado.csv
  python gerar_codigo.py --modelo llama3 --tipo tipo2_documentacao --nivel medio --circuito multiplicacao --saida output.csv
  python gerar_codigo.py -m llama3 -t tipo3_passoapasso -n dificil -c perceptron -s perceptron.csv

Tipos de prompt disponíveis:
  - tipo1_codigo: Apenas pede o código
  - tipo2_documentacao: Pede código + documentação do DNAr
  - tipo3_passoapasso: Instruções passo a passo

Níveis disponíveis:
  - facil: Adição simples
  - medio: Multiplicação ou função de ativação
  - dificil: Perceptron (cadeia de operações)

Circuitos disponíveis:
  - adicao: Circuito de adição
  - multiplicacao: Circuito de multiplicação
  - ativacao: Função de ativação (sigmóide)
  - perceptron: Simulação de perceptron
        """
    )
    
    parser.add_argument(
        '-m', '--modelo',
        type=str,
        default='llama3',
        help='Modelo Ollama a ser usado (padrão: llama3)'
    )
    
    parser.add_argument(
        '-t', '--tipo',
        type=str,
        required=True,
        choices=['tipo1_codigo', 'tipo2_documentacao', 'tipo3_passoapasso'],
        help='Tipo de prompt a ser usado'
    )
    
    parser.add_argument(
        '-n', '--nivel',
        type=str,
        required=True,
        choices=['facil', 'medio', 'dificil'],
        help='Nível de dificuldade do circuito'
    )
    
    parser.add_argument(
        '-c', '--circuito',
        type=str,
        required=True,
        choices=['adicao', 'multiplicacao', 'ativacao', 'perceptron', 'relu'],
        help='Tipo de circuito a ser simulado'
    )
    
    parser.add_argument(
        '-s', '--saida',
        type=str,
        required=True,
        help='Nome do arquivo CSV de saída'
    )
    
    args = parser.parse_args()
    
    # Valida combinações
    if args.nivel == 'facil' and args.circuito != 'adicao':
        print("⚠️  Aviso: Nível 'facil' geralmente usa circuito 'adicao'")
    
    if args.nivel == 'medio' and args.circuito not in ['multiplicacao', 'ativacao', 'relu']:
        print("⚠️  Aviso: Nível 'medio' geralmente usa 'multiplicacao' ou 'ativacao'")
    
    if args.nivel == 'dificil' and args.circuito != 'perceptron':
        print("⚠️  Aviso: Nível 'dificil' geralmente usa circuito 'perceptron'")
    
    # Gera o código
    gerar_codigo(
        modelo=args.modelo,
        tipo=args.tipo,
        nivel=args.nivel,
        circuito=args.circuito,
        saida=args.saida
    )


if __name__ == "__main__":
    main()

