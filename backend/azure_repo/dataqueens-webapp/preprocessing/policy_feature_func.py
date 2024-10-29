from preprocessing.av_profile_func import create_av_profile
from preprocessing.user_profile_func import create_user_profile
import pandas as pd

def create_policy_features(av_path: str, user_path: str, number_of_rows=50) -> pd.DataFrame:
    '''
    takes in path for av data
    takes in path for user data

    returns a df of policy features including both av and user profile
    '''

    av_profile = create_av_profile(av_path)
    user_profile = create_user_profile(user_path)

    sample_av = av_profile.sample(n=number_of_rows).reset_index(drop=True)
    sample_user = user_profile.sample(n=number_of_rows).reset_index(drop=True)

    policy_sample = pd.concat([sample_av, sample_user], axis=1)

    return policy_sample