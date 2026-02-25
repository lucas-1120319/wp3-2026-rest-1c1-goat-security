import json
import random
from datetime import date, timedelta

random.seed(42)

# -----------------------
# Base Data
# -----------------------

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

# -----------------------
# Helpers
# -----------------------

def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def make_taxonomy_block(base_kennen, base_kunnen):
    result = []

    for i, level in enumerate(taxonomy_scale):
        kennen = clamp(base_kennen + random.uniform(-0.15, 0.15) - 0.05 * i)
        kunnen = clamp(base_kunnen + random.uniform(-0.15, 0.15) - 0.07 * i)
        confidence = clamp(0.5 + random.uniform(-0.2, 0.2))

        result.append(
            {
                "level": level,
                "kennen": round(kennen, 2),
                "kunnen": round(kunnen, 2),
                "confidence": round(confidence, 2),
            }
        )

    return result

# -----------------------
# Source Pool
# -----------------------

def create_source_pool(n=100):
    types = ["quiz", "test", "observatie", "project"]
    base_date = date(2025, 9, 1)
    pool = []

    for i in range(n):
        source_type = random.choice(types)
        day_offset = random.randint(0, 120)
        d = base_date + timedelta(days=day_offset)

        # Guaranteed unique ID
        source_id = f"{source_type[:2].upper()}-{i+1}"

        pool.append({
            "at": d.isoformat(),
            "source": {
                "type": source_type,
                "id": source_id
            }
        })

    return pool


SOURCE_POOL = create_source_pool(100)

# -----------------------
# Snapshot Generator
# -----------------------

def make_subject_snapshots():
    # Each student per subject gets 10–20 unique sources
    n = random.randint(5, 10)
    chosen_sources = random.sample(SOURCE_POOL, n)

    snapshots = []

    for src in chosen_sources:
        base_kennen = random.uniform(0.3, 0.9)
        base_kunnen = random.uniform(0.2, 0.8)

        snapshots.append(
            {
                "at": src["at"],
                "source": src["source"],
                "taxonomy": make_taxonomy_block(base_kennen, base_kunnen),
            }
        )

    return snapshots

# -----------------------
# Main
# -----------------------

def main():
    data = []

    for student_id, student_name in students:
        subjects_data = []

        for subject_id, subject_name in subjects:
            subjects_data.append({
                "subject": {
                    "id": subject_id,
                    "name": subject_name
                },
                "taxonomyScale": taxonomy_scale,
                "snapshots": make_subject_snapshots(),
            })

        data.append({
            "student": {
                "id": student_id,
                "name": student_name
            },
            "subjects": subjects_data
        })

    with open("data/test/data-sample.json", "w", encoding="utf-8") as f:
        json.dump({"students": data}, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()