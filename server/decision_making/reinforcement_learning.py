import torch
import torch.nn as nn
import torch.optim as optim

class CombatAgent(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(CombatAgent, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.linear = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, hidden):
        lstm_out, hidden = self.lstm(x, hidden)
        return self.linear(lstm_out[:, -1, :]), hidden

    def init_hidden(self, batch_size):
        return (torch.zeros(1, batch_size, self.hidden_dim),
                torch.zeros(1, batch_size, self.hidden_dim))


    def run(self, opponent_information):
        # Example input and output dimensions
        input_dim = 5  
        hidden_dim = 128  
        output_dim = 2  # Angular velocity and velocity

        model = CombatAgent(input_dim, hidden_dim, output_dim)