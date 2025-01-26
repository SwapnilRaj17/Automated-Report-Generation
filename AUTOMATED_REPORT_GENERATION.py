import csv
from fpdf import FPDF
import os

def read_data(file_path):
    """
    Reads data from a CSV file and returns it as a list of dictionaries.
    """
    data = []
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    return data

def analyze_data(data):
    """
    Analyzes the data and returns basic statistics.
    """
    analysis = {}
    if not data:
        return analysis

    # Assume data contains numeric values for analysis
    numeric_columns = {key: [] for key in data[0].keys() if data[0][key].replace('.', '', 1).isdigit()}

    for row in data:
        for key in numeric_columns.keys():
            try:
                numeric_columns[key].append(float(row[key]))
            except ValueError:
                pass

    for key, values in numeric_columns.items():
        if values:
            analysis[key] = {
                'count': len(values),
                'sum': sum(values),
                'mean': sum(values) / len(values),
                'max': max(values),
                'min': min(values)
            }
    return analysis

def generate_pdf_report(data, analysis, output_path):
    """
    Generates a formatted PDF report using FPDF.
    """
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Data Analysis Report', border=False, ln=True, align='C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', align='C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # Add raw data to the PDF
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Raw Data:', ln=True)
    pdf.set_font('Arial', '', 12)

    if data:
        for row in data[:5]:  # Display first 5 rows
            row_data = ', '.join([f"{key}: {value}" for key, value in row.items()])
            pdf.cell(0, 10, row_data, ln=True)
    else:
        pdf.cell(0, 10, 'No data available.', ln=True)

    pdf.ln(10)
    # Add analysis to the PDF
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Data Analysis:', ln=True)
    pdf.set_font('Arial', '', 12)

    if analysis:
        for key, stats in analysis.items():
            pdf.cell(0, 10, f"{key}:", ln=True)
            for stat_key, stat_value in stats.items():
                pdf.cell(0, 10, f"  {stat_key}: {stat_value}", ln=True)
    else:
        pdf.cell(0, 10, 'No analysis available.', ln=True)

    pdf.output(output_path)

if __name__ == "__main__":
    # File paths
    input_file = 'data.csv'  # Replace with your CSV file path
    output_file = 'report.pdf'

    # Read data
    data = read_data(input_file)

    # Analyze data
    analysis = analyze_data(data)

    # Generate PDF report
    generate_pdf_report(data, analysis, output_file)

    if os.path.exists(output_file):
        print(f"Report generated successfully: {output_file}")
    else:
        print("Failed to generate the report.")
