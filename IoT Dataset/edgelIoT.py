import pandas as pd

def format_edgeiiot_dataset(input_filepath, output_filepath):
    # 1. read CSV
    print(f"Reading Data: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)
    
    # 2. Column mapping
    # Attack_type -> attack_name
    # Attack_label -> attack_flag
    rename_mapping = {}
    if 'Attack_type' in df.columns:
        rename_mapping['Attack_type'] = 'attack_name'
    if 'Attack_label' in df.columns:
        rename_mapping['Attack_label'] = 'attack_flag'
        
    # Apply column name changes
    df.rename(columns=rename_mapping, inplace=True)
    
    # 3. If no attack_step -> append
    # Default: 0
    if 'attack_step' not in df.columns:
        df['attack_step'] = 0
        
    # 4. Relocate order
    # attack_name, attack_flag, attack_step : at the very-end
    target_columns = ['attack_name', 'attack_flag', 'attack_step']
    
    feature_columns = [col for col in df.columns if col not in target_columns]
    new_column_order = feature_columns + target_columns
    df = df[new_column_order]
    
    # 5. save as new CSV file
    print(f"Saving: {output_filepath}")
    df.to_csv(output_filepath, index=False)
    print("Process completed!")

if __name__ == "__main__":
    input_file = "ML-EdgeIIoT-dataset.csv" 
    
    # new file name
    output_file = "Reformatted_ML-EdgeIIoT-dataset.csv"
    
    format_edgeiiot_dataset(input_file, output_file)