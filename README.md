
# Explainable AI Application for Visual Analytics

Dieses Repository enthält die Projektarbeit für das Modul Visual Analytics an der Hochschule Aalen. Ziel des Projekts ist es, ein Convolutional Neural Network (CNN) zur Klassifikation von Äpfeln und Bananen zu implementieren und die Ergebnisse mittels Explainable AI (XAI) Methoden zu interpretieren. Die verwendeten XAI Methoden sind Contrastive Explanation Method (CEM) und Local Interpretable Model-agnostic Explanations (LIME).

## Inhaltsverzeichnis
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Projektstruktur](#projektstruktur)
- [Modellbeschreibung](#modellbeschreibung)
- [XAI Methoden](#xai-methoden)
  - [CEM](#cem)
  - [LIME](#lime)
- [XAI Dashboard](#xai-dashboard)

## Installation

Um das Repository zu klonen und die benötigten Abhängigkeiten zu installieren, führen Sie folgende Befehle aus:

```bash
git clone https://github.com/Kn3ule/visual_analytics.git
cd visual_analytics
pip install -r requirements.txt
```

Stellen Sie sicher, dass Sie Python 3.7 oder höher installiert haben.

## Verwendung

1. Starten Sie das Jupyter Notebook und führen Sie die Zellen im `visualAnalytics - CEM - LIME.ipynb` aus, um das CNN-Modell zu trainieren und zu evaluieren.
2. Um das XAI Dashboard zu starten, führen Sie das `app.py` Skript aus:

```bash
python app.py
```

## Projektstruktur

- `visualAnalytics - CEM - LIME.ipynb`: Jupyter Notebook mit dem CNN-Modell zur Klassifikation von Äpfeln und Bananen sowie den XAI Methoden CEM und LIME.
- `app.py`: Python Skript zur Erstellung und Darstellung des XAI Dashboards.
- `images/`: Dieser Ordner beinhaltet die Bilder, welche im XAI Dashboard verwendet werden.
- `data/`: Dieser Ordner beinhaltet die Daten zur Klassifikation, welche im XAI Dashboard dargestellt werden.
- `requirements.txt`: Liste der benötigten Python-Pakete.

## Modellbeschreibung

Das Convolutional Neural Network (CNN) in diesem Projekt wurde zur Klassifikation von Äpfeln und Bananen entwickelt. Das Modell besteht aus mehreren Convolutional und Pooling Schichten um die Klassifikation durchzuführen.

## XAI Methoden

### CEM

Contrastive Explanation Method (CEM) ist eine Methode zur Generierung von kontrastiven Erklärungen für Modellvorhersagen. Sie hilft zu verstehen, warum eine bestimmte Klasse vorhergesagt wurde, indem sie kontrastierende Merkmale hervorhebt, die zu einer anderen Klasse führen könnten.

### LIME

Local Interpretable Model-agnostic Explanations (LIME) ist eine Methode zur Erklärung individueller Vorhersagen eines Modells. LIME approximiert das Verhalten des Modells lokal um die zu erklärende Vorhersage herum und identifiziert wichtige Merkmale, die zur Vorhersage beitragen.

## XAI Dashboard

Das XAI Dashboard, definiert in `app.py`, ermöglicht eine interaktive Visualisierung der Modellvorhersagen und ihrer Erklärungen. Es bietet eine benutzerfreundliche Oberfläche, um die Auswirkungen verschiedener Merkmale auf die Modellvorhersagen zu erkunden.

---

Dieses Projekt wurde im Rahmen des Moduls Visual Analytics an der Hochschule Aalen erstellt.
