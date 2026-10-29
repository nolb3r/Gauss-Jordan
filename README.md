# Solucionador de Sistemas de Ecuaciones Lineales — Gauss-Jordan

Proyecto Final · Álgebra Lineal · Ing. Rocío Jiménez

Programa en **Python** que resuelve sistemas de **m ecuaciones con n incógnitas** (de 1×1 hasta 10×10)
con el **método de Gauss-Jordan**, mostrando cada operación de fila paso a paso.

## Archivos

| Archivo | Qué hace |
|---|---|
| `gauss_jordan.py` | La matemática: el algoritmo de Gauss-Jordan (con fracciones exactas) |
| `app.py` | La interfaz web (lo que ve el usuario) |
| `requirements.txt` | Librerías necesarias |
| `.streamlit/config.toml` | Colores de la página |
| `iniciar.bat` | Doble clic para abrir el programa en Windows |

## Cómo ejecutarlo en tu computadora

1. Instala Python 3 desde https://python.org (marca la casilla **"Add Python to PATH"**).
2. Abre una terminal en esta carpeta y escribe:
   ```
   pip install -r requirements.txt
   streamlit run app.py
   ```
   (En Windows también puedes hacer doble clic en `iniciar.bat`.)
3. Se abre solo en el navegador en `http://localhost:8501`.

## Cómo obtener el LINK público (para que cualquiera lo use)

Gratis con **Streamlit Community Cloud**:

1. Crea una cuenta en https://github.com y crea un repositorio nuevo (público).
2. Sube estos archivos: `app.py`, `gauss_jordan.py`, `requirements.txt` y la carpeta `.streamlit`.
3. Entra a https://share.streamlit.io e inicia sesión con tu cuenta de GitHub.
4. Clic en **"Create app"** → elige tu repositorio → archivo principal: `app.py` → **Deploy**.
5. En 1–2 minutos te da un link como `https://tu-proyecto.streamlit.app` que funciona para cualquiera.

## Cómo funciona (resumen para la presentación)

1. Se arma la matriz aumentada `[A | b]`.
2. Para cada columna se busca un **pivote** ≠ 0 (si hace falta, se intercambian filas).
3. Se divide la fila para que el pivote sea **1**.
4. Se hacen **ceros** arriba y abajo del pivote.
5. Al final se analiza con **Rouché–Frobenius**:
   - rango(A) = rango([A|b]) = n → **solución única**
   - rango(A) = rango([A|b]) < n → **infinitas soluciones** (variables libres t₁, t₂…)
   - rango(A) < rango([A|b]) → **sin solución** (aparece una fila 0 = c)

Se usan fracciones exactas (`fractions.Fraction`), así que no hay errores de redondeo.
La respuesta se **comprueba** sustituyéndola en las ecuaciones originales.
