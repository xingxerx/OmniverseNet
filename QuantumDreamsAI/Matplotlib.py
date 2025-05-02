import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
# (your existing code remains the same...)
quantum_df = pd.DataFrame(quantum_data, columns=['Universe', 'Reality', 'Quantum_State'])
# Matplotlib 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(quantum_df['Universe'], quantum_df['Reality'], quantum_df['Quantum_State'].map({'0':0, '1':1}))
plt.show()
# Plotly interactive 3D scatter plot
fig = px.scatter_3d(quantum_df, x='Universe', y='Reality', z='Quantum_State', color='Quantum_State')
fig.show()
