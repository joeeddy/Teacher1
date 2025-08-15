import numpy as np

def get_dynamic_neighborhood(ai, i, j, c):
    # Example: dynamic, deformable and possibly learned neighborhood
    r = int(2 + ai.dynamic_params[i, j, c, 0] * 10)
    kernel_shape = (2*r+1, 2*r+1)
    arr = ai.state[:, :, c, 0]
    ni = [(i + dx) % ai.size for dx in range(-r, r+1)]
    nj = [(j + dy) % ai.size for dy in range(-r, r+1)]
    neighborhood = arr[np.ix_(ni, nj)]
    # Dynamic weights, could be learned or context-dependent
    weights = np.tanh(np.random.randn(*kernel_shape) * ai.dynamic_params[i, j, c, 1])
    return neighborhood, weights

def param_vector_leaky_relu(x, a):
    return np.where(x > 0, x, a*x)

def apply_hierarchical_attention(ai, i, j, c, glob):
    # Example: combine levels of global, local, and historical features via attention
    attn = ai.dynamic_params[i, j, c, 2:5]
    local = ai.state[i, j, c]
    globalv = glob['mean'][c, :]
    history = np.mean(ai.history[i, j, c], axis=0)
    return attn[0]*local + attn[1]*globalv + attn[2]*history

def update_history_variable(history, i, j, c, new_val):
    history[i,j,c] = np.roll(history[i,j,c], shift=-1, axis=0)
    history[i,j,c][-1] = new_val

def global_measures_advanced(state, history, global_workspace):
    mean = np.mean(state, axis=(0,1))
    std = np.std(state, axis=(0,1))
    entropy = -np.sum(state * np.log(np.clip(state, 1e-8, 1)), axis=(0,1)) / (state.shape[0]*state.shape[1])
    mean_all = np.mean(state)
    hist_mean = np.mean(history, axis=(0,1,2))
    gw_mean = np.mean(global_workspace)
    return dict(mean=mean, std=std, entropy=entropy, mean_all=mean_all, hist_mean=hist_mean, gw_mean=gw_mean)

def meta_learn_params(ai, i, j, c):
    p = ai.dynamic_params[i, j, c]
    out = {
        'attn_nh': p[0],
        'attn_hier': p[1],
        'attn_rec': p[2],
        'attn_syn': p[3],
        'attn_pred': p[4],
        'attn_gw': p[5],
        'activation_a': np.clip(p[6], 0.01, 1.0)
    }
    return out

def dynamic_synaptic_update(ai, i, j, c):
    # Example: sum of remote synaptic signals
    syns = ai.synapses[i, j, c]
    vals = [ai.state[si%ai.size, sj%ai.size, c] for si, sj in syns]
    return np.sum(vals, axis=0) / max(1, len(vals))

def recursive_state_update(ai, i, j, c, input_state=None):
    # Example: apply a recursive nonlinear transformation
    s = ai.state[i, j, c] if input_state is None else input_state
    for _ in range(2):  # two layers of recursion
        s = np.tanh(s * 1.4 - 0.7)
    return s

def predictive_coding_update(ai, i, j, c, history):
    # Example: prediction error of the next state
    pred = np.mean(history[i, j, c][-4:-1], axis=0)
    error = ai.state[i, j, c] - pred
    return -error

def global_workspace_update(ai, i, j, c, gw, mode="cell", latest_state=None):
    # Example: update the global workspace vector
    if mode == "full" and latest_state is not None:
        return 0.99*gw + 0.01*np.mean(latest_state, axis=(0,1,2))
    elif i is not None and j is not None and c is not None:
        return gw * 0.99 + 0.01 * ai.state[i, j, c, :]
    else:
        return gw
