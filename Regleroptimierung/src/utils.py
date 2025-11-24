import numpy as np
import logging
import matplotlib.pyplot as plt
import sys
import torch
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_losses_and_model(target_path, train_losses, val_losses, model, epoch):
    """Speichert die Trainings- und Validierungsverluste sowie den aktuellen Modellzustand (state_dict)."""

    try:
        target_path = Path(target_path)
        target_path.mkdir(parents=True, exist_ok=True)

        np.save(target_path / 'train_losses.npy', np.array(train_losses))
        np.save(target_path / 'val_losses.npy', np.array(val_losses))
        torch.save(model.state_dict(), target_path / f"model_{epoch}.pt")

        logger.warning(f"Model gespeichert unter {target_path} /model_{epoch}.pt")

    except Exception as e:
        logger.error(f"Fehler beim Speichern: {e}")
        raise e

def save_predictions(target_path, all_train_preds, all_train_targets, split = "unknown"):
    """Speichert die vorhergesagten und die tatsächlichen Zielwerte (Targets) als NumPy-Arrays."""

    try:
        target_path = Path(target_path)
        target_path.mkdir(parents=True, exist_ok=True)

        np.save(target_path / f'{split}_preds.npy', np.vstack(all_train_preds))
        np.save(target_path / f'{split}_targets.npy', np.vstack(all_train_targets))

    except Exception as e:
        logger.error(f"Fehler beim Speichern: {e}")
        raise e

def plot_losses(train_losses, val_losses, num_epochs, title = 'Training and Validation Loss Over Epochs'):
    """Plottet den Trainings- und Validierungsverlust über die Epochen."""
    plt.plot(range(1, num_epochs+1), train_losses, label='Training Loss')
    plt.plot(range(1, num_epochs+1), val_losses, label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def setup_logging():
    """Konfiguriert ein detailliertes Logging-Setup für stdout und stderr."""
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(error_handler)