# NanoComp

Sistema para geração de código R usando a biblioteca DNAr através de prompts simplificados.

## Estrutura dos Prompts

Foram criados 3 tipos de prompts, cada um com diferentes níveis de complexidade:

### Tipo 1: Apenas Código
Prompts diretos que pedem apenas o código R:
- `tipo1_codigo_facil_adicao.txt` - Adição simples
- `tipo1_codigo_medio_multiplicacao.txt` - Multiplicação
- `tipo1_codigo_medio_ativacao.txt` - Função de ativação
- `tipo1_codigo_dificil_perceptron.txt` - Perceptron

### Tipo 2: Código + Documentação
Prompts que incluem documentação do dnaR:
- `tipo2_documentacao_facil_adicao.txt`
- `tipo2_documentacao_medio_multiplicacao.txt`
- `tipo2_documentacao_medio_ativacao.txt`
- `tipo2_documentacao_dificil_perceptron.txt`

### Tipo 3: Passo a Passo
Prompts com instruções detalhadas passo a passo:
- `tipo3_passoapasso_facil_adicao.txt`
- `tipo3_passoapasso_medio_multiplicacao.txt`
- `tipo3_passoapasso_medio_ativacao.txt`
- `tipo3_passoapasso_dificil_perceptron.txt`

## Como Usar

### Pré-requisitos
- Python 3.7+
- Ollama instalado e rodando
- Modelo LLM configurado no Ollama (ex: llama3)
- Biblioteca `ollama` instalada: `pip install ollama`

### Uso Principal (Recomendado)

O script `gerar_codigo.py` permite escolher modelo, tipo de prompt e salvar resultado em CSV:

```bash
# Forma completa
python gerar_codigo.py --modelo llama3 --tipo tipo1_codigo --nivel facil --circuito adicao --saida resultado.csv

# Forma abreviada
python gerar_codigo.py -m llama3 -t tipo1_codigo -n facil -c adicao -s resultado.csv

# Exemplos com diferentes tipos
python gerar_codigo.py -m llama3 -t tipo2_documentacao -n medio -c multiplicacao -s mult.csv
python gerar_codigo.py -m llama3 -t tipo3_passoapasso -n dificil -c perceptron -s perceptron.csv
```

### Parâmetros do Script

- `-m, --modelo`: Modelo Ollama (padrão: llama3)
- `-t, --tipo`: Tipo de prompt (tipo1_codigo, tipo2_documentacao, tipo3_passoapasso)
- `-n, --nivel`: Nível de dificuldade (facil, medio, dificil)
- `-c, --circuito`: Tipo de circuito (adicao, multiplicacao, ativacao, perceptron)
- `-s, --saida`: Nome do arquivo CSV de saída (obrigatório)

### Teste Rápido (Scripts Antigos)

```bash
# Teste um prompt específico
python test_prompt.py tipo1_codigo facil adicao

# Ou execute todos os exemplos
python test_prompt.py

# Exemplo simples
python exemplo_simples.py
```

### Uso Programático

```python
from models import OllamaClient

# Inicializa o cliente
client = OllamaClient(model_version="llama3")

# Testa um prompt
resultado = client.process(
    PROMPT="tipo1_codigo_facil_adicao"
)

print(resultado)
```

### Parâmetros Disponíveis

- `PROMPT`: Nome do template (sem extensão .txt)
- `VERSION` ou `MODEL_VERSION`: Versão do modelo Ollama
- `DNAR_DOCUMENTATION`: Documentação do dnaR (para tipo2)
- `INPUT_PATH`: Caminho para arquivo de entrada (opcional)

## Exemplos de Uso

### Exemplo 1: Prompt Simples (Tipo 1)
```python
from models import OllamaClient

client = OllamaClient()
resultado = client.process(PROMPT="tipo1_codigo_facil_adicao")
print(resultado)
```

### Exemplo 2: Prompt com Documentação (Tipo 2)
```python
from models import OllamaClient

client = OllamaClient()
resultado = client.process(
    PROMPT="tipo2_documentacao_medio_multiplicacao",
    DNAR_DOCUMENTATION="[sua documentação aqui]"
)
print(resultado)
```

### Exemplo 3: Prompt Passo a Passo (Tipo 3)
```python
from models import OllamaClient

client = OllamaClient()
resultado = client.process(PROMPT="tipo3_passoapasso_dificil_perceptron")
print(resultado)
```