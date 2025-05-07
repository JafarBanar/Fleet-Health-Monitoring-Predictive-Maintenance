# Fleet Health Monitoring Dashboard

This dashboard visualizes vehicle telemetry from Azure SQL and includes tools for predictive maintenance.

## Setup
1. Create a virtual environment
2. Install requirements with `pip install -r requirements.txt`
3. Run the app: `streamlit run app/streamlit_app.py`

## Structure
- `app/`: Dashboard and logic
- `etl/`: Scripts to load or simulate data
- `data/`: CSV and telemetry sources
- `tests/`: Validation scripts

## 📸 Dashboard Preview

![Dashboard Screenshot](screenshots/dashboard_main.png)


## 🚀 Deploy on Streamlit Cloud

You can deploy this project in a few clicks:

1. Fork this repo to your GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click “New app” → link your repo
4. Set main file to: `app/streamlit_app.py`
5. (Optional) Add secrets under Settings if needed



