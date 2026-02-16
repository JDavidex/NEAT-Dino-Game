# 🦖 **Dino Game con IA - NEAT (NeuroEvolution of Augmenting Topologies)**

Una réplica del icónico juego del dinosaurio de Google Chrome, ahora potenciado con **inteligencia artificial** usando el algoritmo **NEAT**. Los dinosaurios aprenden a jugar por sí mismos a través de evolución neural.

## 🧠 **¿Qué es NEAT?**

**NEAT** (NeuroEvolution of Augmenting Topologies) es un algoritmo de aprendizaje automático que evoluciona redes neuronales artificiales mediante selección natural. En lugar de entrenar una red con retropropagación, NEAT:

- 🧬 **Evoluciona** la estructura de las redes neuronales generación tras generación
- 🎯 **Selecciona** los mejores individuos basándose en su desempeño (fitness)
- 🔄 **Muta** conexiones y nodos para crear nuevas variaciones
- 🏆 **Optimiza** tanto la topología como los pesos de la red

En este proyecto, cada dinosaurio representa un "genoma" con su propia red neuronal que decide cuándo saltar o agacharse.

## 🎮 **¿Cómo funciona?**

Cada generación de 100 dinosaurios juega simultáneamente. Los mejores sobreviven y crean la siguiente generación con mutaciones. El ciclo se repite hasta dominar el juego.

- 📥 **Inputs** (7): Posición del dino, posición/tamaño/tipo del obstáculo, velocidad del juego  
- 📤 **Outputs** (2): Saltar o agacharse (activado si > 0.5)

---

## 📸 **Capturas de pantalla**

![](https://github.com/JDavidex/NEAT-Dino-Game/blob/main/(1).png)
![](https://github.com/JDavidex/NEAT-Dino-Game/blob/main/(2).gif)

---

## 🚀 **Instalación y ejecución**

### Requisitos
- **Python 3.11+**
- **Pygame**
- **NEAT-Python**

### Pasos de instalación

1. Clona este repositorio:
   ```bash
   git clone <repo-url>
   cd NEAT-Dino-Game
   ```

2. Instala las dependencias:
   ```bash
   pip install pygame neat-python
   ```

3. Ejecuta el entrenamiento:
   ```bash
   python dino_game.py
   ```

---

## ⚙️ **Configuración de NEAT**

El archivo `config_neat.txt` contiene los parámetros de evolución:

- **Población**: 100 individuos por generación
- **Fitness threshold**: 10,000 puntos (objetivo a alcanzar)
- **Generaciones**: Configurado para 24 generaciones de entrenamiento
- **Mutaciones**: Tasas de mutación configuradas para conexiones y nodos
- **Activación**: Función tangente hiperbólica (tanh)

## **Sistema de recompensas (Fitness)**

El modelo aprende mediante este sistema de puntuación:

| Acción | Fitness |
|--------|---------|
| Sobrevivir un frame | +0.1 |
| Pasar un obstáculo | +50 |
| Colisionar | -10 |

---

## 🛠️ **Tecnologías utilizadas**

* 🐍 **Python 3.11**
* 🎮 **Pygame**
* 🧠 **NEAT-Python**

---

## 📜 **Créditos**

Proyecto desarrollado con fines educativos y de aprendizaje.  
- Inspirado en el [juego del dinosaurio de Google Chrome](https://en.wikipedia.org/wiki/Dinosaur_Game)
- Algoritmo NEAT desarrollado por Kenneth O. Stanley
- Implementación usando [NEAT-Python](https://neat-python.readthedocs.io/)

## 📝 **Licencia**

Este proyecto es de código abierto y está disponible para experimentación y aprendizaje.

