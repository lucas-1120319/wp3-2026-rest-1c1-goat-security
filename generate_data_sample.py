import json
import random
from datetime import date, timedelta

random.seed(42)

# -----------------------------
# Configuration / Constants
# -----------------------------
students = [
    (1, "Sam"), (2, "Alex"), (3, "Jamie"), (4, "Taylor"), (5, "Robin"),
    (6, "Noah"), (7, "Emma"), (8, "Milan"), (9, "Lotte"), (10, "Daan"),
]

subjects = [
    (12, "Biologie"),
    (21, "Natuurkunde"),
    (22, "Scheikunde"),
    (31, "Wiskunde"),
]

taxonomy_scale = ["Onthouden", "Begrijpen", "Toepassen", "Analyseren"]

# Learning goals per subject
subject_learning_goals = {
    12: [
        {"id": "LG-B-1", "title": "Fotosynthese uitleggen", "keywords": ["chlorofyl", "glucose", "CO2", "zuurstof"]},
        {"id": "LG-B-2", "title": "Cellen en organellen herkennen", "keywords": ["celkern", "mitochondriën", "celmembraan"]},
        {"id": "LG-B-3", "title": "DNA en erfelijkheid beschrijven", "keywords": ["DNA", "gen", "chromosoom", "erfelijkheid"]},
        {"id": "LG-B-4", "title": "Ecosystemen analyseren", "keywords": ["ecosysteem", "voedselketen", "producent", "consument"]},
    ],
    21: [
        {"id": "LG-N-1", "title": "Beweging en snelheid beschrijven", "keywords": ["snelheid", "versnelling", "kracht"]},
        {"id": "LG-N-2", "title": "Energie en behoud verklaren", "keywords": ["energie", "arbeid", "behoud"]},
        {"id": "LG-N-3", "title": "Elektrische circuits analyseren", "keywords": ["stroom", "spanning", "weerstand"]},
        {"id": "LG-N-4", "title": "Golven en geluid begrijpen", "keywords": ["frequentie", "amplitude", "trilling"]},
    ],
    22: [
        {"id": "LG-S-1", "title": "Atomaire structuur uitleggen", "keywords": ["atoom", "elektron", "proton", "neutron"]},
        {"id": "LG-S-2", "title": "Chemische bindingen herkennen", "keywords": ["ionbinding", "covalent", "metaalbinding"]},
        {"id": "LG-S-3", "title": "Reacties en reactiemechanismen", "keywords": ["oxidatie", "reductie", "reactiesnelheid"]},
        {"id": "LG-S-4", "title": "Zuren en basen classificeren", "keywords": ["pH", "zuur", "base", "neutralisatie"]},
    ],
    31: [
        {"id": "LG-W-1", "title": "Algebraïsche vergelijkingen oplossen", "keywords": ["x", "vergelijking", "variabele"]},
        {"id": "LG-W-2", "title": "Functies en grafieken interpreteren", "keywords": ["functie", "grafiek", "asymptoot"]},
        {"id": "LG-W-3", "title": "Meetkunde: eigenschappen en bewijs", "keywords": ["hoek", "driehoek", "bewijs"]},
        {"id": "LG-W-4", "title": "Statistiek en kansberekening", "keywords": ["gemiddelde", "mediaan", "kans"]},
    ],
}

# -----------------------------
# Utility Functions
# -----------------------------
def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def make_taxonomy_block(base_kennen, base_kunnen):
    result = []
    for i, level in enumerate(taxonomy_scale):
        kennen = clamp(base_kennen + random.uniform(-0.15, 0.15) - 0.05 * i)
        kunnen = clamp(base_kunnen + random.uniform(-0.15, 0.15) - 0.07 * i)
        confidence = clamp(0.5 + random.uniform(-0.2, 0.2))
        result.append({
            "level": level,
            "kennen": round(kennen, 2),
            "kunnen": round(kunnen, 2),
            "confidence": round(confidence, 2)
        })
    return result

# -----------------------------
# Source Pool (MORE DATA)
# -----------------------------
def create_source_pool(n=500):
    types = ["quiz", "test", "observatie", "project"]
    base_date = date(2025, 9, 1)
    pool = []

    for i in range(n):
        source_type = random.choice(types)
        day_offset = random.randint(0, 180)

        d = base_date + timedelta(days=day_offset)
        source_id = f"{source_type[:2].upper()}-{i+1}"

        pool.append({
            "at": d.isoformat(),
            "source": {"type": source_type, "id": source_id}
        })

    return pool

SOURCE_POOL = create_source_pool()

# -----------------------------
# Learning Goal Progression
# -----------------------------
def make_learning_goal_snapshots():
    n = random.randint(5, 10)

    chosen = random.sample(SOURCE_POOL, n)
    chosen = sorted(chosen, key=lambda x: x["at"])

    # Start low, end higher
    start_kennen = random.uniform(0.1, 0.4)
    end_kennen = random.uniform(0.6, 0.95)

    start_kunnen = random.uniform(0.1, 0.3)
    end_kunnen = random.uniform(0.5, 0.9)

    snapshots = []

    for i, src in enumerate(chosen):
        t = i / (n - 1) if n > 1 else 1

        # Non-linear growth curve
        curve = t ** random.uniform(0.7, 1.5)

        kennen = start_kennen + (end_kennen - start_kennen) * curve
        kunnen = start_kunnen + (end_kunnen - start_kunnen) * curve

        # Add randomness (important!)
        kennen += random.uniform(-0.1, 0.1)
        kunnen += random.uniform(-0.1, 0.1)

        snapshots.append({
            "at": src["at"],
            "source": src["source"],
            "taxonomy": make_taxonomy_block(
                clamp(kennen),
                clamp(kunnen)
            )
        })

    return snapshots

# -----------------------------
# Create one student entry
# -----------------------------
def make_student_entry(student_id, student_name):
    subjects_list = []

    for subject_id, subject_name in subjects:
        goals_for_subject = subject_learning_goals[subject_id]
        lg_list = []

        for g in goals_for_subject:
            snapshots_for_lg = make_learning_goal_snapshots()

            lg_list.append({
                "id": g["id"],
                "title": g["title"],
                "keywords": g["keywords"],
                "snapshots": snapshots_for_lg
            })

        subjects_list.append({
            "subject": {"id": subject_id, "name": subject_name},
            "learningGoals": lg_list
        })

    return {
        "student": {"id": student_id, "name": student_name},
        "subjects": subjects_list,
        "taxonomyScale": taxonomy_scale
    }

# -----------------------------
# Main generation
# -----------------------------
def main():
    students_data = []

    for student_id, student_name in students:
        entry = make_student_entry(student_id, student_name)
        students_data.append(entry)

    with open("data/data-sample.json", "w", encoding="utf-8") as f:
        json.dump({"students": students_data}, f, ensure_ascii=False, indent=2)

    print("JSON generation complete: data/data-sample.json")

# -----------------------------
if __name__ == "__main__":
    main()