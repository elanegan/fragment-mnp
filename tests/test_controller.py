from fragmentmnp.FragmentController import FragmentController
import numpy as np
import json

fsd_beta = 0.0
n_size_classes = 7
size_range = [-9, -3]
psd = np.logspace(*size_range, n_size_classes)
dt = 1
solver_params = {
    'method': 'RK45',
    'rtol': 1e-3,
    'atol': 1e-6,
    'max_step': np.inf,
    't_eval': 'timesteps'
}

_k_dist_params = {}
for x in ['t', 's']:
    _k_dist_params[f'A_{x}'] = 1.0
    _k_dist_params[f'alpha_{x}'] = 0.0
    _k_dist_params[f'B_{x}'] = 1.0
    _k_dist_params[f'beta_{x}'] = 0.0
    _k_dist_params[f'C_{x}'] = None
    _k_dist_params[f'gamma_{x}'] = 1.0
    _k_dist_params[f'D_{x}'] = None
    _k_dist_params[f'delta1_{x}'] = 1.0
    _k_dist_params[f'delta2_{x}'] = None

data = {
    'initial_concs': [42.0] * n_size_classes,
    'initial_concs_diss': 0.0,
    'density': 1380,              # PET density [kg/m3]
    'k_frag': {'k_f': 0.01,
               'k_0': 0.0,
               'is_compound': True,
               **_k_dist_params},
    'k_diss': {'k_f': 0.0,
               'k_0': 0.0,
               'is_compound': True,
               **_k_dist_params}
}

data_input_location = "data.json"
data_output_location = "output.json"

with open(data_input_location, "w") as datafile:
    json.dump(data, datafile)

n_timesteps = 100

save_on_solve = False
id = 1

controller = FragmentController(fsd_beta, n_size_classes, psd, dt, solver_params, save_on_solve, data_input_location, data_output_location, id)

controller.step(n_timesteps)
controller.finalize()

with open(data_output_location, "r") as outdatafile:
    outdata = outdatafile.read()

print(outdata)
