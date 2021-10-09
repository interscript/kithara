
import argparse
import random

import numpy as np
import torch
import wandb

from trainer import (
    CBHGTrainer
)

SEED = 1234
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


def train_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_kind", dest="model_kind", type=str, required=True)
    parser.add_argument("--config", dest="config", type=str, required=True)
    parser.add_argument(
        "--reset_dir",
        dest="clear_dir",
        action="store_true",
        help="deletes everything under this config's folder.",
    )
    return parser


parser = train_parser()
args = parser.parse_args()


if args.model_kind in ['baseline',"cbhg"]:
    trainer = CBHGTrainer(args.config, args.model_kind)
else:
    raise ValueError("The model kind is not supported")

    
"""
        if not self.config['wandb_run'] is None:
            wandb.login()
            wandb.watch(self.model, self.criterion, log="all", log_freq=10)
            wandb.log({**test(model, test_dataset),
                       **test_metrics(model, config)})
"""

# Define Experiments using Wandb
sweep_config = {
    # search method
    'method': 'random', #grid, random
    # metric and objective
    'metric': {
      'name': 'DEC',
      'goal': 'maximize' #'minimize'   
    },
    # define search parameters
    'parameters': {
        'max_steps': {
            'values': [4000]
        },
        'batch_size': {
            'values': [32] #[128, 64, 32]
        },
        'cbhg_filters': {
            'values': [16]
        },
        'cbhg_gru_units': {
            'values': [256]
        },
        'cbhg_projections': {
            'values': [[128, 256]] #, [256, 512]]
        },
        
        'dropout': {
            'values': [0.3, 0.4, 0.5]
        },
        'learning_rate': {
            'values': [1e-2, 1e-3, 1e-4, 3e-4, 3e-5, 1e-5]
        },
        'fc_layer_size': {
            'values': [128,256,512]
        },
        'post_cbhg_layers_units': {
            'values': [256, 256]
        },
        
        'optimizer': {
            'values': ['Adam', 'SGD']
        },
        'use_prenet': {
            'values': ['false']
        }
        prenet_sizes: {
            'values': [[512, 256]]
        }
        
    }
}

run_name = "Hyperparams Search"

wandb.login()
sweep_id = wandb.sweep(sweep_config, project=run_name)
wandb.init(config=config_defaults)
    
# Config is a variable that holds and saves hyperparameters and inputs
config = wandb.config


trainer.run_wandb(config)



