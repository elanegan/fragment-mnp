"""
Numerical solver for fragment model (:mod:`fragmentmnp.FragmentSolver`)
=============================================================

Runs the calculation for the FRAGMENT-MNP model
"""
from typing import Tuple
from collections.abc import Callable
import numpy as np
import numpy.typing as npt
from scipy.integrate import solve_ivp
from scipy import interpolate
from schema import SchemaError
from . import validation
from .output import FMNPOutput
from ._errors import FMNPNumericalError, FMNPDistributionValueError

def _validate_config(config: dict) -> dict:
    try:
        # Returns the config dict with defaults filled
        config = validation.validate_config(config)
    except SchemaError as err:
        raise SchemaError('Model config did not pass validation!') from err
    return config

def make_fsd(n: int, psd: npt.NDArray[np.float64], beta: float) -> npt.NDArray[np.float64]:
    r"""
    Create the fragment size distribution matrix, assuming that
    fragmentation events result in a split in mass between daughter
    fragments that scales proportionally to :math:`d^\beta`,
    where :math:`d` is the particle diameter and :math:`\beta`
    is an empirical fragment size distribution parameter. For
    example, if :math:`\beta` is negative, then a larger
    proportion of the fragmenting mass goes to smaller size
    classes than larger.

    For an equal split between daughter size classes, set
    :math:`\beta` to 0.

    Parameters
    ----------
    n : int
        Number of particle size classes
    psd : np.ndarray
        Particle size distribution
    beta : float
        Fragment size distribution empirical parameter

    Returns
    -------
    np.ndarray
        Matrix of fragment size distributions for all size classes
    """
    # Start with a zero-filled array of shape (N,N)
    fsd = np.zeros((n, n))
    # Fill with the split to daughter size classes scaled
    # proportionally to d^beta
    for i in np.arange(1, n):
        fsd[i, :-(n-i)] = (psd[:-(n-i)] ** beta
                           / np.sum(psd[:-(n-i)] ** beta))
    return fsd

def make_differential(n_size_classes: int, t_grid: np.ndarray, ik_frag: np.ndarray, ik_diss: np.ndarray, fsd: npt.NDArray[np.float64]) -> Callable[[int, dict], np.ndarray]:
    def f(t, c):
        k_frag = ik_frag
        k_diss = ik_diss

        # Get the number of size classes and create results to be filled
        N = n_size_classes
        dcdt = np.empty(N)
        # Interpolate the time-dependent parameters to the specific
        # timestep given (which will be a float, rather than integer index)
        f_frag = interpolate.interp1d(t_grid, k_frag, axis=1,
                                      fill_value='extrapolate')
        f_diss = interpolate.interp1d(t_grid, k_diss, axis=1,
                                      fill_value='extrapolate')
        k_frag = f_frag(t)
        k_diss = f_diss(t)
        # Loop over the size classes and perform the calculation
        for k in np.arange(N):
            # The differential equation that is being solved
            dcdt[k] = - k_frag[k] * c[k] \
                + np.sum(fsd[:, k] * k_frag * c[:N]) \
                - k_diss[k] * c[k]
        # Return the solution for all of the size classes
        return dcdt
    return f

