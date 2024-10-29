import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preprocessing.policy_feature_func import create_policy_features
import pandas as pd
from agents.embed import embed
from agents.completion import complete, extract_info_from_policy
import ast
from json import load, loads



def pre_process_df(df: pd.DataFrame) -> pd.DataFrame:
    "Returns a list of each df row as a dictionary"
    list_of_data_dict = [df.iloc[index].to_dict() for index in range(df.shape[0])]
    return list_of_data_dict


def true_false_for_column_group(data: dict, columns: list[str]) -> str:
    "Helper function to process one-hot-encoding"
    text = ''
    for column in columns:
        if data[column] == 1:
            text += column + ', '
        else:
            continue
    return text



def flatten_dict(dd, separator ='_', prefix =''):
    return { prefix + separator + k if prefix else k : v
            for kk, vv in dd.items()
            for k, v in flatten_dict(vv, separator, kk).items()
            } if isinstance(dd, dict) else { prefix : dd }


def documents_to_dict(data: list[dict]) -> list[dict]:
    "Formats the dict for better semantic search"
    new_dict_list = []
    for element in data:
        new_dict = {
            'auto_make' : element["Make"],
            'auto_model' : element["Model"],
            'auto_year' : element["auto_year"],
            'age' : element["age"],
            'sex' : element["insured_sex"],
            'education_level' : element["insured_education_level"],
            'relationship' : element["insured_relationship"],
            'previous_accidents' : {
                'injuries' : true_false_for_column_group(element, ['No Injuries Reported', 'Minor', 'Moderate', 'Serious', 'Fatality']),
                'crash_speed' : element["SV Precrash Speed (MPH)"],
                'conditions' : true_false_for_column_group(element, ['high light', 'low light', 'medium light', 'weather_is_clear', 'weather_is_snow', 'weather_is_cloudy', 'weather_is_fog', 'weather_is_rain', 'weather_is_severe_wind', ]),
            }
        }
        new_dict_list.append(new_dict)
    return new_dict_list


def embed_pipeline(document: dict) -> dict:
    """Embeds the documents in the dict and returns the same dict with the embeddings in it."""
    string_document = str(document)
    vector_embedding = embed(string_document)
    dictionary = ast.literal_eval(string_document)
    dictionary["embedding"] = vector_embedding
    # new_list_of_dicts.append(dictionary)

    return dictionary


def load_vector_database():
    av_data_path = 'CD80_dataset/CD80_dataset/Human-Driving and AV Crash Data/Self-Driving Crash Datasets/SGO-2021-01_Incident_Reports_ADAS.csv'
    user_data_path = 'CD80_dataset/CD80_dataset/Insurance Claims Data/insurance_claims.csv'
    print("##### Loading df\n")
    df = create_policy_features(av_path=av_data_path, user_path=user_data_path, number_of_rows=50)
    list_of_data_dict = pre_process_df(df)
    preprocessed_dicts = documents_to_dict(list_of_data_dict)
    return_list = []

    document_index = 1
    # for document in preprocessed_dicts:
        # try:
    print(f"##### Starting to edit document {document_index}/{len(preprocessed_dicts)}")
    print("###### Creating policy")
    sample_policy = complete(str(preprocessed_dicts[0]), json_formatting=False) # Writes the Policy Contract
    sample_policy_content = sample_policy.content

    print("###### Extracting policy info")
    metadata_json = extract_info_from_policy(str(sample_policy_content)) # Extracts the json from the policy contract
    metadata_json_content = str(metadata_json.content).strip("```json").strip("```") 
    metadata_json_to_dict = loads(metadata_json_content) # Turns str back to dict
    preprocessed_dicts[0].update(metadata_json_to_dict) # Adds metadata_json_to_dict to the current dict

    print(f"##### Starting embedding for document {document_index}")
    dict_with_embeddings = embed_pipeline(preprocessed_dicts[0]) # Embeds the individual dict
    # preprocessed_dicts[0].update(dict_with_embeddings) 
    flattened_dict = flatten_dict(dict_with_embeddings)
    return_list.append(flattened_dict)
    print(f"###### Document {document_index}\n")
    document_index += 1
        # except:
            # continue
    return return_list



if __name__ == '__main__':
    x = load_vector_database()
    for n in x:
        with open("knsk.txt", 'w') as file:
            file.write(str(n))