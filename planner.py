from datetime import timedelta

def generate_plan(subjects, study_hours, exam_date):
    subject_list = [s.strip() for s in subjects.split(",") if s.strip()]

    if len(subject_list) == 0:
        return "Please enter at least one subject."

    hours_per_subject = round(study_hours / len(subject_list), 1)

    plan = f"📅 Daily Study Plan (Until {exam_date})\n\n"

    for subject in subject_list:
        plan += f"📖 {subject} → {hours_per_subject} hours\n"

    plan += "\n✅ Remember to take a 10–15 minute break after every hour."

    return plan