def make_k_distribution(dims: dict, k_f: float, k_0: float = 0.0,
                       params: dict = {},
                       is_compound: bool = True) -> npt.NDArray[np.float64]:
    r"""
    Create a distribution based on the rate constant scaling factor ``k_f``
    and baseline adjustment factor ``k_0``. The distribution will be a
    compound combination of power law / polynomial, exponential,
    logarithmic and logistic regressions, encapsulated in the function
    :math:`X(x)`, and have dimensions given by `dims`. For a distribution
    with `D` dimensions:

    .. math::
        k(\mathbf{x}) = k_f \prod_{d=1}^D X(x_d) + k_0

    :math:`X(x)` is then given either by:

    .. math::
        X(x) = A_x \hat{x}^{\alpha_x} \cdot B_x e^{-\beta_x \hat{x}}
        \cdot C_x \ln (\gamma_x \hat{x}) \cdot
        \frac{D_x}{1 + e^{-\delta_{x,1}(\hat{x} - \delta_{x,2})}}

    or the user can specify a polynomial instead of the power law term:

    .. math::
        X(x) = \sum_{n=1}^N A_{x,n} \hat{x}^n \cdot
        B_x e^{-\beta_x \hat{x}} \cdot
        C_x \ln (\gamma_x \hat{x}) \cdot
        \frac{D_x}{1 + e^{-\delta_{x,1}(\hat{x} - \delta_{x,2})}}

    In the above, the dimension value :math:`\hat{x}` is normalised such
    that the median value is equal to 1: :math:`\hat{x} = x/\tilde{x}`.

    Parameters
    ----------
    dims : dict
        A dictionary that maps dimension names to their grids, e.g. to
        create a distribution of time `t` and particle surface area `s`,
        `dims` would equal `{'t': t, 's': s}`, where `t` and `s` are the
        timesteps and particle surface area bins over which to create this
        distribution. The dimension names must correspond to the subscripts
        used in `params`. The values are normalised such that the median
        of each dimension is 1.
    k_f : float
        Rate constant scaling factor
    k_0 : float, default=0
        Rate constant baseline adjustment factor
    params : dict, default={}
        A dictionary of values to parameterise the distribution with. See
        the notes below.
    is_compound : bool, default=True
        Whether the regression for each dimension are combined by
        multiplying (compound) or adding.

    Returns
    -------
    k = np.ndarray
        Distribution array over the dims provided

    Notes
    -----
    `k` is modelled as a function of the dims provided, and the model
    builds this distribution as a combination of power law / polynomial,
    exponential, logarithmic and logistic regressions, enabling a broad
    range of dependencies to be accounted for. This distribution is
    intended to be applied to rate constants used in the model, such as
    `k_frag` and `k_diss`. The `params` dict gives the parameters used
    to construct this distribution using the equation above. That is,
    :math:`A_{x}` (where `x` is the dimension), :math:`\alpha_{x_i}` etc
    are given in the `params` dict as e.g. `A_t`, `alpha_t`, where the
    subscript (`t` in this case) is the name of the dimension corresponding
    to the `dims` dict.

    This function does not require any parameters to be present in
    `params`. Non-present values are defaulted to values that remove the
    influence of that particular expression, and letting all parameters
    default results in a constant `k` distribution.

    More specifically, the params that can be specified are:

    A_x : array-like or float, default=1
        Power law coefficient(s) for dim `x` (e.g. ``A_t`` for dim `t`).
        If a scalar is provided, this is used as the coefficient for a
        power law expression with ``alpha_x`` as the exponent. If a list is
        provided, these are used as coefficients in a polynomial
        expression, where the order of the polynomial is given by the
        length of the list. For example, if a length-2 list ``A_t=[2, 3]``
        is given, then the resulting polynomial will be :math:`3t^2 + 2t`
        (note the list is in *ascending* order of polynomials).
    alpha_x : float, default=0
        If `A_x` is a scalar, `alpha_x` is the exponent for this power law
        expression. For example, if ``A_t=2`` and ``alpha_t=0.5``, the
        resulting power law will be :math:`2t^{0.5}`.
    B_x : float, default=1
        Exponential coefficient.
    beta_x : float, default=0
        Exponential scaling factor.
    C_x : float or None, default=None
        If a scalar is given, this is the coefficient for the logarithmic
        expression. If ``None`` is given, the logarithmic expression is
        set to 1 (i.e. it is ignored).
    gamma_x : float, default=1
        Logarithmic scaling factor.
    D_x : float or None, default=None
        If a scalar is given, this is the coefficient for the logistic
        expression. If `None` is given, the logistic expression is set
        to 1.
    delta1_x : float, default=1
        Logistic growth rate (steepness of the logistic curve).
    delta2_x : float or None, default=None
        Midpoint of the logistic curve, which denotes the `x` value where
        the logistic curve is at its midpoint. If `None` is given, the
        midpoint is assumed to be the at the midpoint of the `x` range. For
        example, for the time dimension `t`, if the model timesteps go
        from 1 to 100, then the default is ``delta2_t=50``.

    If any dimension values are equal to 0, the logarithmic term returns 0
    rather than being undefined.

    .. warning:: The parameters used for calculating distributions such as
        `k_frag` and `k_diss` have changed from previous versions, which
        only allowed for a power law relationship. This causes breaking
        changes after v0.1.0.
    """
    if dims == {}:
        raise Exception('Trying to create k distribution but `dims` dict',
                        'is empty. You must provide at least one',
                        'dimension.')
    else:
        # Create a grid out of our dimensions (and preserve the matrix
        # indexing order with 'ij')
        grid = np.meshgrid(*[x for x in dims.values()],
                           indexing='ij')
        # List of the regressions for each dimension, which will be
        # populated when we loop over the dimensions
        X = []
        # Loop over the dimensions
        for i, x in enumerate(grid):
            # Normalise the values
            x_norm = x / np.median(x)
            # Get the name of this dim
            name = list(dims.keys())[i]
            # Pull out the params for convenience
            A = params.get(f'A_{name}', 1.0)
            alpha = float(params.get(f'alpha_{name}', 0.0))
            B = float(params.get(f'B_{name}', 1.0))
            beta = float(params.get(f'beta_{name}', 0.0))
            C = params.get(f'C_{name}', None)
            gamma = float(params.get(f'gamma_{name}', 1.0))
            D = params.get(f'D_{name}', None)
            delta_1 = float(params.get(f'delta1_{name}', 1.0))
            delta_2 = params.get(f'delta2_{name}', None)
            # Let users specify a polynomial by listing A coefficients,
            # presuming the exponents (alpha) will be 1, 2, 3 etc
            # corresponding to the list elements in A. Otherwise, use
            # A and alpha as a power law A*x**alpha
            if isinstance(A, (list, tuple, np.ndarray)):
                powers = np.arange(1, len(A) + 1)
                power_x = 0.0
                for i, power in enumerate(powers):
                    power_x = power_x + A[i] * x_norm**power
            else:
                power_x = float(A) * x_norm**alpha
            # Exponential term
            exp_x = B * np.exp(-beta*x_norm)
            # Only calculate the ln term if C is not None, and if x=0,
            # then set ln(x) to 0
            if C is not None:
                arg = gamma * x_norm
                ln_term = np.log(arg,
                                 out=np.zeros_like(arg, dtype=np.float64),
                                 where=(arg != 0))
                ln_x = float(C) * ln_term
            else:
                ln_x = 1.0
            # If the logistic delta_2 term (the x value at the midpoint
            # along the k axis) isn't specified, # then calculate it as
            # halfway along the x axis
            if (delta_2 is None) and (D is not None):
                delta_2 = (x_norm.max() - x_norm.min()) / 2
            # Calculate the logistic contribution, only if D is not None
            logit_x = float(D) / \
                (1 + np.exp(-delta_1 * (x_norm - float(delta_2)))) \
                if D is not None else 1.0
            # Multiply all the expressions together for this dimension
            X.append(power_x * exp_x * ln_x * logit_x)
        # Calculate the final distribution by multiplying X across the
        # dimensions
        if is_compound:
            k = k_f * np.prod(X, axis=0) + k_0
        else:
            k = k_f * np.sum(X, axis=0) + k_0
        return k

