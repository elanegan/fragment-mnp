VERSION = "2.21.1"
from decimal import Decimal
from fastjsonschema import JsonSchemaValueException


NoneType = type(None)

def validate(data, custom_formats={}, name_prefix=None):
    if not isinstance(data, (dict)):
        raise JsonSchemaValueException("" + (name_prefix or "data") + " must be object", value=data, name="" + (name_prefix or "data") + "", definition={'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'Config', 'description': 'Configuration options for Fragment-MNP model.', 'type': 'object', 'properties': {'n_size_classes': {'description': 'Number of particle size classes to model', 'type': 'integer', 'minimum': 1}, 'particle_size_classes': {'description': 'Particle size distribution', 'type': 'array', 'items': {'type': 'number', 'exclusiveMinimum': 0}, 'minItems': 1}, 'dt': {'description': 'Size of time step', 'type': 'number', 'exclusiveMinimum': 0}, 'solver_config': {'description': 'Configuration options for the numerical solver', 'type': 'object', 'properties': {'method': {'description': 'Name of the numerical solver to use', 'type': 'string'}, 'rtol': {'description': 'Relative tolerance for solver', 'type': 'number'}, 'atol': {'description': 'Absolute tolerance for solver', 'type': 'number'}, 'max_step': {'description': 'Maximum allowed step size for solver', 'type': 'number'}, 't_eval': {'description': 'Times at which to store the computed solution', 'type': 'array', 'items': {'type': 'number', 'minItems': 1}}}}, 'input_location': {'description': 'Location to load the input data from', 'type': 'string'}, 'output_location': {'description': 'Location to store solution data to', 'type': 'string'}, 'id': {'description': 'Unique identifier for this model run', 'type': 'integer'}}, 'required': ['n_size_classes', 'particle_size_classes', 'input_location', 'output_location', 'id']}, rule='type')
    data_is_dict = isinstance(data, dict)
    if data_is_dict:
        data__missing_keys = set(['n_size_classes', 'particle_size_classes', 'input_location', 'output_location', 'id']) - data.keys()
        if data__missing_keys:
            raise JsonSchemaValueException("" + (name_prefix or "data") + " must contain " + (str(sorted(data__missing_keys)) + " properties"), value=data, name="" + (name_prefix or "data") + "", definition={'$schema': 'https://json-schema.org/draft/2020-12/schema', 'title': 'Config', 'description': 'Configuration options for Fragment-MNP model.', 'type': 'object', 'properties': {'n_size_classes': {'description': 'Number of particle size classes to model', 'type': 'integer', 'minimum': 1}, 'particle_size_classes': {'description': 'Particle size distribution', 'type': 'array', 'items': {'type': 'number', 'exclusiveMinimum': 0}, 'minItems': 1}, 'dt': {'description': 'Size of time step', 'type': 'number', 'exclusiveMinimum': 0}, 'solver_config': {'description': 'Configuration options for the numerical solver', 'type': 'object', 'properties': {'method': {'description': 'Name of the numerical solver to use', 'type': 'string'}, 'rtol': {'description': 'Relative tolerance for solver', 'type': 'number'}, 'atol': {'description': 'Absolute tolerance for solver', 'type': 'number'}, 'max_step': {'description': 'Maximum allowed step size for solver', 'type': 'number'}, 't_eval': {'description': 'Times at which to store the computed solution', 'type': 'array', 'items': {'type': 'number', 'minItems': 1}}}}, 'input_location': {'description': 'Location to load the input data from', 'type': 'string'}, 'output_location': {'description': 'Location to store solution data to', 'type': 'string'}, 'id': {'description': 'Unique identifier for this model run', 'type': 'integer'}}, 'required': ['n_size_classes', 'particle_size_classes', 'input_location', 'output_location', 'id']}, rule='required')
        data_keys = set(data.keys())
        if "n_size_classes" in data_keys:
            data_keys.remove("n_size_classes")
            data__nsizeclasses = data["n_size_classes"]
            if not isinstance(data__nsizeclasses, (int)) and not (isinstance(data__nsizeclasses, float) and data__nsizeclasses.is_integer()) or isinstance(data__nsizeclasses, bool):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".n_size_classes must be integer", value=data__nsizeclasses, name="" + (name_prefix or "data") + ".n_size_classes", definition={'description': 'Number of particle size classes to model', 'type': 'integer', 'minimum': 1}, rule='type')
            if isinstance(data__nsizeclasses, (int, float, Decimal)):
                if data__nsizeclasses < 1:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".n_size_classes must be bigger than or equal to 1", value=data__nsizeclasses, name="" + (name_prefix or "data") + ".n_size_classes", definition={'description': 'Number of particle size classes to model', 'type': 'integer', 'minimum': 1}, rule='minimum')
        if "particle_size_classes" in data_keys:
            data_keys.remove("particle_size_classes")
            data__particlesizeclasses = data["particle_size_classes"]
            if not isinstance(data__particlesizeclasses, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".particle_size_classes must be array", value=data__particlesizeclasses, name="" + (name_prefix or "data") + ".particle_size_classes", definition={'description': 'Particle size distribution', 'type': 'array', 'items': {'type': 'number', 'exclusiveMinimum': 0}, 'minItems': 1}, rule='type')
            data__particlesizeclasses_is_list = isinstance(data__particlesizeclasses, (list, tuple))
            if data__particlesizeclasses_is_list:
                data__particlesizeclasses_len = len(data__particlesizeclasses)
                if data__particlesizeclasses_len < 1:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".particle_size_classes must contain at least 1 items", value=data__particlesizeclasses, name="" + (name_prefix or "data") + ".particle_size_classes", definition={'description': 'Particle size distribution', 'type': 'array', 'items': {'type': 'number', 'exclusiveMinimum': 0}, 'minItems': 1}, rule='minItems')
                for data__particlesizeclasses_x, data__particlesizeclasses_item in enumerate(data__particlesizeclasses):
                    if not isinstance(data__particlesizeclasses_item, (int, float, Decimal)) or isinstance(data__particlesizeclasses_item, bool):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".particle_size_classes[{data__particlesizeclasses_x}]".format(**locals()) + " must be number", value=data__particlesizeclasses_item, name="" + (name_prefix or "data") + ".particle_size_classes[{data__particlesizeclasses_x}]".format(**locals()) + "", definition={'type': 'number', 'exclusiveMinimum': 0}, rule='type')
                    if isinstance(data__particlesizeclasses_item, (int, float, Decimal)):
                        if data__particlesizeclasses_item <= 0:
                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".particle_size_classes[{data__particlesizeclasses_x}]".format(**locals()) + " must be bigger than 0", value=data__particlesizeclasses_item, name="" + (name_prefix or "data") + ".particle_size_classes[{data__particlesizeclasses_x}]".format(**locals()) + "", definition={'type': 'number', 'exclusiveMinimum': 0}, rule='exclusiveMinimum')
        if "dt" in data_keys:
            data_keys.remove("dt")
            data__dt = data["dt"]
            if not isinstance(data__dt, (int, float, Decimal)) or isinstance(data__dt, bool):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".dt must be number", value=data__dt, name="" + (name_prefix or "data") + ".dt", definition={'description': 'Size of time step', 'type': 'number', 'exclusiveMinimum': 0}, rule='type')
            if isinstance(data__dt, (int, float, Decimal)):
                if data__dt <= 0:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".dt must be bigger than 0", value=data__dt, name="" + (name_prefix or "data") + ".dt", definition={'description': 'Size of time step', 'type': 'number', 'exclusiveMinimum': 0}, rule='exclusiveMinimum')
        if "solver_config" in data_keys:
            data_keys.remove("solver_config")
            data__solverconfig = data["solver_config"]
            if not isinstance(data__solverconfig, (dict)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".solver_config must be object", value=data__solverconfig, name="" + (name_prefix or "data") + ".solver_config", definition={'description': 'Configuration options for the numerical solver', 'type': 'object', 'properties': {'method': {'description': 'Name of the numerical solver to use', 'type': 'string'}, 'rtol': {'description': 'Relative tolerance for solver', 'type': 'number'}, 'atol': {'description': 'Absolute tolerance for solver', 'type': 'number'}, 'max_step': {'description': 'Maximum allowed step size for solver', 'type': 'number'}, 't_eval': {'description': 'Times at which to store the computed solution', 'type': 'array', 'items': {'type': 'number', 'minItems': 1}}}}, rule='type')
            data__solverconfig_is_dict = isinstance(data__solverconfig, dict)
            if data__solverconfig_is_dict:
                data__solverconfig_keys = set(data__solverconfig.keys())
                if "method" in data__solverconfig_keys:
                    data__solverconfig_keys.remove("method")
                    data__solverconfig__method = data__solverconfig["method"]
                    if not isinstance(data__solverconfig__method, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".solver_config.method must be string", value=data__solverconfig__method, name="" + (name_prefix or "data") + ".solver_config.method", definition={'description': 'Name of the numerical solver to use', 'type': 'string'}, rule='type')
                if "rtol" in data__solverconfig_keys:
                    data__solverconfig_keys.remove("rtol")
                    data__solverconfig__rtol = data__solverconfig["rtol"]
                    if not isinstance(data__solverconfig__rtol, (int, float, Decimal)) or isinstance(data__solverconfig__rtol, bool):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".solver_config.rtol must be number", value=data__solverconfig__rtol, name="" + (name_prefix or "data") + ".solver_config.rtol", definition={'description': 'Relative tolerance for solver', 'type': 'number'}, rule='type')
                if "atol" in data__solverconfig_keys:
                    data__solverconfig_keys.remove("atol")
                    data__solverconfig__atol = data__solverconfig["atol"]
                    if not isinstance(data__solverconfig__atol, (int, float, Decimal)) or isinstance(data__solverconfig__atol, bool):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".solver_config.atol must be number", value=data__solverconfig__atol, name="" + (name_prefix or "data") + ".solver_config.atol", definition={'description': 'Absolute tolerance for solver', 'type': 'number'}, rule='type')
                if "max_step" in data__solverconfig_keys:
                    data__solverconfig_keys.remove("max_step")
                    data__solverconfig__maxstep = data__solverconfig["max_step"]
                    if not isinstance(data__solverconfig__maxstep, (int, float, Decimal)) or isinstance(data__solverconfig__maxstep, bool):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".solver_config.max_step must be number", value=data__solverconfig__maxstep, name="" + (name_prefix or "data") + ".solver_config.max_step", definition={'description': 'Maximum allowed step size for solver', 'type': 'number'}, rule='type')
                if "t_eval" in data__solverconfig_keys:
                    data__solverconfig_keys.remove("t_eval")
                    data__solverconfig__teval = data__solverconfig["t_eval"]
                    if not isinstance(data__solverconfig__teval, (list, tuple)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".solver_config.t_eval must be array", value=data__solverconfig__teval, name="" + (name_prefix or "data") + ".solver_config.t_eval", definition={'description': 'Times at which to store the computed solution', 'type': 'array', 'items': {'type': 'number', 'minItems': 1}}, rule='type')
                    data__solverconfig__teval_is_list = isinstance(data__solverconfig__teval, (list, tuple))
                    if data__solverconfig__teval_is_list:
                        data__solverconfig__teval_len = len(data__solverconfig__teval)
                        for data__solverconfig__teval_x, data__solverconfig__teval_item in enumerate(data__solverconfig__teval):
                            if not isinstance(data__solverconfig__teval_item, (int, float, Decimal)) or isinstance(data__solverconfig__teval_item, bool):
                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".solver_config.t_eval[{data__solverconfig__teval_x}]".format(**locals()) + " must be number", value=data__solverconfig__teval_item, name="" + (name_prefix or "data") + ".solver_config.t_eval[{data__solverconfig__teval_x}]".format(**locals()) + "", definition={'type': 'number', 'minItems': 1}, rule='type')
                            data__solverconfig__teval_item_is_list = isinstance(data__solverconfig__teval_item, (list, tuple))
                            if data__solverconfig__teval_item_is_list:
                                data__solverconfig__teval_item_len = len(data__solverconfig__teval_item)
                                if data__solverconfig__teval_item_len < 1:
                                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".solver_config.t_eval[{data__solverconfig__teval_x}]".format(**locals()) + " must contain at least 1 items", value=data__solverconfig__teval_item, name="" + (name_prefix or "data") + ".solver_config.t_eval[{data__solverconfig__teval_x}]".format(**locals()) + "", definition={'type': 'number', 'minItems': 1}, rule='minItems')
        if "input_location" in data_keys:
            data_keys.remove("input_location")
            data__inputlocation = data["input_location"]
            if not isinstance(data__inputlocation, (str)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".input_location must be string", value=data__inputlocation, name="" + (name_prefix or "data") + ".input_location", definition={'description': 'Location to load the input data from', 'type': 'string'}, rule='type')
        if "output_location" in data_keys:
            data_keys.remove("output_location")
            data__outputlocation = data["output_location"]
            if not isinstance(data__outputlocation, (str)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".output_location must be string", value=data__outputlocation, name="" + (name_prefix or "data") + ".output_location", definition={'description': 'Location to store solution data to', 'type': 'string'}, rule='type')
        if "id" in data_keys:
            data_keys.remove("id")
            data__id = data["id"]
            if not isinstance(data__id, (int)) and not (isinstance(data__id, float) and data__id.is_integer()) or isinstance(data__id, bool):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".id must be integer", value=data__id, name="" + (name_prefix or "data") + ".id", definition={'description': 'Unique identifier for this model run', 'type': 'integer'}, rule='type')
    return data