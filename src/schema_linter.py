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
REQUIRED_PROPERTIES = ['describedBy', 'schema_version']

VALID_TYPES = ['string', 'number', 'boolean', 'array', 'object', 'integer']
VALID_JSON_FORMATS = ['date', 'date-time', 'email', 'uri']

GRAPH_RESTRICTION_ATTRIBUTES = ['ontologies', 'classes', 'relations',
                                'direct', 'include_self']

OLS_API_DEFAULT = 'https://ontology.dev.data.humancellatlas.org/api'

SCHEMA_URL = "http://json-schema.org/draft-07/schema#"


class SchemaLinter:
    def __init__(self, schemas, schema_path, jsons):
        self.schemas = schemas
        self.schema_path = schema_path
        self.jsons = jsons
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

        # Property level checks
        self.properties_must_have_required_properties(properties,
                                                      schema_filename,
                                                      schema_errors)

        # Per property checks
        for my_property in properties:
            self.property_name_should_be_valid(my_property, schema_filename,
                                               schema_warnings)
            self.property_must_have_description(my_property, properties,
                                                schema_filename, schema_errors)
            self.property_must_have_type(my_property, properties,
                                         schema_filename, schema_errors)
            self.format_must_be_valid_json(my_property, properties,
                                           schema_filename, schema_errors)
            self.property_description_should_be_sentence(my_property,
                                                         properties,
                                                         schema_filename,
                                                         schema_warnings)
            self.pattern_must_be_valid_regex(my_property, properties,
                                             schema_filename, schema_errors)
            self.ref_schemas_must_exist(my_property, properties,
                                        schema_filename, schema_errors)
            # Ontology checks
            self.check_graph_restriction(my_property, properties,
                                         schema_filename, schema_errors)

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
    def properties_must_have_required_properties(properties, schema_filename,
                                                 errors):
        """properties should have REQUIRED_PROPERTIES"""
        for my_property in REQUIRED_PROPERTIES:
            if my_property not in properties:
                errors.append(f"'{schema_filename}': Missing required property "
                              f"'{my_property}'.")

    @staticmethod
    def property_name_should_be_valid(my_property, schema_filename, warnings):
        """Property name should contain only lowercase letters, numbers, and
        underscores"""
        if not re.match("^[a-z0-9_-]+$", my_property) and my_property not in \
                ['describedBy']:
            warnings.append(f"'{schema_filename}': Property '{my_property}' "
                            f"contains non-lowercase/underscore characters.")

    @staticmethod
    def property_must_have_description(my_property, properties,
                                       schema_filename, errors):
        """Property must contain description attribute"""
        if 'description' not in properties[my_property] and my_property not in \
                ['describedBy']:
            errors.append(f"'{schema_filename}': Keyword 'description' missing "
                          f"from property '{my_property}'")

    @staticmethod
    def property_must_have_type(my_property, properties, schema_filename,
                                errors):
        """Property must contain type attribute"""
        if 'type' not in properties[my_property] and my_property not in \
                ['describedBy']:
            errors.append(f"'{schema_filename}': Keyword 'type' missing from "
                          f"property '{my_property}'.")
        elif 'type' in properties[my_property] and my_property not in \
                ['describedBy']:
            # type attribute must be set to one of the valid JSON types
            if properties[my_property]['type'] not in VALID_TYPES:
                errors.append(f"'{schema_filename}': Type "
                              f"'{properties[my_property]['type']}' is not a "
                              f"valid JSON type.")

            # Property of type array must contain the attribute items
            if properties[my_property]['type'] == "array" and 'items' not in \
                    properties[my_property]:
                errors.append(f"'{schema_filename}': Property '{my_property}' "
                              f"is type array but doesn't contain items.")

            # Property of type array must contains the attribute items
            # items must have either type or $ref attribute
            if properties[my_property]['type'] == "array" and 'items' in \
                    properties[my_property] and '$ref' not in \
                    properties[my_property]['items'] and 'type' not in \
                    properties[my_property]['items']:
                errors.append(f"'{schema_filename}': Property '{my_property}' "
                              f"is type array but items attribute doesn't "
                              f"contain type of $ref attribute")

    @staticmethod
    def format_must_be_valid_json(my_property, properties, schema_filename,
                                  errors):
        """format in properties must be a valid JSON format"""
        my_object = properties[my_property]
        if 'type' in my_object and my_object['type'] == 'object' and \
                'properties' in my_object:
            my_properties = my_object['properties']
            for _, v in my_properties.items():
                if 'format' in v and v['format'] not in VALID_JSON_FORMATS:
                    errors.append(
                        f"'{schema_filename}': Format '{v['format']}' is not "
                        f"a valid JSON format.")


    @staticmethod
    def property_description_should_be_sentence(my_property, properties,
                                                schema_filename, warnings):
        """description should be a sentence - start with capital letter and end
        with full stop"""
        if 'description' in properties[my_property]:
            my_description = properties[my_property]['description']
            if not re.match('^[A-Z][^?!]*[.]$', my_description):
                warnings.append(f"'{schema_filename}': The 'description' for "
                                f"property '{my_property}' is not a sentence")

    @staticmethod
    def pattern_must_be_valid_regex(my_property, properties, schema_filename,
                                    errors):
        """pattern must be a valid regex"""
        if 'pattern' in properties[my_property]:
            my_pattern = properties[my_property]['pattern']
            try:
                re.compile(my_pattern)
                is_valid_regex = True
            except re.error:
                is_valid_regex = False
            if not is_valid_regex:
                errors.append(f"'{schema_filename}': The 'pattern' for "
                              f"property '{my_property}' is not a valid regex "
                              f"pattern")

    def ref_schemas_must_exist(self, my_property, properties, schema_filename,
                               errors):
        """All $ref referenced schemas must exist"""
        if '$ref' in properties[my_property]:
            my_ref = properties[my_property]['$ref']
            if f"{self.schema_path}/{my_ref}" not in self.jsons:
                errors.append(f"'{schema_filename}': $ref schema ({my_ref}) "
                              f"in property {my_property} doesn't exist.")

    def check_graph_restriction(self, my_property, properties, schema_filename,
                                errors):
        """graph_restriction checks"""
        my_object = properties[my_property]
        if 'type' in my_object and my_object['type'] == 'object' and \
                'properties' in my_object and \
                'term' in my_object['properties'] and \
                'graph_restriction' in my_object['properties']['term']:
            my_graph_restriction = my_object['properties']['term'][
                'graph_restriction']
            self.graph_restriction_must_have_required_attributes(
                my_graph_restriction, schema_filename, errors)
            self.graph_restriction_must_have_only_allowed_attributes(
                my_graph_restriction, schema_filename, errors)
            self.graph_restriction_direct_must_be_false(my_graph_restriction,
                                                        schema_filename, errors)
            self.graph_restriction_include_self_must_be_bool(
                my_graph_restriction, schema_filename, errors)
            self.graph_restriction_relations_must_be_list(my_graph_restriction,
                                                          schema_filename,
                                                          errors)
            self.graph_restriction_classes_must_be_list(my_graph_restriction,
                                                        schema_filename, errors)
            self.graph_restriction_ontologies_must_be_list(my_graph_restriction,
                                                           schema_filename,
                                                           errors)
            self.graph_restriction_relations_must_have_subclassof(
                my_graph_restriction, schema_filename, errors)

    @staticmethod
    def graph_restriction_must_have_required_attributes(graph_restriction,
                                                        schema_filename,
                                                        errors):
        """graph_restriction property must contain all required attributes"""
        for gra in GRAPH_RESTRICTION_ATTRIBUTES:
            if gra not in graph_restriction:
                errors.append(f"'{schema_filename}': 'graph_restriction' "
                              f"missing a required attribute: '{gra}'.")

    @staticmethod
    def graph_restriction_must_have_only_allowed_attributes(graph_restriction,
                                                            schema_filename,
                                                            errors):
        """graph_restriction property must contain only allowed attributes"""
        for ga in graph_restriction:
            if ga not in GRAPH_RESTRICTION_ATTRIBUTES:
                errors.append(f"'{schema_filename}': Keyword '{ga}' is not "
                              f"acceptable graph_restriction keyword property.")

    @staticmethod
    def graph_restriction_direct_must_be_false(graph_restriction,
                                               schema_filename, errors):
        """graph_restriction 'direct' attribute must be 'false'"""
        if graph_restriction['direct'] is not False:
            errors.append(f"'{schema_filename}': Keyword 'direct' must be set "
                          f"to false, not '{graph_restriction['direct']}'.")

    @staticmethod
    def graph_restriction_include_self_must_be_bool(graph_restriction,
                                                    schema_filename, errors):
        """graph_restriction 'include_self' attribute must be 'false' or
        'true'"""
        if not isinstance(graph_restriction['include_self'], bool):
            errors.append(f"'{schema_filename}': Keyword 'include_self' "
                          f"must be set to 'false' or 'true' not "
                          f"'{graph_restriction['include_self']}'")

    @staticmethod
    def graph_restriction_relations_must_be_list(graph_restriction,
                                                 schema_filename, errors):
        """graph_restriction 'relations' attribute must be a list"""
        if not isinstance(graph_restriction['relations'], list):
            errors.append(f"'{schema_filename}': Keyword 'realtions' must be a "
                          f"list")

    @staticmethod
    def graph_restriction_classes_must_be_list(graph_restriction,
                                               schema_filename, errors):
        """graph_restriction 'classes' attribute must be a list"""
        if not isinstance(graph_restriction['classes'], list):
            errors.append(f"'{schema_filename}': Keyword 'classes' must be a "
                          f"list")

    @staticmethod
    def graph_restriction_ontologies_must_be_list(graph_restriction,
                                                  schema_filename, errors):
        """graph_restriction 'ontologies' attribute must be a list"""
        if not isinstance(graph_restriction['ontologies'], list):
            errors.append(f"'{schema_filename}': Keyword 'ontologies' must be "
                          f"a list")

    @staticmethod
    def graph_restriction_relations_must_have_subclassof(graph_restriction,
                                                         schema_filename,
                                                         errors):
        """graph_restriction 'relations' must at least contain item
        rdfs:subClassOf"""
        if 'rdfs:subClassOf' not in graph_restriction['relations']:
            errors.append(f"'{schema_filename}': Keyword 'relations' must "
                          f"contain item 'rdfs:subClassOf'.")


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
    linter = SchemaLinter(my_schemas, schema_path, jsons)
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
