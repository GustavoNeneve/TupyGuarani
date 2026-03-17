# TupyGuarani

Dicionário **Tupy-Guarani → Português** em Python.

## Sobre

Este projeto reúne palavras e expressões do Tupy-Guarani — língua indígena de origem Tupiana amplamente falada no Brasil e nos países vizinhos — com suas traduções para o Português.

O dicionário é armazenado no arquivo [`dicionario.json`](dicionario.json) e pode ser consultado diretamente pela linha de comando ou importado como módulo Python.

## Requisitos

- Python 3.8 ou superior (sem dependências externas)

## Uso

### Linha de comando

```bash
# Buscar uma palavra específica
python dicionario.py pirá

# Listar todas as entradas
python dicionario.py
```

### Como módulo Python

```python
from dicionario import buscar, listar_todas

# Buscar uma palavra
resultados = buscar("pirá")
for r in resultados:
    print(r["tupy_guarani"], "→", r["portugues"])

# Listar todas as entradas em ordem alfabética
for entrada in listar_todas():
    print(entrada["tupy_guarani"], "→", entrada["portugues"])
```

## Estrutura do projeto

```
TupyGuarani/
├── dicionario.json   # Dados do dicionário (entradas Tupy-Guarani / Português)
├── dicionario.py     # Módulo Python para busca e listagem
└── README.md
```

## Exemplo de saída

```
$ python dicionario.py y
y → água, rio

$ python dicionario.py
abá                  → pessoa, gente
abacaxi              → ananás, abacaxi
...
```

## Contribuindo

Para adicionar novas palavras, edite o arquivo `dicionario.json` seguindo o formato:

```json
{ "tupy_guarani": "palavra", "portugues": "tradução em português" }
```