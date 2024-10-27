import gymnasium as gym
import ale_py
import torch

from agent import DeepQLearningAgent

gym.register_envs(ale_py)

env = gym.make("ALE/Breakout-v5", obs_type="grayscale", render_mode="human")
agent = DeepQLearningAgent(1e-4, 0.05, env.action_space.n)  # pyright: ignore
agent.model.load_state_dict(torch.load("../w_01eps/ep_10000.pt", weights_only=False, map_location=torch.device("cpu")))
agent.model.eval()

s, _ = env.reset(seed=42)
last_frames = [torch.tensor(s) for _ in range(4)]
for i in range(10000):
    phi_t = agent.preprocess_frames(torch.stack(last_frames))
    action = agent.get_action(phi_t.unsqueeze(0))

    # execute action in env and clip reward
    new_s, r, done, _, _ = env.step(action)

    last_frames.pop(0)
    last_frames.append(torch.tensor(new_s))

    if done:
        break