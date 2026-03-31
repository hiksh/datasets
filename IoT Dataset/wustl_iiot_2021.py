import pandas as pd

# ==========================================
# Idea (데이터 전처리 가정 및 전제조건)
# ==========================================
# 1. 컬럼명 정제: CSV 헤더에 포함될 수 있는 불필요한 따옴표(")와 공백을 제거
# 2. 라벨 매핑: 
#    - 'Traffic': 구체적인 트래픽/공격 명칭 (attack_name)
#    - 'Target': 공격 발생 여부 (attack_flag)
# 3. 사이버 킬 체인 매핑 (attack_step):
#    - 'attack_name'을 기반으로 공격 단계를 추론하여 1~7단계로 수치화
#    - 새로 확인된 'DoS' 공격은 7단계로 추가
# ==========================================

def format_fourth_dataset(input_filepath, output_filepath):
    print(f"Reading Data: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)
    
    # 1. Remove quotes and spaces from column names
    df.columns = df.columns.str.strip().str.replace('"', '', regex=False)
    
    # 2. Mapping column name
    rename_mapping = {}
    if 'Traffic' in df.columns: rename_mapping['Traffic'] = 'attack_name'
    if 'Target' in df.columns:  rename_mapping['Target'] = 'attack_flag'
        
    df.rename(columns=rename_mapping, inplace=True)
    
    # 3. attack_step: Mapping according to Cyber Kill Chain
    if 'attack_name' in df.columns:
        kill_chain_mapping = {
            # 0. Noraml
            'normal': 0,
            
            # 1. Reconnaissance
            'reconn': 1,
            
            # 2. Weaponization
            'weapon': 2, 'weaponization': 2, 'insider_malcious': 2,
            
            # 4. Exploitation
            'comminj':4, # Command Injection
            
            # 5. Installation
            'backdoor': 5,
            
            # 7. Actions on Objectives (Append DoS)
            'dos': 7, 'ddos': 7 
        }
        
        # Converting to lowercase before applying mapping
        name_series = df['attack_name'].astype(str).str.strip().str.lower()
        
        # Reconfirm unmapped values
        unmapped_values = name_series[~name_series.isin(kill_chain_mapping.keys())].unique()
        if len(unmapped_values) > 0:
            print(f"\n[Alert] Unmapped Values : {unmapped_values}\n")
            
        df['attack_step'] = name_series.map(kill_chain_mapping).fillna(-1).astype(int)

        # Results aggregation and print output
        total_rows = len(df)
        unmapped_count = (df['attack_step'] == -1).sum()
        mapped_count = total_rows - unmapped_count
        
        print("-" * 40)
        print("[Summary of Cyber Kill Chain Mapping Results]")
        print(f"  • Total number of data: {total_rows:,} ")
        print(f"  • Mapping well (0~7): {mapped_count:,} ")
        print(f"  • Unconfirmed value (-1): {unmapped_count:,} ")
        print("-" * 40)
        
        print("[Detailed distribution by stage(Step 0 ~ 7)]")
        step_counts = df['attack_step'].value_counts().sort_index()
        for step, count in step_counts.items():
            print(f"  Step {step:2} : {count:,}")
        print("-" * 40 + "\n")
        
    # The Target column (attack_flag) is already a number, but fixed it to int just in case.
    if 'attack_flag' in df.columns:
        df['attack_flag'] = pd.to_numeric(df['attack_flag'], errors='coerce').fillna(0).astype(int)

    # 4. Relocate order
    target_columns = ['attack_name', 'attack_flag', 'attack_step']
    target_columns = [col for col in target_columns if col in df.columns]
    feature_columns = [col for col in df.columns if col not in target_columns]
    
    new_column_order = feature_columns + target_columns
    df = df[new_column_order]
    
    # 5. Save as CSV file
    print(f"Saving: {output_filepath}")
    df.to_csv(output_filepath, index=False)
    print("Process completed!\n")

if __name__ == "__main__":
    input_file = "wustl_iiot_2021.csv" 
    output_file = "Reformatted_wustl_iiot_2021.csv"
    
    format_fourth_dataset(input_file, output_file)