"""
Dicionário Tupy-Guarani → Português
Permite buscar palavras em Tupy-Guarani e obter seus significados em Português.
"""

import json
import os
import unicodedata

_CAMINHO_JSON = os.path.join(os.path.dirname(__file__), "dicionario.json")


def _normalizar(texto: str) -> str:
    """Remove acentos e converte para minúsculas para facilitar a busca."""
    sem_acento = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return sem_acento.lower()


def carregar_dicionario(caminho: str = _CAMINHO_JSON) -> list:
    """Carrega as entradas do dicionário a partir do arquivo JSON."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Arquivo do dicionário não encontrado: {caminho}"
        ) from None
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Arquivo do dicionário com formato inválido: {caminho}"
        ) from exc
    return dados["entradas"]


def buscar(palavra: str, entradas: list = None) -> list:
    """
    Busca uma palavra em Tupy-Guarani no dicionário.

    Parâmetros
    ----------
    palavra : str
        Palavra ou trecho em Tupy-Guarani a ser buscado.
    entradas : list, opcional
        Lista de entradas já carregadas. Se omitido, carrega do arquivo JSON.

    Retorno
    -------
    list
        Lista de dicionários com as chaves ``tupy_guarani`` e ``portugues``
        para cada entrada que corresponda à busca.
    """
    if entradas is None:
        entradas = carregar_dicionario()
    termo = _normalizar(palavra)
    return [
        entrada
        for entrada in entradas
        if termo in _normalizar(entrada["tupy_guarani"])
    ]


def listar_todas(entradas: list = None) -> list:
    """Retorna todas as entradas do dicionário em ordem alfabética."""
    if entradas is None:
        entradas = carregar_dicionario()
    return sorted(entradas, key=lambda e: _normalizar(e["tupy_guarani"]))


if __name__ == "__main__":
    import sys

    entradas = carregar_dicionario()

    if len(sys.argv) < 2:
        print("Uso: python dicionario.py <palavra>")
        print("\nTodas as entradas disponíveis:\n")
        for entrada in listar_todas(entradas):
            print(f"  {entrada['tupy_guarani']:20s} → {entrada['portugues']}")
        sys.exit(0)

    termo = " ".join(sys.argv[1:])
    resultados = buscar(termo, entradas)

    if not resultados:
        print(f"Nenhuma entrada encontrada para: '{termo}'")
        sys.exit(1)

    for resultado in resultados:
        print(f"{resultado['tupy_guarani']} → {resultado['portugues']}")
