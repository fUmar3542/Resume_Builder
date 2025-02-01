from fpdf import FPDF
import csv

# Formatting variables for different font styles and spacing
FONT_HEADER = ('Helvetica', 'B', 14)  # Header font style (Bold, size 14)
FONT_SUBHEADER = ('Helvetica', 'B', 12)  # Subheader font style (Bold, size 12)
FONT_POSITION = ('Helvetica', 'B', 10)  # Position font style (Bold, size 10)
FONT_TEXT = ('Helvetica', '', 10)  # Text font style (Regular, size 10)
FONT_DETAILS = ('Helvetica', '', 10)  # Details font style (Regular, size 10)
SPACING_SMALL = 2  # Small spacing between elements
SPACING_MEDIUM = 5  # Medium spacing between elements
SPACING_LARGE = 8  # Large spacing between elements
INDENT = 8  # Indentation for bullet points
LINE_WIDTH = 0.3  # Line width for drawing lines

# PDF class inheriting from FPDF to create a custom resume layout
class PDF(FPDF):
    personal_info = {"name": "", "contact_details": ""}  # Personal information (name and contact details)

    # Header of the PDF, including the name and contact details
    def header(self):
        try:
            self.set_font(*FONT_HEADER)  # Set font for the header
            self.cell(0, SPACING_LARGE, self.personal_info['name'], new_x="LMARGIN", new_y="NEXT", align='C')  # Name centered
            self.set_font(*FONT_DETAILS)  # Set font for contact details
            self.cell(0, SPACING_MEDIUM, self.personal_info['contact_details'], new_x="LMARGIN", new_y="NEXT", align='C')  # Contact details centered
            self.ln(SPACING_MEDIUM)  # Add a line break after the header
        except Exception as e:
            print(f"Error in header: {e}")  # Catch and print any header-related errors

    # Draws a horizontal line on the PDF
    def draw_line(self):
        try:
            self.set_line_width(LINE_WIDTH)  # Set the line width
            self.line(10, self.get_y(), 200, self.get_y())  # Draw a line at the current y-position
            self.ln(SPACING_SMALL)  # Add a small line break after the line
        except Exception as e:
            print(f"Error in draw_line: {e}")  # Catch and print any line drawing errors

    # Adds a section title to the PDF
    def add_section_title(self, title):
        try:
            self.set_font(*FONT_SUBHEADER)  # Set font for the section title
            self.cell(0, SPACING_MEDIUM, title, new_x="LMARGIN", new_y="NEXT")  # Print the title
            self.draw_line()  # Draw a line under the section title
        except Exception as e:
            print(f"Error in add_section_title: {e}")  # Catch and print any section title-related errors

    # Adds a bullet point with text to the PDF
    def add_bullet_point(self, text):
        try:
            self.set_font(*FONT_TEXT)  # Set font for the text
            self.cell(INDENT, SPACING_SMALL + 3, ' -')  # Indent and add a bullet point
            self.multi_cell(0, SPACING_SMALL + 3, text, new_x="LMARGIN", new_y="NEXT")  # Print the text
        except Exception as e:
            print(f"Error in add_bullet_point: {e}")  # Catch and print any bullet point-related errors

    # Adds professional experience details to the PDF
    def add_experience(self, experience):
        try:
            self.set_font(*FONT_SUBHEADER)  # Set font for the company and position
            company_width = self.get_string_width(experience['company'] + ", ")  # Calculate width for the company name
            self.cell(company_width, SPACING_SMALL + 3, experience['company'] + ",", border=0)  # Print company name

            self.set_font(*FONT_TEXT)  # Set font for the location
            location_width = self.get_string_width(experience['location'])  # Calculate width for the location
            self.cell(location_width, SPACING_SMALL + 3, experience['location'], border=0)  # Print location

            self.cell(0, SPACING_SMALL + 3, experience['dates'], align='R', new_x="LMARGIN", new_y="NEXT")  # Print the dates on the right side

            self.set_font(*FONT_POSITION)  # Set font for the position
            self.cell(0, SPACING_SMALL + 3, f"{experience['position']}", new_x="LMARGIN", new_y="NEXT")  # Print the position

            self.ln(1)  # Add a small line break
            for detail in experience['details']:
                self.add_bullet_point(detail)  # Add each bullet point under experience details
            self.ln(SPACING_MEDIUM)  # Add medium spacing after experience
        except Exception as e:
            print(f"Error in add_experience: {e}")  # Catch and print any experience-related errors

    # Adds education details to the PDF
    def add_education(self, educations):
        try:
            for education in educations:
                self.set_font(*FONT_SUBHEADER)  # Set font for the institution name
                institute_width = self.get_string_width(education['institution'] + ", ")  # Calculate width for institution name
                self.cell(institute_width, SPACING_SMALL + 3, education['institution'] + ",", border=0)  # Print institution name

                self.set_font(*FONT_TEXT)  # Set font for the location
                location_width = self.get_string_width(education['location'])  # Calculate width for location
                self.cell(location_width, SPACING_SMALL + 3, education['location'], border=0)  # Print location

                self.cell(0, SPACING_SMALL + 3, education['date'], align='R', new_x="LMARGIN", new_y="NEXT")  # Print the date on the right side
                self.multi_cell(0, SPACING_SMALL + 3, education['description'])  # Print the description of the education
                self.ln(SPACING_MEDIUM)  # Add medium spacing after education details
        except Exception as e:
            print(f"Error in add_education: {e}")  # Catch and print any education-related errors

    # Adds skills and other details to the PDF
    def add_skills_and_other(self, skills):
        try:
            self.set_font(*FONT_TEXT)  # Set font for skills text
            self.multi_cell(0, SPACING_SMALL + 3, skills)  # Print skills
            self.ln(SPACING_MEDIUM)  # Add medium spacing after skills
        except Exception as e:
            print(f"Error in add_skills_and_other: {e}")  # Catch and print any skills-related errors

    # Adds projects details to the PDF (similar to skills)
    def add_projects(self, projects):
        try:
            self.set_font(*FONT_TEXT)  # Set font for projects text
            self.multi_cell(0, SPACING_SMALL + 3, projects)  # Print projects
            self.ln(SPACING_MEDIUM)  # Add medium spacing after projects
        except Exception as e:
            print(f"Error in add_projects: {e}")  # Catch and print any projects-related errors


