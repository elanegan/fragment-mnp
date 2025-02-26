from fragmentmnp.FragmentSolver import FragmentSolver
import numpy as np

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

n_timesteps = 100

solver = FragmentSolver(fsd_beta, n_size_classes, psd, dt, solver_params)

soln = solver.solve(data, n_timesteps)

print(soln)
