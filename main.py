import os
import zipfile
from flask import Flask, render_template_string, send_file
import wikipedia
from fpdf import FPDF

app = Flask(__name__)

@app.route('/')
def index():
    with open('index.html', 'r') as f:
        html = f.read()
    return render_template_string(html)

@app.route('/generate_pdfs')
def generate_pdfs():
    pdfs = []
    for i in range(10):
        try:
            page = wikipedia.page(titles=wikipedia.random())
            content = page.content
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=content)
            filename = f"{i+1}.pdf"
            pdf.output(filename)
            pdfs.append(filename)
        except:
            pass

    zip_filename = "pdfs.zip"
    with zipfile.ZipFile(zip_filename, mode="w") as archive:
        for pdf in pdfs:
            archive.write(pdf)

    for pdf in pdfs:
        os.remove(pdf)

    return send_file(zip_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
