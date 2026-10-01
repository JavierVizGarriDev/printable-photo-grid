# Printable Photo Grid

Dos scripts de Python que generan PDFs listos para imprimir a partir de cuadrículas de imágenes. Creados para automatizar un flujo de trabajo repetitivo en Photoshop en una imprenta.

[![Licencia: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

> 🇪🇸 Español · 🇬🇧 [English version](README.md)

---

## 📖 Descripción general

En la imprenta donde trabajo, los clientes suelen traer decenas de imágenes de cartas, capturas de pantalla o fotos para imprimir en hojas tamaño Carta. El proceso original requería abrir cada imagen en Photoshop, redimensionarla al tamaño exacto, organizarlas manualmente en una cuadrícula e imprimir hoja por hoja.

Estos dos scripts automatizan todo el proceso: leen imágenes desde `input/`, las acomodan en una cuadrícula sobre hojas Carta a 300 DPI y exportan un único PDF multipágina a `output/`.

El primer script se creó para un caso muy concreto (cartas Yu-Gi-Oh, siempre 3×3). El segundo se añadió después para manejar diseños más flexibles cuando aparecieron nuevas necesidades de los clientes. Ambos se conservan en el mismo repositorio porque cada uno tiene su nicho.

---

## 🛠️ Las dos herramientas

| Script | Caso de uso | Configuración |
|---|---|---|
| `yugioh_cards.py` | Cartas Yu-Gi-Oh, siempre 3×3, tamaño exacto de carta | Ninguna — solo ejecutarlo |
| `image_grid.py` | Cualquier diseño: capturas, evidencias legales, fotos enmarcadas | Pregunta columnas, filas y proporción |

### `yugioh_cards.py` — Herramienta especializada

Acomoda las cartas en una cuadrícula fija 3×3 al tamaño exacto de una carta Yu-Gi-Oh real (5.9 × 8.6 cm a 300 DPI). Cero preguntas: pon las imágenes en `input/` y ejecútalo. Salida: `output/Complete_Card_Print.pdf`.

### `image_grid.py` — Herramienta flexible

Pregunta el número de columnas y filas por página, y si se debe mantener la proporción original de cada imagen. Cuando se mantiene, las imágenes se ajustan dentro de su celda y se centran; cuando no, se estiran para llenarla. Salida: `output/Image_Grid_Print.pdf`.

---

## 🚀 Cómo ejecutarlo

### Preparación

```bash
git clone https://github.com/JavierVizGarriDev/printable-photo-grid.git
cd printable-photo-grid
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### Cartas Yu-Gi-Oh

1. Coloca las imágenes de las cartas en `input/` (la carpeta se crea en la primera ejecución si no existe).
2. Ejecuta:
   ```bash
   python yugioh_cards.py
   ```
3. Obtienes `output/Complete_Card_Print.pdf`.

### Cuadrícula personalizada

1. Coloca las imágenes en `input/`.
2. Ejecuta:
   ```bash
   python image_grid.py
   ```
3. Responde a las preguntas (columnas, filas, proporción).
4. Obtienes `output/Image_Grid_Print.pdf`.

---

## 📂 Estructura del proyecto

```
printable-photo-grid/
├── yugioh_cards.py      # Especializado: cuadrícula fija 3×3 para cartas Yu-Gi-Oh
├── image_grid.py        # Flexible: columnas, filas y proporción configurables
├── requirements.txt     # Pillow
├── input/               # Imágenes de origen (gitignored)
└── output/              # PDFs generados (gitignored)
```

---

## 🧠 Notas de diseño

Ambos scripts comparten la misma lógica central: leer imágenes, redimensionarlas, colocarlas en una hoja Carta a 300 DPI y exportar un PDF multipágina. Se mantienen separados a propósito:

- El **script especializado** está optimizado para el caso más común: sin configuración, sin decisiones. Es la opción preferida cuando el formato de salida no cambia.
- El **script flexible** cubre los casos menos frecuentes: cuadrículas personalizadas, proporciones mixtas, formatos que aparecieron con el tiempo.

Se consideró unificarlos en un solo script con flags, pero la simplicidad del especializado es parte de su valor.

---

## ⚙️ Requisitos

- Python 3.10 o superior
- [Pillow](https://python-pillow.org/) (se instala con `requirements.txt`)

Sin otras dependencias. Sin GUI, sin servicios externos.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT — consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Javier A. Vizcaino Garriga**
- GitHub: [@JavierVizGarriDev](https://github.com/JavierVizGarriDev)
- Email: javieralejandrovizcainogarriga@gmail.com

---

<p align="center">
  <i>Automatizando las partes aburridas, un script a la vez.</i>
</p>