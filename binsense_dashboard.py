import streamlit as st
import serial
import time
import pandas as pd

# --- Arduino setup ---
arduino = serial.Serial('COM11', 9600, timeout=1)
time.sleep(2)

st.title("💧 Smart Bin IR & Rain Sensor Dashboard")

data = []
placeholder = st.empty()

# --- Live data collection loop ---
for _ in range(10000):
    line = arduino.readline().decode('utf-8').strip()
    if line.startswith("IR:"):
        try:
            parts = line.split(',')
            ir_value = int(parts[0].split(':')[1])
            rain_value = int(parts[1].split(':')[1])

            ir_status = "Object Detected" if ir_value == 1 else "No Object"
            rain_status = "Rain Detected" if rain_value == 1 else "No Rain"

            data.append({
                "Time": time.strftime("%H:%M:%S"),
                "IR Value": ir_value,
                "IR Status": ir_status,
                "Rain Value": rain_value,
                "Rain Status": rain_status
            })

            df = pd.DataFrame(data[-20:])  # last 20 readings
            df_full = pd.DataFrame(data)

            # Summary counts
            ir_count = df_full["IR Value"].sum()
            rain_count = df_full["Rain Value"].sum()
            summary_df = pd.DataFrame({
                "Sensor": ["IR Sensor", "Rain Sensor"],
                "Times Value = 1": [ir_count, rain_count]
            })

            with placeholder.container():
                st.subheader("📊 Live Sensor Readings")
                st.dataframe(df, use_container_width=True)

                st.metric("IR Status", ir_status)
                st.metric("Rain Status", rain_status)

                st.subheader("📈 Sensor Detection Summary (Live)")
                st.bar_chart(summary_df.set_index("Sensor"))

            time.sleep(1)

        except Exception as e:
            st.write("Error parsing:", e)

arduino.close()
