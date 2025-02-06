import streamlit as st
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the trained model, scaler, and label encoder
with open('svm_model.pkl', 'rb') as model_file:
    classifier = pickle.load(model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

with open('label_encoder.pkl', 'rb') as le_file:
    le = pickle.load(le_file)

# Streamlit app interface
st.title("Health Condition Prediction")
st.write("Please enter the values for the health conditions:")

# User input fields for each health parameter (adjust as needed)
cold = st.selectbox("Cold", [0, 1])  # 0: No, 1: Yes
cough = st.selectbox("Cough", [0, 1])
dehydration = st.selectbox("Dehydration", [0, 1])
medicine_overdose = st.selectbox("Medicine Overdose", [0, 1])
acidious = st.selectbox("Acidious", [0, 1])
cold_dup = st.selectbox("Cold Dup", [0, 1])  # Add necessary features
cough_dup = st.selectbox("Cough Dup", [0, 1])  # Add necessary features
type_ = st.selectbox("Type", [0, 1, 2, 3])  # Depending on the possible types, adjust as needed
temperature = st.number_input("Temperature", min_value=30.0, max_value=42.0, step=0.1)
heart_rate = st.number_input("Heart Rate", min_value=50, max_value=150, step=1)
pulse = st.number_input("Pulse", min_value=40, max_value=120, step=1)
bpsys = st.number_input("Systolic BP", min_value=80, max_value=180, step=1)
bpdia = st.number_input("Diastolic BP", min_value=50, max_value=120, step=1)
respiratory_rate = st.number_input("Respiratory Rate", min_value=10, max_value=40, step=1)
oxygen_saturation = st.number_input("Oxygen Saturation", min_value=90.0, max_value=100.0, step=0.1)
ph = st.number_input("pH", min_value=7.0, max_value=7.9, step=0.1)

# Prepare input data as numpy array (ensure it has 16 features)
input_data = np.array([cold, cough, dehydration, medicine_overdose, acidious, cold_dup, cough_dup, type_,
                       temperature, heart_rate, pulse, bpsys, bpdia, respiratory_rate, oxygen_saturation, ph])

# Apply transformations: LabelEncoding and Scaling
input_data[0] = le.transform([input_data[0]])[0]  # Encoding Cold
input_data[1] = le.transform([input_data[1]])[0]  # Encoding Cough
input_data[2] = le.transform([input_data[2]])[0]  # Encoding Dehydration
input_data[3] = le.transform([input_data[3]])[0]  # Encoding Medicine Overdose
input_data[4] = le.transform([input_data[4]])[0]  # Encoding Acidious

# Reshape input data and scale
input_data = input_data.reshape(1, -1)
input_data_scaled = scaler.transform(input_data)

# Make prediction when the button is pressed
if st.button('Predict'):
    prediction = classifier.predict(input_data_scaled)

    # Map prediction to the corresponding condition
    conditions = ['Normal', 'Mild', 'Severe', 'Chronic']
    result = conditions[prediction[0]]

    st.write(f"Prediction: {result}")
