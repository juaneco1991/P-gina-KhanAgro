from flask import Flask, render_template

app = Flask(__name__)

PROYECTOS = [
    {
        "nombre": "Agro",
        "carpeta": "AGRO",
        "imagen": "agro.jpeg",
        "descripcion": "Desarrollo de soluciones tecnológicas para el sector agropecuario, automatización y optimización de procesos productivos."
    },
    {
        "nombre": "Electricidad",
        "carpeta": "ELECTRICIDAD",
        "imagen": "electricidad.jpeg",
        "descripcion": "Diseño e implementación de sistemas eléctricos, instalaciones industriales y soluciones energéticas."
    },
    {
        "nombre": "Electrónica",
        "carpeta": "ELECTRONICA",
        "imagen": "electronica.jpeg",
        "descripcion": "Diseño de circuitos electrónicos, sistemas embebidos, instrumentación y control."
    },
    {
        "nombre": "Equipos",
        "carpeta": "EQUIPOS",
        "imagen": "equipos.jpeg",
        "descripcion": "Fabricación, integración y mantenimiento de equipos tecnológicos."
    },
    {
        "nombre": "OIT",
        "carpeta": "OIT",
        "imagen": "oit.jpeg",
        "descripcion": "Desarrollo de proyectos de innovación tecnológica y transformación digital."
    },
    {
        "nombre": "Programación",
        "carpeta": "PROGRAMACION",
        "imagen": "programacion.jpeg",
        "descripcion": "Desarrollo de software, aplicaciones web, móviles, automatización e inteligencia artificial."
    },
    {
        "nombre": "Robótica",
        "carpeta": "ROBOTICA",
        "imagen": "robotica.jpeg",
        "descripcion": "Diseño y construcción de soluciones robóticas para la industria y la educación."
    },
    {
        "nombre": "STEAM",
        "carpeta": "STEAM",
        "imagen": "steam.jpeg",
        "descripcion": "Proyectos educativos basados en Ciencia, Tecnología, Ingeniería, Arte y Matemáticas."
    }
]


@app.route('/')
def inicio():
    return render_template(
        'index.html',
        proyectos=PROYECTOS
    )


if __name__ == '__main__':
    app.run(debug=True)