import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

def import_data(time_horizon,test_run = False):
    if test_run:
        train_dataset = HAST_Dataset(split = "dummy", time_horizon= time_horizon)
        val_dataset = HAST_Dataset(split = "dummy_val", time_horizon= time_horizon)
        test_dataset = HAST_Dataset(split = "dummy_val", time_horizon= time_horizon)
    else:
        train_dataset = HAST_Dataset(split = "train", time_horizon= time_horizon)
        val_dataset = HAST_Dataset(split = "val", time_horizon= time_horizon)
        test_dataset = HAST_Dataset(split = "test", time_horizon= time_horizon)

    return train_dataset, val_dataset, test_dataset


class HAST_Dataset(Dataset):
    def __init__(self, time_horizon, split = "dummy"):
        """
        Initialize the dataset. This is where you can load or prepare your data.
        """
        super().__init__()
        root = Path(__file__).parent.parent.resolve()/"data"
        param_file = root/"dummy_setUp.csv"
        self.regelparams = pd.read_csv(param_file)[["Steigung", "Level"]]
        self.time_horizon = time_horizon

        if split== "dummy":
            input_file = root/"dummy_dummy_inputs.csv"
            target_file = root/"dummy_dummy_targets.csv"
            original_inputs = pd.read_csv(input_file)
            original_targets = pd.read_csv(target_file)
            self.timestamps = original_inputs["time"]

        elif split== "dummy_val":
            input_file = root/"dummy_dummy_val_inputs.csv"
            target_file = root/"dummy_dummy_val_targets.csv"
            original_inputs = pd.read_csv(input_file)
            original_targets = pd.read_csv(target_file)
            self.timestamps = original_inputs["time"]

        assert (original_inputs["time"] != original_targets["timeVec"]).sum() == 0
        targets_orinigal = original_targets.drop(columns=["timeVec"])

        #hours only
        inputs = original_inputs.drop(columns=["mbc60Slp","mbr1003RaumsollTagHk1", "interpPowerWODHW", "interpFlowWODHW"])
        inputs["timeVec"] = pd.to_datetime(original_inputs["time"], format="%d-%b-%Y %H:%M:%S", errors='coerce')
        inputs["hour"] = inputs["timeVec"].dt.hour
        inputs["minute"] = inputs["timeVec"].dt.minute
        inputs["fractional_hour"] = inputs["hour"] + inputs["minute"] / 60.0
        inputs["time_sin"] = np.sin(2 * np.pi * inputs["fractional_hour"] / 24)
        inputs["time_cos"] = np.cos(2 * np.pi * inputs["fractional_hour"] / 24)
        inputs = inputs.drop(columns=["hour", "minute", "fractional_hour", "timeVec", "time"])

        inputs.loc[inputs["mbr106BetriebsartHk1"] == "4,5", "mbr106BetriebsartHk1"] = "Nacht"
        inputs["mbr106BetriebsartHk1"] = inputs["mbr106BetriebsartHk1"].map({"Tag": 1, "Nacht": 0})

        # Min Max Scaling
        self.time_series_inputs = inputs.to_numpy()
        scaler_inputs = MinMaxScaler()
        self.time_series_inputs = scaler_inputs.fit_transform(self.time_series_inputs)


        self.regelparams = self.regelparams.to_numpy()
        scaler_params = MinMaxScaler()

        expanded_inputs= np.tile(self.time_series_inputs, (self.regelparams.shape[0], 1))
        expanded_params = np.repeat(self.regelparams, repeats=self.time_series_inputs.shape[0], axis=0)
        self.final_inputs = np.concatenate([expanded_inputs, expanded_params], axis=1)
        self.flattened_targets = targets_orinigal.to_numpy().ravel(order='F')

    def __len__(self):
        return (self.final_inputs.shape[0] //  self.time_horizon)

    def input_dim(self):
        return self.final_inputs.shape[1]

    def output_dim(self):
        return 1



    def __getitem__(self, idx):
        """
        Retrieve a sample (N tim steps) by index.
        :param idx: Index of the sample to retrieve.
        :return: A sample or a tuple (e.g., data, label).
        """
        start_idx = idx * self.time_horizon
        end_idx = start_idx +  self.time_horizon
        inputs = torch.tensor(self.final_inputs[start_idx:end_idx], dtype=torch.float)
        targets = torch.tensor(self.flattened_targets[start_idx:end_idx], dtype=torch.float)

        return inputs, targets

if __name__ == '__main__':
    config={"time_horizon" : 100}

    dummy_dataset = HAST_Dataset(time_horizon= config["time_horizon"])
    train_dataset = HAST_Dataset(split = "dummy", time_horizon= config["time_horizon"])
    val_dataset = HAST_Dataset(split = "dummy_val", time_horizon= config["time_horizon"])
    print(f"Dataset length: {len(train_dataset)}, {len(val_dataset)}, {len(dummy_dataset)}")

