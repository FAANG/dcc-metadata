import re
import json
import sys
from urllib.request import urlopen
from urllib.error import HTTPError
import os

# Schema fields
required_schema_fields = ['$schema', 'description', 'name', 'type',
                          'properties']
ALLOWED_SCHEMA_FIELDS = ['$schema', 'description', 'title', 'name', '$async',
                         'type', 'required', 'properties']

# Properties
required_properties = ['describedBy', 'schema_version']
required_ontology_properties = ['text', 'ontology', 'ontology_label']
system_supplied_properties = ['describedBy', 'schema_version', 'schema_type',
                              'provenance']

# The following properties are exempt from needing examples
# because an example might bias what value a contributor supplies
example_exempt_properties = ['biomaterial_id', 'biomaterial_name',
                             'biomaterial_description', 'process_id',
                             'process_name', 'process_description',
                             'protocol_id', 'protocol_name',
                             'protocol_description', 'project_description',
                             'parent', 'sibling', 'child']

# Property attributes

property_attributes = ['description', 'type', 'pattern', 'example', 'enum',
                       '$ref', 'user_friendly', 'items', 'guidelines',
                       'format', 'comment', 'maximum', 'minimum', 'oneOf',
                       'mandatory', 'value', 'text', 'term', 'name',
                       'properties', 'units']
ontology_attributes = ['graph_restriction', 'ontologies', 'classes',
                       'relations', 'direct', 'include_self']
graph_restriction_attributes = ['ontologies', 'classes', 'relations', 'direct',
                                'include_self']

OLS_API_DEFAULT = 'https://ontology.dev.data.humancellatlas.org/api'

SCHEMA_URL = "http://json-schema.org/draft-07/schema#"


class SchemaLinter:
    def __init__(self, schemas):
        self.schemas = schemas
        self.warnings = list()
        self.errors = list()

    def lint_schemas(self):
        # Going through schemas and adding errors and warnings
        for s in self.schemas:
            if 'versions.json' not in s:
                return_msg = self.lint_schema(s)
                self.warnings.extend(return_msg[0])
                self.errors.extend(return_msg[1])
        return self.warnings, self.errors

    def lint_schema(self, path):
        # Lint particular schema
        schema_warnings = list()
        schema_errors = list()

        # Read file and get properties
        schema = self.get_json_from_file(path)
        properties = schema['properties']

        # Get filename (without json), example faang_samples_core.metadata_rules
        schema_filename = ".".join(path.split("/")[-1].split(".")[0:2])

        # Schema level checks
        self.schema_has_only_allowed_fields(schema, schema_filename,
                                            schema_errors)

        return schema_warnings, schema_errors

    @staticmethod
    def schema_has_only_allowed_fields(schema, schema_filename, errors):
        for key in schema:
            if key not in ALLOWED_SCHEMA_FIELDS:
                errors.append(
                    f"Schema field '{key}' in '{schema_filename}' not in list "
                    f"of ALLOWED_SCHEMA_FIELDS.")

    @staticmethod
    def get_json_from_file(filename):
        """Loads json from a file."""
        f = open(filename, 'r')
        return json.loads(f.read())


if __name__ == "__main__":
    # Get current working directory
    cwd = os.getcwd().split("/")[-1]

    # Get all filenames with path
    schema_path = '../json_schema' if cwd == 'src' else 'json_schema'
    jsons = [
        os.path.join(path, f) for path, _, files in
        os.walk(schema_path) for f in files if f.endswith('.json')]

    # Exclude top-level JSON files like versions.json and
    # property_migrations.json by including JSON file only if the path contains
    # "core", "module", "system", or "type"
    my_schemas = [
        j for j in jsons if any(substring in j for substring in
                                ("core", "module", "type"))]

    print(f"Linting {len(my_schemas)} schemas")
    linter = SchemaLinter(my_schemas)
    warnings, errors = linter.lint_schemas()

    # Print error and warning messages. If any error is found,
    # exit after printing.
    if errors:
        print("The following errors were found:")
        for error_msg in errors:
            print(error_msg)
        sys.exit("Please correct the errors before your code is reviewed.")

    if warnings:
        print("Linter finished with the following warnings:")
        for warning_msg in warnings:
            print(warning_msg)
    else:
        print("Linter finished with no errors and no warnings.")
