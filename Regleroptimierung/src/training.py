import json
import logging
from pathlib import Path
from torch.utils.data import DataLoader, random_split, Subset

import numpy as np
import torch
import torch.nn as nn
from dataset import import_data
from models import MLPModel, CNNModel, LSTMModel
from utils import save_losses_and_model, plot_losses, setup_logging, save_predictions
from optimze_regel_params import  optimize_regelparams_for_trained_model
from datetime import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

setup_logging()

def train_and_optimize(train_dataset, val_dataset,experiments_dir_path,model, config, save_train_pred = True):
    """Führt das Training des Modells und die anschließende Regelparameter-Optimierung durch."""
    experiments_dir_path.mkdir(parents=True)
    model.to(device)
    # Konfigurationsparameter laden
    epochs = config["epochs"]
    batch_size = config["batch_size"]
    learning_rate = config["learning_rate"]
    # DataLoader für Training, Validierung und Test erstellen
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, drop_last=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, drop_last=True)
    # Kriterium (Loss-Funktion) und Optimierer definieren (L1Loss = Mean Absolute Error)
    logging.warning(f"Training auf {len(train_dataset)} train samples und {len(val_loader)} validation batches")

    # Kriterium (Loss-Funktion) und Optimierer definieren (L1Loss = Mean Absolute Error)
    criterion = nn.L1Loss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-2)

    train_losses = []
    val_losses = []
    if save_train_pred:
        all_preds_train = []
        all_targets_train = []

    # Trainings-Schleife
    for epoch in range(epochs):
        avg_train_loss , preds_train, targets_train = train_model(model, train_loader,optimizer, criterion)
        if save_train_pred:
            all_preds_train.append(preds_train)
            all_targets_train.append(targets_train)
        train_losses.append(avg_train_loss)
        # Validierung nach jeder Epoche
        avg_val_loss= test_model(experiments_dir_path, model, val_loader, criterion, split = "val")
        val_losses.append(avg_val_loss)

        logging.warning(f"Epoch {epoch + 1}/{epochs}: Train Loss = {avg_train_loss:.4f}, Val Loss = {avg_val_loss:.4f}")
        save_losses_and_model(experiments_dir_path, train_losses, val_losses, model, epoch)

    logging.warning("Training completed. Now determining the best epoch and evaluate model on test dataset.")
    # Bestes Modell basierend auf Validierungsverlust auswählen und evaluieren
    val_loss_final, test_loss= evaluate_best_model(experiments_dir_path, val_losses, model, test_loader, val_loader, criterion)
    optimize_regelparams_for_trained_model(model=model, dataset=train_loader.dataset, root=experiments_dir_path)

    return train_losses, val_losses, val_loss_final, test_loss

def evaluate_best_model(experiments_dir_path, val_losses, model, test_loader, val_loader, criterion):
    """Lädt das Modell mit dem besten Validierungsverlust und evaluiert es."""
    best_epoch = np.argmin(val_losses)
    model.load_state_dict(torch.load(experiments_dir_path/f"model_{best_epoch}.pt"))
    test_loss = test_model(experiments_dir_path,model, test_loader, criterion, split = "test")
    val_loss = test_model(experiments_dir_path,model, val_loader, criterion, split = "val")
    optimize_regelparams_for_trained_model(model=model, dataset=test_loader.dataset, root=experiments_dir_path)
    return val_loss, test_loss

def train_model(model, train_loader, optimizer, criterion):
    model.train()
    total_loss = 0
    for inputs, targets in train_loader:
        inputs = inputs.to(torch.float32).to(device)
        targets = targets.to(torch.float32).to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(torch.squeeze(outputs), targets)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        all_preds_train= outputs.detach().cpu().numpy()
        all_targets_train =targets.detach().cpu().numpy()

    avg_train_loss = total_loss / len(train_loader)
    return avg_train_loss, all_preds_train, all_targets_train

def test_model(experiments_dir_path,model, loader, criterion, split = "train"):
    """Führt eine Trainings-Epoche durch."""
    all_preds_test = []
    all_targets_test = []
    test_losses= []

    total_val_loss = 0
    model.eval()
    model.to(device)
    with torch.no_grad():
        for inputs, targets in loader:
            inputs = inputs.to(torch.float32).to(device)
            targets = targets.to(torch.float32).to(device)

            outputs = model(inputs)
            loss = criterion(np.squeeze(outputs), targets)
            total_val_loss += loss.item()

            all_preds_test.append(outputs.detach().cpu().numpy())
            all_targets_test.append(targets.detach().cpu().numpy())

    avg_val_loss = total_val_loss / len(loader)
    test_losses.append(avg_val_loss)
    save_predictions(experiments_dir_path,all_preds_test,all_targets_test, split = split)

    return  np.mean(test_losses)

if __name__ == "__main__":
    # ---- Konfiguration der Trainingsparameter ----
    config = {
        "batch_size":64,
        "epochs":3,
        "time_horizon":150,
        "n_layers": 5,
        "batch_norm": False,
        "dropout":0.5,
        "learning_rate":0.001,
        "kernel_size" : 5,
        "pool" : False,
        "test_run" :True

    }
    # Erstellen des Verzeichnisses für Experiment-Ergebnisse
    experiments_dir = Path("../experiments") / f"Test_Run_with_dummy_data/"
    if not experiments_dir.exists():
        experiments_dir.mkdir(parents=True)
    with open(experiments_dir/"config.json", "w") as config_file:
        json.dump(config, config_file)

    train_dataset, val_dataset, test_dataset = import_data(time_horizon= config["time_horizon"],test_run=config["test_run"])

    # ---- Modell-Auswahl und Training (hier CNN) ----
    # MLP und LSTM sind auskommentiert
    # MLP
    # model = MLPModel()
    # train_losses, val_losses = train_and_validate(train_dataset, val_dataset,experiments_dir/"MLP", model, dataset, epochs=epochs,continuous_split=continuous_split)
    # plot_losses(train_losses, val_losses, num_epochs=epochs, title="Training and Validation Loss of MLP-based Model")

    #1D CNN
    model = CNNModel(sequence_length=config["time_horizon"],n_layers = config["n_layers"], batch_norm = config["batch_norm"],
                     dropout_rate= config["dropout"], kernel_size=config["kernel_size"], pool = config["pool"], size_out=config["time_horizon"])
    # Training starten und Regelparameter optimieren
    train_losses, val_losses , val_loss_final, test_loss = train_and_optimize(train_dataset, val_dataset,experiments_dir/"CNN", model, config)
    # Verluste plotten
    plot_losses(train_losses, val_losses, num_epochs=config["epochs"], title="Training and Validation Loss of CNN-based Model")

    logging.warning(f"Final Test Loss = {test_loss}, Final Val Loss=  {val_loss_final:.4f}")
    logging.warning(config)

    # # #LSTM
    # model = LSTMModel()
    # train_losses, val_losses = train_and_validate(train_dataset, val_dataset,experiments_dir/"LSTM", model, dataset, epochs=epochs,continuous_split=continuous_split)
    # plot_losses(train_losses, val_losses, num_epochs=epochs, title="Training and Validation Loss of LSTM-based Model")
