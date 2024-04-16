import os
import env

files = []

for item in env.PEGAR_ARQUIVO_BRUTO:
    footers = os.listdir(item['RODAPE'])
    arts = os.listdir(item['ARTE'])

    if len(footers) > 0 and len(arts) > 0:
        files.append({
            'destFolder': item['DESTINO'],
            'destCompressFolder': item['DESTINO_ARTE'],
            'paths': [item['ARTE'], item['RODAPE']],
            'arts': arts,
            'footers': footers,
        })
