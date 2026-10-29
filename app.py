"""
app.py
------
Interfaz gráfica (página web) del proyecto.
Se ejecuta con:   streamlit run app.py

Aquí solo va lo VISUAL. Toda la matemática está en gauss_jordan.py
"""

import random
from fractions import Fraction

import streamlit as st

from gauss_jordan import gauss_jordan, leer_numero, a_texto, verificar

MAX_DIM = 10  # tamaño máximo permitido (10 x 10)

st.set_page_config(
    page_title="Gauss-Jordan | Proyecto Final",
    page_icon="🧮",
    layout="wide",
)

# ======================================================================
# ESTILOS (colores inspirados en la presentación del curso)
# ======================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.6rem; max-width: 1200px; }

/* ---------- Encabezado ---------- */
.hero {
  background: linear-gradient(135deg, #C0392B 0%, #E06A5A 100%);
  color: #fff; border-radius: 18px; padding: 26px 32px; margin-bottom: 22px;
  box-shadow: 0 10px 30px rgba(192,57,43,.25);
}
.hero h1 { font-family: 'Fraunces', serif; font-size: 2.3rem; margin: 0; color: #fff; line-height: 1.15; }
.hero p  { margin: 6px 0 0 0; opacity: .92; font-size: 1.02rem; }
.hero .chips span {
  display: inline-block; background: rgba(255,255,255,.18); border: 1px solid rgba(255,255,255,.35);
  padding: 3px 12px; border-radius: 999px; font-size: .82rem; margin: 12px 6px 0 0;
}

/* ---------- Títulos de sección ---------- */
.seccion { display: flex; align-items: center; gap: 10px; margin: 18px 0 8px 0; }
.seccion .num {
  background: #C0392B; color: #fff; width: 30px; height: 30px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .95rem;
}
.seccion h3 { margin: 0; font-family: 'Fraunces', serif; color: #7B241C; font-size: 1.35rem; }

/* ---------- Encabezados de la cuadrícula de entrada ---------- */
.cab { text-align: center; font-family: 'JetBrains Mono', monospace; font-weight: 600;
       color: #7B241C; padding: 4px 0; font-size: .95rem; }
.cab.b { color: #1F618D; }
.etq { font-family: 'JetBrains Mono', monospace; color: #7B241C; font-weight: 600;
       padding-top: 9px; font-size: .9rem; white-space: nowrap; }
div[data-testid="stTextInput"] input {
  text-align: center; font-family: 'JetBrains Mono', monospace; font-weight: 500; font-size: 1rem;
}

/* ---------- Matriz ---------- */
.mwrap { overflow-x: auto; padding: 6px 2px 10px 2px; }
table.mat { border-collapse: separate; border-spacing: 0; margin: 4px auto; }
table.mat td, table.mat th {
  padding: 7px 14px; text-align: center; font-family: 'JetBrains Mono', monospace;
  font-size: 1.02rem; min-width: 46px; color: #2B2B2B;
}
table.mat th { font-size: .78rem; color: #A04030; font-weight: 600; padding-bottom: 2px; }
table.mat th.b { color: #1F618D; }
table.mat td.rl { font-size: .78rem; color: #A04030; font-weight: 600; padding-right: 10px; min-width: 24px; }
/* quitar las líneas de tabla que pone Streamlit por defecto */
table.mat, table.mat tr, table.mat td, table.mat th { border: 0 !important; }
table.mat th, table.mat tr { background: transparent !important; }
/* corchetes [ ] : columnas angostas a cada lado */
table.mat td.bk { min-width: 9px !important; width: 9px; padding: 0 !important; }
table.mat td.bk.L { border-left: 3px solid #2B2B2B !important; }
table.mat td.bk.R { border-right: 3px solid #2B2B2B !important; }
table.mat tr.r0 td.bk { border-top: 3px solid #2B2B2B !important; }
table.mat tr.rl td.bk { border-bottom: 3px solid #2B2B2B !important; }
table.mat th.bk { min-width: 9px; padding: 0; }
/* la raya de la matriz aumentada */
table.mat td.bar { border-left: 2px dashed #1F618D !important; }
table.mat td.bcol { color: #1F618D; font-weight: 600; }
/* fila modificada y pivote */
table.mat tr.cambio td.dato { background: #FDEBD0; }
table.mat td.piv { background: #C0392B !important; color: #fff !important; border-radius: 8px; font-weight: 700; }
table.mat td.contra { background: #FADBD8 !important; }

/* fracciones apiladas */
.fr { display: inline-flex; flex-direction: column; vertical-align: middle; line-height: 1.05; font-size: .9em; }
.fr .n { border-bottom: 1.5px solid currentColor; padding: 0 3px; }
.fr .d { padding: 0 3px; }
.sg { margin-right: 2px; }

/* ---------- Tarjetas de pasos ---------- */
.paso {
  background: #FFFFFF; border: 1px solid #EADBC8; border-left: 5px solid #C0392B;
  border-radius: 14px; padding: 14px 18px 8px 18px; margin: 12px 0;
  box-shadow: 0 2px 10px rgba(0,0,0,.04);
}
.paso .tit { font-weight: 600; color: #2B2B2B; font-size: 1.02rem; }
.paso .tit .n { color: #C0392B; font-family: 'Fraunces', serif; font-weight: 700; margin-right: 6px; }
.op {
  display: inline-block; background: #FBEEE6; color: #7B241C; border: 1px solid #F0C9B8;
  padding: 3px 11px; border-radius: 999px; font-family: 'JetBrains Mono', monospace;
  font-size: .9rem; margin: 8px 6px 0 0;
}

/* ---------- Resultado ---------- */
.res { border-radius: 16px; padding: 18px 22px; margin: 6px 0 14px 0; }
.res h2 { margin: 0 0 4px 0; font-family: 'Fraunces', serif; font-size: 1.6rem; }
.res p { margin: 0; }
.res.unica     { background: #E9F7EF; border: 2px solid #27AE60; } .res.unica h2 { color: #1E8449; }
.res.infinitas { background: #EBF5FB; border: 2px solid #2E86C1; } .res.infinitas h2 { color: #1F618D; }
.res.ninguna   { background: #FDEDEC; border: 2px solid #C0392B; } .res.ninguna h2 { color: #922B21; }

.var-card {
  background: #fff; border: 1px solid #EADBC8; border-radius: 14px; padding: 12px 8px;
  text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,.04); margin-bottom: 10px;
}
.var-card .v { font-family: 'JetBrains Mono', monospace; color: #A04030; font-weight: 600; font-size: .95rem; }
.var-card .x { font-family: 'JetBrains Mono', monospace; font-size: 1.45rem; font-weight: 700; color: #2B2B2B; margin-top: 4px; }

.verif { font-family: 'JetBrains Mono', monospace; font-size: .92rem; padding: 6px 12px;
         border-radius: 10px; background: #fff; border: 1px solid #EADBC8; margin: 5px 0; }
.verif .ok { color: #1E8449; font-weight: 700; }
.verif .no { color: #C0392B; font-weight: 700; }

.leyenda span { display: inline-block; margin-right: 16px; font-size: .85rem; color: #555; }
.leyenda i { display: inline-block; width: 14px; height: 14px; border-radius: 4px; vertical-align: -2px; margin-right: 5px; }
</style>
""", unsafe_allow_html=True)


# ======================================================================
# FUNCIONES PARA DIBUJAR
# ======================================================================
def html_num(v, dec):
    """Número como HTML: fracciones apiladas (3 sobre 4) o decimales."""
    if dec or v.denominator == 1:
        return a_texto(v, dec).replace("-", "−")
    signo = '<span class="sg">−</span>' if v < 0 else ""
    return f'{signo}<span class="fr"><span class="n">{abs(v.numerator)}</span><span class="d">{v.denominator}</span></span>'


def html_matriz(M, dec, cambiadas=(), pivote=None, contra=None, n=None):
    """Dibuja la matriz aumentada [A | b] con corchetes, raya y colores."""
    m = len(M)
    n = len(M[0]) - 1 if n is None else n
    h = ['<div class="mwrap"><table class="mat"><tr><th></th><th class="bk"></th>']
    for j in range(n):
        h.append(f"<th>x<sub>{j + 1}</sub></th>")
    h.append('<th class="b">b</th><th class="bk"></th></tr>')
    for i in range(m):
        clases = []
        if i == 0:
            clases.append("r0")
        if i == m - 1:
            clases.append("rl")
        if i in cambiadas:
            clases.append("cambio")
        h.append(f'<tr class="{" ".join(clases)}"><td class="rl">F{i + 1}</td><td class="bk L"></td>')
        for j in range(n + 1):
            c = ["dato"]
            if j == n:
                c += ["bar", "bcol"]
            if pivote == (i, j):
                c.append("piv")
            if contra == i:
                c.append("contra")
            h.append(f'<td class="{" ".join(c)}">{html_num(M[i][j], dec)}</td>')
        h.append('<td class="bk R"></td></tr>')
    h.append("</table></div>")
    return "".join(h)


def latex_num(v, dec):
    if dec or v.denominator == 1:
        return a_texto(v, dec)
    s = r"\frac{%d}{%d}" % (abs(v.numerator), v.denominator)
    return "-" + s if v < 0 else s


def latex_ecuacion(fila, bi, dec):
    """Ej: [2, -1, 0], 5  ->  2x_1 - x_2 = 5"""
    partes = []
    for j, a in enumerate(fila):
        if a == 0:
            continue
        mag = "" if abs(a) == 1 else latex_num(abs(a), dec)
        var = f"{mag}x_{{{j + 1}}}"
        if not partes:
            partes.append(("-" if a < 0 else "") + var)
        else:
            partes.append(("- " if a < 0 else "+ ") + var)
    izq = " ".join(partes) if partes else "0"
    return f"{izq} = {latex_num(bi, dec)}"


def latex_param(constante, terminos, nombres, dec):
    """Ej: 3, {2: -2}  ->  3 - 2t_1   (x pivote en función de los parámetros)"""
    partes = []
    if constante != 0 or not terminos:
        partes.append(latex_num(constante, dec))
    for j, k in terminos.items():
        mag = "" if abs(k) == 1 else latex_num(abs(k), dec)
        var = f"{mag}t_{{{nombres[j][1:]}}}"
        if not partes:
            partes.append(("-" if k < 0 else "") + var)
        else:
            partes.append(("- " if k < 0 else "+ ") + var)
    return " ".join(partes)


def titulo_seccion(num, texto):
    st.markdown(f'<div class="seccion"><div class="num">{num}</div><h3>{texto}</h3></div>',
                unsafe_allow_html=True)


# ======================================================================
# EJEMPLOS LISTOS PARA LA PRESENTACIÓN
# ======================================================================
EJEMPLOS = {
    "✅ 3×3 solución única": ([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]),
    "♾️ 2×3 infinitas soluciones": ([[1, 2, -1], [2, 4, 1]], [3, 9]),
    "❌ 3×3 sin solución": ([[1, 1, 1], [2, 2, 2], [1, -1, 0]], [3, 7, 1]),
    "📐 3×2 (más ecuaciones)": ([[1, 1], [1, -1], [2, 3]], [5, 1, 12]),
    "🔢 4×4 con fracciones": ([["1/2", 1, 0, 2], [1, -1, 3, 0], [0, 2, 1, "-1"], [3, 0, -2, 1]], [4, 2, "5/2", 1]),
}


def cargar(A, b):
    st.session_state["m"] = len(A)
    st.session_state["n"] = len(A[0])
    for i in range(MAX_DIM):
        for j in range(MAX_DIM + 1):
            st.session_state[f"c_{i}_{j}"] = ""
    for i, fila in enumerate(A):
        for j, v in enumerate(fila):
            st.session_state[f"c_{i}_{j}"] = str(v)
        st.session_state[f"c_{i}_{len(fila)}"] = str(b[i])
    st.session_state["resuelto"] = True


def limpiar():
    for i in range(MAX_DIM):
        for j in range(MAX_DIM + 1):
            st.session_state[f"c_{i}_{j}"] = ""
    st.session_state["resuelto"] = False


def aleatorio():
    """Sistema aleatorio del tamaño actual con solución entera (si es cuadrado)."""
    m, n = st.session_state["m"], st.session_state["n"]
    x = [random.randint(-5, 5) for _ in range(n)]
    A = [[random.randint(-6, 6) for _ in range(n)] for _ in range(m)]
    b = [sum(A[i][j] * x[j] for j in range(n)) for i in range(m)]
    cargar(A, b)


# Estado inicial
if "m" not in st.session_state:
    cargar(*EJEMPLOS["✅ 3×3 solución única"])
    st.session_state["resuelto"] = False


# ======================================================================
# BARRA LATERAL
# ======================================================================
with st.sidebar:
    st.markdown("## ⚙️ Configuración")
    st.number_input("Número de ecuaciones (m · filas)", 1, MAX_DIM, key="m", step=1)
    st.number_input("Número de incógnitas (n · columnas)", 1, MAX_DIM, key="n", step=1)
    st.caption(f"Sistema de **{st.session_state['m']} × {st.session_state['n']}**")

    st.markdown("### 👁️ Mostrar números como")
    modo = st.radio("Formato", ["Fracciones", "Decimales"], horizontal=True, label_visibility="collapsed")
    dec = modo == "Decimales"

    st.markdown("### 📚 Ejemplos")
    for nombre, (A_ej, b_ej) in EJEMPLOS.items():
        st.button(nombre, on_click=cargar, args=(A_ej, b_ej), use_container_width=True)

    st.markdown("### 🛠️ Herramientas")
    c1, c2 = st.columns(2)
    c1.button("🎲 Aleatorio", on_click=aleatorio, use_container_width=True)
    c2.button("🧹 Limpiar", on_click=limpiar, use_container_width=True)

    st.divider()
    st.caption("Proyecto Final · Álgebra Lineal\nIng. Rocío Jiménez\n\nMétodo: **Gauss-Jordan**")


# ======================================================================
# ENCABEZADO
# ======================================================================
st.markdown("""
<div class="hero">
  <h1>Solucionador de Sistemas de Ecuaciones Lineales</h1>
  <p>Resuelve cualquier sistema de <b>m ecuaciones</b> con <b>n incógnitas</b> usando el
  <b>Método de Gauss-Jordan</b>, mostrando cada operación de fila paso a paso.</p>
  <div class="chips"><span>🐍 Python</span><span>📐 Álgebra Lineal</span>
  <span>🔢 Fracciones exactas</span><span>📝 Paso a paso</span></div>
</div>
""", unsafe_allow_html=True)

tab_resolver, tab_teoria = st.tabs(["🧮 Resolver sistema", "📘 ¿Cómo funciona Gauss-Jordan?"])


# ======================================================================
# PESTAÑA 1: RESOLVER
# ======================================================================
with tab_resolver:
    m, n = int(st.session_state["m"]), int(st.session_state["n"])

    # ---------- 1. Entrada de datos ----------
    titulo_seccion(1, "Ingresa los coeficientes del sistema")
    st.caption("Puedes escribir enteros (5), negativos (-3), decimales (2.5) o fracciones (1/3). "
               "Una casilla vacía cuenta como 0.  La columna **b** es el resultado de cada ecuación.")

    anchos = [0.7] + [1] * n + [0.15, 1]
    cab = st.columns(anchos)
    cab[0].markdown("&nbsp;", unsafe_allow_html=True)
    for j in range(n):
        cab[j + 1].markdown(f'<div class="cab">x<sub>{j + 1}</sub></div>', unsafe_allow_html=True)
    cab[n + 2].markdown('<div class="cab b">b</div>', unsafe_allow_html=True)

    for i in range(m):
        fila = st.columns(anchos)
        fila[0].markdown(f'<div class="etq">Ec. {i + 1}</div>', unsafe_allow_html=True)
        for j in range(n):
            fila[j + 1].text_input(f"a{i}{j}", key=f"c_{i}_{j}", label_visibility="collapsed",
                                   placeholder="0")
        fila[n + 1].markdown('<div class="etq" style="text-align:center;color:#1F618D">|</div>',
                             unsafe_allow_html=True)
        fila[n + 2].text_input(f"b{i}", key=f"c_{i}_{n}", label_visibility="collapsed",
                               placeholder="0")

    # ---------- Validar lo escrito ----------
    errores = []
    A, b = [], []
    for i in range(m):
        fila_A = []
        for j in range(n + 1):
            texto = st.session_state.get(f"c_{i}_{j}", "")
            try:
                v = leer_numero(texto)
            except ValueError as e:
                nombre = "b" if j == n else f"x{j + 1}"
                errores.append(f"Ecuación {i + 1}, columna **{nombre}**: «{texto}» → {e}")
                v = Fraction(0)
            if j < n:
                fila_A.append(v)
            else:
                b.append(v)
        A.append(fila_A)

    if errores:
        st.error("⚠️ Hay valores que no son números válidos. Corrígelos para poder resolver:\n\n- "
                 + "\n- ".join(errores))
    else:
        # Vista previa del sistema
        with st.container(border=True):
            st.markdown("**Así queda tu sistema de ecuaciones:**")
            sistema = r" \\ ".join(latex_ecuacion(A[i], b[i], dec) for i in range(m))
            st.latex(r"\begin{cases}" + sistema + r"\end{cases}")

    col_btn, _ = st.columns([1, 2])
    if col_btn.button("🚀 Resolver con Gauss-Jordan", type="primary", use_container_width=True,
                      disabled=bool(errores)):
        st.session_state["resuelto"] = True

    # ---------- 2. Resultado ----------
    if st.session_state.get("resuelto") and not errores:
        r = gauss_jordan(A, b)

        titulo_seccion(2, "Resultado")
        info_rango = (f"rango(A) = <b>{r['rango_A']}</b> &nbsp;·&nbsp; rango([A|b]) = <b>{r['rango_Ab']}</b>"
                      f" &nbsp;·&nbsp; incógnitas n = <b>{n}</b>")

        if r["tipo"] == "unica":
            st.markdown(f'<div class="res unica"><h2>✅ El sistema tiene SOLUCIÓN ÚNICA</h2>'
                        f'<p>Sistema compatible determinado: {info_rango} (rango = n)</p></div>',
                        unsafe_allow_html=True)
            por_fila = min(n, 5)
            for inicio in range(0, n, por_fila):
                cols = st.columns(por_fila)
                for k, j in enumerate(range(inicio, min(inicio + por_fila, n))):
                    cols[k].markdown(
                        f'<div class="var-card"><div class="v">x<sub>{j + 1}</sub></div>'
                        f'<div class="x">{html_num(r["solucion"][j], dec)}</div></div>',
                        unsafe_allow_html=True)

            with st.expander("✔️ Comprobación: sustituir la solución en cada ecuación", expanded=True):
                for i, (izq, bi, ok) in enumerate(verificar(A, b, r["solucion"])):
                    sust = " + ".join(f"({a_texto(A[i][j], dec)})({a_texto(r['solucion'][j], dec)})"
                                      for j in range(n))
                    marca = '<span class="ok">✔ correcto</span>' if ok else '<span class="no">✘</span>'
                    st.markdown(f'<div class="verif">Ec. {i + 1}: {sust} = <b>{a_texto(izq, dec)}</b>'
                                f' &nbsp;=&nbsp; b<sub>{i + 1}</sub> = {a_texto(bi, dec)} &nbsp; {marca}</div>',
                                unsafe_allow_html=True)

        elif r["tipo"] == "infinitas":
            libres = r["columnas_libres"]
            nombres = {j: f"t{k + 1}" for k, j in enumerate(libres)}
            st.markdown(f'<div class="res infinitas"><h2>♾️ El sistema tiene INFINITAS SOLUCIONES</h2>'
                        f'<p>Sistema compatible indeterminado: {info_rango} (rango &lt; n). '
                        f'Hay <b>{len(libres)}</b> variable(s) libre(s).</p></div>',
                        unsafe_allow_html=True)
            st.markdown("**Solución general** (cada parámetro t puede ser cualquier número real):")
            lineas = []
            for j in range(n):
                v = r["parametrica"][j]
                if v is None:
                    lineas.append(f"x_{{{j + 1}}} = t_{{{nombres[j][1:]}}} \\quad (\\text{{libre}})")
                else:
                    c, t = v
                    lineas.append(f"x_{{{j + 1}}} = {latex_param(c, t, nombres, dec)}")
            st.latex(r"\begin{cases}" + r" \\ ".join(lineas) + r"\end{cases}")

            # Una solución particular (todos los parámetros = 0) para comprobar
            x0 = [Fraction(0)] * n
            for j, v in r["parametrica"].items():
                if v is not None:
                    x0[j] = v[0]
            with st.expander("✔️ Ejemplo: solución particular con todos los parámetros = 0", expanded=True):
                st.markdown(" &nbsp;,&nbsp; ".join(f"x<sub>{j + 1}</sub> = <b>{html_num(x0[j], dec)}</b>"
                                         for j in range(n)), unsafe_allow_html=True)
                todas_ok = all(ok for *_, ok in verificar(A, b, x0))
                if todas_ok:
                    st.success("Al sustituirla, se cumplen todas las ecuaciones del sistema.")
                else:
                    st.error("La comprobación falló.")

        else:
            fc = r["fila_contradiccion"]
            st.markdown(f'<div class="res ninguna"><h2>❌ El sistema NO tiene solución</h2>'
                        f'<p>Sistema incompatible: {info_rango} (rango(A) ≠ rango([A|b])).</p></div>',
                        unsafe_allow_html=True)
            st.markdown(f"La fila **F{fc + 1}** de la matriz final quedó así:")
            st.latex(r"0x_1 + \dots + 0x_n = " + latex_num(r["final"][fc][n], dec)
                     + r"\quad \Longrightarrow \quad 0 = " + latex_num(r["final"][fc][n], dec)
                     + r"\quad \text{(¡imposible!)}")

        # Matriz final
        st.markdown("**Matriz final (forma escalonada reducida):**")
        st.markdown(html_matriz(r["final"], dec, contra=r["fila_contradiccion"]), unsafe_allow_html=True)

        # ---------- 3. Paso a paso ----------
        titulo_seccion(3, "Procedimiento paso a paso")
        st.markdown('<div class="leyenda"><span><i style="background:#C0392B"></i>Pivote</span>'
                    '<span><i style="background:#FDEBD0;border:1px solid #F0C9B8"></i>Fila modificada</span>'
                    '<span><i style="border:2px dashed #1F618D"></i>Separa A de b</span></div>',
                    unsafe_allow_html=True)

        pasos = r["pasos"]
        vista = st.radio("Vista", ["📜 Todos los pasos", "🎬 Uno por uno (modo presentación)"],
                         horizontal=True, label_visibility="collapsed")

        def dibujar_paso(k, p):
            ops = "".join(f'<span class="op">{o}</span>' for o in p["operaciones"])
            st.markdown(
                f'<div class="paso"><div class="tit"><span class="n">Paso {k}</span>{p["titulo"]}</div>'
                f'{ops}{html_matriz(p["matriz"], dec, p["filas_cambiadas"], p["pivote"])}</div>',
                unsafe_allow_html=True)

        if vista.startswith("📜"):
            for k, p in enumerate(pasos):
                dibujar_paso(k, p)
        else:
            if len(pasos) > 1:
                k = st.slider("Paso", 0, len(pasos) - 1, 0, key=f"slider_{m}_{n}_{len(pasos)}")
            else:
                k = 0
            dibujar_paso(k, pasos[k])
            st.caption(f"Paso {k} de {len(pasos) - 1}. Mueve la barra para avanzar o retroceder.")

        st.caption(f"Total de pasos realizados: **{len(pasos) - 1}**")


# ======================================================================
# PESTAÑA 2: TEORÍA (útil para la presentación)
# ======================================================================
with tab_teoria:
    st.markdown("### ¿Qué es el método de Gauss-Jordan?")
    st.markdown(
        "Es un método para resolver sistemas de ecuaciones lineales transformando la "
        "**matriz aumentada** `[A | b]` en su **forma escalonada reducida**, usando solo "
        "**operaciones elementales de fila**. Al final, la solución se lee directamente.")
    st.latex(r"A\,X = C \quad\Longrightarrow\quad [\,A \mid C\,] \;\xrightarrow{\text{operaciones de fila}}\; [\,I \mid X\,]")

    c1, c2, c3 = st.columns(3)
    c1.info("**1. Intercambiar filas**\n\n`F1 ↔ F2`\n\nSe usa cuando el pivote es 0.")
    c2.info("**2. Multiplicar una fila**\n\n`F1 → (1/2)·F1`\n\nPara convertir el pivote en 1.")
    c3.info("**3. Sumar un múltiplo**\n\n`F2 → F2 − 3·F1`\n\nPara hacer ceros arriba y abajo.")

    st.markdown("### Algoritmo que sigue el programa")
    st.markdown(
        "1. Se arma la matriz aumentada `[A | b]` de tamaño **m × (n+1)**.\n"
        "2. Para cada columna, se busca un **pivote** distinto de 0 (si hace falta, se intercambian filas).\n"
        "3. Se divide la fila del pivote para que el pivote valga **1**.\n"
        "4. Se hacen **ceros** en todas las demás filas de esa columna (arriba y abajo).\n"
        "5. Se repite con la siguiente columna hasta terminar.\n"
        "6. Se analiza la matriz final para saber qué tipo de solución tiene.")

    st.markdown("### ¿Cómo se sabe el tipo de solución? (Teorema de Rouché–Frobenius)")
    st.markdown(
        "| Condición | Tipo de sistema | Resultado |\n"
        "|---|---|---|\n"
        "| rango(A) = rango([A\\|b]) = n | Compatible determinado | ✅ Solución única |\n"
        "| rango(A) = rango([A\\|b]) < n | Compatible indeterminado | ♾️ Infinitas soluciones |\n"
        "| rango(A) < rango([A\\|b]) | Incompatible | ❌ Sin solución (aparece 0 = c) |")

    st.markdown("### Detalles técnicos")
    st.markdown(
        "- **Lenguaje:** Python 3 · **Interfaz:** Streamlit (página web).\n"
        "- Usa **fracciones exactas** (`fractions.Fraction`), así que no hay errores de redondeo: "
        "1/3 se guarda como 1/3 y no como 0.3333.\n"
        "- Funciona para cualquier tamaño **m × n** (de 1×1 hasta 10×10), sea cuadrado o no.")
