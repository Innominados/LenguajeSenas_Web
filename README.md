# 🌐 GestureGuide - Traducción de Lenguaje de Señas a Texto

## 🧠 Proyecto Final - Inteligencia Artificial y Lenguaje de Señas

Bienvenidos a **GestureGuide**, un proyecto innovador que traduce lenguaje de señas a texto en tiempo real. Desarrollado por Cristian, Frandy, Jensey, y Ronald, este proyecto utiliza modelos de aprendizaje automático y tecnologías avanzadas de detección de gestos para facilitar la comunicación.

## 🚀 Funcionalidades

- **Traducción en tiempo real** ⏱️: Convierte gestos del lenguaje de señas a texto en cuestión de segundos.
- **Interfaz amigable** 🖥️: Diseñada con Bootstrap para una experiencia de usuario intuitiva.
- **Compatibilidad multiplataforma** 📱: Funciona en cualquier navegador con soporte para cámaras web.
- **Modelos de IA avanzados** 🤖: Utiliza Keras y Mediapipe para una detección de gestos precisa.

## 📁 Estructura del Proyecto

```plaintext
GestureGuide/
├── app.py
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── videosData.json
├── templates/
│   ├── index.html
│   ├── tutorial-page.html
│   ├── starter-page.html
│   └── service-details.html
├── models/
│   └── modeloprueba.keras
└── README.md
 ```
## 🛠️ Tecnologías Utilizadas

- **Flask**: Framework web para Python.
- **Flask-CORS**: Extensión de Flask para manejar Cross-Origin Resource Sharing (CORS).
- **OpenCV (cv2)**: Biblioteca de visión por computadora para el procesamiento de imágenes y videos.
- **NumPy (np)**: Biblioteca para el cálculo numérico y el manejo de arreglos multidimensionales.
- **Mediapipe (Holistic)**: Biblioteca de Google para soluciones de visión por computadora, utilizada para la detección de poses y gestos.
- **TensorFlow y Keras (load_model)**: Biblioteca y API de alto nivel para construir y entrenar modelos de aprendizaje profundo.
- **gTTS**: Google Text-to-Speech, una biblioteca para convertir texto a habla.
- **Pygame**: Biblioteca para desarrollar videojuegos en Python, también utilizada para reproducir audio.
- **Werkzeug (secure_filename)**: Biblioteca que complementa Flask, proporcionando utilidades adicionales.
- **Otros módulos de Python**: 
  - **os**: Interacción con el sistema operativo.
  - **time (sleep)**: Funciones relacionadas con el tiempo.
  - **typing (NamedTuple)**: Anotaciones de tipo en Python.

## 📋 Requisitos

- Python 3.11
- Flask
- Flask-CORS
- OpenCV (cv2)
- NumPy (np)
- Mediapipe
- TensorFlow y Keras
- gTTS
- Pygame
- Otros módulos de Python:
  - os
  - time
  - typing
  - Werkzeug


## 🛠️ Instalación

### Clonar el Repositorio

Para clonar este proyecto, sigue los siguientes pasos:

1. **Clona el repositorio**:
    ```sh
    git clone https://github.com/FrandyAquino/LenguajeSenas_Web.git
    cd LenguajeSenas_Web
    ```

2. **Instala las dependencias**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Ejecuta la aplicación**:
    ```sh
    python app.py
    ```

### 🎥 Uso de la Aplicación

1. **Accede a la aplicación** en tu navegador:
    ```
    http://127.0.0.1:5000
    ```

2. **Permite el acceso a la cámara web** cuando se te solicite.

3. **Empieza a traducir**: Coloca tu mano frente a la cámara y realiza gestos en lenguaje de señas para ver la traducción en tiempo real.

## 🧩 Contribuir

¡Contribuciones son bienvenidas! Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. **Fork el repositorio**
2. **Crea una rama para tu característica** (`git checkout -b feature/AmazingFeature`)
3. **Confirma tus cambios** (`git commit -m 'Add some AmazingFeature'`)
4. **Haz push a la rama** (`git push origin feature/AmazingFeature`)
5. **Abre un Pull Request**

## 📞 Contacto

Si tienes alguna pregunta, no dudes en contactarnos:

- [Frandy Aquino](https://github.com/FrandyAquino) 👨🏽
- [Ronald Serre](https://github.com/ronaldserre) 🧑‍💻
- [Cristian Encarnación](https://github.com/cristianEncarnacion) 🧑🏽‍🦲
- [Jensey Jimenez](https://github.com/JenseyJim) 🧒 

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