# Reads the CSV file containing the resume data
def read_data(file_path):
    try:
        with open(file_path, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            lines = list(reader)  # Read the file contents
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return {}, "", [], [], ""  # Return empty data if file not found
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return {}, "", [], [], ""  # Return empty data if any error occurs

    personal_info = {}  # Dictionary for personal info (name, contact details)
    summary = ""  # Summary of the resume
    experiences = []  # List to store work experience
    education = []  # List to store education details
    skills = ""  # Skills section of the resume
    projects = ""  # Projects
    current_experience = None  # Temporary storage for the current experience being read
    current_education = None  # Temporary storage for the current education being read

    # Parse each line of the CSV file and populate the resume data
    try:
        for line in lines:
            if len(line) < 2:  # Skip lines with insufficient data
                continue

            section, details = line[0].strip().lower(), line[1].strip().strip('"')  # Extract section and details

            # Process each section in the CSV file
            if section == "name":
                personal_info["name"] = details
            elif section in {"contact", "phone", "email", "linkedin"}:
                if "contact_details" not in personal_info:
                    personal_info["contact_details"] = ""
                personal_info["contact_details"] += f"{details} | "
            elif section == "summary":
                summary = details
            # Process the "projects" section in the CSV file
            elif section == "projects":
                projects = details  # Assign the projects details to a variable
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

        # Add any remaining data to experiences or education
        if current_education:
            education.append(current_education)
        if current_experience:
            experiences.append(current_experience)

        personal_info["contact_details"] = personal_info.get("contact_details", "").rstrip(" | ")
    except Exception as e:
        print(f"Error processing CSV data: {e}")  # Catch and print any errors while processing CSV data

    return personal_info, summary, experiences, education, skills, projects  # Return the processed data


# Main function to generate the PDF
def main():
    try:
        file_path = "resume_data.csv"  # Path to the CSV file
        personal_info, summary, experiences, education, skills, projects = read_data(file_path)  # Read the data

        if not personal_info:  # Check if data is available
            print("No data to generate the PDF.")
            return

        pdf = PDF()  # Create a PDF object
        pdf.personal_info = personal_info  # Set personal information
        pdf.add_page()  # Add a page to the PDF

        # Add summary if available
        if summary:
            pdf.add_section_title("SUMMARY")
            pdf.set_font(*FONT_TEXT)
            pdf.multi_cell(0, SPACING_SMALL + 3, summary)
            pdf.ln(SPACING_MEDIUM)

        # Add experiences if available
        if experiences:
            pdf.add_section_title("PROFESSIONAL EXPERIENCE")
            for exp in experiences:
                pdf.add_experience(exp)

        # Add education if available
        if education:
            pdf.add_section_title("EDUCATION")
            pdf.add_education(education)

        # Add skills if available
        if skills:
            pdf.add_section_title("SKILLS & OTHER")
            pdf.add_skills_and_other(skills)

        # Add projects if available
        if projects:
            pdf.add_section_title("PROJECTS")
            pdf.add_projects(projects)

        # Output the PDF to a file
        output_path = "professional_resume.pdf"
        pdf.output(output_path)
        print(f"PDF generated successfully: {output_path}")  # Print success message
    except Exception as e:
        print(f"Error in main: {e}")  # Catch and print any errors in the main function


# Entry point for script execution
if __name__ == "__main__":
    main()  # Run the main function
