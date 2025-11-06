#!/usr/bin/env python3
"""
Exemplo simples e direto para testar um prompt.
"""

from models import OllamaClient

# Inicializa o cliente (usa llama3 por padrão)
client = OllamaClient()

# Testa o prompt mais simples: adição
print("Gerando código para circuito de adição...\n")
resultado = client.process(PROMPT="tipo1_codigo_facil_adicao")

print("=" * 60)
print("CÓDIGO GERADO:")
print("=" * 60)
print(resultado)
print("=" * 60)

