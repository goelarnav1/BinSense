import streamlit as st
import serial
import time
import pandas as pd

# ---- Page Config ----
st.set_page_config(page_title="Smart Bin Dashboard", layout="wide")

# ---- Arduino Setup ----
if "arduino" not in st.session_state:
    st.session_state.arduino = serial.Serial('COM11', 9600, timeout=1)
    time.sleep(2)

arduino = st.session_state.arduino

# ---- Data Storage ----
if "data" not in st.session_state:
    st.session_state.data = []

st.title("💧 Smart Bin - IR & Rain Sensor Dashboard")

# ---- Read One Line From Serial ----
line = arduino.readline().decode(errors="ignore").strip()

if line.startswith("IR:"):
    try:
        parts = line.split(',')
        ir_value = int(parts[0].split(':')[1])
        rain_value = int(parts[1].split(':')[1])

        ir_status = "Object Detected" if ir_value == 1 else "No Object"
        rain_status = "Rain Detected" if rain_value == 1 else "No Rain"

        st.session_state.data.append({
            "Time": time.strftime("%H:%M:%S"),
            "IR Value": ir_value,
            "IR Status": ir_status,
            "Rain Value": rain_value,
            "Rain Status": rain_status
        })

    except:
        st.write("⚠️ Error parsing:", line)


# ---- Convert Data ----
df = pd.DataFrame(st.session_state.data[-20:])
df_full = pd.DataFrame(st.session_state.data)

# ---- Summary ----
if not df_full.empty:
    ir_count = df_full["IR Value"].sum()
    rain_count = df_full["Rain Value"].sum()
else:
    ir_count = rain_count = 0


summary_df = pd.DataFrame({
    "Sensor": ["IR Sensor", "Rain Sensor"],
    "Times Value = 1": [ir_count, rain_count]
})

# ---- Display ----
placeholder = st.empty()

with placeholder.container():

    st.subheader("📊 Live Sensor Readings (Last 20)")
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("IR Status", df.iloc[-1]["IR Status"] if not df.empty else "-")
    col2.metric("Rain Status", df.iloc[-1]["Rain Status"] if not df.empty else "-")

    st.subheader("📈 Detection Summary")
    st.bar_chart(summary_df.set_index("Sensor"))

# ---- Auto Refresh every 1 second ----
time.sleep(1)
st.experimental_rerun()
