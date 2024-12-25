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
        try:
            self.set_font(*FONT_HEADER)
            self.cell(0, SPACING_LARGE, self.personal_info['name'], new_x="LMARGIN", new_y="NEXT", align='C')
            self.set_font(*FONT_DETAILS)
            self.cell(0, SPACING_MEDIUM, self.personal_info['contact_details'], new_x="LMARGIN", new_y="NEXT", align='C')
            self.ln(SPACING_MEDIUM)
        except Exception as e:
            print(f"Error in header: {e}")

    def draw_line(self):
        try:
            self.set_line_width(LINE_WIDTH)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(SPACING_SMALL)
        except Exception as e:
            print(f"Error in draw_line: {e}")

    def add_section_title(self, title):
        try:
            self.set_font(*FONT_SUBHEADER)
            self.cell(0, SPACING_MEDIUM, title, new_x="LMARGIN", new_y="NEXT")
            self.draw_line()
        except Exception as e:
            print(f"Error in add_section_title: {e}")

    def add_bullet_point(self, text):
        try:
            self.set_font(*FONT_TEXT)
            self.cell(INDENT, SPACING_SMALL + 3, ' -')
            self.multi_cell(0, SPACING_SMALL + 3, text, new_x="LMARGIN", new_y="NEXT")
        except Exception as e:
            print(f"Error in add_bullet_point: {e}")

    def add_experience(self, experience):
        try:
            self.set_font(*FONT_SUBHEADER)
            company_width = self.get_string_width(experience['company'] + ", ")
            self.cell(company_width, SPACING_SMALL + 3, experience['company'] + ",", border=0)

            self.set_font(*FONT_TEXT)
            location_width = self.get_string_width(experience['location'])
            self.cell(location_width, SPACING_SMALL + 3, experience['location'], border=0)

            self.cell(0, SPACING_SMALL + 3, experience['dates'], align='R', new_x="LMARGIN", new_y="NEXT")

            self.set_font(*FONT_POSITION)
            self.cell(0, SPACING_SMALL + 3, f"{experience['position']}", new_x="LMARGIN", new_y="NEXT")

            self.ln(1)
            for detail in experience['details']:
                self.add_bullet_point(detail)
            self.ln(SPACING_MEDIUM)
        except Exception as e:
            print(f"Error in add_experience: {e}")

    def add_education(self, educations):
        try:
            for education in educations:
                self.set_font(*FONT_SUBHEADER)
                institute_width = self.get_string_width(education['institution'] + ", ")
                self.cell(institute_width, SPACING_SMALL + 3, education['institution'] + ",", border=0)

                self.set_font(*FONT_TEXT)
                location_width = self.get_string_width(education['location'])
                self.cell(location_width, SPACING_SMALL + 3, education['location'], border=0)

                self.cell(0, SPACING_SMALL + 3, education['date'], align='R', new_x="LMARGIN", new_y="NEXT")
                self.multi_cell(0, SPACING_SMALL + 3, education['description'])
                self.ln(SPACING_MEDIUM)
        except Exception as e:
            print(f"Error in add_education: {e}")

    def add_skills_and_other(self, skills):
        try:
            self.set_font(*FONT_TEXT)
            self.multi_cell(0, SPACING_SMALL + 3, skills)
            self.ln(SPACING_MEDIUM)
        except Exception as e:
            print(f"Error in add_skills_and_other: {e}")


def read_data(file_path):
    try:
        with open(file_path, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            lines = list(reader)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return {}, "", [], [], ""
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return {}, "", [], [], ""

    personal_info = {}
    summary = ""
    experiences = []
    education = []
    skills = ""
    current_experience = None
    current_education = None

    try:
        for line in lines:
            if len(line) < 2:
                continue

            section, details = line[0].strip().lower(), line[1].strip().strip('"')

            if section == "name":
                personal_info["name"] = details
            elif section in {"contact", "phone", "email", "linkedin"}:
                if "contact_details" not in personal_info:
                    personal_info["contact_details"] = ""
                personal_info["contact_details"] += f"{details} | "
            elif section == "summary":
                summary = details
            elif section == "educational institute":
                if current_education:
                    education.append(current_education)
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
                    experiences.append(current_experience)
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
                current_experience["details"].append(details)

        if current_education:
            education.append(current_education)
        if current_experience:
            experiences.append(current_experience)

        personal_info["contact_details"] = personal_info.get("contact_details", "").rstrip(" | ")
    except Exception as e:
        print(f"Error processing CSV data: {e}")

    return personal_info, summary, experiences, education, skills


def main():
    try:
        file_path = "resume_data.csv"
        personal_info, summary, experiences, education, skills = read_data(file_path)

        if not personal_info:
            print("No data to generate the PDF.")
            return

        pdf = PDF()
        pdf.personal_info = personal_info
        pdf.add_page()

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

        output_path = "professional_resume.pdf"
        pdf.output(output_path)
        print(f"PDF generated successfully: {output_path}")
    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()
