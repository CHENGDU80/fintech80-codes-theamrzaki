import pandas as pd

def create_user_profile(path: str) -> pd.DataFrame:
    '''
    takes in a path
    returns a df of user profile such as:
    - sex
    - education
    - age
    - time as customer etc
    '''
    data = pd.read_csv(path)
    feature_list = [0,1,10,11,14,37]
    data_features = pd.DataFrame()
    for i in feature_list:
        data_features[data.columns[i]] = data[data.columns[i]]

    education_mapping = {
        'High School': 1,
        'Associate': 2,
        'College': 2,
        'JD': 3,
        'MD': 3,
        'Masters': 3,
        'PhD': 3
    }

    # Apply the mapping to the column
    data_features['insured_education_level_category'] = data_features['insured_education_level'].map(education_mapping)

    relationship_mapping = {
        'unmarried' : 1,
        'other-relative' : 1,
        'not-in-family' : 1,
        'husband' : 2,
        'wife' : 2,
        'own-child' : 3
    }

    data_features['insured_relationship_category'] = data_features['insured_relationship'].map(relationship_mapping)
    data_features['sex_encoded'] = data_features['insured_sex'].apply(lambda x: 1 if x == 'MALE' else 2)
    
    return data_features