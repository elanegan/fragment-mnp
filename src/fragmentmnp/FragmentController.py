"""
Handler of data produced by FragmentSolver (:mod:`fragmentmnp.FragmentController`)
=============================================================

Controls running and data input/output for the FRAGMENT-MNP model
"""
from typing import Tuple
import numpy as np
import numpy.typing as npt
from scipy.integrate import solve_ivp
from scipy import interpolate
from schema import SchemaError
from . import validation
from . import FragmentSolver
from .output import FMNPOutput
from ._errors import FMNPNumericalError, FMNPDistributionValueError
import json
import fastjsonschema as fjs
from . import jsonvalidator
import io

# Mostly just a class to handle IO for the solver.
# Saves results, loads config
class FragmentController:
    def _validate_config(config: dict) -> dict:
        try:
            # Returns the config dict with defaults filled
            config = validation.validate_config(config)
        except SchemaError as err:
            raise SchemaError('Model config did not pass validation!') from err
        return config

    def __init__(self, fsd_beta: float, n_size_classes: int, psd: npt.NDArray[np.float64], dt: float, solver_params: dict, save_on_solve: bool, io_input_data: io.TextIOBase, io_output_data: io.TextIOBase, id: int):
        self._solver = FragmentSolver(fsd_beta, n_size_classes, psd, dt, solver_params)
        self._id = id
        self._time = 0.0
        self._save_on_solve = save_on_solve
        self._io_input_data = io_input_data
        self._io_output_data = io_output_data
        self._soln_t = []
        self._soln_y = []
        self._c_diss_from_sc = []

    def from_json(cls, json_str):
        schema_validated = validate(json_str)
        # config = validation.validate_config(schema_validated)
        return cls(**schema_validated)

#    def from_file_like(cls: type[FragmentController], file_like: TextIOBase) -> FragmentController:
#        # do some basic manipulations on config to fit to a more clean interface
#        config = validation.validate_config(yaml.safe_load(file_like))
#
#        if "initial_concs" in config:
#            config["initial_concs"] = np.array(config["initial_concs"])
#
#        if "particle_size_classes" in config:
#            config["psd"] = np.array(config["particle_size_classes"])
#            config.pop("particle_size_classes", None)
#        elif "particle_size_range" in config:
#            config["psd"] = np.logspace(*config["particle_size_range"], config["n_size_classes"])
#            config.pop("particle_size_range", None)
#        else:
#            raise ValueError('particle_size_classes or particle_size_range ' +
#                             'must be present in the model config, but ' +
#                             'neither were found.')
#        return cls(**config)

    def step(self, n_timesteps: int = 1) -> None:
        # data locations from config file
        # get data from file
        indata = json.load(self._io_input_data)
        # solve on data
        soln_t, soln_y, c_diss_from_sc = self._solver.solve(indata, n_timesteps)
        # store results
        self._soln_t.append(soln_t.tolist())
        self._soln_y.append(soln_y.tolist())
        self._c_diss_from_sc.append(c_diss_from_sc.tolist())
        if self._save_on_solve:
            # convert solution to text format, for portability
            # save output at save location
            self.save()

    def output_to_json(self, soln_t, soln_y, c_diss_from_sc):
        jsonstr = json.dumps({"soln_t": soln_t, "soln_y": soln_y, "c_diss_from_sc": c_diss_from_sc})
        return jsonstr

    def save(self) -> None:
        outjson = self.output_to_json(self._soln_t, self._soln_y, self._c_diss_from_sc)
        self._io_output_data.write(outjson)

    def finalize(self) -> None:
        # convert solution to text format, for portability
        # save output at save location
        self.save()

    @property
    def time(self) -> float:
        return self._time

    @property
    def time_step(self) -> float:
        return self._time_step

    @time_step.setter
    def set_time_step(self, time_step: float) -> None:
        self._time_step = time_step

    def advance_in_time(self) -> None:
        self._time += self._time_step
