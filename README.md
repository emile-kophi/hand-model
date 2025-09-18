# Hand Movement Simulation with ROS and Unity

This project demonstrates a method for simulating human hand movements in Unity based on real-time hand tracking performed in Python using the MediaPipe library and ROS (Robot Operating System).  
The system captures hand movements via a webcam, processes the data, and visualizes the landmarks in a Unity scene.

---

## Introduction
This work outlines an approach that leverages ROS and the roslibpy library to replicate human hand movements in Unity.

- Uses the updated MediaPipe hand landmark detection model (February 2023).  
- Tracks a hand using **21 key landmarks**, each with X, Y, and Z coordinates.  
- Python scripts create ROS publishers and subscribers using `roslibpy`.  
- Unity uses a C# subscriber script to visualize the landmark data in real time.  

This workflow enables Unity to visualize the real-time position and movement of hand landmarks.

---

## Methods
A webcam provides a live video stream.  For each frame, 21 points on the hand are detected and assigned to a fixed configuration (see Figure 1).Each landmark has x, y, and relative depth (z) coordinates. The landmark data is published on a ROS topic using roslibpy and OOP principles. In Unity, the subscriber confirms the received data in the terminal and updates the landmark spheres prefab in real time.  

Instead of a detailed hand mesh, this project uses spheres prefabs to represent the hand’s shape.

---

## Future Improvements
 Improved Landmark Model: Current MediaPipe works best with frontal views. Side views (midsagittal plane) reduce accuracy. A more robust model is needed.  
 Unity Hand Model: Replace spheres with a proper 3D hand model for more realistic feedback and latency evaluation.  

---

## Materials
- **GitHub Repository**: [hand-model](https://github.com/emile-kophi/hand-model)  
- **MediaPipe Hands**: [docs](https://mediapipe.readthedocs.io/en/latest/solutions/hands.html)  
- **roslibpy**: [docs](https://roslibpy.readthedocs.io/en/latest/)  
- **Unity Robotics Hub**: [PickAndPlace Project](https://github.com/Unity-Technologies/Unity-Robotics-Hub)  

---
