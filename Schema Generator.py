import streamlit as st
import pandas as pd
import random

# SessionState class for persisting state between button clicks
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

Gym = 'Gym.csv'
Gym = pd.read_csv(Gym)

# Drop rows where the 'Type' column contains "Stretching", "Plyometrics", or "Cardio", "Strongman"
types_to_drop = ["Stretching", "Plyometrics", "Cardio", "Strongman"]
Gym = Gym[~Gym['Type'].isin(types_to_drop)]

types_to_drop = ["Other"]
Gym = Gym[~Gym['Equipment'].isin(types_to_drop)]

def main():
    st.title("FitMate")
    st.write("Welkom bij deze sportschema generator")

Doelen = st.radio("Wat zijn je fitness doelen", ["Afvallen", "Spieropbouw"])

if Doelen:
    st.write("")
else:
    st.write("Selecteer een optie.")

Level = st.radio("Wat is je huidige Fitness Level", ["Beginner", "Gevorderde", "Vergevorderde"])

if Level:
    st.write("")
else:
    st.write("Selecteer een optie.")

locatie = st.radio("Waar train je?", ["Sportschool", "Thuis"])

if locatie:
    st.write("")
    if locatie == "Thuis":
        fitnessapparatuur = st.multiselect("Welke fitnessapparatuur heb je tot je beschikking?", ["Dumbbells", "Weerstandsbanden", "Kettlebells", "Niets"])
        if fitnessapparatuur:
            st.write("")

            # Initialiseer een lege DataFrame
            filtered_gym = pd.DataFrame()

            # Filter de dataset op basis van de geselecteerde fitnessapparatuur
            for equipment_type in fitnessapparatuur:
                if equipment_type == "Dumbbells":
                    filtered_gym = pd.concat([filtered_gym, Gym[Gym['Equipment'].isin(["Body Only", "Dumbbell", "None"])]])
                elif equipment_type == "Weerstandsbanden":
                    filtered_gym = pd.concat([filtered_gym, Gym[Gym['Equipment'].isin(["Body Only", "Bands", "None"])]])
                elif equipment_type == "Kettlebells":
                    filtered_gym = pd.concat([filtered_gym, Gym[Gym['Equipment'].isin(["Body Only", "Kettlebells", "None"])]])
                elif equipment_type == "Niets":
                    filtered_gym = pd.concat([filtered_gym, Gym[Gym['Equipment'].isin(["Body Only", "None"])]])
            
            # Verwijder duplicaten uit de gefilterde dataset
            filtered_gym = filtered_gym.drop_duplicates()

            if not filtered_gym.empty:
                Gym = filtered_gym
            else:
                st.warning("Geen beschikbare oefeningen gevonden voor de geselecteerde fitnessapparatuur.")
        else:
            st.write("Selecteer ten minste één optie voor fitnessapparatuur.")
else:
    st.write("Selecteer een optie.")

leeftijd = st.slider("Hoe oud ben je?", min_value=10, max_value=100, value=25)
st.write("")

gewicht = st.slider("Wat is je gewicht in kilogram?", min_value=30, max_value=200, value=70)
st.write("")

dagen_per_week = st.slider("Hoeveel dagen per week wil je sporten?", min_value=1, max_value=6, value=3)
st.write("")

# Initialize SessionState
state = SessionState(day=0, muscle_group='', exercise_index=0)

