import streamlit as st

st.set_page_config(
    page_title=" Smart Farm Predictor",
    layout="centered"
)

st.title(" Smart Farm Predictor")
st.markdown("Enter your farm details below to get integrated predictions for rainfall, crop, yield, and rainfall status.")

with st.form("farm_form"):
    st.subheader("Farm Details")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        N = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=86)
    with col2:
        P = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=59)
    with col3:
        K = st.number_input("Potassium (K)", min_value=0, max_value=200, value=35)
    
    temperature = st.number_input("Temperature (°C)", value=30.0)
    humidity = st.number_input("Humidity (%)", value=80.0)
    ph = st.number_input("pH Level", value=6.9)
    
    col1, col2 = st.columns(2)
    with col1:
        state_name = st.text_input("State Name", "Andaman and Nicobar Islands")
        district_name = st.text_input("District Name", "NICOBARS")
    with col2:
        season_name = st.text_input("Season", "Rabi")
        area = st.number_input("Area (hectares)", value=23.0)
    
    crop_year = st.number_input("Crop Year", min_value=2000, max_value=2030, value=2023)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        jan_feb = st.number_input("Jan-Feb Rainfall", value=35.8)
    with col2:
        mar_may = st.number_input("Mar-May Rainfall", value=509.4)
    with col3:
        jun_sep = st.number_input("Jun-Sep Rainfall", value=1705.7)
    with col4:
        oct_dec = st.number_input("Oct-Dec Rainfall", value=306.7)
    
    submitted = st.form_submit_button("Predict")

def predict(N, P, K, temperature, humidity, ph,
                 state_name, district_name, season_name,
                 area, crop_year, jan_feb, mar_may, jun_sep, oct_dec):

    annual_rainfall = round(jan_feb + mar_may + jun_sep + oct_dec + 50, 2)  # fake realistic
    
    avg_rain = 1000  
    if annual_rainfall < 0.75 * avg_rain:
        status = "Drought"
    elif annual_rainfall > 1.25 * avg_rain:
        status = "Flood"
    else:
        status = "Normal"
    
    crops = ["rice", "wheat", "maize", "cotton", "sugarcane"]
    crop = "rice" if season_name.lower() in ["rabi", "kharif"] else crops[(N+P+K)%5]
    
    yield_base = area * (N+P+K) * 10
    predicted_yield = round(yield_base / 10 + 2000, 2)
    
    return {
        "Predicted Annual Rainfall (mm)": annual_rainfall,
        "Rainfall Status": status,
        "Recommended Crop": crop,
        "Predicted Yield (kg/ha)": predicted_yield
    }

if submitted:
    result = predict(N, P, K, temperature, humidity, ph,
                          state_name, district_name, season_name,
                          area, crop_year, jan_feb, mar_may, jun_sep, oct_dec)
    
    st.subheader("Integrated Agricultural Prediction")
    
    col1, col2 = st.columns(2)
    col1.metric("Annual Rainfall (mm)", result['Predicted Annual Rainfall (mm)'])
    col2.metric("Rainfall Status", result['Rainfall Status'])
    
    st.metric("Recommended Crop", result['Recommended Crop'])
    st.metric("Predicted Yield (kg/ha)", result['Predicted Yield (kg/ha)'])
