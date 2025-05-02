def filter_multiverse(df):
    universe_id = int(input("Enter universe ID (or -1 for all): "))
    reality_type = input("Enter reality type (or 'all' for all): ")
    quantum_state = input("Enter quantum state (|0⟩, |1⟩, or 'superposition'): ")
    data_value_min = float(input("Enter min data value (or -1 for no limit): "))
    data_value_max = float(input("Enter max data value (or 2 for no limit): "))
    filtered_df = df.copy()
    if universe_id != -1:
        filtered_df = filtered_df[filtered_df['Universe'] == universe_id]
    if reality_type != 'all':
        filtered_df = filtered_df[filtered_df['Reality'] == reality_type]
    if quantum_state != 'superposition':
        filtered_df = filtered_df[filtered_df['Quantum_State'] == quantum_state]
    if data_value_min != -1:
        filtered_df = filtered_df[filtered_df['Data'] >= data_value_min]
    if data_value_max != 2:
        filtered_df = filtered_df[filtered_df['Data'] <= data_value_max]
    return filtered_df
filtered_df = filter_multiverse(quantum_df)
print(filtered_df.head())
