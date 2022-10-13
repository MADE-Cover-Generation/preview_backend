import os
from dotenv import load_dotenv

import torch

from model_providers.maniqa.maniqa import MANIQA


class ModelProvider:
    def __init__(self):
        load_dotenv() 
        model_path = os.getenv('model_path')
        self.model = MANIQA()
        self.model.load_state_dict(torch.load(model_path))
        print(model_path)
        
        self.model.eval()
        self.is_init = True

    def get_maniqa_model(self):
        return self.model