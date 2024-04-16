import os
import time
from datetime import datetime
from PIL import Image
import asyncio
# import env
# import data as files
# import compress


ARQUIVO_BRUTO = "ARQUIVO_BRUTO"
RODAPE_LARGURA = 526
RODAPE_ALTURA = 120
POSICAO_HORIZONTAL= 132
POSICAO_VERTICAL= 1224

SALVAR_ARQUIVO_PRONTO = os.path.join(os.path.dirname(__file__),"ARTES_FINALIZADAS")

PEGAR_ARQUIVO_BRUTO = [{
      'DESTINO': "ME_IGNORA/MG",
      'DESTINO_ARTE': "MG",
      'ARTE': os.path.join(os.path.dirname(__file__), f"{ARQUIVO_BRUTO}/Artes/MG"),
      'RODAPE': os.path.join(os.path.dirname(__file__), f"{ARQUIVO_BRUTO}/Rodapes/MG")
    }]

files = []

for item in PEGAR_ARQUIVO_BRUTO:
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




async def compress_images(from_path, to_path):
    # Define the compression options for each file type
    options = {
        "jpg": {"engine": "mozjpeg", "command": ["-quality", "60"]},
        "png": {"engine": "pngquant", "command": ["--quality=20-50", "-o"]},
        "svg": {"engine": "svgo", "command": "--multipass"},
        "gif": {"engine": "gifsicle", "command": ["--colors", "64", "--use-col=web"]}
    }

    # Get the file extension (type)
    ext = os.path.splitext(from_path)[1].lower()

    # Use the appropriate compression command for the file type
    if ext in options:
        cmd = options[ext]["command"]
        engine = options[ext]["engine"]

        # Compress the image using the command
        # This is a placeholder and may need to be replaced with actual compression code
        print(f"Compressing {from_path} to {to_path} using {engine} with options {cmd}")

        # Simulate async compression with sleep
        await asyncio.sleep(1)

        print(f"Compression of {from_path} completed!")

    else:
        print(f"File type {ext} not supported.")
        

def to_locate(date):
    return date.strftime("%d/%m/%Y, %H:%M:%S")

def console_response(footer_name, dest_folder, start_time):
    print(f"LICENCIADO: {footer_name}, modificou uma arte: {dest_folder}, [INICIO]: {to_locate(start_time)} [FIM]: {to_locate(datetime.now())}")

def watermark(footer, art, paths, dest_folder, dest_compress_folder):
    footer_name = footer.split(".")[0]
    start_time = datetime.now()

    footer_img = Image.open(f"{paths[1]}/{footer}").resize((int(RODAPE_LARGURA), int(RODAPE_ALTURA)))

    image = Image.open(f"{paths[0]}/{art}")

    image.paste(footer_img, (int(POSICAO_HORIZONTAL), int(POSICAO_VERTICAL)), footer_img)

    if not os.path.exists(f"{SALVAR_ARQUIVO_PRONTO}/{dest_folder}/{footer_name}"):
        os.makedirs(f"{SALVAR_ARQUIVO_PRONTO}/{dest_folder}/{footer_name}")

    image.save(f"{SALVAR_ARQUIVO_PRONTO}/{dest_folder}/{footer_name}/{art}")

    console_response(footer_name, dest_folder, start_time)

def read_files(file):
    for footer in file['footers']:
        for art in file['arts']:
            if footer != ".DS_Store" and art != ".DS_Store":
                watermark(footer, art, file['paths'], file['destFolder'], file['destCompressFolder'])

            # time.sleep(0.15)

            footer_name = footer.split(".")[0]
            from_path = f"{SALVAR_ARQUIVO_PRONTO}/{file['destFolder']}/{footer_name}/{art}"
            to_path = f"{SALVAR_ARQUIVO_PRONTO}/{file['destCompressFolder']}/{footer_name}/"

            compress_images(from_path, to_path)

for file in files:
    read_files(file)
