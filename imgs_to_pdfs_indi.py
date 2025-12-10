#!/usr/bin/env python3
"""
Convierte todas las imágenes de una carpeta en **PDFs individuales** (uno por imagen).

Uso:
    python imagenes_a_pdfs_individuales.py /ruta/a/carpeta_de_imagenes /ruta/a/carpeta_salida

Requisitos:
    pip install pillow
"""

import sys
import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: hace falta instalar Pillow. Ejecuta:")
    print("    pip install pillow")
    sys.exit(1)

EXTENSIONES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def main():
    if len(sys.argv) != 3:
        print("Uso: python imagenes_a_pdfs_individuales.py <carpeta_imagenes> <carpeta_salida>")
        sys.exit(1)

    carpeta_imagenes = Path(sys.argv[1])
    carpeta_salida = Path(sys.argv[2])

    if not carpeta_imagenes.is_dir():
        print(f"Error: {carpeta_imagenes} no es una carpeta válida.")
        sys.exit(1)

    carpeta_salida.mkdir(parents=True, exist_ok=True)

    for nombre in sorted(os.listdir(carpeta_imagenes)):
        ruta_img = carpeta_imagenes / nombre
        if not (ruta_img.is_file() and ruta_img.suffix.lower() in EXTENSIONES):
            continue

        try:
            img = Image.open(ruta_img).convert("RGB")
        except Exception as e:
            print(f"Advertencia: no se pudo abrir {ruta_img}: {e}")
            continue

        salida_pdf = carpeta_salida / (ruta_img.stem + ".pdf")
        img.save(salida_pdf, "PDF")
        print(f"Creado: {salida_pdf}")

    print("Proceso terminado.")


if __name__ == "__main__":
    main()
