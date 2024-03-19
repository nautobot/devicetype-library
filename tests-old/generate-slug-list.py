import decimal
import glob
import json
import os
from urllib.request import urlopen

from jsonschema import Draft4Validator, RefResolver
from jsonschema.exceptions import ValidationError
import pickle_operations
from test_configuration import KNOWN_MODULES, KNOWN_SLUGS, ROOT_DIR, SCHEMAS
import yaml
from yaml_loader import DecimalSafeLoader


def _get_type_files(device_or_module):
    """
    Return a list of all definition files within the specified path.
    """
    file_list = []

    for path, schema in SCHEMAS:
        if path == f"{device_or_module}-types":
            # Initialize the schema
            with open(f"{ROOT_DIR}/schema/{schema}") as schema_file:
                schema = json.loads(schema_file.read(), parse_float=decimal.Decimal)

            # Validate that the schema exists
            if not schema:
                print(f"Schema definition for {path} is empty!")
                exit(1)

            # Map each definition file to its schema as a tuple (file, schema)
            for file in sorted(glob.glob(f"{path}/*/*", recursive=True)):
                file_list.append((f"{file}", schema))

    return file_list


def _decimal_file_handler(uri):
    """
    Handler to work with floating decimals that fail normal validation.
    """
    with urlopen(uri) as url:
        result = json.loads(url.read().decode("utf-8"), parse_float=decimal.Decimal)
    return result


def load_file(file_path, schema):
    # Read file
    try:
        with open(file_path) as definition_file:
            content = definition_file.read()
    except Exception as exc:
        return (False, f'Error opening "{file_path}". stderr: {exc}')

    # Check for trailing newline. YAML files must end with an emtpy newline.
    if not content.endswith("\n"):
        return (False, f"{file_path} is missing trailing newline")

    # Load YAML data from file
    try:
        definition = yaml.load(content, Loader=DecimalSafeLoader)
    except Exception as exc:
        return (False, f'Error during yaml.load "{file_path}". stderr: {exc}')

    # Validate YAML definition against the supplied schema
    try:
        resolver = RefResolver(
            f"file://{os.getcwd()}/schema/devicetype.json",
            schema,
            handlers={"file": _decimal_file_handler},
        )
        # Validate definition against schema
        Draft4Validator(schema, resolver=resolver).validate(definition)
    except ValidationError as exc:
        # Schema validation failure. Ensure you are following the proper format.
        return (False, f"{file_path} failed validation: {exc}")

    return (True, definition)


def _generate_knowns(device_or_module):
    all_files = _get_type_files(device_or_module)

    for file_path, schema in all_files:
        definition_status, definition = load_file(file_path, schema)
        if not definition_status:
            print(definition)
            exit(1)

        if device_or_module == "device":
            KNOWN_SLUGS.add((definition.get("slug"), file_path))
        else:
            KNOWN_MODULES.add(
                (
                    os.path.splitext(os.path.basename(file_path))[0],
                    os.path.dirname(file_path),
                )
            )


_generate_knowns("device")
pickle_operations.write_pickle_data(KNOWN_SLUGS, f"{ROOT_DIR}/tests/known-slugs.pickle")

_generate_knowns("module")
pickle_operations.write_pickle_data(KNOWN_MODULES, f"{ROOT_DIR}/tests/known-modules.pickle")
