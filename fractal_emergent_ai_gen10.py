import numpy as np
import matplotlib.pyplot as plt
from fractal_modules import (
    get_dynamic_neighborhood,
    param_vector_leaky_relu,
    apply_hierarchical_attention,
    update_history_variable,
    global_measures_advanced,
    meta_learn_params,
    dynamic_synaptic_update,
    recursive_state_update,
    predictive_coding_update,
    global_workspace_update,
)

class FractalEmergentAI:
    def __init__(self, size=64, channels=33, state_dim=5, max_species=20):
        self.size = size
        self.channels = channels
        self.state_dim = state_dim
        self.state = np.random.rand(size, size, channels, state_dim)
        self.species = np.random.randint(0, max_species, (size, size, channels))
        self.dynamic_params = np.random.rand(size, size, channels, 8)
        self.synapses = np.random.randint(0, size, (size, size, channels, 4, 2))
        self.history = np.random.rand(size, size, channels, 24, state_dim)
        self.global_workspace = np.random.rand(16)

    def step(self, lr=0.0011):
        new_state = np.zeros_like(self.state)
        glob = global_measures_advanced(self.state, self.history, self.global_workspace)
        for i in range(self.size):
            for j in range(self.size):
                for c in range(self.channels):
                    dyn_nh, nh_weights = get_dynamic_neighborhood(self, i, j, c)
                    hierarchy_in = apply_hierarchical_attention(self, i, j, c, glob)
                    rec_state = recursive_state_update(self, i, j, c)
                    syn_input = dynamic_synaptic_update(self, i, j, c)
                    pred_coding = predictive_coding_update(self, i, j, c, self.history)
                    meta_params = meta_learn_params(self, i, j, c)
                    gw_in = global_workspace_update(self, i, j, c, self.global_workspace)
                    agg = (
                        meta_params['attn_nh'] * np.sum(dyn_nh * nh_weights, axis=0) +
                        meta_params['attn_hier'] * hierarchy_in +
                        meta_params['attn_rec'] * rec_state +
                        meta_params['attn_syn'] * syn_input +
                        meta_params['attn_pred'] * pred_coding +
                        meta_params['attn_gw'] * gw_in
                    )
                    out = param_vector_leaky_relu(agg, meta_params['activation_a'])
                    out = recursive_state_update(self, i, j, c, input_state=out)
                    new_state[i,j,c] = out
                    update_history_variable(self.history, i, j, c, out)
        self.global_workspace = global_workspace_update(self, None, None, None, self.global_workspace, mode="full", latest_state=new_state)
        self.state = new_state

    def run(self, steps=8000, show=True):
        if show:
            plt.ion()
        for t in range(steps):
            self.step()
            if show:
                plt.clf()
                img = np.clip(self.state[:,:,:3,0], 0, 1)
                plt.imshow(img, interpolation="nearest")
                plt.title("Gen 10: Ultra-Recursive, Meta-Fractal, Self-Organizing, Self-Learning AI")
                gmean = np.mean(self.state)
                gstd = np.std(self.state)
                gentropy = -np.sum(self.state * np.log(np.clip(self.state,1e-8, 1))) / (self.size*self.size*self.channels*self.state_dim)
                plt.xlabel(f"Step {t} | Mean: {gmean:.3f} | Std: {gstd:.3f} | Entropy: {gentropy:.2f}")
                plt.axis('off')
                plt.pause(0.003)
        if show:
            plt.ioff()
            plt.show()

if __name__ == "__main__":
    ai = FractalEmergentAI(size=64, channels=33, state_dim=5, max_species=20)
    ai.run(steps=8000)
