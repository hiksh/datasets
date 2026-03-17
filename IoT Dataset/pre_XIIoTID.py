import pandas as pd

# ==========================================
# Idea (데이터 전처리 가정 및 전제조건)
# ==========================================
# 1. 라벨 매핑: 
#    - 'class': 공격의 큰 범주 및 단계 (attack_step)
#    - 'class2': 구체적인 공격 기법 (attack_name)
#    - 'class3': 공격 발생 여부 (attack_flag)
# 2. 사이버 킬 체인(Cyber Kill Chain) 기반 attack_step 수치화:
#    - 정상(Normal)은 0, 텍스트로 된 공격 단계/기법은 1~7단계로 분류하여 수치화
# 3. 이진 분류 최적화: 
#    - 'attack_flag'의 'Normal'은 0으로, 그 외는 1로 수치화 (0,1 이외 값 없음)
# ==========================================

def format_custom_dataset_with_killchain(input_filepath, output_filepath):
    print(f"Reading Data: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)
    
    # 1. Mapping column name
    rename_mapping = {}
    if 'class2' in df.columns: rename_mapping['class2'] = 'attack_name'
    if 'class3' in df.columns: rename_mapping['class3'] = 'attack_flag'
    if 'class' in df.columns:  rename_mapping['class'] = 'attack_step'
        
    df.rename(columns=rename_mapping, inplace=True)
    
    # 2. attack_flag Quantification (Normal -> 0, Other -> 1)
    if 'attack_flag' in df.columns:
        df['attack_flag'] = df['attack_flag'].astype(str).str.strip().str.lower().apply(lambda x: 0 if x == 'normal' else 1)
    
    # 3. attack_step: Mapping according to Cyber Kill Chain
    if 'attack_step' in df.columns:
        kill_chain_mapping = {
            # 0. Noraml
            'normal': 0,
            
            # 1. Reconnaissance
            'reconnaissance': 1, 'os_scan': 1, 'vul_scan': 1, 'coap_scan': 1, 
            'modbus_reading': 1, 'fuzzing': 1, 'mqtt_subscription': 1,
            
            # 2. Weaponization
            'weapon': 2, 'weaponization': 2, 'insider_malcious': 2,
            
            # 3. Delivery
            'delivery': 3, 'fake_notification': 3,
            
            # 4. Exploitation
            'exploitation': 4, 'bruteforce': 4, 'dictionary': 4, 
            'data_injection': 4, 'mitm': 4,
            
            # 5. Installation
            'installation': 5, 'shell': 5,
            
            # 6. C&C
            'c&c': 6, 'command & control': 6, 'tcp_relay': 6,
            
            # 7. Actions on Objectives
            'exfiltration': 7, 'actions on objectives': 7, 'rdos': 7, 'crypto_ransom': 7
        }
        
        step_series = df['attack_step'].astype(str).str.strip().str.lower()
        
        # Reconfirm unmapped values
        unmapped_values = step_series[~step_series.isin(kill_chain_mapping.keys())].unique()
        if len(unmapped_values) > 0:
            print(f"\n[Alert] Unmapped Values : {unmapped_values}\n")
        
        df['attack_step'] = step_series.map(kill_chain_mapping).fillna(-1).astype(int)
        
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
    
    # 4. Relocate order
    target_columns = ['attack_name', 'attack_flag', 'attack_step']
    target_columns = [col for col in target_columns if col in df.columns]
    feature_columns = [col for col in df.columns if col not in target_columns]
    
    new_column_order = feature_columns + target_columns
    df = df[new_column_order]
    
    # 5. Save as CSV file
    print(f"Saving: {output_filepath}")
    df.to_csv(output_filepath, index=False)
    print("Process completed!")

if __name__ == "__main__":
    input_file = "pre_XIIoTID.csv" 
    output_file = "Reformatted_pre_XIIoTID.csv"
    
    format_custom_dataset_with_killchain(input_file, output_file)