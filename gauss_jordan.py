"""
gauss_jordan.py
---------------
Motor matemático del proyecto: resuelve sistemas de ecuaciones lineales
de m ecuaciones y n incógnitas con el MÉTODO DE GAUSS-JORDAN.

Se usan fracciones exactas (módulo `fractions` de Python) para que NO
haya errores de redondeo: 1/3 se guarda como 1/3, no como 0.3333...

Operaciones elementales de fila que se usan:
  1) Intercambiar dos filas            F1 <-> F2
  2) Multiplicar una fila por k != 0   F1 -> (1/2)·F1
  3) Sumar a una fila otra multiplicada F2 -> F2 - 3·F1
"""

from fractions import Fraction
import copy


# ----------------------------------------------------------------------
# 1. Lectura de números escritos por el usuario
# ----------------------------------------------------------------------
def leer_numero(texto):
    """
    Convierte lo que escribe el usuario en una fracción exacta.
    Acepta: 5, -3, 2.5, 0,75, 1/3, -7/2   (vacío = 0)
    Lanza ValueError si el texto no es un número válido.
    """
    t = str(texto).strip().replace("−", "-").replace(" ", "")
    if t in ("", "+"):
        return Fraction(0)
    if t == "-":
        raise ValueError("solo un signo")
    t = t.replace(",", ".")          # permite coma decimal: 0,5
    try:
        return Fraction(t)
    except ZeroDivisionError:
        raise ValueError("división entre cero")
    except (ValueError, TypeError):
        raise ValueError("no es un número")


# ----------------------------------------------------------------------
# 2. Formato bonito de fracciones
# ----------------------------------------------------------------------
def a_texto(valor, decimales=False):
    """Fracción -> texto. Ej: Fraction(3,4) -> '3/4' o '0.75'."""
    if decimales:
        if valor.denominator == 1:
            return str(valor.numerator)
        texto = f"{float(valor):.4f}".rstrip("0").rstrip(".")
        return "0" if texto in ("-0", "") else texto
    if valor.denominator == 1:
        return str(valor.numerator)
    return f"{valor.numerator}/{valor.denominator}"


def coef_texto(k, decimales=False):
    """Texto de un factor para las operaciones: 1 -> '', -1 -> '-', 2 -> '2·', 1/2 -> '(1/2)·'."""
    if k == 1:
        return ""
    if k == -1:
        return "−"
    s = a_texto(abs(k), decimales)
    signo = "−" if k < 0 else ""
    if "/" in s:
        return f"{signo}({s})·"
    return f"{signo}{s}·"


