import os
import random
import unicodedata
import streamlit as st

st.set_page_config(page_title="Reino de las Palabras Mágicas", page_icon="🦄", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stMarkdown, button, label {font-family:'Fredoka',sans-serif !important;}
.stApp {background: radial-gradient(circle at 10% 0%,#ffe3f3 0%,transparent 40%),
        radial-gradient(circle at 100% 20%,#e0ecff 0%,transparent 45%),
        linear-gradient(160deg,#fff5fb 0%,#f4eaff 100%);}
.block-container {padding-top:1.2rem; max-width:760px;}
h1,h2,h3 {color:#8e2de2 !important;}
.hero {text-align:center;background:linear-gradient(135deg,#ff9ac9,#b388ff 60%,#7cc4ff);color:white;
       border-radius:28px;padding:18px 12px;margin-bottom:12px;box-shadow:0 8px 20px #b388ff55;}
.hero h1 {color:white !important;margin:0;font-size:2rem;}
.hero p {margin:4px 0 0;font-size:1.05rem;opacity:.95;}
.card {background:#ffffffcc;border:3px dashed #e879b9;border-radius:20px;padding:14px 18px;margin:10px 0;font-size:1.1rem;}
.pink {color:#d6336c;font-weight:700;} .blue {color:#1c7ed6;font-weight:700;}
.green {color:#2f9e44;font-weight:700;} .purple {color:#7048e8;font-weight:700;}
.orange {color:#e8590c;font-weight:700;}
/* diapositivas */
.s-head {background:linear-gradient(135deg,var(--c1),var(--c2));border-radius:24px 24px 0 0;padding:16px 18px;color:white;position:relative;}
.s-badge {display:inline-block;background:#ffffff55;border-radius:999px;padding:2px 12px;font-size:.9rem;font-weight:600;}
.s-emoji {font-size:3rem;line-height:1.1;margin-top:4px;}
.s-title {font-size:1.7rem;font-weight:700;margin:0;color:white;}
.s-pag {font-size:.95rem;opacity:.95;}
.s-label {background:#fff;border-left:6px solid var(--c1);padding:6px 14px;font-weight:600;color:#6b2fb3;margin-top:0;}
.s-body {background:#ffffffee;border:3px solid var(--c1);border-top:none;border-radius:0 0 24px 24px;padding:14px 18px 18px;margin-bottom:10px;font-size:1.15rem;}
.s-body ul {margin:6px 0 10px 0;padding-left:1.2rem;} .s-body li {margin:6px 0;}
.chips span {display:inline-block;background:var(--c2);color:#4a2a7a;border-radius:999px;padding:3px 14px;margin:3px 4px 3px 0;font-weight:600;}
.remember {background:#fff8d6;border:2px dashed #f5b700;border-radius:16px;padding:10px 14px;margin-top:10px;font-weight:600;color:#7a5a00;}
.dots {text-align:center;font-size:1.4rem;letter-spacing:6px;margin:4px 0 8px;}
.stTabs [data-baseweb="tab-list"] {gap:6px;flex-wrap:wrap;}
.stTabs [data-baseweb="tab"] {background:#ffffffaa;border-radius:16px;padding:6px 12px;font-weight:600;}
.stTabs [aria-selected="true"] {background:#e879b9 !important;color:white !important;}
div[data-testid="stRadio"] label {font-size:1.1rem;}
.stButton>button {background:linear-gradient(135deg,#ff7eb6,#b388ff);color:white;border-radius:20px;font-size:1.15rem;
                  padding:.5rem 1.2rem;border:none;box-shadow:0 4px 10px #b388ff55;width:100%;}
.stButton>button:disabled {background:#ddd;box-shadow:none;}
</style>
""", unsafe_allow_html=True)

FM = ["Físico", "Comportamiento"]
DA = ["Diminutivo", "Aumentativo"]
PUNTOS = ["Punto y seguido", "Punto y aparte", "Punto final"]

# (pregunta, correcta, opciones, explicación)
ANIMAL = [
    ("Su pelaje es muy abundante y de color marrón claro.", "Físico", FM, "El pelaje se ve: es un rasgo físico."),
    ("Le encanta jugar con todo lo que se encuentra.", "Comportamiento", FM, "Habla de lo que hace: comportamiento."),
    ("Sus ojos son verdes.", "Físico", FM, "El color de los ojos es un rasgo físico."),
    ("Es muy nerviosa.", "Comportamiento", FM, "Cómo se comporta o cómo es su carácter."),
    ("Sus blancos bigotes le dan mucha personalidad.", "Físico", FM, "Los bigotes se ven: físico."),
    ("Se mueve con mucha agilidad.", "Comportamiento", FM, "Cómo se mueve es comportamiento."),
    ("Es una gata cariñosísima y muy mimosona.", "Comportamiento", FM, "Cariñosa y mimosa: cómo actúa."),
    ("Sus patitas son rechonchas.", "Físico", FM, "Las patas son parte del cuerpo."),
    ("La descripción de un animal consiste en explicar...", "cómo son sus rasgos físicos y su comportamiento",
     ["solo cuánto pesa", "solo qué come", "cómo son sus rasgos físicos y su comportamiento"],
     "Se explican los rasgos físicos y el comportamiento."),
]

DIMAUM = [
    ("gatita", "Diminutivo", DA, "Termina en -ita: tamaño menor y cariño."),
    ("ojazos", "Aumentativo", DA, "Termina en -azo: tamaño mayor."),
    ("naricilla", "Diminutivo", DA, "Termina en -illa."),
    ("perrazo", "Aumentativo", DA, "Termina en -azo."),
    ("orejitas", "Diminutivo", DA, "Termina en -ita."),
    ("narizota", "Aumentativo", DA, "Termina en -ota."),
    ("florecillas", "Diminutivo", DA, "Termina en -illa (¡sale en Platero!)."),
    ("cucharón", "Aumentativo", DA, "Termina en -ón."),
    ("¿Cuál de estas terminaciones forma DIMINUTIVOS?", "-illo", ["-illo", "-azo", "-ona"],
     "Diminutivos: -ito, -ita, -illo, -illa."),
    ("¿Cuál de estas terminaciones forma AUMENTATIVOS?", "-ote", ["-ote", "-ito", "-illa"],
     "Aumentativos: -ón, -ona, -azo, -aza, -ote, -ota."),
    ("Diminutivo de «casa»:", "casita", ["casita", "casota", "casazo"], "casa + -ita = casita."),
    ("Aumentativo de «libro»:", "librote", ["librito", "librote", "librillo"], "libro + -ote = librote."),
    ("Los diminutivos indican un tamaño...", "menor (y a veces cariño)", ["mayor", "menor (y a veces cariño)", "igual"],
     "Diminutivos = más pequeño y, a veces, cariño."),
    ("Los aumentativos expresan un tamaño...", "mayor", ["mayor", "menor", "igual"], "Aumentativos = más grande."),
]

PUNTO = [
    ("Separa dos oraciones del mismo párrafo.", "Punto y seguido", PUNTOS, "Seguimos en el mismo párrafo."),
    ("Separa dos oraciones de distintos párrafos.", "Punto y aparte", PUNTOS, "Después empieza otra línea (otro párrafo)."),
    ("Es el que finaliza un texto.", "Punto final", PUNTOS, "Es el último del texto."),
    ("En «Pica es la mascota de Elisa. | Es una gatita...» el punto después de Elisa es...", "Punto y aparte", PUNTOS,
     "Después de Elisa empieza un párrafo nuevo."),
    ("En «...que no lleva huesos. Solo los espejos...» el punto es...", "Punto y seguido", PUNTOS,
     "Sigue el mismo párrafo."),
    ("Las oraciones comienzan con...", "mayúscula", ["mayúscula", "minúscula", "coma"], "Empiezan con mayúscula y terminan con punto."),
    ("¿Cuál de estas palabras lleva mayúscula en una oración?", "Platero", ["burrito", "Platero", "prado"],
     "Los nombres propios (Pica, Elisa, Platero) llevan mayúscula."),
    ("Las oraciones terminan con...", "punto (.)", ["punto (.)", "una mayúscula", "un dibujo"], "Mayúscula al empezar, punto al terminar."),
]

ADJ = [
    ("Wendy es una chica delgada. El adjetivo es...", "delgada", ["Wendy", "chica", "delgada"], "Delgada dice cómo es la chica."),
    ("«pelo rubio»: el adjetivo es...", "rubio", ["pelo", "rubio"], "Rubio dice cómo es el pelo."),
    ("«ojos azules»: el adjetivo es...", "azules", ["ojos", "azules"], "Azules dice cómo son los ojos."),
    ("«juego divertido»: el adjetivo es...", "divertido", ["juego", "divertido"], "Divertido dice cómo es el juego."),
    ("«mochila voladora»: el adjetivo es...", "voladora", ["mochila", "voladora"], "Voladora dice cómo es la mochila."),
    ("«león hambriento»: el adjetivo es...", "hambriento", ["león", "hambriento"], "Hambriento dice cómo está el león."),
    ("Platero es pequeño, peludo y suave. ¿Cuál NO es adjetivo?", "Platero", ["pequeño", "peludo", "Platero"], "Platero es el nombre."),
    ("Un adjetivo es una palabra que...", "dice cómo es o cómo está lo nombrado",
     ["dice cómo es o cómo está lo nombrado", "dice lo que hace alguien", "es el nombre de una persona"],
     "El adjetivo expresa cualidades y estados."),
    ("«comilón» describe a...", "Platero", ["Pica", "Platero"], "Platero come cuanto le dan."),
    ("«ágil» describe a...", "Pica", ["Pica", "Platero"], "Pica se mueve con mucha agilidad."),
    ("«juguetona» describe a...", "Pica", ["Pica", "Platero"], "A Pica le encanta jugar."),
    ("«obediente» describe a...", "Platero", ["Pica", "Platero"], "Platero viene cuando lo llaman."),
]

GENERO = [
    ("Plural de «energía limpia»:", "energías limpias", ["energía limpias", "energías limpias", "energías limpia"],
     "Nombre y adjetivo van en plural: energías limpias."),
    ("Plural de «papel reciclado»:", "papeles reciclados", ["papeles reciclado", "papeles reciclados", "papel reciclados"],
     "papel → papeles; reciclado → reciclados."),
    ("Plural de «trabajo digno»:", "trabajos dignos", ["trabajos dignos", "trabajos digno", "trabajo dignos"],
     "Los dos cambian a plural."),
    ("Plural de «agricultura ecológica»:", "agriculturas ecológicas",
     ["agriculturas ecológica", "agricultura ecológicas", "agriculturas ecológicas"], "Los dos cambian a plural."),
    ("Los adjetivos tienen el mismo ... que el nombre al que acompañan.", "género y número",
     ["género y número", "tamaño y color", "sonido y letra"], "Mismo género (masc./fem.) y mismo número (sing./pl.)."),
    ("Femenino de «perro casero»:", "perra casera", ["perra casero", "perro casera", "perra casera"],
     "El adjetivo cambia igual que el nombre."),
    ("Corrige: «Sus orejitas puntiagudos». Lo correcto es...", "orejitas puntiagudas",
     ["orejitas puntiagudos", "orejitas puntiagudas", "orejita puntiagudas"], "Orejitas es femenino plural → puntiagudas."),
    ("Corrige: «el pelo corta». Lo correcto es...", "el pelo corto", ["el pelo corta", "el pelo corto", "la pelo corto"],
     "Pelo es masculino → corto."),
]

COMPAR = [
    ("«Estaba feliz como unas castañuelas» significa...", "Estar muy alegre.",
     ["Estar muy alegre.", "Moverse mucho.", "Hacer mucho ruido."], "Es una comparación para decir que estaba muy contento."),
    ("«Su pelaje es como el de un peluche» quiere decir que es...", "muy suave y blandito",
     ["muy suave y blandito", "muy duro", "muy sucio"], "Los peluches son blanditos."),
    ("Platero es «fuerte y seco por dentro, como de piedra». Quiere decir que es...", "muy duro y resistente",
     ["muy blando", "muy duro y resistente", "muy pequeño"], "La piedra es dura."),
    ("Las comparaciones en una descripción sirven para...", "entender mejor cómo es algo",
     ["entender mejor cómo es algo", "poner más puntos", "escribir menos"], "Facilitan la comprensión."),
    ("Completa: «El cuello de la jirafa se parece a...»", "una torre muy alta",
     ["una torre muy alta", "una pelota pequeña", "una gota de agua"], "El cuello es largo y alto."),
]

SECCIONES = {
    "🐱 Animal": ("Describir un animal (pág. 32)", ANIMAL),
    "🔍 Diminutivos": ("Diminutivos y aumentativos (págs. 31 y 33)", DIMAUM),
    "🔴 Punto": ("El punto y las mayúsculas (pág. 35)", PUNTO),
    "🌈 Adjetivo": ("Identificar el adjetivo (pág. 36)", ADJ),
    "👫 Género/número": ("Género y número del adjetivo (pág. 36)", GENERO),
    "🍃 Comparar": ("Comparaciones (págs. 32, 33 y 35)", COMPAR),
}


def opciones(q, i):
    o = list(q[2])
    random.Random(f"{q[0]}{i}").shuffle(o)
    return o


def quiz(key, preguntas):
    done = st.session_state.get(f"{key}_done", False)
    for i, q in enumerate(preguntas):
        st.markdown(f"**{i+1}. {q[0]}**")
        st.radio("resp", opciones(q, i), index=None, key=f"{key}_{i}", label_visibility="collapsed", disabled=done)
        if done:
            r = st.session_state.get(f"{key}_{i}")
            if r == q[1]:
                st.success(f"✅ ¡Muy bien! {q[3]}")
            else:
                st.error(f"❌ La respuesta es «{q[1]}». {q[3]}")
    if not done:
        if st.button("✨ Comprobar", key=f"{key}_btn"):
            st.session_state[f"{key}_done"] = True
            st.rerun()
    else:
        ok = sum(st.session_state.get(f"{key}_{i}") == q[1] for i, q in enumerate(preguntas))
        n = len(preguntas)
        st.markdown(f"### {'⭐' * round(5 * ok / n)} {ok} de {n}")
        if ok == n:
            st.balloons()
            st.success("🦄 ¡Perfecto! Eres una campeona del reino.")
        elif ok >= n * 0.7:
            st.info("🧚 ¡Muy bien! Repasa lo que has fallado y vuelve a intentarlo.")
        else:
            st.warning("🌟 ¡Ánimo! Lee la pestaña «Aprende» y prueba otra vez.")
        if st.button("🔄 Repetir", key=f"{key}_rep"):
            for i in range(n):
                st.session_state.pop(f"{key}_{i}", None)
            st.session_state[f"{key}_done"] = False
            st.rerun()



# ---------- AUDIOS ----------
BASE = os.path.dirname(os.path.abspath(__file__))


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower().replace("_", " ").replace("-", " ")


def buscar_audio(clave):
    """Busca el mp3 (en ./audios, ./audio o junto a la app) cuyo nombre empieza por la clave."""
    for carpeta in ("audios", "audio", ""):
        d = os.path.join(BASE, carpeta)
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.lower().endswith(".mp3") and norm(f).startswith(clave):
                    with open(os.path.join(d, f), "rb") as fh:
                        return fh.read()
    return None


# ---------- DIAPOSITIVAS ----------
SLIDES = [
    dict(clave="la descripcion de un animal", emoji="🐱", titulo="Describir un animal", pag="pág. 32",
         c1="#ff7eb6", c2="#ffc2dd",
         puntos=["La descripción de un animal explica <b>cómo es</b>.",
                 "<b>Rasgos físicos</b>: lo que se ve (pelaje, ojos, patas, bigotes).",
                 "<b>Comportamiento</b>: cómo actúa (juguetona, nerviosa, ágil)."],
         ejemplos=["Pica: gatita suave y pequeña", "ojos verdes (físico)", "le encanta jugar (comportamiento)"],
         recuerda="Físico = se ve 👀 · Comportamiento = lo que hace 🏃"),
    dict(clave="los diminutivos indican", emoji="🔍", titulo="Los diminutivos", pag="pág. 31",
         c1="#9775fa", c2="#d0bfff",
         puntos=["Indican un <b>tamaño menor</b> y, a veces, <b>cariño</b>.",
                 "Terminaciones: <b>-ito, -ita, -illo, -illa</b>."],
         ejemplos=["gatita", "patitas", "naricilla", "florecillas", "casita"],
         recuerda="Diminutivo = pequeño y con cariño 💗"),
    dict(clave="los aumentativos expresan", emoji="💪", titulo="Los aumentativos", pag="pág. 33",
         c1="#ff6b6b", c2="#ffc9c9",
         puntos=["Expresan un <b>tamaño mayor</b>.",
                 "Terminaciones: <b>-ón, -ona, -azo, -aza, -ote, -ota</b>."],
         ejemplos=["ojazos", "perrazo", "narizota", "cucharón", "librote"],
         recuerda="Aumentativo = más grande 🐘"),
    dict(clave="las oraciones empiezan", emoji="🔴", titulo="El punto y las mayúsculas", pag="pág. 35",
         c1="#ff922b", c2="#ffd8a8",
         puntos=["Las oraciones empiezan con <b>mayúscula</b> y terminan con <b>punto</b>.",
                 "<b>Punto y seguido</b>: separa oraciones del mismo párrafo.",
                 "<b>Punto y aparte</b>: separa oraciones de distintos párrafos.",
                 "<b>Punto final</b>: termina el texto.",
                 "Los nombres propios también llevan mayúscula."],
         ejemplos=["Pica", "Elisa", "Platero"],
         recuerda="Seguido = sigo en la línea ➡️ · Aparte = párrafo nuevo ⬇️ · Final = fin 🏁"),
    dict(clave="un adjetivo es una palabra", emoji="🌈", titulo="El adjetivo", pag="pág. 36",
         c1="#339af0", c2="#a5d8ff",
         puntos=["Es una palabra que se refiere a un <b>nombre</b>.",
                 "Dice <b>cómo es</b> o <b>cómo está</b> lo nombrado.",
                 "Suele ir junto al nombre, casi siempre <b>después</b>."],
         ejemplos=["chica delgada", "pelo rubio", "ojos azules", "juego divertido", "león hambriento"],
         recuerda="Nombre = la cosa 🧸 · Adjetivo = cómo es ✨"),
    dict(clave="el adjetivo tiene el mismo", emoji="👫", titulo="Género y número del adjetivo", pag="pág. 36",
         c1="#20c997", c2="#96f2d7",
         puntos=["El adjetivo tiene el <b>mismo género</b> (masculino o femenino) que el nombre.",
                 "Y el <b>mismo número</b> (singular o plural)."],
         ejemplos=["energías limpias", "papeles reciclados", "trabajos dignos", "perra casera"],
         recuerda="El adjetivo se pone igual que el nombre 👯"),
    dict(clave="las descripciones usan", emoji="🍃", titulo="Las comparaciones", pag="págs. 32, 33 y 35",
         c1="#51cf66", c2="#b2f2bb",
         puntos=["Se usan para <b>entender mejor</b> cómo es algo.",
                 "Comparan una cosa con otra usando «como»."],
         ejemplos=["como el de un peluche = muy suave", "como de piedra = muy duro", "feliz como unas castañuelas = muy alegre"],
         recuerda="«Como…» nos ayuda a imaginar 💭"),
]

if "slide" not in st.session_state:
    st.session_state["slide"] = 0


def ir(delta):
    st.session_state["slide"] = max(0, min(len(SLIDES) - 1, st.session_state["slide"] + delta))


def mostrar_diapositiva():
    n = len(SLIDES)
    i = st.session_state["slide"]
    s = SLIDES[i]
    st.markdown(
        f'<div class="s-head" style="--c1:{s["c1"]};--c2:{s["c2"]}">'
        f'<span class="s-badge">Diapositiva {i+1} de {n}</span>'
        f'<div class="s-emoji">{s["emoji"]}</div>'
        f'<p class="s-title">{s["titulo"]}</p><div class="s-pag">📖 {s["pag"]}</div></div>'
        f'<div class="s-label" style="--c1:{s["c1"]}">🎧 Escucha la explicación</div>',
        unsafe_allow_html=True)
    audio = buscar_audio(s["clave"])
    if audio:
        st.audio(audio, format="audio/mp3")
    else:
        st.info("🎧 Falta el audio de esta diapositiva: sube el mp3 a la carpeta «audios» del repositorio.")
    puntos = "".join(f"<li>{p}</li>" for p in s["puntos"])
    chips = "".join(f"<span>{e}</span>" for e in s["ejemplos"])
    st.markdown(
        f'<div class="s-body" style="--c1:{s["c1"]};--c2:{s["c2"]}">'
        f'<b>📝 Resumen</b><ul>{puntos}</ul>'
        f'<b>⭐ Ejemplos</b><div class="chips">{chips}</div>'
        f'<div class="remember">💡 {s["recuerda"]}</div></div>',
        unsafe_allow_html=True)
    dots = "".join("🟣" if k == i else "⚪" for k in range(n))
    st.markdown(f'<div class="dots">{dots}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.button("⬅️ Anterior", on_click=ir, args=(-1,), disabled=i == 0, key="prev")
    c2.button("Siguiente ➡️", on_click=ir, args=(1,), disabled=i == n - 1, key="next")
    if i == n - 1:
        st.success("🎉 ¡Has terminado todas las diapositivas! Ahora practica en las otras pestañas.")


st.markdown("""<div class="hero"><h1>🦄 Reino de las Palabras Mágicas 🧚</h1>
<p>Repaso del EXAMEN UNIDAD 2 · Lengua 3.º EP-A · lunes 9 de noviembre</p></div>""", unsafe_allow_html=True)

tabs = st.tabs(["📖 Aprende"] + list(SECCIONES.keys()) + ["🏆 Mini examen"])

with tabs[0]:
    mostrar_diapositiva()

for tab, (nombre, (titulo, preguntas)) in zip(tabs[1:-1], SECCIONES.items()):
    with tab:
        st.subheader(titulo)
        quiz("q_" + nombre, preguntas)

with tabs[-1]:
    st.subheader("🏆 Mini examen (10 preguntas mezcladas)")
    todas = [q for _, (_, p) in SECCIONES.items() for q in p]
    if "mini" not in st.session_state:
        st.session_state["mini"] = random.sample(todas, 10)
    quiz("mini_q", st.session_state["mini"])
    if st.button("🎲 Preguntas nuevas"):
        st.session_state["mini"] = random.sample(todas, 10)
        for i in range(10):
            st.session_state.pop(f"mini_q_{i}", None)
        st.session_state["mini_q_done"] = False
        st.rerun()