if st.button("Genereer Sportschema", key="genereer_button"):
    if Doelen == "Afvallen":
        herhalingen = "10-15"
    elif Doelen == "Spieropbouw":
        herhalingen = "8-12"
    else:
        herhalingen = "Niet gespecificeerd"

    if Level == "Beginner":
        filtered_exercises = Gym[Gym["Level"] == "Beginner"]
    elif Level == "Gevorderde":
        filtered_exercises = Gym[Gym["Level"].isin(["Beginner", "Intermediate"])]
    elif Level == "Vergevorderde":
        filtered_exercises = Gym[Gym["Level"].isin(["Beginner", "Intermediate"])]

    daily_workouts = []
    chosen_muscle_groups = []

    for day in range(dagen_per_week):
        daily_workout = {}

        # Initialisatie van selected_muscle_groups binnen de lus
        selected_muscle_groups = []
        
        if dagen_per_week == 1:
            if day == 0:
                selected_muscle_groups = ["Chest", "Shoulders", "Middle Back", "Lats", "Biceps", "Triceps", "Hamstrings", "Quadriceps"]
        elif dagen_per_week == 2:
            if day == 0:
                selected_muscle_groups = ["Chest", "Shoulders","Lower Back", "Middle Back", "Lats", "Biceps", "Triceps"]
            elif day == 1:
                selected_muscle_groups = ["Hamstrings", "Abductors", "Glutes", "Calves", "Adductors", "Quadriceps"]
        elif dagen_per_week == 3:
            if day == 0:
                selected_muscle_groups = ["Chest", "Shoulders","Lower Back", "Middle Back", "Lats", "Biceps", "Triceps"]
            elif day == 1:
                selected_muscle_groups = ["Hamstrings", "Abductors", "Glutes", "Calves", "Adductors", "Quadriceps"]
            elif day == 2:
                selected_muscle_groups = ["Chest", "Lats", "Shoulders", "Biceps", "Triceps", "Quadriceps", "Hamstrings", "Glutes"]
        elif dagen_per_week == 4:
            if day == 0:
                selected_muscle_groups = ["Chest", "Shoulders","Lower Back", "Middle Back", "Lats", "Biceps", "Triceps"]
            elif day == 1:
                selected_muscle_groups = ["Hamstrings", "Abductors", "Glutes", "Calves", "Adductors", "Quadriceps"]
            elif day == 2:
                selected_muscle_groups = ["Chest", "Shoulders","Lower Back", "Middle Back", "Lats", "Biceps", "Triceps"]
            elif day == 3:
                selected_muscle_groups = ["Hamstrings", "Abductors", "Glutes", "Calves", "Adductors", "Quadriceps"]
        elif dagen_per_week == 5:
            if day == 0:
                selected_muscle_groups = ["Chest", "Chest", "Chest", "Shoulders" ,"Shoulders", "Triceps"]
            elif day == 1:
                selected_muscle_groups = ["Lower Back", "Middle Back", "Lats", "Forearms", "Traps", "Biceps"]
            elif day == 2:
                selected_muscle_groups = ["Hamstrings", "Abductors", "Glutes", "Calves", "Adductors", "Quadriceps"]
            elif day == 3:
                selected_muscle_groups = ["Chest", "Shoulders","Lower Back", "Middle Back", "Lats", "Biceps", "Triceps"]
            elif day == 4:
                selected_muscle_groups = ["Hamstrings", "Abductors", "Glutes", "Calves", "Adductors", "Quadriceps"]
        elif dagen_per_week == 6:
            if day == 0:
                selected_muscle_groups = ["Chest","Chest","Chest", "Shoulders", "Shoulders", "Triceps", "Triceps"]
            elif day == 1:
                selected_muscle_groups = ["Lower Back", "Middle Back", "Lats", "Forearms", "Traps", "Biceps"]
            elif day == 2:
                selected_muscle_groups = ["Hamstrings", "Abductors", "Glutes", "Calves", "Adductors", "Quadriceps"]
            elif day == 3:
                selected_muscle_groups = ["Chest","Chest","Chest", "Shoulders", "Shoulders", "Triceps", "Triceps"]
            elif day == 4:
                selected_muscle_groups = ["Lower Back", "Middle Back", "Lats", "Forearms", "Traps", "Biceps"]
            elif day == 5:
                selected_muscle_groups = ["Hamstrings", "Abductors", "Glutes", "Calves", "Adductors", "Quadriceps"]

        for muscle_group in selected_muscle_groups:
            available_exercises = filtered_exercises[filtered_exercises['BodyPart'] == muscle_group]

            if not available_exercises.empty:
                num_exercises = selected_muscle_groups.count(muscle_group)

                selected_exercises = random.sample(available_exercises['Title'].tolist(), k=min(num_exercises, len(available_exercises)))

                daily_workout[muscle_group] = []
                for selected_exercise in selected_exercises:
                    daily_workout[muscle_group].append({
                        'Exercise': selected_exercise,
                        'Sets': 3,
                        'Reps': herhalingen
                    })

                chosen_muscle_groups.append(muscle_group)
            else:
                st.warning(f"Geen beschikbare oefeningen gevonden voor spiergroep: {muscle_group} en fitness level: {Level}")

        daily_workouts.append(daily_workout)

    st.success(f"Sportschema's voor {dagen_per_week} dagen succesvol gegenereerd! Aantal herhalingen per oefening: {herhalingen}.")

    for i, daily_workout in enumerate(daily_workouts):
        st.write(f"Dag {i+1} sportschema:")
        for muscle_group, exercise_list in daily_workout.items():
            st.write(f"\nSpiergroep: {muscle_group}")
            for i, exercise_details in enumerate(exercise_list):
                # Display the current exercise
                st.write(f"{exercise_details['Exercise']} - {exercise_details['Sets']} sets, {exercise_details['Reps']} reps")

    