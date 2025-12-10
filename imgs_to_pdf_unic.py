#!/usr/bin/env python3
"""
Convierte todas las imágenes de una carpeta en **un solo PDF** multipágina.

Uso:
    python imagenes_a_pdf_unico.py /ruta/a/carpeta_de_imagenes salida.pdf

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


def listar_imagenes(carpeta: Path):
    archivos = []
    for nombre in sorted(os.listdir(carpeta)):
        ruta = carpeta / nombre
        if ruta.is_file() and ruta.suffix.lower() in EXTENSIONES:
            archivos.append(ruta)
    return archivos


def main():
    if len(sys.argv) != 3:
        print("Uso: python imagenes_a_pdf_unico.py <carpeta_imagenes> <salida.pdf>")
        sys.exit(1)

    carpeta = Path(sys.argv[1])
    salida_pdf = Path(sys.argv[2])

    if not carpeta.is_dir():
        print(f"Error: {carpeta} no es una carpeta válida.")
        sys.exit(1)

    imagenes = listar_imagenes(carpeta)
    if not imagenes:
        print("No se encontraron imágenes en la carpeta.")
        sys.exit(1)

    paginas = []
    for ruta in imagenes:
        try:
            img = Image.open(ruta).convert("RGB")
            paginas.append(img)
        except Exception as e:
            print(f"Advertencia: no se pudo abrir {ruta}: {e}")

    if not paginas:
        print("No se pudo cargar ninguna imagen válida.")
        sys.exit(1)

    primera = paginas[0]
    restantes = paginas[1:]

    salida_pdf.parent.mkdir(parents=True, exist_ok=True)
    primera.save(salida_pdf, save_all=True, append_images=restantes)
    print(f"PDF generado correctamente en: {salida_pdf}")


if __name__ == "__main__":
    main()
