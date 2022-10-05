import os
from dotenv import load_dotenv

import torch


#workaround for https://github.com/facebookresearch/fairseq/issues/2510
class GELU(torch.nn.Module):
    def forward(self, input: torch.Tensor) -> torch.Tensor:
        return torch.nn.functional.gelu(input)
torch.nn.modules.activation.GELU = GELU


class ModelProvider:
    def __init__(self) -> None:
        load_dotenv() 
        self.is_init = False
        self.model = torch.load(os.getenv('model_path'))
        self.model.eval()
        self.is_init = True

    def get_maniqa_model(self) -> torch.nn.Module:
        return self.model