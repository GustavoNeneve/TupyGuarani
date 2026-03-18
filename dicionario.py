"""
Dicionário de Línguas Indígenas → Português
Permite buscar palavras de diversas línguas indígenas brasileiras e obter seus
significados em Português.
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


def buscar(palavra: str, entradas: list = None, lingua: str = None) -> list:
    """
    Busca uma palavra indígena no dicionário.

    Parâmetros
    ----------
    palavra : str
        Palavra ou trecho a ser buscado.
    entradas : list, opcional
        Lista de entradas já carregadas. Se omitido, carrega do arquivo JSON.
    lingua : str, opcional
        Filtra os resultados pela língua especificada. Se omitido, busca em
        todas as línguas.

    Retorno
    -------
    list
        Lista de dicionários com as chaves ``tupy_guarani``, ``portugues`` e,
        opcionalmente, ``lingua`` para cada entrada que corresponda à busca.
    """
    if entradas is None:
        entradas = carregar_dicionario()
    termo = _normalizar(palavra)
    lingua_norm = _normalizar(lingua) if lingua else None
    return [
        entrada
        for entrada in entradas
        if termo in _normalizar(entrada["tupy_guarani"])
        and (
            lingua_norm is None
            or lingua_norm == _normalizar(entrada.get("lingua", ""))
        )
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
        print("Uso: python dicionario.py <palavra> [--lingua <língua>]")
        print("\nTodas as entradas disponíveis:\n")
        for entrada in listar_todas(entradas):
            lingua_info = f"  [{entrada['lingua']}]" if entrada.get("lingua") else ""
            print(f"  {entrada['tupy_guarani']:20s} → {entrada['portugues']}{lingua_info}")
        sys.exit(0)

    # Parse optional --lingua argument
    args = sys.argv[1:]
    lingua_filtro = None
    if "--lingua" in args:
        idx = args.index("--lingua")
        if idx + 1 < len(args):
            lingua_filtro = args[idx + 1]
            args = args[:idx] + args[idx + 2:]

    termo = " ".join(args)
    resultados = buscar(termo, entradas, lingua=lingua_filtro)

    if not resultados:
        msg = f"Nenhuma entrada encontrada para: '{termo}'"
        if lingua_filtro:
            msg += f" (língua: {lingua_filtro})"
        print(msg)
        sys.exit(1)

    for resultado in resultados:
        lingua_info = f"  [{resultado['lingua']}]" if resultado.get("lingua") else ""
        print(f"{resultado['tupy_guarani']} → {resultado['portugues']}{lingua_info}")
