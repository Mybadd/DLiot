# Lightweight IoT Edge Intrusion Detection System (IDS)

This project implements a lightweight and computationally efficient Intrusion Detection System (IDS) specifically designed to run on resource-constrained Edge gateways (e.g., Raspberry Pi, local routers). It protects IoT environments by detecting zero-day attacks and anomalies without relying on cloud infrastructure.

## 🎯 Project Objectives
*   **Edge-Native Architecture:** Compute heavy tasks (training) are done offline. The edge device only runs a highly compressed inference model.
*   **Zero-Day Detection:** Uses Anomaly Detection to catch unknown attacks rather than relying on signature databases.
*   **Dual Simulation Testing:** Proves the model works using both dataset replays (Mirai, DDoS) and active live-network simulations.

---

## 🛠️ Technology Stack & Architecture Choices

To ensure the system remains lightweight enough to run on an IoT Edge Gateway, specific tools were chosen over enterprise-grade alternatives.

| Tech Stack Used | Enterprise Alternative | Reason for Choosing the Lightweight Stack |
| :--- | :--- | :--- |
| **Python 3.x** | C++ / Rust | Python offers the vast array of Machine Learning libraries needed (Scikit-Learn). While C++ is faster for inference, Python is fast enough for gateway-level routing and is much easier to develop and test locally. |
| **Scikit-Learn (Isolation Forest)** | Deep Autoencoders / TensorFlow | Deep learning models with "attention" mechanisms are massive. Scikit-Learn's anomaly detection algorithms calculate mathematical outliers with minimal CPU/RAM usage, perfect for an edge device. |
| **CICFlowMeter-Python (or PyShark)** | Zeek (formerly Bro) | Zeek is powerful but heavy to install and configure. A Python-based flow meter natively generates the statistical summaries required for ML natively without needing external engine processes. |
| **Pickle / Joblib (Model Save)** | Dockerized Microservices | Running fully isolated Docker containers for a single model inference on a 1GB RAM edge device consumes too much overhead. Loading a tiny `.pkl` file directly into memory is faster. |
| **Local File Data Feeds (CSV)** | Kafka / ELK Stack | A full data pipeline (Kafka) is massive overkill for a local home network. Reading and routing directly from the local traffic listener is instant and resource-free. |

---

## Key Technical Features
Dataset Agnostic: Features a custom dataset_adapter.py that maps varying CSV headers (CICIOT23, etc.) to a standardized AI feature set.

Memory Optimized: Implements Chunked Data Evaluation to process over 1.1 Million rows of network traffic without crashing system RAM.

Fast Inference: Uses Isolation Forest, an unsupervised learning algorithm that is significantly faster than Deep Learning for real-time Edge deployment.

Live UI: Interactive Streamlit Dashboard for real-time traffic visualization and security alerts.

## 🚀 Pipeline & Structure

The project is structured into functional, numbered steps from data processing to live deployment.

### 1. Data Processing Tools
*   `1_prepare_data.py`: Loads the raw IoT dataset (e.g., CICIoT2023 or Bot-IoT), cleans the data, and selects only the necessary network flow features.

### 2. Machine Learning Tools
*   `2_train_model.py`: Takes the cleaned "normal" data and trains the Anomaly Detection model. Saves the trained model to disk.

### 3. The Core Engine
*   `3_run_live_detector.py`: The deployment engine. It loads the saved AI model and acts as a gateway function, taking incoming network flow features and instantly outputting an anomaly score and alert threshold.

### 4. Testing & Dual-Simulation
We prove the AI works using two specific methodologies:
*   `4a_replay_simulator.py`: **(Dataset Replay)** Safely tests the model by reading the testing portion of our original dataset row-by-row. This proves the math works against advanced botnets like Mirai.
*   `4b_active_simulator.py`: **(Live Network Simulation)** Listens to the local machine's network card and runs live (but harmless) DDoS floods or Port Scans via `localhost` to catch active threats in real-time.

---