# ----------------------------------------------------------------------
# 3. El método de Gauss-Jordan
# ----------------------------------------------------------------------
def gauss_jordan(A, b):
    """
    Resuelve A·x = b.

    A: lista de m filas, cada una con n Fractions (coeficientes)
    b: lista de m Fractions (términos independientes)

    Devuelve un diccionario con:
      pasos       -> lista de pasos (descripción, operaciones, matriz, filas cambiadas, pivote)
      final       -> matriz aumentada reducida (forma escalonada reducida)
      tipo        -> 'unica', 'infinitas' o 'ninguna'
      rango_A, rango_Ab
      columnas_pivote, columnas_libres
      solucion    -> (si es única) lista de valores x1..xn
      parametrica -> (si son infinitas) expresión de cada variable
      fila_contradiccion -> (si no hay solución) índice de la fila 0 = c
    """
    m = len(A)
    n = len(A[0]) if m else 0

    # Matriz aumentada [A | b]
    M = [list(map(Fraction, A[i])) + [Fraction(b[i])] for i in range(m)]

    pasos = [{
        "titulo": "Matriz aumentada inicial [A | b]",
        "operaciones": [],
        "matriz": copy.deepcopy(M),
        "filas_cambiadas": [],
        "pivote": None,
    }]

    fila_pivote = 0
    columnas_pivote = []

    for col in range(n):
        if fila_pivote >= m:
            break

        # a) Buscar un pivote distinto de cero en esta columna
        candidata = None
        for i in range(fila_pivote, m):
            if M[i][col] != 0:
                candidata = i
                break

        if candidata is None:
            pasos.append({
                "titulo": f"Columna {col + 1}: no hay pivote (todos son 0) → x{col + 1} será variable libre",
                "operaciones": [],
                "matriz": copy.deepcopy(M),
                "filas_cambiadas": [],
                "pivote": None,
            })
            continue

        # b) Intercambiar filas si el pivote no está en su lugar
        if candidata != fila_pivote:
            M[fila_pivote], M[candidata] = M[candidata], M[fila_pivote]
            pasos.append({
                "titulo": f"Intercambio de filas para tener un pivote ≠ 0 en la columna {col + 1}",
                "operaciones": [f"F{fila_pivote + 1} ↔ F{candidata + 1}"],
                "matriz": copy.deepcopy(M),
                "filas_cambiadas": [fila_pivote, candidata],
                "pivote": (fila_pivote, col),
            })

        # c) Hacer que el pivote valga 1
        piv = M[fila_pivote][col]
        if piv != 1:
            factor = 1 / piv
            M[fila_pivote] = [v * factor for v in M[fila_pivote]]
            pasos.append({
                "titulo": f"Convertir el pivote de la fila {fila_pivote + 1} en 1",
                "operaciones": [f"F{fila_pivote + 1} → {coef_texto(factor) or ''}F{fila_pivote + 1}"],
                "matriz": copy.deepcopy(M),
                "filas_cambiadas": [fila_pivote],
                "pivote": (fila_pivote, col),
            })

        # d) Hacer ceros arriba y abajo del pivote
        ops, cambiadas = [], []
        for i in range(m):
            if i != fila_pivote and M[i][col] != 0:
                k = M[i][col]
                M[i] = [M[i][j] - k * M[fila_pivote][j] for j in range(n + 1)]
                # F_i -> F_i - k·F_p   (si k<0 se muestra como suma)
                if k > 0:
                    ops.append(f"F{i + 1} → F{i + 1} − {coef_texto(k)}F{fila_pivote + 1}")
                else:
                    ops.append(f"F{i + 1} → F{i + 1} + {coef_texto(-k)}F{fila_pivote + 1}")
                cambiadas.append(i)
        if ops:
            pasos.append({
                "titulo": f"Hacer ceros arriba y abajo del pivote en la columna {col + 1}",
                "operaciones": ops,
                "matriz": copy.deepcopy(M),
                "filas_cambiadas": cambiadas,
                "pivote": (fila_pivote, col),
            })

        columnas_pivote.append(col)
        fila_pivote += 1

    rango_A = len(columnas_pivote)

    # ¿Hay alguna fila del tipo  0 0 ... 0 | c  con c != 0 ?
    fila_contra = None
    for i in range(m):
        if all(M[i][j] == 0 for j in range(n)) and M[i][n] != 0:
            fila_contra = i
            break
    rango_Ab = rango_A + (1 if fila_contra is not None else 0)

    columnas_libres = [j for j in range(n) if j not in columnas_pivote]
    res = {
        "pasos": pasos,
        "final": M,
        "m": m,
        "n": n,
        "rango_A": rango_A,
        "rango_Ab": rango_Ab,
        "columnas_pivote": columnas_pivote,
        "columnas_libres": columnas_libres,
        "solucion": None,
        "parametrica": None,
        "fila_contradiccion": fila_contra,
    }

    if fila_contra is not None:
        res["tipo"] = "ninguna"
    elif rango_A == n:
        res["tipo"] = "unica"
        sol = [Fraction(0)] * n
        for fila, col in enumerate(columnas_pivote):
            sol[col] = M[fila][n]
        res["solucion"] = sol
    else:
        res["tipo"] = "infinitas"
        # Cada variable pivote = constante - sum(coef * variable_libre)
        param = {}
        for fila, col in enumerate(columnas_pivote):
            constante = M[fila][n]
            terminos = {j: -M[fila][j] for j in columnas_libres if M[fila][j] != 0}
            param[col] = (constante, terminos)
        for j in columnas_libres:
            param[j] = None  # variable libre
        res["parametrica"] = param

    return res


# ----------------------------------------------------------------------
# 4. Utilidades para explicar el resultado
# ----------------------------------------------------------------------
def expresion_parametrica(constante, terminos, decimales=False, nombres=None):
    """Arma un texto como:  3 − 2·t1 + (1/2)·t2"""
    partes = []
    if constante != 0 or not terminos:
        partes.append(a_texto(constante, decimales))
    for j, k in terminos.items():
        nombre = nombres[j] if nombres else f"x{j + 1}"
        c = coef_texto(abs(k), decimales)
        signo = "−" if k < 0 else "+"
        if not partes:
            partes.append(("−" if k < 0 else "") + c + nombre)
        else:
            partes.append(f"{signo} {c}{nombre}")
    return " ".join(partes)


def verificar(A, b, x):
    """Comprueba A·x = b exactamente. Devuelve lista de (lado_izq, b_i, ok)."""
    filas = []
    for i in range(len(A)):
        izq = sum(Fraction(A[i][j]) * x[j] for j in range(len(x)))
        filas.append((izq, Fraction(b[i]), izq == Fraction(b[i])))
    return filas
