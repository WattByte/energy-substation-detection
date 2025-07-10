import requests
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from emoji import emojize

report_header_style = ParagraphStyle(
    name="Report Header",
    fontName='Helvetica-Bold',
    fontSize=50,
    alignment=TA_CENTER

)

title_style = ParagraphStyle(
    name='Title',
    fontName='Helvetica',
    fontSize=23
)

paragraph_style = ParagraphStyle(
    name='Paragraph',
    fontName='Symbola',
    fontSize=13
)

# Document needed to build PDF file + basic setup
document = []
document.append(Image('images/logo.jpeg', 1.1*inch,1.1*inch))
document.append(Paragraph('Substation Report', report_header_style))
document.append(Spacer(1,45))

# Font being registered (Symbola supports emojis)
font_file = 'fonts/Symbola.ttf'
symbola_font = TTFont('Symbola', font_file)
pdfmetrics.registerFont(symbola_font)

def fetch_substations(north, east, south, west):
    url = "https://overpass-api.de/api/interpreter"
    
    query = f"""
    [out:json][timeout:25];
    (
      node["power"="substation"]({south},{west},{north},{east});
      way["power"="substation"]({south},{west},{north},{east});
      relation["power"="substation"]({south},{west},{north},{east});
    );
    out center;
    """
    
    response = requests.post(url, data=query)
    
    if response.status_code == 200:
        data = response.json()
        return data["elements"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def add_title(title):
    document.append(Paragraph(f'{title}:', title_style))

def add_paragraph(paragraph):
    document.append(Paragraph(paragraph, paragraph_style))

def get_aeso_api():
    # Placeholder
    return

def get_ercot_api():
    # Placeholder
    return

def get_lat_lon(substation):
    if 'center' in substation:
        return substation['center']['lat'], substation['center']['lon']
    elif 'lat' in substation and 'lon' in substation:
        return substation['lat'], substation['lon']
    else:
        return "Unknown", "Unknown"

def run_program():
    north = input("Enter north-bound coordinate: ")
    east = input("Enter east-bound coordinate: ")
    south = input("Enter south-bound coordinate: ")
    west = input("Enter west-bound coordinate: ")
    provider = input("Is the provider AESO or ERCOT: ").upper()

    if provider not in ["AESO", "ERCOT"]:
        print("❌ Provider must be AESO or ERCOT")
        return

    substations = fetch_substations(north, east, south, west)

    for substation in substations:
        tags = substation.get('tags', {})
        name = tags.get('name')
        
        # Only process substations with a name (identifable)
        if (name):
            lat, lon = get_lat_lon(substation)
            voltage = tags.get('voltage', 'Unknown')

            document.append(Spacer(1, 35))
            add_title(name)
            document.append(Spacer(1,20))
            add_paragraph(f'''
                {emojize(f':round_pushpin: Location (latitude, longitude): {lat}, {lon}')}
                <br />
                <br />
                {emojize(f':high_voltage: Voltage: {voltage}')} 
            ''')

    # Build the PDF for viewing
    SimpleDocTemplate(
        'report.pdf',
        pagesize=letter,
        rightMargin=12, leftMargin=12,
        topMargin=12, bottomMargin=6
    ).build(document)

if __name__ == "__main__":
    run_program()
