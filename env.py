import os

ARQUIVO_BRUTO = "ARQUIVO_BRUTO"
RODAPE_LARGURA = 526
RODAPE_ALTURA = 120
POSICAO_HORIZONTAL: 132
POSICAO_VERTICAL: 1224

SALVAR_ARQUIVO_PRONTO = os.path.join(os.path.dirname(__file__), "ARTES_FINALIZADAS"),

PEGAR_ARQUIVO_BRUTO = [{
      'DESTINO': "ME_IGNORA/MG",
      'DESTINO_ARTE': "MG",
      'ARTE': os.path.join(os.path.dirname(__file__), f"{ARQUIVO_BRUTO}/Artes/MG"),
      'RODAPE': os.path.join(os.path.dirname(__file__), f"{ARQUIVO_BRUTO}/Rodapes/MG")
    }]


