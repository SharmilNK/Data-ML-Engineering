import streamlit as st
import requests
import json
from datetime import datetime
import calendar

# Page configuration
st.set_page_config(
    page_title="From Air to Care - Hospital Admission Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .prediction-number {
        font-size: 4rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .input-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<p class="main-header">🏥 From Air to Care</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Predicting Tomorrow\'s ER Strain Today</p>', unsafe_allow_html=True)

st.markdown("""
    This application predicts hospital admission counts in NYC boroughs based on date and location.
    Select a date and borough to get predictions.
""")

# API Configuration
API_URL = st.sidebar.text_input(
    "API URL",
    value="https://from-air-to-care-api-4ahsfteyfa-uc.a.run.app/predict",
    help="Enter the deployed API endpoint URL"
)

# Check API health
@st.cache_data(ttl=60)
def check_api_health(api_base_url):
    """Check if API is available."""
    try:
        health_url = api_base_url.replace("/predict", "/health")
        response = requests.get(health_url, timeout=5)
        return response.status_code == 200
    except:
        return False

# Display API status
api_healthy = check_api_health(API_URL)
if api_healthy:
    st.sidebar.success("✅ API is healthy")
else:
    st.sidebar.warning("⚠️ API health check failed. Please verify the URL.")

# Main input form
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.subheader("📊 Input Parameters")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Select Date")
        selected_date = st.date_input(
            "Date",
            value=datetime(2023, 6, 15).date(),
            min_value=datetime(2022, 1, 1).date(),
            max_value=datetime(2024, 12, 31).date(),
            help="Select a date between January 1, 2022 and December 31, 2024"
        )
        
        # Display date info
        st.info(f"""
        **Selected Date:** {selected_date.strftime('%B %d, %Y')}
        - Day of Week: {calendar.day_name[selected_date.weekday()]}
        - Month: {calendar.month_name[selected_date.month]}
        """)
    
    with col2:
        st.markdown("### 📍 Select Borough")
        borough = st.selectbox(
            "NYC Borough",
            options=["brooklyn", "bronx", "manhattan", "queens", "staten island"],
            index=0,
            help="Select the NYC borough for prediction"
        )
        
        # Display borough info
        borough_display = borough.title().replace("_", " ")
        st.info(f"""
        **Selected Borough:** {borough_display}
        """)
    
    # Submit button
    submit_button = st.form_submit_button("🔮 Get Prediction", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle form submission
if submit_button:
    # Extract temporal features from date
    month = selected_date.month
    day = selected_date.day
    day_of_week = selected_date.weekday()  # 0=Monday, 6=Sunday
    
    # Calculate quarter
    quarter = (month - 1) // 3 + 1
    
    # Calculate season (1=Winter, 2=Spring, 3=Summer, 4=Fall)
    if month in [12, 1, 2]:
        season = 1  # Winter
    elif month in [3, 4, 5]:
        season = 2  # Spring
    elif month in [6, 7, 8]:
        season = 3  # Summer
    else:
        season = 4  # Fall
    
    # Prepare request data (only date and borough)
    request_data = {
        "month": month,
        "day": day,
        "day_of_week": day_of_week,
        "quarter": quarter,
        "season": season,
        "borough": borough.lower().strip()
    }
    
    # Make API request
    with st.spinner("🔄 Getting prediction from API..."):
        try:
            response = requests.post(
                API_URL,
                json=request_data,
                timeout=30,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    predictions = result.get("predictions", {})
                    
                    # Get regression result (predicted admissions) - ONLY show this
                    regression = predictions.get("regression", {})
                    predicted_admissions = regression.get("predicted_admissions", 0.0)
                    predicted_admissions_rounded = regression.get("predicted_admissions_rounded", 0)
                    
                    # Display prediction result
                    st.markdown("---")
                    st.markdown("## 📊 Prediction Result")
                    
                    st.markdown(
                        f'''
                        <div class="prediction-card">
                            <h2 style="margin-bottom: 1rem;">Predicted Hospital Admissions</h2>
                            <div class="prediction-number">{predicted_admissions_rounded}</div>
                            <p style="font-size: 1.2rem; margin-top: 1rem;">patients</p>
                            <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">
                                Exact prediction: {predicted_admissions:.1f} patients
                            </p>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )
                    
                    # Additional information
                    st.markdown("### 📋 Prediction Details")
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        st.info(f"""
                        **Date:** {selected_date.strftime('%B %d, %Y')}  
                        **Day of Week:** {calendar.day_name[day_of_week]}  
                        **Month:** {calendar.month_name[month]}  
                        **Season:** {['Winter', 'Spring', 'Summer', 'Fall'][season-1]}
                        """)
                    
                    with col_info2:
                        st.info(f"""
                        **Borough:** {borough_display}  
                        **Quarter:** Q{quarter}  
                        **Prediction:** {predicted_admissions_rounded} admissions
                        """)
                    
                    # Interpretation
                    st.markdown("### 💡 What This Means")
                    st.success(f"""
                    Based on historical patterns for **{borough_display}** on **{selected_date.strftime('%B %d, %Y')}**, 
                    the model predicts approximately **{predicted_admissions_rounded} patients** will be admitted to hospitals.
                    
                    This prediction considers:
                    - Seasonal patterns (time of year)
                    - Day of week effects
                    - Borough-specific historical trends
                    """)
                    
                    # Optional: Show raw API response
                    with st.expander("🔍 View Raw API Response"):
                        st.json(result)
                        
                else:
                    st.error(f"❌ API returned unsuccessful response: {result}")
                    
            else:
                st.error(f"❌ API request failed with status code {response.status_code}")
                st.error(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Please check:")
            st.error("1. The API URL is correct")
            st.error("2. The API service is running")
            st.error("3. Your internet connection is working")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. The API may be slow or unavailable.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>From Air to Care</strong> - Predicting Tomorrow's ER Strain Today</p>
        <p>Built with Streamlit | Powered by Machine Learning</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">
            <strong>Supported Date Range:</strong> January 1, 2022 - December 31, 2024
        </p>
    </div>
""", unsafe_allow_html=True)
