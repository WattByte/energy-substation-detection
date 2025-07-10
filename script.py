import requests
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

# Report document to build PDF file
document = []
document.append(Image('logo.jpeg', 1.1*inch,1.1*inch))

title_style = ParagraphStyle(
    name='Title',
    fontFamily='Helvetica',
    fontSize=36
)

paragraph_style = ParagraphStyle(
    name='Paragraph',
    fontFamily='Helvetica',
    fontSize=15
)

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
    document.append(Spacer(1,20))
    document.append(Paragraph(title, title_style))
    document.append(Spacer(1,50))

def add_paragraph(paragraph):
    document.append(Spacer(1,15))
    document.append(Paragraph(paragraph, paragraph_style))
    document.append(Spacer(1,30))


def get_aeso_api():
    # For those in Alberta
    

def get_ercot_api():
    # For those in Texas


def run_program():
    north = input("Enter north-bound coordinate:")
    east = input("Enter east-bound coordinate:")
    south = input("Enter south-bound coordinate:")
    west = input("Enter west-bound coordinate:")
    provider = input("Is the provider AESO or ERCOT:").upper()

    if (provider not in ["AESO", "ERCOT"]):
        print("❌ Provider must be AESO or ERCOT")
        return

    substations = fetch_substations(north, east, south, west)

    for item in substations:
        tags = item.get("tags")
        name = tags.get("name")

        if name:
            add_title(name)
            add_paragraph('''
            
            ''')

    SimpleDocTemplate('report.pdf', pagesize=letter, rightMargin=12, leftMargin=12, topMargin=12, bottomMargin=6).build(document)

if __name__ == "__main__":
    run_program()