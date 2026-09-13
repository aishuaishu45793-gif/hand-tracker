# ✋ Hand Tracker

A real-time **Hand Tracking application** that uses computer vision and machine learning techniques to detect and track hand movements through a webcam.

The project processes live video frames, identifies the hand, detects hand landmarks, and tracks hand movement in real time.

## 🚀 Features

* 📷 Real-time webcam video processing
* ✋ Hand detection and tracking
* 📍 Detection of hand landmarks
* 🖐️ Tracks hand and finger movements
* ⚡ Real-time processing
* 💻 Simple and interactive interface
* 🎯 Useful for gesture-based applications
* 🔍 Computer vision-based hand tracking

## 🛠️ Technologies Used

* **Python**
* **OpenCV** – Image and video processing
* **MediaPipe** – Hand detection and landmark tracking
* **NumPy** – Numerical operations
* **Webcam** – Real-time video input

## 📁 Project Structure

```text
hand-tracker/
│
├── main.py
├── requirements.txt
├── README.md
│
├── src/
│   └── ...
│
└── assets/
    └── ...
```

> The exact file structure may vary depending on the implementation of the project.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/aishuaishu45793-gif/hand-tracker.git
```

### 2. Open the project

```bash
cd hand-tracker
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

Run the main Python file:

```bash
python main.py
```

Allow the application to access your webcam when prompted.

The webcam feed will open and the application will detect and track your hand in real time.

## 🧠 How It Works

The Hand Tracker works through the following steps:

1. The webcam captures live video.
2. OpenCV reads the video frames.
3. Each frame is processed by the hand-tracking model.
4. MediaPipe detects the hand.
5. Hand landmarks are identified.
6. The detected landmarks are displayed on the video.
7. The system continuously tracks hand movement in real time.

## 📌 Applications

This project can be extended to build:

* Gesture-controlled applications
* Virtual mouse systems
* Sign language recognition
* Touchless interfaces
* Interactive games
* Presentation controllers
* Human-computer interaction systems
* Fitness and motion tracking applications

## 🔮 Future Improvements

* Add multiple-hand tracking
* Implement gesture recognition
* Add voice commands
* Create a virtual mouse
* Add sign language recognition
* Improve tracking accuracy
* Add a graphical user interface
* Deploy as a web or desktop application

## 📷 Demo

Add screenshots or a demo video of the Hand Tracker here.

```text
Example:

![Hand Tracker Demo](assets/demo.png)
```

## 👩‍💻 Author

**Aishwarya**

GitHub:
https://github.com/aishuaishu45793-gif

## 📄 License

This project is created for educational and development purposes.
