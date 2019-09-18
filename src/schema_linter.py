# from schema_test_suite import get_json_from_file
import logging
import re
import json
import sys
from urllib.request import urlopen
from urllib.error import HTTPError
import os

# Current working directory

cwd = os.getcwd().split("/")[-1]

# Schema fields

required_schema_fields = ['$schema', 'description', 'name', 'type',
                          'properties']

allowed_schema_fields = ['$schema', 'description', 'additionalProperties',
                         'required', 'title', 'name', 'type', 'properties',
                         'definitions', '$async']

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
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def lint_schema(self, path):
        schema = self.get_json_from_file(path)
        properties = schema['properties']
        schema_filename = path.split("/")[-1].split(".")[0]
        errors = []
        warnings = []

        # SCHEMA-LEVEL CHECKS

        # All schema fields must be part of the list of allowed schema fields
        for key in schema.keys():
            if key not in allowed_schema_fields:
                errors.append(
                    "Schema field `" + key + "` in " + schema_filename +
                    ".json" + " not an allowed schema field.")

        # All required schema fields must be present in the schema
        for prop in required_schema_fields:
            if prop not in schema.keys():
                errors.append(
                    f"{schema_filename}.json: Missing required schema field "
                    f"{prop}.")

        # $schema must be set to draft-07
        if "$schema" in schema and schema['$schema'] != SCHEMA_URL:
            errors.append(
                f"{schema_filename}.json: Must have $schema set to {SCHEMA_URL}"
            )

        # description should be a sentence - start with capital letter and end
        # with full stop
        if 'description' in schema and not re.match('^[A-Z][^?!]*[.]$',
                                                    schema['description']):
            warnings.append(
                f"{schema_filename}.json: The 'description' of the schema is "
                f"not a sentence ({schema['description']}).")

        # Schema filename must match name of the schema in the describedBy URL
        if "describedBy" in schema:
            described_by = properties['describedBy']['pattern'].split("/")[-1]
            if described_by != schema_filename:
                errors.append(f"{schema_filename}.json: End of 'describedBy' "
                              f"URL ({described_by}) must match schema "
                              f"filename ({schema_filename}).")

        # Schema filename must match schema name field
        if "name" in schema and schema['name'] != schema_filename:
            errors.append(f"{schema_filename}.json: The 'name attribute "
                          f"({schema['name']}) must match the schema "
                          f"filename ({schema_filename})")

        # Schema type must be set to object
        if "type" in schema and schema['type'] != "object":
            errors.append(f"{schema_filename}.json: The 'type' attribute must "
                          f"be set to 'object'.")

        # All required fields must actually be in the schema
        if "required" in schema:
            for req_prop in schema["required"]:
                if req_prop not in properties:
                    errors.append(
                        f"Property '{req_prop}' is required in "
                        f"{schema_filename}.json but is missing under "
                        f"properties.")

        # Schema titles should be sentence-case (begin with uppercase letter,
        # no underscores)
        if "title" in schema:
            if (not schema['title'][0].isupper()) or ("_" in schema['title']):
                warnings.append(
                    f"{schema_filename}.json: title '{schema['title']}' "
                    f"doesn't start with an uppercase char or contains an "
                    f"underscore."
                )

        # PROPERTY-LEVEL CHECKS

        # Properties 'describedBy' and 'schema_version' must be present in
        # each schema
        for ep in required_properties:
            if ep not in properties:
                errors.append(f"{schema_filename}.json: Missing required "
                              f"property '{ep}'.")

        # Properties 'tex'`, 'ontology' and 'ontology_label' must be present
        # in each ontology schema
        if "ontology" in schema_filename:
            for p in required_ontology_properties:
                if p not in properties:
                    errors.append(f"{schema_filename}.json: Missing required "
                                  f"property '{p}'.")

        # All type schemas must have corresponding _core property

        # PER-PROPERTY CHECKS

        for property in properties:
            # Property name must contain only lowercase letters, numbers, and
            # underscores
            # TODO: Should be sys.exit() but currently HDBR_accession field
            #  fails this
            # TODO: Fix HDBR_accession field prior to implementing sys.exit()
            if not re.match("^[a-z0-9_-]+$", property) and property != \
                    'describedBy':
                warnings.append(f"{schema_filename}.json: Property "
                                f"'{property}' contains non-lowercase/"
                                f"underscore characters.")

            # Property must contain description attribute
            if 'description' not in properties[property].keys():
                errors.append(f"{schema_filename}.json: Keyword 'description' "
                              f"missing from property '{property}'.")

            # Property must contain type attribute
            if 'type' not in properties[property].keys():
                errors.append(f"{schema_filename}.json: Keyword `type` missing "
                              f"from property '{property}'.")

            else:
                # type attribute must be set to one of the valid JSON types
                if properties[property]['type'] not in ["string", "number",
                                                        "boolean", "array",
                                                        "object", "integer"]:
                    errors.append(f"{schema_filename}.json: Type "
                                  f"'{properties[property]['type']}' is not a "
                                  f"valid JSON type.")

                # Property of type array must contain the attribute items
                if properties[property]['type'] == "array" and 'items' not in \
                        properties[property].keys():
                    errors.append(f"{schema_filename}.json: Property "
                                  f"'{property}' is type array but doesn't "
                                  f"contain items.")

                # Property of type array must contains the attribute items
                # items must have either type or $ref attribute
                if properties[property]['type'] == "array" and \
                        'items' in properties[property].keys() and \
                        'type' not in properties[property]['items'].keys():
                    errors.append(f"{schema_filename}.json: Property "
                                  f"'{property}' is type array but items "
                                  f"attribute doesn't contain type or $ref "
                                  f"attribute.")

            # description should be a sentence - start with capital letter and
            # end with full stop
            if 'description' in properties[property].keys() and \
                    not re.match('^[A-Z][^?!]*[.]$',
                                 properties[property]['description']):
                warnings.append(f"{schema_filename}.json: The 'description' "
                                f"for property '{property}' is not a sentence "
                                f"({properties[property]['description']}).")

            # guidelines should be a sentence
            if 'guidelines' in properties[property].keys() and \
                    not re.match('^[A-Z][^?!]*[.]$',
                                 properties[property]['guidelines']):
                warnings.append(f"{schema_filename}.json: The 'guidelines' "
                                f"for property {property} is not a sentence "
                                f"({properties[property]['guidelines']}).")

            # pattern must be a valid regex
            if 'pattern' in properties[property].keys():
                try:
                    re.compile(properties[property]['pattern'])
                    is_valid_regex = True
                except re.error:
                    is_valid_regex = False
                if not is_valid_regex:
                    errors.append(f"{schema_filename}.json: The 'pattern' for "
                                  f"property '{property}' "
                                  f"({properties[property]['pattern']}) is not "
                                  f"a valid regex pattern.")

            # example values must match regex pattern
            if 'pattern' in properties[property].keys() and 'example' in \
                    properties[property].keys():
                examples = properties[property]['example'].split(";")
                for ex in examples:
                    if not re.match(properties[property]['pattern'],
                                    ex.strip()):
                        errors.append(f"{schema_filename}.json: Example "
                                      f"{ex.strip()} for property '{property}' "
                                      f"(properties[property]['pattern']) "
                                      f"does not match regex pattern "
                                      f"{properties[property]['pattern']}.")

            # _unit properties should have matching property w/o _unit
            if re.match("^[a-z_]+_unit$", property):
                if property.split("_unit")[0] not in properties:
                    warnings.append(f"{schema_filename}.json: Has unit "
                                    f"property '{property}' but no "
                                    f"corresponding "
                                    f"'{property.split('_unit')[0]}' property")

            # ADDITIONAL PROPERTY CHECKS & SPECIFIC ONTOLOGY CHECKS

            for kw in properties[property].keys():
                # Ontology field must have graph_restriction property that is
                # an object
                if property == 'ontology' and 'graph_restriction' not in \
                        properties[property].keys():
                    errors.append(f"{schema_filename}.json: Keyword "
                                  f"'graph_restriction' missing from property "
                                  f"'{property}'.")

                if property == 'ontology' and kw == 'graph_restriction':
                    nested_keywords = properties[property][kw]

                    # graph_restriction property must contain all required
                    # attributes
                    for gra in graph_restriction_attributes:
                        if gra not in nested_keywords:
                            errors.append(f"{schema_filename}.json: "
                                          f"'graph_restriction' missing a "
                                          f"required attribute '{gra}'.")

                    for nkw in nested_keywords.keys():

                        # Attributes for graph_restriction must be one of
                        # acceptable values
                        if nkw not in ontology_attributes:
                            errors.append(f"{schema_filename}.json: Keyword "
                                          f"'{nkw}' is not an acceptable "
                                          f"graph_restriction keyword"
                                          f"property.")

                    # graph_restriction 'direct' attribute must be 'false'
                    direct_attribute = \
                        properties['ontology']['graph_restriction']['direct']
                    if direct_attribute is not False:
                        errors.append(f"{schema_filename}.json: Keyword "
                                      f"'direct' must be set to 'false', "
                                      f"not {direct_attribute}.")

                    # graph_restriction 'include_self' attribute must be
                    # 'false' or 'true'
                    include_self_attribute = properties['ontology'][
                        'graph_restriction']['include_self']
                    if not isinstance(include_self_attribute, bool):
                        errors.append(f"{schema_filename}.json: Keyword "
                                      f"'include_self' must be set to 'false' "
                                      f"or 'true', "
                                      f"not {str(include_self_attribute)}.")

                    # graph_restriction 'relations' attribute must be a list
                    if not isinstance(properties['ontology'][
                                          'graph_restriction'][
                                          'relations'], list):
                        errors.append(f"{schema_filename}.json: Keyword "
                                      f"'relations' must be a list.")

                    # graph_restriction 'classes' attribute must be a list
                    if not isinstance(properties['ontology'][
                                          'graph_restriction'][
                                          'classes'], list):
                        errors.append(f"{schema_filename}.json: Keyword "
                                      f"'classes' must be a list.")

                    # graph_restriction 'ontologies' attribute must be a list
                    if not isinstance(properties['ontology'][
                                          'graph_restriction']['ontologies'],
                                      list):
                        errors.append(f"{schema_filename}.json: Keyword "
                                      f"'ontologies' must be a list.")

                    # graph_restriction 'relations' must at least contain item \
                    # "rdfs:subClassOf"
                    if 'rdfs:subClassOf' not in properties['ontology'][
                        'graph_restriction']['relations']:
                        errors.append(f"{schema_filename}.json: Keyword "
                                      f"'relations' must contain item "
                                      f"'rdfs:subClassOf'")

                    # graph_restriction 'ontologies' must contain ontologies
                    # that are valid within the HCA ontology space
                    # TODO: consider removing ontologies that are not within
                    #  the HCA namespace and making this an error
                    checked_ontologies = {}
                    for ontology in properties['ontology'][
                        'graph_restriction']['ontologies']:
                        if ontology not in checked_ontologies:
                            ols_ontologies_url = OLS_API_DEFAULT + \
                                                 '/ontologies/' + \
                                                 ontology.replace('obo:', '')

                            try:
                                urlopen(ols_ontologies_url)
                                checked_ontologies[ontology] = "pass"
                            except HTTPError as e:
                                warnings.append(f"{schema_filename}.json: "
                                                f"Ontology {ontology} is not a "
                                                f"valid ontology in the HCA "
                                                f"ontology space")
                                checked_ontologies[ontology] = "fail"
                        else:
                            if checked_ontologies[ontology] == "fail":
                                warnings.append(f"{schema_filename}.json: "
                                                f"Ontology {ontology} is not a "
                                                f"valid ontology in the HCA "
                                                f"ontology space")

                    #  graph_restrictions 'classes' must contain only ontology
                    #  classes that are valid in the HCA ontology space
                    for parent_class in properties['ontology'][
                        'graph_restriction']['classes']:
                        ols_search_url = OLS_API_DEFAULT + '/search?q=' + \
                                         parent_class.replace('obo:', '') + \
                                         "&exact=true&groupField=true&query" \
                                         "Fields=obo_id"

                        json_url = urlopen(ols_search_url)
                        result = json.loads(json_url.read())

                        if "response" in result and "numFound" in \
                                result["response"] and \
                                result["response"]["numFound"] == 0:
                            errors.append(f"{schema_filename}.json: Class "
                                          f"{parent_class} is not a valid "
                                          f"ontology term in the HCA ontology "
                                          f"space")

                # All property attributes must be in the allowed list of
                # property attributes
                elif kw not in property_attributes:
                    errors.append(f"{schema_filename}.json: Keyword '{kw}' "
                                  f"in property '{property}' is not an "
                                  f"allowed property.")

                if isinstance(properties[property][kw], dict) and \
                        property != 'ontology':
                    for nkw in properties[property][kw].keys():
                        if nkw not in property_attributes:
                            errors.append(f"{schema_filename}.json: Keyword "
                                          f"'{nkw}' in property '{property}' "
                                          f"is not an allowed property.")

        return warnings, errors

    @staticmethod
    def get_json_from_file(filename):
        """Loads json from a file.
        Optionally specify warn = True to warn, rather than
        fail if file not found."""
        f = open(filename, 'r')
        return json.loads(f.read())


if __name__ == "__main__":

    schema_path = '../json_schema' if cwd == 'src' else 'json_schema'
    jsons = [
        os.path.join(dirpath, f) for dirpath, dirnames, files in
        os.walk(schema_path) for f in files if f.endswith('.json')]

    linter = SchemaLinter()

    # Exclude top-level JSON files like versions.json and
    # property_migrations.json by including JSON file only if the path contains
    # "core", "module", "system", or "type"
    schemas = [j for j in jsons if any(substring in j for substring in (
        "core", "module", "system", "type"))]

    print("Linting %d schemas" % len(schemas))

    warnings = []
    errors = []
    for s in schemas:
        if 'versions.json' not in s:
            return_msg = linter.lint_schema(s)
            warnings.extend(return_msg[0])
            errors.extend(return_msg[1])

    # Print error and warning messages. If any error is found,
    # exit after printing.
    if errors:
        print("\nThe following errors were found:")
        for error_msg in errors:
            print(error_msg)
        sys.exit("\nPlease correct the errors before your code is reviewed.")

    if warnings:
        print("\nLinter finished with the following warnings:")
        for warning_msg in warnings:
            print(warning_msg)
    else:
        print("\nLinter finished with no errors and no warnings.")
