from fpdf import FPDF
import csv

# Formatting variables
FONT_HEADER = ('Helvetica', 'B', 14)
FONT_SUBHEADER = ('Helvetica', 'B', 12)
FONT_POSITION = ('Helvetica', 'B', 10)
FONT_TEXT = ('Helvetica', '', 10)
FONT_DETAILS = ('Helvetica', '', 10)
SPACING_SMALL = 2
SPACING_MEDIUM = 5
SPACING_LARGE = 8
INDENT = 8
LINE_WIDTH = 0.3


class PDF(FPDF):
    personal_info = {"name": "", "contact_details": ""}

    def header(self):
        # Header with personal information
        self.set_font(*FONT_HEADER)
        self.cell(0, SPACING_LARGE, self.personal_info['name'], new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font(*FONT_DETAILS)
        self.cell(0, SPACING_MEDIUM, self.personal_info['contact_details'], new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(SPACING_MEDIUM)
        # self.draw_line()

    def draw_line(self):
        # Draw horizontal line
        self.set_line_width(LINE_WIDTH)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(SPACING_SMALL)

    def add_section_title(self, title):
        # Format section titles
        self.set_font(*FONT_SUBHEADER)
        self.cell(0, SPACING_MEDIUM, title, new_x="LMARGIN", new_y="NEXT")
        self.draw_line()

    def add_bullet_point(self, text):
        # Format bullet points
        self.set_font(*FONT_TEXT)
        # Add some indentation for the bullet point (icon)
        self.cell(INDENT, SPACING_SMALL + 3, ' -')  # Bullet point with additional indentation
        # Add the text, ensuring it's properly wrapped and aligned without extra indentation
        self.multi_cell(0, SPACING_SMALL + 3, text, new_x="LMARGIN", new_y="NEXT")

    # def add_experience(self, experience):
    #     # Add professional experience
    #     self.set_font(*FONT_SUBHEADER)
    #     self.cell(0, SPACING_SMALL + 3, f"{experience['company']}, {experience['location']}", new_x="LMARGIN", new_y="NEXT")
    #     self.set_font(*FONT_TEXT)
    #     self.cell(0, SPACING_SMALL + 3, f"{experience['position']} | {experience['dates']}", new_x="LMARGIN", new_y="NEXT")
    #     self.ln(SPACING_SMALL)
    #     for detail in experience['details']:
    #         self.add_bullet_point(detail)
    #     self.ln(SPACING_MEDIUM)

    def add_experience(self, experience):
        # Add professional experience
        self.set_font(*FONT_SUBHEADER)

        # Get the dynamic width of the company name
        company_width = self.get_string_width(experience['company'] + ", ")

        # Add the left content (Company, Location)
        self.cell(company_width, SPACING_SMALL + 3, experience['company'] + ",", border=0)

        # Set the font for the location and add it after the company, dynamically
        self.set_font(*FONT_TEXT)
        location_width = self.get_string_width(experience['location'])  # Measure the width of the location
        self.cell(location_width, SPACING_SMALL + 3, experience['location'], border=0)

        # Add the right content (Position, Dates), aligned to the right
        self.set_font(*FONT_TEXT)
        self.cell(0, SPACING_SMALL + 3, experience['dates'], align='R', new_x="LMARGIN", new_y="NEXT")

        # Add the position
        self.set_font(*FONT_POSITION)
        self.cell(0, SPACING_SMALL + 3, f"{experience['position']}", new_x="LMARGIN", new_y="NEXT")

        # Add details as bullet points
        self.ln(1)
        for detail in experience['details']:
            self.add_bullet_point(detail)
        self.ln(SPACING_MEDIUM)

    def add_education(self, educations):
        for education in educations:
            # Add education details
            self.set_font(*FONT_SUBHEADER)

            # Get the dynamic width of the company name
            institute_width = self.get_string_width(education['institution'] + ", ")
            # Add the left content (Company, Location)
            self.cell(institute_width, SPACING_SMALL + 3, education['institution'] + ",", border=0)

            # Set the font for the location and add it after the company, dynamically
            self.set_font(*FONT_TEXT)
            location_width = self.get_string_width(education['location'])  # Measure the width of the location
            self.cell(location_width, SPACING_SMALL + 3, education['location'], border=0)

            # Add the right content (Position, Dates), aligned to the right
            self.set_font(*FONT_TEXT)
            self.cell(0, SPACING_SMALL + 3, education['date'], align='R', new_x="LMARGIN", new_y="NEXT")

            self.set_font(*FONT_TEXT)
            self.multi_cell(0, SPACING_SMALL + 3, education['description'])
            self.ln(SPACING_MEDIUM)

    def add_skills_and_other(self, skills):
        # Add skills and additional details
        self.set_font(*FONT_TEXT)
        self.multi_cell(0, SPACING_SMALL + 3, skills)
        self.ln(SPACING_MEDIUM)


def read_data(file_path):
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
        elif section == "edu. location" and current_education:
            current_education["location"] = details
        elif section == "edu. date" and current_education:
            current_education["date"] = details
        elif section == "edu. description" and current_education:
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
                "dates": "",
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
    # Example usage
    file_path = "resume_data.csv"  # Replace with your CSV file path
    personal_info, summary, experiences, education, skills = read_data(file_path)

    # Generate PDF
    pdf = PDF()
    pdf.personal_info = personal_info
    pdf.add_page()

    # Add content to PDF
    pdf.add_section_title("SUMMARY")
    pdf.set_font(*FONT_TEXT)
    pdf.multi_cell(0, SPACING_SMALL + 3, summary)
    pdf.ln(SPACING_MEDIUM)

    pdf.add_section_title("PROFESSIONAL EXPERIENCE")
    for exp in experiences:
        pdf.add_experience(exp)

    pdf.add_section_title("EDUCATION")
    pdf.add_education(education)

    pdf.add_section_title("SKILLS & OTHER")
    pdf.add_skills_and_other(skills)

    # Save PDF
    output_path = "professional_resume.pdf"
    pdf.output(output_path)


if __name__ == "__main__":
    main()
