import streamlit as st
import serial
import time
import pandas as pd

# --------- ARDUINO SETUP (SAFE) ---------
if "arduino" not in st.session_state:
    try:
        st.session_state.arduino = serial.Serial('COM10', 9600, timeout=1)
        time.sleep(2)
    except Exception as e:
        st.error(f"❌ Could not open COM10.\nClose Arduino Serial Monitor!\n\n{e}")
        st.stop()

arduino = st.session_state.arduino

st.title("💧 Smart Bin IR / Metal / Rain Sensor Dashboard")

# Save historical data
if "data" not in st.session_state:
    st.session_state.data = []

placeholder = st.empty()

# --------- READ ONE SENSOR PACKET ---------
packet = []
start = time.time()

while True:
    raw = arduino.readline().decode(errors="ignore").strip()

    if raw == "":
        if time.time() - start > 0.5:
            break
        continue

    packet.append(raw)

    if len(packet) >= 4:
        break

# --------- DEFAULT VALUES ---------
ir_status = "Unknown"
proximity_status = "Unknown"
rain_analog = 0
rain_status = "Unknown"

# --------- PARSE LINES ---------
for p in packet:
    if p.startswith("IR Sensor"):
        ir_status = p.split(":")[1].strip()
    elif p.startswith("Proximity Sensor"):
        proximity_status = p.split(":")[1].strip()
    elif p.startswith("Rain Analog Value"):
        try:
            rain_analog = int(p.split(":")[1].strip())
        except:
            rain_analog = 0
    elif p.startswith("Rain Digital Value"):
        rain_status = p.split(":")[1].strip()

# --------- ADD RECORD ---------
record = {
    "Time": time.strftime("%H:%M:%S"),
    "IR Status": ir_status,
    "Metal Status": proximity_status,
    "Rain Analog": rain_analog,
    "Rain Digital": rain_status,
}

st.session_state.data.append(record)

df = pd.DataFrame(st.session_state.data[-20:])
df_full = pd.DataFrame(st.session_state.data)

# --------- SUMMARY ---------
def to_numeric_status(val):
    if val in ["Object Detected", "Object Nearby", "WET"]:
        return 1
    return 0

summary_df = pd.DataFrame({
    "Sensor": ["IR Sensor", "Metal Sensor", "Rain (Digital)"],
    "Count": [
        df_full["IR Status"].apply(to_numeric_status).sum(),
        df_full["Metal Status"].apply(to_numeric_status).sum(),
        df_full["Rain Digital"].apply(lambda x: 1 if x == "WET" else 0).sum(),
    ]
})

summary_df["Count"] = summary_df["Count"].astype(int)

# --------- UI ---------
with placeholder.container():

    st.subheader("📊 Live Sensor Readings (Last 20)")
    st.dataframe(df, width='stretch')

    col1, col2, col3 = st.columns(3)
    col1.metric("IR Sensor", ir_status)
    col2.metric("Metal Sensor", proximity_status)
    col3.metric("Rain Status", rain_status)

    st.subheader("📈 Sensor Detection Summary")
    st.bar_chart(summary_df.set_index("Sensor"))

# --------- AUTO-RUN LOOP WITHOUT PAGE REFRESH ---------
time.sleep(1)
st.stop()   # stops execution but keeps UI alive
