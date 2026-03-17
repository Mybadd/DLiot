# 🛡️ Deep Learning IoT Edge IDS (CICIOT23)

This project implements a **Deep Learning-based Anomaly Detection System** designed for IoT Edge Gateways. By utilizing an unsupervised **Autoencoder architecture**, the system learns the "mathematical DNA" of normal network traffic and can detect malicious bursts (DDoS, Mirai, Brute Force) without needing prior knowledge of attack signatures.

---

### 🎯 Project Objectives
* **Deep Learning at the Edge:** Uses a compressed PyTorch Autoencoder (only ~50KB) that performs real-time inference with minimal CPU overhead.
* **Zero-Day Readiness:** Detects anomalies by calculating **Reconstruction Error**; any traffic that the model cannot "rebuild" is flagged as a potential new threat.
* **High-Fidelity Performance:** Achieved a **93% Detection Accuracy** on the CICIOT23 dataset (1.1 million+ samples).

---

### 🛠️ Technology Stack & Architecture

| Component | Choice | Reason |
| :--- | :--- | :--- |
| **Framework** | **PyTorch** | Allows for precise control over the neural network bottleneck, essential for forcing the model to learn only "normal" features. |
| **Architecture** | **Deep Autoencoder** | A 5-layer symmetric network (12 → 6 → 3 → 6 → 12) that compresses 9 network features into a latent space. |
| **Scaling** | **RobustScaler** | Specifically chosen to handle extreme outliers and high-frequency "Rate" spikes common in IoT traffic. |
| **Dashboard** | **Streamlit** | Provides a professional, web-based UI for real-time monitoring and anomaly score visualization. |

---

### 🚀 How to Run & Test (Step-by-Step)
Data Preparation & Training
Step 1: Run python 1_prepare_data.py

Cleans the 1.5GB CICIOT23 dataset and extracts the 9 core features (IAT, Rate, Flags, etc.).

Step 2: Run python 2_train_model.py

Trains the Autoencoder on Normal Traffic only. Saves model weights and the detection threshold to the models/ folder.

3. Verification (The Final Exam)
Step 3: Run python 5_evaluate_model.py

Tests the model against 1.1 million rows of mixed traffic.

Expected Result: ~93% Accuracy and ~0.93 Attack Recall.

4. Live Demo (Simulating a Hacker)
To see the system working in real-time, open two separate terminal windows:

Terminal 1 (The Guard): ```bash
python 3_run_live_detector.py

*Monitors the live stream and logs attacks to `detection_log.csv`.*

Terminal 2 (The Simulator): ```bash
python 4a_replay_simulator.py  # To replay REAL dataset attacks

OR
python 4b_active_simulator.py  # To launch a MANUAL synthetic burst
#### **1. Environment Setup**
Ensure you have the required libraries installed:
```bash
pip install torch pandas numpy scikit-learn streamlit joblib

📈 Key Technical Features
Bottleneck Compression: By squeezing features into a 3-neuron latent space, we prevent the model from "memorizing" noise, forcing it to learn the true patterns of benign traffic.

Percentile-Based Calibration: The detection threshold is dynamically set at the 75th percentile of training error, optimizing the balance between False Positives and Security Recall.

Forensic Logging: Every detected attack is timestamped and saved with its specific Anomaly Score for later security auditing.