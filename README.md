🌐 CRFS Señas - Traducción de Lenguaje de Señas a Texto

🧠 Proyecto Final - Inteligencia Artificial y Lenguaje de Señas
Bienvenidos a CRFS Señas, un proyecto innovador que traduce lenguaje de señas a texto en tiempo real. Desarrollado por Cristian, Frandy, Jensey, y Ronald, este proyecto utiliza modelos de aprendizaje automático y tecnologías avanzadas de detección de gestos para facilitar la comunicación.

🚀 Funcionalidades
Traducción en tiempo real: Convierte gestos del lenguaje de señas a texto en cuestión de segundos.
Interfaz amigable: Diseñada con Bootstrap para una experiencia de usuario intuitiva.
Compatibilidad multiplataforma: Funciona en cualquier navegador con soporte para cámaras web.
Modelos de IA avanzados: Utiliza Keras y Mediapipe para una detección de gestos precisa.
📁 Estructura del Proyecto
plaintext
Copy code
CRFS_Señas/
├── app.py
├── constants.py
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── videosData.json
├── templates/
│   ├── index.html
│   ├── starter-page.html
│   └── service-details.html
├── models/
│   └── actions_15.keras
└── README.md
🛠️ Tecnologías Utilizadas
Flask: Framework web para Python.
Bootstrap: Framework CSS para un diseño responsive.
Keras: Biblioteca de aprendizaje profundo para construir y entrenar modelos de IA.
Mediapipe: Soluciones de visión por computadora para la detección de gestos.
📋 Requisitos
Python 3.11
Flask
Keras
Mediapipe
Otros paquetes necesarios listados en requirements.txt
🛠️ Instalación
Clonar el Repositorio
Para clonar este proyecto, sigue los siguientes pasos:

Clona el repositorio:

sh
Copy code
git clone https://github.com/tu_usuario/CRFS_Señas.git
cd CRFS_Señas
Crea un entorno virtual:

sh
Copy code
python3 -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
Instala las dependencias:

sh
Copy code
pip install -r requirements.txt
Ejecuta la aplicación:

sh
Copy code
python app.py
🎥 Uso de la Aplicación
Accede a la aplicación en tu navegador:

arduino
Copy code
http://127.0.0.1:5000
Permite el acceso a la cámara web cuando se te solicite.

Empieza a traducir: Coloca tu mano frente a la cámara y realiza gestos en lenguaje de señas para ver la traducción en tiempo real.

🧩 Contribuir
¡Contribuciones son bienvenidas! Si deseas contribuir a este proyecto, por favor sigue estos pasos:

Fork el repositorio
Crea una rama para tu característica (git checkout -b feature/AmazingFeature)
Confirma tus cambios (git commit -m 'Add some AmazingFeature')
Haz push a la rama (git push origin feature/AmazingFeature)
Abre un Pull Request
📞 Contacto
Si tienes alguna pregunta, no dudes en contactarnos:

Cristian: cristian@correo.com
Frandy: frandy@correo.com
Jensey: jensey@correo.com
Ronald: ronald@correo.com
📜 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
