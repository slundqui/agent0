"""Runs an evaluation episode from a saved model."""

import os

import gymnasium as gym
from stable_baselines3 import A2C
from stable_baselines3.common.monitor import Monitor
from traiderdaive import SimpleHyperdriveEnv


def run_eval():
    """Runs an evaluation episode from a saved model."""
    # Create log dirs
    log_dir = ".traider_models/"
    os.makedirs(log_dir, exist_ok=True)

    gym_config = SimpleHyperdriveEnv.Config()
    env = gym.make("traiderdaive/simple_hyperdrive_env", gym_config=gym_config)
    env = Monitor(env, log_dir)

    model = A2C.load(log_dir + "/best_model.zip", device="cpu")

    # Run Evaluation
    obs, _ = env.reset()
    while True:
        action, _states = model.predict(obs, deterministic=True)
        obs, _, terminated, truncated, _ = env.step(action)
        if terminated or truncated:
            break

    # Run dashboard from env
    dashboard_cmd = env.interactive_hyperdrive.get_dashboard_command()
    print(dashboard_cmd)

    # Put breakpoint here to keep the database running under the hood when accessing the dashboard
    # TODO fix this workflow


if __name__ == "__main__":
    run_eval()