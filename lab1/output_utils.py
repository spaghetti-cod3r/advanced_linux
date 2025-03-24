from fpdf import FPDF

def save_to_txt(output, filename):
    """Save the output to a text file."""
    with open(filename, 'w') as file:
        file.write(output)

def save_to_pdf(output, filename):
    """Save the output to a PDF file."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, output)
    pdf.output(filename)
