# 🌐 CRFS Señas - Traducción de Lenguaje de Señas a Texto

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
│   └── actions_15.keras
└── README.md

## 🛠️ Tecnologías Utilizadas

- **Flask**: Framework web para Python.
- **Bootstrap**: Framework CSS para un diseño responsive.
- **Keras**: Biblioteca de aprendizaje profundo para construir y entrenar modelos de IA.
- **Mediapipe**: Soluciones de visión por computadora para la detección de gestos.

## 📋 Requisitos

- Python 3.11
- Flask
- Keras
- Mediapipe
- Otros paquetes necesarios listados en `requirements.txt`

## 🛠️ Instalación

### Clonar el Repositorio

Para clonar este proyecto, sigue los siguientes pasos:

1. **Clona el repositorio**:
    ```sh
    git clone https://github.com/tu_usuario/CRFS_Señas.git
    cd CRFS_Señas
    ```

2. **Crea un entorno virtual**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. **Instala las dependencias**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Ejecuta la aplicación**:
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

- Cristian: [cristian@correo.com](mailto:cristian@correo.com)
- Frandy: [frandy@correo.com](mailto:frandy@correo.com)
- Jensey: [jensey@correo.com](mailto:jensey@correo.com)
- Ronald: [ronald@correo.com](mailto:ronald@correo.com)

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
