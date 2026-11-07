import random
import streamlit as st

st.set_page_config(page_title="Reino de las Palabras Mágicas", page_icon="🦄", layout="centered")

st.markdown("""
<style>
.stApp {background: linear-gradient(160deg,#fff0f8 0%,#f3e8ff 50%,#e6f4ff 100%);}
h1,h2,h3 {color:#8e2de2 !important;}
.card {background:#ffffffcc;border:3px dashed #e879b9;border-radius:20px;padding:14px 18px;margin:10px 0;font-size:1.1rem;}
.big {font-size:1.25rem;}
.pink {color:#d6336c;font-weight:700;} .blue {color:#1c7ed6;font-weight:700;}
.green {color:#2f9e44;font-weight:700;} .purple {color:#7048e8;font-weight:700;}
.orange {color:#e8590c;font-weight:700;}
div[data-testid="stRadio"] label {font-size:1.1rem;}
.stButton>button {background:#e879b9;color:white;border-radius:20px;font-size:1.2rem;padding:.5rem 1.2rem;border:none;}
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


st.title("🦄 Reino de las Palabras Mágicas 🧚")
st.caption("Repaso del EXAMEN UNIDAD 2 · Lengua 3.º EP-A · lunes 9 de noviembre")

tabs = st.tabs(["📖 Aprende"] + list(SECCIONES.keys()) + ["🏆 Mini examen"])

with tabs[0]:
    st.markdown("### 🐱 Descripción de un animal (pág. 32)")
    st.markdown("""<div class="card">La <b>descripción de un animal</b> explica cómo son sus
    <b>rasgos físicos</b> (lo que se ve) y su <b>comportamiento</b> (cómo actúa).<br><br>
    Ejemplos: <i>Pica es una gatita de cuerpo <span class="blue">suave</span> y
    <span class="blue">pequeño</span>.</i> · <i>Platero es pequeño, peludo, suave.</i></div>""", unsafe_allow_html=True)

    st.markdown("### 🔍 Diminutivos (pág. 31)")
    st.markdown("""<div class="card">Los <b>diminutivos</b> indican un <b>tamaño menor</b> y a veces <b>cariño</b>.<br>
    Terminaciones: <span class="purple">-ito, -ita, -illo, -illa</span><br>
    Ejemplos: gat<b>ita</b>, patit<b>as</b>, nariz<b>illa</b>, flor<b>ecillas</b></div>""", unsafe_allow_html=True)

    st.markdown("### 💪 Aumentativos (pág. 33)")
    st.markdown("""<div class="card">Los <b>aumentativos</b> expresan un <b>tamaño mayor</b>.<br>
    Terminaciones: <span class="pink">-ón, -ona, -azo, -aza, -ote, -ota</span><br>
    Ejemplos: oj<b>azos</b>, perr<b>azo</b>, nariz<b>ota</b>, cuchar<b>ón</b></div>""", unsafe_allow_html=True)

    st.markdown("### 🔴 El punto y las mayúsculas (pág. 35)")
    st.markdown("""<div class="card">Las oraciones empiezan con <b>mayúscula</b> y terminan con <b>punto (.)</b><br><br>
    • <b>Punto y seguido</b>: separa dos oraciones del <u>mismo párrafo</u>.<br>
    • <b>Punto y aparte</b>: separa oraciones de <u>distintos párrafos</u>.<br>
    • <b>Punto final</b>: es el que <u>finaliza el texto</u>.<br><br>
    Los nombres propios (Pica, Elisa, Platero) también llevan mayúscula.</div>""", unsafe_allow_html=True)

    st.markdown("### 🌈 El adjetivo (pág. 36)")
    st.markdown("""<div class="card">Un <b>adjetivo</b> es una palabra que se refiere a un <b>nombre</b> y expresa
    <b>cómo es</b> o <b>cómo está</b> lo nombrado.<br><br>
    Wendy es una <span class="orange">chica</span> <span class="blue">delgada</span>, de
    <span class="orange">pelo</span> <span class="blue">rubio</span> y
    <span class="orange">ojos</span> <span class="blue">azules</span>.<br>
    <span class="orange">Naranja = nombre</span> · <span class="blue">Azul = adjetivo</span><br><br>
    • El adjetivo suele ir <b>junto a un nombre</b>: <i>juego divertido</i>.<br>
    • Casi siempre va <b>después</b> del nombre (<i>león hambriento</i>), pero a veces va antes (<i>simpáticos avatares</i>).</div>""",
                unsafe_allow_html=True)

    st.markdown("### 👫 Género y número del adjetivo (pág. 36)")
    st.markdown("""<div class="card">El adjetivo tiene el <b>mismo género</b> (masculino/femenino) y el
    <b>mismo número</b> (singular/plural) que el nombre.<br><br>
    energía limpia → energí<b>as</b> limpi<b>as</b><br>
    papel reciclado → papel<b>es</b> reciclad<b>os</b><br>
    trabajo digno → trabajo<b>s</b> digno<b>s</b></div>""", unsafe_allow_html=True)

    st.markdown("### 🍃 Comparaciones")
    st.markdown("""<div class="card">Las descripciones usan <b>comparaciones</b> para entender mejor:<br>
    <span class="green">como el de un peluche</span> (muy suave) ·
    <span class="green">como de piedra</span> (muy duro) ·
    <span class="green">feliz como unas castañuelas</span> (muy alegre)</div>""", unsafe_allow_html=True)

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
