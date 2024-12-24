import csv

def parse_csv_experiences(file_path):
    with open(file_path, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        lines = list(reader)

    personal_info = {}
    summary = ""
    experiences = []
    education = []
    skills = ""
    current_experience = None  # Temporary storage for the current experience block
    current_education = None  # Temporary storage for the current education block

    for line in lines:
        if len(line) < 2:
            continue  # Skip empty or malformed lines

        section, details = line[0].strip().lower(), line[1].strip().strip('"')

        if section == "name":
            personal_info["name"] = details
        elif section in {"contact", "phone", "email", "linkedin"}:
            if "contact_details" not in personal_info:
                personal_info["contact_details"] = ""
            personal_info["contact_details"] += f"{details} | "
        elif section == "summary":
            summary = details
        elif section == "institution":
            if current_education:
                education.append(current_education)  # Save the previous education block
            current_education = {
                "institution": details,
                "location": "",
                "date": "",
                "description": ""
            }
        elif section == "location" and current_education:
            current_education["location"] = details
        elif section == "date" and current_education:
            current_education["date"] = details
        elif section == "description" and current_education:
            current_education["description"] += details
        elif section == "skills":
            skills = details
        elif section == "company":
            if current_experience:
                experiences.append(current_experience)  # Save the previous experience block
            current_experience = {
                "company": details,
                "location": "",
                "position": "",
                "date": "",
                "details": []
            }
        elif section == "location" and current_experience:
            current_experience["location"] = details
        elif section == "position" and current_experience:
            current_experience["position"] = details
        elif section == "date" and current_experience:
            current_experience["dates"] = details
        elif section == "details" and current_experience:
            current_experience["details"].append(details)
        elif section == "" and current_experience and details:
            # Handle continuation lines for details
            current_experience["details"].append(details)

    # Append the last education and experience blocks
    if current_education:
        education.append(current_education)
    if current_experience:
        experiences.append(current_experience)

    # Final cleanup
    personal_info["contact_details"] = personal_info.get("contact_details", "").rstrip(" | ")

    return personal_info, summary, experiences, education, skills


def main():
    # Replace with your CSV file path
    file_path = "resume_data.csv"

    personal_info, summary, experiences, education, skills = parse_csv_experiences(file_path)

    # Display parsed results
    print("Personal Info:", personal_info)
    print("Summary:", summary)
    print("Experiences:", experiences)
    print("Education:", education)
    print("Skills:", skills)

if __name__ == "__main__":
    main()
