from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

def create_compact_pdf(output_path):
    # Create the document
    doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Create header data
    header_data = [
        ['', 'Mobile No: 9923181856', '', ''],
        ['', '/', '', ''],
        ['', '', '', '']
    ]
    
    # Create table data for 70 rows
    table_data = []
    
    # Add the numbered rows 1-70
    for i in range(1, 71):
        table_data.append([str(i), '', '', ''])
    
    # Combine all data
    all_data = header_data + table_data
    
    # Create the table
    table = Table(all_data, colWidths=[0.5*inch, 3*inch, 1.5*inch, 1.5*inch])
    
    # Apply table styles
    table_style = [
        # Header styles
        ('SPAN', (1, 0), (3, 0)),  # Span mobile number across columns
        ('ALIGN', (1, 0), (3, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 2), 10),
        
        # Grid for the main table
        ('GRID', (0, 3), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 3), (-1, -1), 8),  # Smaller font for compact layout
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 3), (0, -1), 'CENTER'),  # Center align the row numbers
        
        # Reduce row height by using smaller font and tight spacing
        ('ROWBACKGROUNDS', (0, 3), (-1, -1), [colors.white, colors.lightgrey]),
        ('FONTNAME', (0, 3), (-1, -1), 'Helvetica'),
    ]
    
    table.setStyle(TableStyle(table_style))
    
    # Build the PDF
    elements = [table]
    doc.build(elements)
    
    print(f"Compact PDF created successfully at: {output_path}")

def main():
    input_path = r"C:\Users\awati\Downloads\compact_adityalist.pdf"
    output_path = r"C:\Users\awati\Downloads\compact_adityalist_modified.pdf"
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return
    
    try:
        create_compact_pdf(output_path)
        print(f"\nOriginal PDF: {input_path}")
        print(f"Modified PDF: {output_path}")
        print("\nThe new PDF contains all 70 rows on a single page with compact formatting.")
        
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")

if __name__ == "__main__":
    main()