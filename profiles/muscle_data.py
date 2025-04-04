# profiles/muscle_data.py

EXERCISE_MUSCLE_MAP = {

    "Squat": ["quadriceps", "gluteus_maximus", "hamstrings", "adductors"],
    "Squats": ["quadriceps", "gluteus_maximus", "hamstrings", "adductors"], # Yaygın çoğul kullanımı
    "Çömelme (Squats)": ["quadriceps", "gluteus_maximus", "hamstrings", "adductors"],

    "Bench Press": ["pectorals_major", "deltoids_anterior", "triceps_brachii"],
    "Göğüs Pres (Bench Press)": ["pectorals_major", "deltoids_anterior", "triceps_brachii"],

    "Deadlift": ["hamstrings", "gluteus_maximus", "erector_spinae", "quadriceps", "trapezius", "forearms"],
    "Ölü Ağır Kaldırma (Deadlift)": ["hamstrings", "gluteus_maximus", "erector_spinae", "quadriceps", "trapezius", "forearms"],

    "Pull-up": ["latissimus_dorsi", "biceps_brachii", "trapezius", "rhomboids", "forearms"],
    "Pull-ups": ["latissimus_dorsi", "biceps_brachii", "trapezius", "rhomboids", "forearms"],
    "Barfiks (Pull-ups)": ["latissimus_dorsi", "biceps_brachii", "trapezius", "rhomboids", "forearms"],
    "Lat Pulldown": ["latissimus_dorsi", "biceps_brachii", "trapezius", "rhomboids"], # Barfiks alternatifi

    "Overhead Press": ["deltoids_anterior", "deltoids_lateral", "triceps_brachii", "trapezius_upper"],
    "Omuz Pres (Overhead Press)": ["deltoids_anterior", "deltoids_lateral", "triceps_brachii", "trapezius_upper"],
    "Dumbbell Shoulder Press": ["deltoids_anterior", "deltoids_lateral", "triceps_brachii", "trapezius_upper"],

    "Barbell Row": ["latissimus_dorsi", "trapezius", "rhomboids", "biceps_brachii", "deltoids_posterior"],
    "Dumbbell Row": ["latissimus_dorsi", "trapezius", "rhomboids", "biceps_brachii", "deltoids_posterior"],

    "Bicep Curl": ["biceps_brachii", "brachialis"],
    "Bicep Curls": ["biceps_brachii", "brachialis"],
    "Hammer Curl": ["biceps_brachii", "brachialis", "brachioradialis"], # Hammer curl biraz daha farklı kasları da vurur
    "Hammer Curls": ["biceps_brachii", "brachialis", "brachioradialis"],

    "Triceps Extension": ["triceps_brachii"],
    "Triceps Extensions": ["triceps_brachii"],
    "Overhead Triceps Extension": ["triceps_brachii"],
    "Triceps Pushdown": ["triceps_brachii"],
    "Close-Grip Bench Press": ["triceps_brachii", "pectorals_major", "deltoids_anterior"], # Triceps odaklı bench

    "Lunge": ["quadriceps", "gluteus_maximus", "hamstrings", "adductors"],
    "Lunges": ["quadriceps", "gluteus_maximus", "hamstrings", "adductors"],

    "Leg Press": ["quadriceps", "gluteus_maximus", "hamstrings", "adductors"],
    "Romanian Deadlift": ["hamstrings", "gluteus_maximus", "erector_spinae"],
    "Hamstring Curl": ["hamstrings"],
    "Leg Curl": ["hamstrings"],
    "Calf Raise": ["gastrocnemius", "soleus"], # Baldır kasları
    "Calf Raises": ["gastrocnemius", "soleus"],

    "Lateral Raise": ["deltoids_lateral"],
    "Lateral Raises": ["deltoids_lateral"],
    "Dumbbell Flye": ["pectorals_major", "deltoids_anterior"],
    "Dumbbell Flyes": ["pectorals_major", "deltoids_anterior"],

    # --- Buradan İtibaren Daha Fazla Egzersiz Eklenebilir ---
    "Push-up": ["pectorals_major", "deltoids_anterior", "triceps_brachii", "abdominals_core"],
    "Şınav (Push-up)": ["pectorals_major", "deltoids_anterior", "triceps_brachii", "abdominals_core"],
    "Plank": ["abdominals_core", "erector_spinae"], # Core bölgesi
    "Crunch": ["rectus_abdominis"], # Karın kası
    # ...
}


MUSCLE_GROUP_TR = {
    "quadriceps": "Ön Bacak (Kuadriseps)",
    "hamstrings": "Arka Bacak (Hamstring)",
    "gluteus_maximus": "Kalça (Gluteus)",
    "adductors": "İç Bacak (Adduktorler)",
    "calves": "Baldır (Kalf)",
    "gastrocnemius": "Baldır (Gastroknemius)",
    "soleus": "Baldır (Soleus)",
    "pectorals_major": "Göğüs",
    "deltoids_anterior": "Ön Omuz",
    "deltoids_lateral": "Yan Omuz",
    "deltoids_posterior": "Arka Omuz",
    "triceps_brachii": "Arka Kol (Triceps)",
    "biceps_brachii": "Ön Kol (Biceps)",
    "brachialis": "Ön Kol (Brakialis)",
    "brachioradialis": "Ön Kol (Brakioradialis)",
    "forearms": "Ön Kol (Genel)",
    "latissimus_dorsi": "Kanat (Latisimus Dorsi)",
    "trapezius": "Trapez",
    "trapezius_upper": "Üst Trapez",
    "rhomboids": "Sırt (Romboidler)",
    "erector_spinae": "Sırt (Omurga Kasları)",
    "abdominals_core": "Karın & Core Bölgesi",
    "rectus_abdominis": "Karın Kası (Rektus Abdominis)",
    # ... diğer kas grupları eklenebilir ...
}