# Classification of Defects in Photovoltaic Modules using Thermal Imagery

This repository contains the implementation of a Deep Learning pipeline for the automatic detection and classification of anomalies in infrared images of photovoltaic (PV) modules. Developed for the Computer Vision course (Assignment 2) at FEUP (2025/2026), this project compares a custom Convolutional Neural Network (CNN) with a Transfer Learning approach (ResNet18) to solve the challenge of imbalanced thermal datasets.

## 👥 Authors
* **Afonso Tomás de Magalhães Mateus** (202204126)
* **Diogo Soares de Albergaria Oliveira** (202108325)
## Grade: 17.84
---

## 📌 Project Overview
Thermal inspection is crucial for maintaining solar farm efficiency. This project automates the identification of defects (e.g., Hotspots, Cracking, Diode failures) using the **Raptor Maps Infrared Solar Modules dataset** (20,000 images).

The workflow includes:
1.  **Data Preprocessing:** Enhancement of low-contrast thermal images.
2.  **Hybrid Augmentation:** A dual-strategy to handle severe class imbalance.
3.  **Model Training:** Comparison between a custom CNN and ResNet18.
4.  **Evaluation:** Testing on Binary (2-class), Multi-class (11-class), and Full (12-class) scenarios.

---

## ⚙️ Methodology & Code Structure

The implementation is modular, defined in the `Assignment2_202204126_202108325.ipynb` notebook:

### 1. Preprocessing (`ImagePreprocessor`)
Thermal images often lack edge definition. We implemented a preprocessing pipeline that:
* **Unsharp Masking:** Applies a sharpening filter (Radius=2, Percent=150, Threshold=3) to enhance defect boundaries.
* **Normalization:** Pixel values are normalized based on ImageNet statistics.

### 2. Hybrid Data Augmentation (`AugmentationWorker`)
A key feature of this implementation is the separation of augmentation into two distinct phases to solve class imbalance without causing data leakage:

* **Offline Augmentation (Balancing):**
    * *Goal:* Equalize the dataset distribution before training.
    * *Method:* Generates synthetic images (using rotation and flipping) for minority classes (e.g., *Diode-Multi*, *Soiling*).
    * *Code:* `generate_offline_aug` function saves these new files to disk.

* **Online Augmentation (Generalization):**
    * *Goal:* Prevent overfitting during training.
    * *Method:* Applies dynamic, random transformations to every batch fed into the model.
    * *Techniques:* Random Affine (Rotation/Translation), Color Jitter (Brightness/Contrast), and Random Horizontal/Vertical Flips.

### 3. Model Architectures
We implemented and compared two architectures:
* **Custom CNN (`PVClassifier`):** A lightweight network built from scratch with 4 convolutional blocks (`Conv2d` + `BatchNorm` + `ReLU` + `MaxPool`) followed by Global Average Pooling. Designed to be efficient for edge devices.
* **ResNet18 (`ResNet18_Custom`):** A transfer learning approach using a pre-trained ResNet18. We modified the first convolutional layer to accept **1-channel grayscale input** (averaging the original RGB weights) and adapted the final fully connected layer to the specific number of classes (2, 11, or 12).
* **MobileNetV2 (Transfer Learning):** A highly efficient architecture optimized for mobile/edge devices, tested to compare the trade-off between accuracy and model size.

---

## 🧪 Experiments

The code is structured to run three main experimental scenarios:

1.  **Binary Classification:**
    * Aggregates all defect types into a single "Anomaly" class vs. "No-Anomaly".


2.  **11-Class Classification (Anomalies Only):**
    * Focuses on distinguishing specific defect types (e.g., *Cell* vs. *Hot-Spot* vs. *Cracking*) excluding healthy panels.
    

3.  **12-Class Classification (Full Spectrum):**
    * Classifies all anomaly types plus the "No-Anomaly" class.
   

4.  **Augmentation Impact Study:**
    * Specifically compares model performance with vs. without the balancing strategy to demonstrate the necessity of data augmentation in imbalanced datasets.

---

## 📚 References
* *Ramadan, E.A., et al.* (2024). "An innovative transformer neural network for fault detection and classification for photovoltaic modules". Energy Conversion and Management.
* *Le, M., et al.* (2023). "Thermal inspection of photovoltaic modules with deep convolutional neural networks on edge devices in AUV". Measurement.