def make_2D_distribution(k_params: dict, surface_areas: np.ndarray, t_grid: np.ndarray ) -> npt.NDArray[np.float64]:
    if isinstance(k_params, dict):
        k_f = k_params['k_f']
        k_0 = k_params['k_0']
        is_compound = k_params['is_compound']
        # Get the params from the dict, excluding the average
        params = {n: p for n, p in k_params.items()
                  if n not in ['k_f', 'k_0']}
    else:
        k_f = k_params
        k_0 = 0.0
        is_compound = True
        params = {}
    # Calculate the 2D (s, t) distribution
    k_dist = make_k_distribution(dims={'s': surface_areas,
                                           't': t_grid},
                                     k_f=k_f, k_0=k_0,
                                     params=params,
                                     is_compound=is_compound)
    # Check no values are less than zero
    if np.any(k_dist < 0.0):
        msg = (f'Value for {k} distribution calculated from input '
               'data resulted in negative values. Ensure '
               f'distribution params are such that all {k} values '
               'are positive.')
        raise FMNPDistributionValueError(msg)
    return k_dist


def surface_area(psd: npt.NDArray[np.float64]) -> \
        npt.NDArray[np.float64]:
    """
    Return the surface area of the particles, presuming they are
    spheres. This function can be overloaded to account for different
    shaped particles.
    """
    return 4.0 * np.pi * (psd / 2.0) ** 2


