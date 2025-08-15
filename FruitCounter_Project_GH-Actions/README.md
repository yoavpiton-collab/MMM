# FruitCounter (Offline) – Android APK via GitHub Actions

This package contains a Kivy app that counts fruits in an image using a TensorFlow Lite model (offline).
You can build the APK locally with Buildozer *or* automatically via GitHub Actions (recommended).

## Contents
- app/main.py
- app/fruit_counter.kv
- app/tflite_model/fruit_model.tflite (placeholder)
- app/assets/labels.txt
- buildozer.spec
- .github/workflows/android-apk.yml
- requirements.txt

## A) Build APK with GitHub Actions
1. Create a new repo on GitHub.
2. Upload these files (keep the folder structure).
3. Enable Actions and push a commit to start the workflow.
4. Download the APK from the run artifacts.

## B) Build locally
sudo apt update && sudo apt install -y python3-pip openjdk-17-jdk zip unzip git
pip3 install --upgrade pip
pip3 install buildozer cython kivy pillow numpy tensorflow
buildozer android debug
# APK will be in bin/

Replace the placeholder TFLite model with your trained model for production.
