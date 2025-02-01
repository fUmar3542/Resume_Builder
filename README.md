# ATS Resume Generator

## Overview
This script generates an ATS (Applicant Tracking System) friendly resume from a CSV file using the `fpdf` library in Python. The generated resume is structured with clearly defined sections, including personal information, a summary, work experience, education, and skills.

## Features
- Parses resume data from a CSV file
- Formats the resume using predefined fonts and styles
- Generates a professional PDF resume
- Includes error handling for missing or incorrect data

## Prerequisites
- Python 3.x
- Required library: `fpdf`

Install `fpdf` using:
```sh
pip install fpdf
```

## CSV Format
The script reads data from a CSV file (`resume_data.csv`). The expected format is:

| Section | Details |
|---------|---------|
| Name | John Doe |
| Contact | johndoe@example.com |
| Phone | +1 234 567 890 |
| LinkedIn | linkedin.com/in/johndoe |
| Summary | Experienced software developer... |
| Company | ABC Corp |
| Location | New York, NY |
| Position | Software Engineer |
| Date | Jan 2020 - Present |
| Details | Developed scalable applications |
| Educational Institute | XYZ University |
| Edu. Location | California |
| Edu. Date | 2018 |
| Edu. Description | Bachelor's in Computer Science |
| Skills | Python, Java, SQL, Machine Learning |

## How to Use
1. Prepare the `resume_data.csv` file following the format above.
2. Run the script:
   ```sh
   python script.py
   ```
3. The resume will be saved as `professional_resume.pdf`.

## Error Handling
- If the CSV file is missing or incorrectly formatted, an error message will be displayed.
- Missing sections will be skipped, but the script will continue execution.

## Output
The script generates a professional PDF resume with the following sections (if provided):
- **Header:** Name and contact details
- **Summary**
- **Professional Experience**
- **Education**
- **Skills & Other**

## License
This script is open-source and can be modified as needed.

