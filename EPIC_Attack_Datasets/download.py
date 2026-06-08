import pandas as pd
import argparse

def process_dataframe(df):
    """
    데이터프레임의 인덱스를 제거하고 라벨(attack_name, attack_flag, attack_step)을 생성하여 반환합니다.
    """
    # 1. Remove unnecessary index column (Unnamed: 0)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # 2. Create a new labeling column
    # - attack_name: Unify existing status values ​​to lowercase
    df['attack_name'] = df['status'].str.lower()

    # - attack_flag: 0 for normal, 1 otherwise (fdia, etc.)
    df['attack_flag'] = df['attack_name'].apply(lambda x: 0 if x == 'normal' else 1)

    # - attack_step: -1
    df['attack_step'] = -1

    # 3. Delete existing status column
    df = df.drop(columns=['status'])

    # 4. Rearrange column order (put labeling column at the back)
    feature_cols = [col for col in df.columns if col not in ['attack_name', 'attack_flag', 'attack_step']]
    new_col_order = feature_cols + ['attack_name', 'attack_flag', 'attack_step']
    df = df[new_col_order]

    return df

def main():
    parser = argparse.ArgumentParser(description="Download and preprocess EPIC data from GitHub.")
    parser.add_argument(
        '--mode', 
        type=str, 
        choices=['separate', 'merge'], 
        default='separate',
        help="ave file as 'separated' or 'merged'"
    )
    args = parser.parse_args()

    # GitHub Raw URL
    url_a = 'https://raw.githubusercontent.com/smartgridadsc/EPIC_Attack_Datasets/main/dataset_raw/dataset_EPICA_raw.csv'
    url_b = 'https://raw.githubusercontent.com/smartgridadsc/EPIC_Attack_Datasets/main/dataset_raw/dataset_EPICB_raw.csv'

    print("Downlading Raw Data in Github")
    df_a = pd.read_csv(url_a)
    df_b = pd.read_csv(url_b)
    print("Download completed\n")

    if args.mode == 'separate':
        
        df_a_processed = process_dataframe(df_a)
        df_b_processed = process_dataframe(df_b)
        
        df_a_processed.to_csv('Reformatted_EPICA.csv', index=False)
        df_b_processed.to_csv('Reformatted_EPICB.csv', index=False)
        
        print("'Reformatted_EPICA.csv' and 'Reformatted_EPICB.csv' files have been created.")

    elif args.mode == 'merge':
        df_merged = pd.concat([df_a, df_b], ignore_index=True)
        df_processed = process_dataframe(df_merged)
        
        df_processed.to_csv('Reformatted_EPIC.csv', index=False)

        print("'Reformatted_EPIC.csv' file has been created.")

if __name__ == "__main__":
    main()