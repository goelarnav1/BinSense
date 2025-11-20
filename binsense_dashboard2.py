import streamlit as st
import serial
import time
import pandas as pd

<<<<<<< HEAD
# --------- ARDUINO SETUP (SAFE) ---------
if "arduino" not in st.session_state:
    try:
        st.session_state.arduino = serial.Serial('COM10', 9600, timeout=1)
        time.sleep(2)
    except Exception as e:
        st.error(f"❌ Could not open COM10.\nClose Arduino Serial Monitor!\n\n{e}")
=======
# ---- AUTO REFRESH EVERY 1 SECOND (JAVASCRIPT, NO FLICKER) ----
refresh_rate_ms = 1000  # 1 second
st.markdown(
    f"""
    <meta http-equiv="refresh" content="{refresh_rate_ms/1000}">
    """,
    unsafe_allow_html=True
)

# --------- ARDUINO SETUP (SAFE) ---------
if "arduino" not in st.session_state:
    try:
        st.session_state.arduino = serial.Serial('COM12', 9600, timeout=1)
        time.sleep(2)
    except Exception as e:
        st.error(f"❌ COM12 cannot be opened.\nClose Arduino Serial Monitor!\n\n{e}")
>>>>>>> a9ba6a80b81ed13e987752c87f30df9a64c51d67
        st.stop()

arduino = st.session_state.arduino

st.title("💧 Smart Bin IR / Metal / Rain Sensor Dashboard")

<<<<<<< HEAD
# Save historical data
=======
# Data list
>>>>>>> a9ba6a80b81ed13e987752c87f30df9a64c51d67
if "data" not in st.session_state:
    st.session_state.data = []

placeholder = st.empty()

<<<<<<< HEAD
# --------- READ ONE SENSOR PACKET ---------
=======
# --------- READ ONE FULL SENSOR PACKET ---------
>>>>>>> a9ba6a80b81ed13e987752c87f30df9a64c51d67
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
<<<<<<< HEAD

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
=======

# --------- PARSE PACKET LINES ---------
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

# --------- APPEND CLEAN RECORD ---------
record = {
    "Time": time.strftime("%H:%M:%S"),
    "IR Status": ir_status,
    "Metal Status": proximity_status,
    "Rain Analog": rain_analog,
    "Rain Digital": rain_status,
}

st.session_state.data.append(record)

# Keep last 20 rows
df = pd.DataFrame(st.session_state.data[-20:])
df_full = pd.DataFrame(st.session_state.data)

# --------- SAFE CONVERSION FOR SUMMARY ---------
>>>>>>> a9ba6a80b81ed13e987752c87f30df9a64c51d67
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

<<<<<<< HEAD
# --------- UI ---------
=======
# --------- ORIGINAL UI (UNCHANGED) ---------
>>>>>>> a9ba6a80b81ed13e987752c87f30df9a64c51d67
with placeholder.container():

    st.subheader("📊 Live Sensor Readings (Last 20)")
    st.dataframe(df, width='stretch')

    col1, col2, col3 = st.columns(3)
    col1.metric("IR Sensor", ir_status)
    col2.metric("Metal Sensor", proximity_status)
    col3.metric("Rain Status", rain_status)

    st.subheader("📈 Sensor Detection Summary")
    st.bar_chart(summary_df.set_index("Sensor"))
<<<<<<< HEAD

# --------- AUTO-RUN LOOP WITHOUT PAGE REFRESH ---------
time.sleep(1)
st.stop()   # stops execution but keeps UI alive
=======
>>>>>>> a9ba6a80b81ed13e987752c87f30df9a64c51d67
