import re
import json
import sys
from urllib.request import urlopen
from urllib.error import HTTPError
import os

# Schema fields
REQUIRED_SCHEMA_FIELDS = ['$schema', 'description', 'name', '$async', 'type',
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
        self.required_fields_should_be_in_schema(schema, schema_filename,
                                                 schema_errors)
        self.schema_mast_be_set_to_proper_draft(schema, schema_filename,
                                                schema_errors)
        self.description_is_sentence(schema, schema_filename, schema_warnings)
        # TODO uncomment this method when everything is ready
        # self.schema_should_describe_itself(properties, schema_filename,
        #                                    schema_errors)
        self.name_should_be_equal_to_filename(schema, schema_filename,
                                              schema_errors)
        self.schema_type_must_be_object(schema, schema_filename, schema_errors)
        self.schema_must_have_required_properties(schema, properties,
                                                  schema_filename,
                                                  schema_errors)
        self.schema_title_should_be_sentence_case(schema, schema_filename,
                                                  schema_warnings)

        return schema_warnings, schema_errors

    @staticmethod
    def schema_has_only_allowed_fields(schema, schema_filename, errors):
        """Check that schema has only allowed fields"""
        for key in schema:
            if key not in ALLOWED_SCHEMA_FIELDS:
                errors.append(
                    f"Schema field '{key}' in '{schema_filename}' not in list "
                    f"of ALLOWED_SCHEMA_FIELDS.")

    @staticmethod
    def required_fields_should_be_in_schema(schema, schema_filename, errors):
        """Check that all required fields are present in schema"""
        for field in REQUIRED_SCHEMA_FIELDS:
            if field not in schema:
                errors.append(f"'{schema_filename}': Missing required schema "
                              f"field '{field}'.")

    @staticmethod
    def schema_mast_be_set_to_proper_draft(schema, schema_filename, errors):
        """Check that schema points to proper draft"""
        if schema['$schema'] != SCHEMA_URL:
            errors.append(f"'{schema_filename}': Must have $schema set to "
                          f"'{SCHEMA_URL}'.")

    @staticmethod
    def description_is_sentence(schema, schema_filename, warnings):
        """Check that description is a sentence - starts with capital letter
        and ends with full stop
        """
        if not re.match('^[A-Z][^?!]*[.]$', schema['description']):
            warnings.append(f"'{schema_filename}': The 'description' of the "
                            f"schema is not a sentence.")

    @staticmethod
    def schema_should_describe_itself(properties, schema_filename, errors):
        """
        Schema must describe itself
        """
        described_by = properties['describedBy']['const'].split('/')[-1]
        if described_by != schema_filename:
            errors.append(f"'{schema_filename}': describedBy URL "
                          f"({described_by}) must match schema filename "
                          f"({schema_filename}).")

    @staticmethod
    def name_should_be_equal_to_filename(schema, schema_filename, errors):
        """Schema filename must match schema name"""
        if schema['name'] != schema_filename:
            errors.append(f"'{schema_filename}': The 'name' attribute "
                          f"({schema['name']}) must match the schema filename "
                          f"({schema_filename}).")

    @staticmethod
    def schema_type_must_be_object(schema, schema_filename, errors):
        """Schema type must be set to object"""
        if schema['type'] != 'object':
            errors.append(f"'{schema_filename}': The 'type' attribute must be "
                          f"set to 'object'.")

    @staticmethod
    def schema_must_have_required_properties(schema, properties,
                                             schema_filename, errors):
        """All required properties should be present in properties field"""
        req_props = schema.get('required', [])
        for req_prop in req_props:
            if req_prop not in properties:
                errors.append(f"'{schema_filename}': Property '{req_prop}' is "
                              f"required but is missing under properties.")

    @staticmethod
    def schema_title_should_be_sentence_case(schema, schema_filename, warnings):
        """Schema titles should be sentence-case (begin with uppercase letter,
        no underscores)"""
        if 'title' in schema:
            if not schema['title'][0].isupper() or "_" in schema['title']:
                warnings.append(f"'{schema_filename}': title "
                                f"'{schema['title']}' doesn't start with "
                                f"uppercase char or contains an underscore.")

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
