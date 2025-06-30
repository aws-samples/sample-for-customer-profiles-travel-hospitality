import json
import traceback
######################################################################
# load the mapping defintions from the mapping file
# the file is contained in the mappings/ directory
######################################################################

def getObjectDef(objectTypeName):
    try:
        # Open the JSON file in read mode
        print(f"going to load file for {objectTypeName}")
        with open(f"mappings/{objectTypeName}.json", 'r') as file:
            data_dictionary = json.load(file)
            print("JSON data loaded successfully into a dictionary:")
            return data_dictionary

    except FileNotFoundError as f:
        print(f"Error: The file '{f}' was not found.")
        traceback.print_exc()
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{objectTypeName}'. Check if the file contains valid JSON.")
        traceback.print_exc()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()


def createObjectTypeMapping(client, domainName, ObjectTypeName):
    try:
        json_data = getObjectDef(ObjectTypeName)
        client.put_profile_object_type(
            DomainName = domainName,
            ObjectTypeName = json_data['ObjectTypeName'],
            Description = json_data['Description'],
            AllowProfileCreation = json_data['AllowProfileCreation'],
            SourceLastUpdatedTimestampFormat = json_data['SourceLastUpdatedTimestampFormat'],
            Fields = json_data['Fields'],
            Keys = json_data['Keys']
        )
        print(f"Created Object Type Mapping {ObjectTypeName} successfully")
    except Exception as e:
        print(f"Error while creating {ObjectTypeName} Object type mapping {e}")
        traceback.print_exc()