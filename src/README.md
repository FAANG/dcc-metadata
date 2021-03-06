# FAANG Metadata Standards: Scripts

This directory contains useful scripts related to exploring the FAANG metadata schemas.

### schemas_are_valid_json.py

This script tests whether each JSON schema in `json_schema/` directory is a valid JSON schema. This script is automatically run as part of Travis CI testing.

Please note that until jsonschema v3 goes into proper release, you will need to run `pip install jsonschema==3.0.0a5` for this script to work


### schema_linter.py

This script inspects every schema in the metadata repo and checks all schemas and properties to ensure that they conform to a set of rules defined in the [schema style guide](https://github.com/HumanCellAtlas/metadata-schema/blob/master/docs/schema_style_guide.md). Check failures are reported as either warnings or errors, depending on the severity of the mistake.

This script can be run as a standalone (and it should be considered good practice to do so!) but it is also integrated into the automatic Travis build.
