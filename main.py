from fpdf import FPDF

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
    def header(self):
        # Header with personal information
        self.set_font(*FONT_HEADER)
        self.cell(0, SPACING_LARGE, personal_info['name'], new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font(*FONT_DETAILS)
        self.cell(0, SPACING_MEDIUM, personal_info['contact_details'], new_x="LMARGIN", new_y="NEXT", align='C')
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

        # Set up the right content
        right_content = f"{experience['position']} | {experience['dates']}"

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
        self.cell(0, SPACING_SMALL + 3, right_content, align='R', new_x="LMARGIN", new_y="NEXT")

        # Add the position
        self.set_font(*FONT_POSITION)
        self.cell(0, SPACING_SMALL + 3, f"{experience['position']}", new_x="LMARGIN", new_y="NEXT")

        # Add details as bullet points
        self.ln(1)
        for detail in experience['details']:
            self.add_bullet_point(detail)
        self.ln(SPACING_MEDIUM)

    def add_education(self, education):
        # Add education details
        self.set_font(*FONT_SUBHEADER)
        self.cell(0, SPACING_SMALL + 3, f"{education['institution']} | {education['date']}", new_x="LMARGIN", new_y="NEXT")
        self.set_font(*FONT_TEXT)
        self.multi_cell(0, SPACING_SMALL + 3, education['description'])
        self.ln(SPACING_MEDIUM)

    def add_skills_and_other(self, skills):
        # Add skills and additional details
        self.set_font(*FONT_TEXT)
        self.multi_cell(0, SPACING_SMALL + 3, skills)
        self.ln(SPACING_MEDIUM)


# Data variables
personal_info = {
    "name": "First Last",
    "contact_details": "Bay Area, California | +1-234-456-789 | professionalemail@resumeworded.com | linkedin.com/in/username"
}

summary = "Big Data Engineer with twelve years of experience designing and executing solutions for complex business problems. Migrated local infrastructures to AWS, using [Skill 1] and [Skill 2]."

experiences = [
    {
        "company": "Resume Worded",
        "location": "New York, NY",
        "position": "Quality Engineer",
        "dates": "Jun 2020 - Present",
        "details": [
            "Attained 25% growth in revenue and customers over the last two years by analyzing business needs, collaborating with stakeholders, and designing a new data warehouse.",
            "Led 10 data extraction, warehousing, and analytics initiatives that reduced operating costs by 20% and created customized programming options.",
            "Designed and developed a Big Data analytics platform for processing customer viewing preferences and social media comments using Java, Hive, and Hadoop.",
            "Integrated Hadoop into traditional ETL, accelerating the extraction, transformation, and loading of structured and unstructured data."
        ]
    },
    {
        "company": "Growthsi",
        "location": "New York, NY",
        "position": "Quality Engineer",
        "dates": "Jan 2016 - May 2020",
        "details": [
            "Worked closely with 15 teams across the company to identify and solve business challenges utilizing large structured and unstructured data in a distributed processing environment.",
            "Developed a new pricing strategy that boosted margins by 4 percent.",
            "Automated ETL processes across millions of rows of data which reduced manual workload by 25% monthly."
        ]
    },
    {
        "company": "Third Company",
        "location": "San Diego, CA",
        "position": "Business Analyst",
        "dates": "May 2008 - Dec 2014",
        "details": [
            "Built basic ETL that ingested transactional and event data from a web app with 5,000 daily active users that saved over $40,000 annually in external vendor costs.",
            "Utilized Spark in Python to distribute data processing on large streaming datasets to improve ingestion and processing of that data by 65%.",
            "Worked with clients to understand business needs and convert those needs into actionable reports in Tableau saving 10 hours of manual work each week."
        ]
    }
]

education = {
    "institution": "Resume Worded University, San Francisco, CA",
    "date": "May 2008",
    "description": "B.S. in Business Management, Minor in Data Analytics\n- Awards: Resume Worded Teaching Fellow (only 5 awarded to class), Dean's List 2012 (Top 10%)\n- Completed one-year study abroad with Singapore University"
}

skills = """Skills: Modeling and Design, Data Analytics, Big Data Processing, Amazon Web Services, Statistical Modeling, Hive, Hadoop, ETL, Java
Volunteering: Volunteer 20 hours/month at the AFG foundation, leading pro-bono city projects (3 month tenure)
Projects: Built forecasting using parameters, trend lines, and reference lines which saved 30 hours/week"""

# Generate PDF
pdf = PDF()
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
