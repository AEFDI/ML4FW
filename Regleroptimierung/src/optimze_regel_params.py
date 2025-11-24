import torch

import numpy as np
from itertools import product
from torch.utils.data import DataLoader
from dataset import HAST_Dataset
from models import CNNModel
from scipy.optimize import minimize
from pathlib import Path
import json
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def predict_ruecklauftemp(model, dataset, regelparams):
    """
    Simuliert die Rücklauftemperatur mit dem trainierten Modell für gegebene Regelparameter.
    """
    all_preds = []
    all_targets = []
    # Aktualisiert die Regelparameter im Dataset-Objekt
    updated_dataset = dataset
    updated_dataset.regelparams[:, :2] = regelparams
    updated_dataloader = DataLoader(updated_dataset, batch_size=len(dataset), shuffle=False, drop_last=False)
    model = model.to(device)
    # Iteriert durch die Daten und macht Vorhersagen
    with torch.no_grad():
        for inputs, targets in updated_dataloader:
            inputs = inputs.to(torch.float32).to(device)
            outputs = model(inputs)
            all_preds.append(outputs.cpu().numpy())
            all_targets.append(targets.cpu().numpy())

    # Berechnet den Mittelwert der vorhergesagten Rücklauftemperatur
    all_preds = np.concatenate(all_preds, axis=0)
    mean_temp = np.mean(all_preds)  # You can modify this depending on how Rücklauftemperatur is defined
    return mean_temp


def objective(regelparams_flat, model, dataset):
    """Zielfunktion für die gradientenbasierte Optimierung (scipy.minimize)."""
    regelparams = regelparams_flat.reshape(1, -1)
    return predict_ruecklauftemp(model, dataset, regelparams)

def optimize_regelparams(model, dataset, initial_guess, bounds):
    """
    Führt die gradientenbasierte Optimierung der Regelparameter durch.

    Nutzt 'L-BFGS-B' zur Minimierung der Zieltemperatur innerhalb der gegebenen Grenzen (Bounds).
    """
    result = minimize(objective, initial_guess, args=(model, dataset),
                      method='L-BFGS-B', bounds=bounds)

    return result.x.tolist()


def optimize_regelparams_for_trained_model(model, dataset,root, split="test"):
    """
    Führt Grid Search und anschließende gradientenbasierte Optimierung durch,
    um die optimalen Regelparameter zu finden.
    """
    min_m, max_m = np.min(dataset.regelparams, axis=0)[0], np.max(dataset.regelparams, axis=0)[0]
    min_l, max_l = np.min(dataset.regelparams, axis=0)[1], np.max(dataset.regelparams, axis=0)[1]
    model.eval()
    regelparam_grid = list(product(
        np.round(np.arange(min_m, max_m + 0.1, 0.1), 2),
        np.round(np.arange(min_l, max_l + 0.5, 0.5), 2)
    ))

    # Perform the grid search over the regelparam combinations
    best_params = None
    best_temp = float('inf')

    for params in regelparam_grid:

        temp = predict_ruecklauftemp(model, dataset, params)
        if temp < best_temp:
            print("Update von min. Rücklauftemperatur von ", best_temp,"auf ", temp)
            print("Update von besten Regelparametern von ", best_params,"auf ", params)
            best_temp = temp
            best_params = params

    print("Optimale Regelparameter (grid search):", best_params)
    print("Minimale Rücklauftemperatur:", best_temp)
    opt_param = {"best_m": best_params[0], "best_l": best_params[1]}

    print("OptimalerParameter: ")
    print(opt_param)

    print("Gradient-based optimization")

    initial_guess = np.array([0.5, 0.5])
    bounds = [(min_m, min_m), (min_l, max_l)]

    optimal_regelparams = optimize_regelparams(model, dataset, initial_guess, bounds)
    opt_param["result gradient based"]= optimal_regelparams

    print(opt_param)
    if split =="train":
        with open(root/"optimized_params_train.json", "w") as f:
            json.dump(opt_param, f)
    else:
        with open(root/"optimized_params.json", "w") as f:
            json.dump(opt_param, f)


if __name__ == "__main__":
    # --- Beispiel-Lade- und Ausführungslogik für das Hauptskript ---
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device. ", device)
    #Load Model
    root = Path("../experiments/Test_Run_with_dummy_data/")
    directory = root/"CNN/"
    with open(root/"config.json", "r") as f:
        config = json.load(f)

    val_losses=np.load(directory/"val_losses.npy")

    best_epoch_loss = np.min(val_losses)
    best_epoch = np.argmin(val_losses)
    print("Best epoch: ", best_epoch, "with loss ", best_epoch_loss)

    model_path = directory/f"model_{best_epoch}.pt"

    model = CNNModel(sequence_length=config["time_horizon"],n_layers = config["n_layers"], batch_norm = config["batch_norm"],
                     dropout_rate= config["dropout"], kernel_size=config["kernel_size"], size_out=config["time_horizon"],
                     pool=config["pool"])
    model.load_state_dict(torch.load(model_path))
    model.eval()

    dataset = HAST_Dataset(time_horizon=config["time_horizon"], split = "dummy_val")
    min_m, max_m = np.min(dataset.regelparams, axis=0)[0], np.max(dataset.regelparams, axis=0)[0]
    min_l, max_l = np.min(dataset.regelparams, axis=0)[1], np.max(dataset.regelparams, axis=0)[1]

    regelparam_grid = list(product(
        np.round(np.arange(min_m, max_m + 0.1, 0.1), 2),
        np.round(np.arange(min_l, max_l + 0.5, 0.5), 2)
    ))

    best_params = None
    best_temp = float('inf')
    opt_param = {}

    for params in regelparam_grid:
        temp = predict_ruecklauftemp(model, dataset, params)
        if temp < best_temp:
            print("Current best updated from ", best_temp,"to ", temp)
            print("Current best updated from ", best_params,"to ", params)
            best_temp = temp
            best_params = params

    print("Optimal regelparams (grid search):", best_params)
    print("Minimum Rücklauftemperatur:", best_temp)
    opt_param = {"best_m": best_params[0], "best_l": best_params[1]}

    print("Opt Param Dict: ")
    print(opt_param)

    print("Now gradient-based optimization")

    initial_guess = np.array([0.5, 0.5])
    bounds = [(min_m, max_m), (min_l, max_l)]

    optimal_regelparams = optimize_regelparams(model, dataset, initial_guess, bounds)
    opt_param["result gradient based"]= optimal_regelparams

    print("Opt Param Dict: ")
    print(opt_param)

    with open(root/"optimized_params.json", "w") as f:
        json.dump(opt_param, f)