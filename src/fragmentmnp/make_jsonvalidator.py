import fastjsonschema
import json

with open("config.schema.json", "r") as schemafile:
    schema = json.load(schemafile)

code = fastjsonschema.compile_to_code(schema)

with open("jsonvalidator.py", "w") as validatorfile:
    validatorfile.write(code)
