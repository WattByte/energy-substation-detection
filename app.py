from flask import Flask, request, send_file, render_template
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter

from helper.substation_report import (
    fetch_substations,
    get_lat_lon,
    add_title,
    add_paragraph,
    set_pdf_metadata,
    emojize
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')

@app.route("/generate_report", methods=["POST"])
def generate_report():
    # Get data from JSON body
    data = request.get_json()

    north = data.get("north")
    east = data.get("east")
    south = data.get("south")
    west = data.get("west")
    provider = data.get("provider", "").upper()

    if provider not in ["AESO", "ERCOT"]:
        return "❌ Provider must be AESO or ERCOT", 400

    substations = fetch_substations(north, east, south, west)

    document = []

    for substation in substations:
        tags = substation.get('tags', {})
        name = tags.get('name')
        
        if name:
            lat, lon = get_lat_lon(substation)
            voltage = tags.get('voltage', 'Unknown')

            document.append(Spacer(1, 35))
            add_title(name, document)
            document.append(Spacer(1, 20))
            add_paragraph(f'''
                {emojize(f':round_pushpin: Location (latitude, longitude): {lat}, {lon}')}
                <br />
                <br />
                {emojize(f':high_voltage: Voltage: {voltage}')} 
            ''', document)

    # Write PDF to a buffer (in-memory)
    buffer = BytesIO()
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=12, leftMargin=12,
        topMargin=12, bottomMargin=6
    )
    pdf.build(document, onFirstPage=set_pdf_metadata, onLaterPages=set_pdf_metadata)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="report.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True)