class FragmentSolver:

    def __init__(self, fsd_beta: float, n_size_classes: int, psd: npt.NDArray[np.float64], dt: float, solver_params: dict) -> None:
        self._dt = dt
        self._n_size_classes = n_size_classes
        self._psd = psd
        self._fsd = make_fsd(n=self._n_size_classes, psd=self._psd, beta=fsd_beta)
        self._surface_areas = surface_area(self._psd)
        self._solver_params = solver_params

    def solve(self, data: dict, n_timesteps: int = 1) -> npt.NDArray[np.float64]:
        k_frag = np.empty((self._n_size_classes, n_timesteps))
        k_diss = np.empty((self._n_size_classes, n_timesteps))
        # make t_grid, distributions
        t_grid = np.arange(0.5*self._dt,
                                n_timesteps*self._dt + 0.5*self._dt,
                                self._dt)
        t_eval = t_grid \
        if self._solver_params['t_eval'] == 'timesteps' \
        else self._solver_params['t_eval']

        k_frag = make_2D_distribution(data['k_frag'], self._surface_areas, t_grid)
        # If the rate constant is k_frag, then no fragmentation is
        # allowed from the smallest size class and therefore we
        # manually set this to zero
        k_frag[0, :] = 0.0
        k_diss = make_2D_distribution(data['k_diss'], self._surface_areas, t_grid)

        # Numerically solve this given the initial values for c
        f = make_differential(n_size_classes=self._n_size_classes, t_grid=t_grid, ik_frag=k_frag, ik_diss=k_diss, fsd=self._fsd)
        soln = solve_ivp(fun=f,
                         method=self._solver_params['method'],
                         t_span=(t_grid.min(), t_grid.max()),
                         y0=data['initial_concs'],
                         t_eval=t_eval,
                         rtol=self._solver_params['rtol'],
                         atol=self._solver_params['atol'],
                         max_step=self._solver_params['max_step'])
        # If we didn't find a solution, raise an error
        if not soln.success:
            raise FMNPNumericalError('Model solution could not be ' +
                                     f'found: {soln.message}')
        return soln
#        # Calculate the timeseries of mass concentration lost to dissolution
#        # from the solution, first interpolating k_diss to the t values
#        # we evaluated the solution over (t_eval)
#        f_diss = interpolate.interp1d(t_grid, k_diss, axis=1,
#                                      fill_value='extrapolate')
#        k_diss_eval = f_diss(t_eval)
#        j_diss = k_diss_eval * soln.y
#        # Use this to calculate the cumulative mass concentration
#        # lost to dissolution
#        c_diss_from_sc = np.cumsum(j_diss, axis=1)
#        # Add initial concentration and sum across size classes
#        c_diss = np.sum(np.cumsum(j_diss, axis=1), axis=0) \
#            + data["initial_concs_diss"]
#        # Now we have the solutions as mass concentrations, we can
#        # convert to particle number concentrations
#        n = self.mass_to_particle_number(soln.y)
#        n_diss_from_sc = self.mass_to_particle_number(c_diss)
#
#        # Return the solution in an FMNPOutput object
#        output = FMNPOutput(soln.t, soln.y, n, c_diss_from_sc, c_diss,
#                          n_diss_from_sc, soln, self._psd)
#        return output
