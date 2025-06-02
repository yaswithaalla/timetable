import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Timetable Generator", layout="centered")

st.title("📅 Study Timetable Generator")

# Step 1: User inputs
st.header("Step 1: Enter Subjects and Weekly Hours")
subjects = st.text_area("List your subjects (one per line)").splitlines()
weekly_hours = {}

if subjects:
    st.subheader("Set Weekly Hours per Subject")
    for subject in subjects:
        weekly_hours[subject] = st.slider(f"{subject}", 1, 20, 5)

# Step 2: Set availability
st.header("Step 2: Set Your Available Time Slots")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
time_slots = [f"{h}:00" for h in range(8, 22)]  # 8 AM to 9 PM

available_slots = []
for day in days:
    selected = st.multiselect(f"{day}", time_slots, default=[], key=day)
    for slot in selected:
        available_slots.append((day, slot))

# Step 3: Generate Timetable
if st.button("Generate Timetable") and subjects and available_slots:
    st.header("📋 Your Timetable")

    # Flatten subjects into hourly chunks
    task_pool = []
    for subject, hours in weekly_hours.items():
        task_pool.extend([subject] * hours)

    random.shuffle(task_pool)

    timetable = pd.DataFrame("", index=days, columns=time_slots)
    slot_idx = 0

    for task in task_pool:
        if slot_idx >= len(available_slots):
            st.warning("Not enough available slots for all subject hours!")
            break

        day, time = available_slots[slot_idx]
        if timetable.loc[day, time] == "":
            timetable.loc[day, time] = task
            slot_idx += 1
        else:
            # Try next available slot
            while slot_idx < len(available_slots) and timetable.loc[available_slots[slot_idx][0], available_slots[slot_idx][1]] != "":
                slot_idx += 1
            if slot_idx < len(available_slots):
                day, time = available_slots[slot_idx]
                timetable.loc[day, time] = task
                slot_idx += 1

    # Display timetable
    st.dataframe(timetable.fillna(""))

    st.success("Done! You can screenshot this or extend it with export/download functionality.")
