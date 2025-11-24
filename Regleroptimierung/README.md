# HAST: Modellierung und Optimierung von Heizungsregelparametern

Dieses Repository enthält den Code für das Training von Machine-Learning-Modellen zur Vorhersage von Heizungsparametern (HAST-Daten) und die anschließende Optimierung der Regelparameter.

## Datenstruktur

Das Projekt nutzt Daten, die in drei Hauptkategorien unterteilt sind, um die Simulation einer Heizanlage abzubilden:

- **Input-Werte (`dummy_*_inputs.csv`)**:  
  Enthält zeitabhängige Eingangsdaten der Simulation (z. B. Außentemperatur, Zeitstempel, Betriebsart).

- **Target-Werte (`dummy_*_targets.csv`)**:  
  Enthält die Zielwerte, insbesondere die Rücklauftemperatur (`T_pri_ret`), die das Modell vorhersagen soll.

- **Regelparameter (`setUp_Petrosawodska_66_72_Winter.csv`)**:  
  Enthält Regelparameter wie *Steigung* und *Level*, welche das Systemverhalten bestimmen und später optimiert werden.

## Dummy-Daten

Für schnelles Testen und Debuggen liegen vorkonfektionierte Dummy-Daten vor (`dummy_dummy_inputs.csv`, `dummy_dummy_targets.csv` etc.), die direkt von der Klasse `HAST_Dataset` geladen werden.

## HAST_Dataset

Die Klasse `HAST_Dataset` (definiert in `dataset.py`) ist für die Vorverarbeitung der Daten verantwortlich:

- **Laden**: Input-, Target- und Regelparameter-Dateien werden eingelesen.  
- **Feature Engineering**: Extrahiert zyklische Zeit-Features (Sinus/Cosinus der Stunde).  
- **Skalierung**: Skaliert Zeitreihen-Inputs und Regelparameter mittels `MinMaxScaler`.  
- **Kombination**: Regelparameter werden über die gesamte Zeitreihe repliziert und als zusätzliche Input-Features hinzugefügt.  
- **Sequenzierung**: Organisiert Daten in Samples der Länge `time_horizon`.

## Modell-Typen

Im Repository stehen drei neuronale Netzarchitekturen zur Verfügung (in `models.py`):

- **MLPModel**: Multi-Layer Perceptron (Feedforward).  
- **CNNModel**: 1D-CNN zur Erkennung zeitlicher Muster.  
- **LSTMModel**: Rekurrentes LSTM-Netz für sequenzielle Zeitreihen.

## Training und Optimierung

Der zentrale Workflow befindet sich in `training.py`:

- **Setup**: Lädt Konfigurationsparameter (z. B. `time_horizon`, `epochs`).  
- **Training**:  
  `train_and_optimize` trainiert das ausgewählte Modell und speichert die besten Modelle basierend auf Validierungsverlust.  
- **Regelparameter-Optimierung**:  
  Das beste Modell wird geladen und zur Optimierung von Steigung und Level genutzt.

### Optimierungsskripte

Das Skript **`optimize_regel_params.py`**:

- führt eine **Grid Search** über mögliche Regelparameterräume durch  
- bestimmt Kombinationen, die die Rücklauftemperatur minimieren  
- nutzt zusätzlich eine **gradientenbasierte Optimierung** (`scipy.optimize.minimize`) für feinere Ergebnisse