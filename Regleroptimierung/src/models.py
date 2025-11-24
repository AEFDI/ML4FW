from dataset import HAST_Dataset
import torch.nn as nn
import torch.nn.functional as F


class MLPModel(nn.Module):
    """
    Multi-Layer Perceptron (MLP) für Sequenzdaten.
    """
    def __init__(self, input_dim=24, hidden_dims=[128, 64], output_dim=20,dropout_rate=0.5, flatten =True):
        super(MLPModel, self).__init__()
        self.flatten= flatten
        self.input_dim = input_dim
        self.sequence_length = 20
        self.flattened_input_dim = input_dim * 20

        self.fc1 = nn.Linear(self.flattened_input_dim, hidden_dims[0])
        self.bn1 = nn.BatchNorm1d(hidden_dims[0])
        self.dropout1 = nn.Dropout(dropout_rate)

        self.fc2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.bn2 = nn.BatchNorm1d(hidden_dims[1])
        self.dropout2 = nn.Dropout(dropout_rate)

        self.fc3 = nn.Linear(hidden_dims[1], output_dim)

    def forward(self, x):
        batch_size = x.size(0)
        if self.flatten:
            x = x.view(batch_size, -1)

        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)

        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)

        x = self.fc3(x)
        return x


class CNNModel(nn.Module):
    """
    1D Convolutional Neural Network (CNN) zur Verarbeitung von Zeitreihendaten.
    """
    def __init__(self, input_features=24, sequence_length=20, dropout_rate=0.6,n_layers = 2, batch_norm = True,
                 kernel_size= 3, pad = 1, size_out = 20, pool=True):
        super(CNNModel, self).__init__()

        layers = []
        self.output_size = size_out
        in_channels = input_features
        for i in range(n_layers):
            out_channels = 64 if i == 0 else 32
            layers.append(nn.Conv1d(in_channels, out_channels, kernel_size=kernel_size, padding=pad))
            sequence_length = sequence_length + 2*pad - kernel_size + 1


            if batch_norm:
                layers.append(nn.BatchNorm1d(out_channels))

            layers.append(nn.ReLU())

            if dropout_rate > 0:
                layers.append(nn.Dropout(dropout_rate))
            if pool and i % 2 == 1:
                layers.append(nn.MaxPool1d(kernel_size=2))
                sequence_length //= 2

            in_channels = out_channels

        self.conv_layers = nn.Sequential(*layers)
        self.fc = nn.Linear(in_channels * sequence_length, self.output_size)

    def forward(self, x):
        x = x.permute(0, 2, 1)
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x


class LSTMModel(nn.Module):
    """
    Long Short-Term Memory (LSTM) Modell für die Sequenzvorhersage.
    """
    def __init__(self, input_size=24, hidden_size=64, num_layers=2, output_size=20, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                            num_layers=num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size, output_size)
        self.bn = nn.BatchNorm1d(hidden_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out, (hn, cn) = self.lstm(x)
        final_hidden = hn[-1]
        final_hidden = self.bn(final_hidden)
        final_hidden = self.dropout(final_hidden)
        output = self.fc(final_hidden)
        return output

if __name__ == '__main__':
    from torch.utils.data import DataLoader
    dataset = HAST_Dataset()
    print(f"Dataset length: {len(dataset)}")
    train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    x,y = next(iter(train_loader))

    mlp = MLPModel()
    cnn = CNNModel()
    lstm = LSTMModel()
    pred_mlp = mlp(x)
    pred_cnn = cnn(x)
    pred_lstm = lstm(x)

    print(pred_mlp.shape)
    print(pred_cnn.shape)
    print(pred_lstm.shape)

