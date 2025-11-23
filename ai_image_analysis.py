#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FULL AI IMAGE FORENSICS PIPELINE (USER INPUT VERSION)
- EXIF metadata inspection
- Noise residual / PRNU-style analysis
- Frequency domain (FFT) artifact scoring
- Edge-map abnormality scoring
- CNN classifier (EfficientNet-B0)
- Final combined AI-likelihood score
- Accepts local file path OR URL via user input
"""

import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as T
from PIL import Image, ExifTags
import torchvision.models as models
import requests
from io import BytesIO
import os
import warnings

warnings.filterwarnings("ignore")

#############################################
# ----------- IMAGE LOADING ---------------
#############################################

def load_image_from_input():
    user_input = input("Enter LOCAL file path or IMAGE URL: ").strip()

    # URL case
    if user_input.startswith("http://") or user_input.startswith("https://"):
        try:
            print("Downloading image...")
            r = requests.get(user_input, timeout=10)
            img_data = BytesIO(r.content)
            img = Image.open(img_data).convert("RGB")
            
            # save temp file
            temp_path = "temp_downloaded_image.jpg"
            img.save(temp_path)
            print(f"Downloaded and saved as: {temp_path}")
            return temp_path
        except Exception as e:
            print("Error downloading image:", e)
            exit()

    # Local file
    if os.path.exists(user_input):
        return user_input
    else:
        print("Error: File not found.")
        exit()


#############################################
# ----------- 1. EXIF METADATA -------------
#############################################

def extract_exif(path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif:
            return {}, 1.0  # missing metadata is suspicious
        meta = {ExifTags.TAGS.get(k, k): v for k, v in exif.items()}
        
        score = 0.0
        tags = ["Make", "Model", "LensModel"]
        missing = [t for t in tags if t not in meta]
        if len(missing) == len(tags):
            score = 1.0

        return meta, score
    except:
        return {}, 1.0


#############################################
# ----------- 2. NOISE RESIDUAL ------------
#############################################

def noise_residual_score(path):
    img = cv2.imread(path)
    if img is None:
        return 0.5

    img_f = img.astype(np.float32)
    denoise = cv2.fastNlMeansDenoisingColored(img, None, 10,10,7,21)
    residual = img_f - denoise.astype(np.float32)
    std_val = np.std(residual)

    if std_val < 2:
        return 1.0
    elif std_val < 5:
        return 0.7
    elif std_val < 10:
        return 0.3
    else:
        return 0.1


#############################################
# ----------- 3. FFT ARTIFACTS -------------
#############################################

def fft_artifact_score(path):
    img = cv2.imread(path, 0)
    if img is None:
        return 0.5

    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    mag = np.log(np.abs(fshift) + 1)

    artifact_strength = np.mean(mag > (mag.mean() + 2*mag.std()))

    if artifact_strength > 0.25:
        return 1.0
    elif artifact_strength > 0.15:
        return 0.7
    elif artifact_strength > 0.08:
        return 0.4
    else:
        return 0.1


#############################################
# ----------- 4. EDGE ARTIFACTS ------------
#############################################

def edge_inconsistency_score(path):
    img = cv2.imread(path)
    if img is None:
        return 0.5

    edges = cv2.Canny(img, 100, 200)
    ratio = np.sum(edges > 0) / edges.size

    if ratio < 0.02:
        return 0.9
    elif ratio > 0.18:
        return 0.8
    elif ratio > 0.12:
        return 0.5
    else:
        return 0.2


#############################################
# ----------- 5. CNN CLASSIFIER ------------
#############################################

class DetectorCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = models.efficientnet_b0(weights="IMAGENET1K_V1")
        self.model.classifier[1] = nn.Linear(1280, 2)

    def forward(self, x):
        return self.model(x)

cnn_model = DetectorCNN()
cnn_model.eval()

preprocess = T.Compose([
    T.Resize((256,256)),
    T.ToTensor(),
    T.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

def cnn_score(path):
    try:
        img = Image.open(path).convert("RGB")
        x = preprocess(img).unsqueeze(0)

        with torch.no_grad():
            out = torch.softmax(cnn_model(x), dim=1)
            ai_prob = float(out[0][1])
        return ai_prob
    except:
        return 0.5


#############################################
# ----------- 6. FINAL AGGREGATION ---------
#############################################

def final_score(path):
    print("\n--- Running AI-Image Forensics ---")

    exif_meta, exif_s = extract_exif(path)
    noise_s = noise_residual_score(path)
    fft_s = fft_artifact_score(path)
    edge_s = edge_inconsistency_score(path)
    cnn_s = cnn_score(path)

    final = (
        exif_s * 0.15 +
        noise_s * 0.20 +
        fft_s * 0.20 +
        edge_s * 0.15 +
        cnn_s * 0.30
    )

    report = {
        "AI_probability": round(final, 3),
        "EXIF_suspicion": exif_s,
        "Noise_suspicion": noise_s,
        "FFT_artifacts": fft_s,
        "Edge_artifacts": edge_s,
        "CNN_model_score": cnn_s,
        "EXIF_metadata": exif_meta
    }

    return report


#############################################
# ---------------- MAIN --------------------
#############################################

if __name__ == "__main__":
    image_path = load_image_from_input()
    result = final_score(image_path)

print("\n--------- FORENSIC REPORT ---------")

def pct(x):
    return f"{round(x*100, 2)}%"

def explain(label, value):
    if value >= 0.75:
        level = "HIGH — Strong indication of AI generation"
    elif value >= 0.50:
        level = "MODERATE — Suspicious characteristics detected"
    elif value >= 0.25:
        level = "LOW — Some signs but not conclusive"
    else:
        level = "MINIMAL — Looks consistent with a real camera"
    return f"{label}: {pct(value)} | {level}"

print(explain("Overall AI Probability", result["AI_probability"]))
print(explain("EXIF Suspicion", result["EXIF_suspicion"]))
print(explain("Noise Residual Suspicion", result["Noise_suspicion"]))
print(explain("FFT Artifact Score", result["FFT_artifacts"]))
print(explain("Edge Artifact Score", result["Edge_artifacts"]))
print(explain("CNN Model Score", result["CNN_model_score"]))

print("\nEXIF Metadata:")
if result["EXIF_metadata"]:
    for k, v in result["EXIF_metadata"].items():
        print(f"   {k}: {v}")
else:
    print("   No metadata found (this is common in AI images).")

print("------------------------------------\n")


