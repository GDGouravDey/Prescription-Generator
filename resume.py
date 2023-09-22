from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfdoc
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT
# Import our font
registerFont(TTFont('Inconsolata', 'fonts/Inconsolata-Regular.ttf'))
registerFont(TTFont('InconsolataBold', 'fonts/Inconsolata-Bold.ttf'))
registerFontFamily('Inconsolata', normal='Inconsolata', bold='InconsolataBold')

# Set the page height and width
HEIGHT = 11 * inch
WIDTH = 8.5 * inch

# Set our styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Content',
                          fontFamily='Inconsolata',
                          fontSize=12,
                          spaceAfter=.5*inch))
                            


def generate_print_pdf(data, contact):
    pdfname = 'resume.pdf'
    doc = SimpleDocTemplate(
        pdfname,
        pagesize=letter,
        bottomMargin=.5 * inch,
        topMargin=.7 * inch,
        rightMargin=.4 * inch,
        leftMargin=.4 * inch)  # set the doc template
    style = styles["Normal"]  # set the style to normal
    story = []  # create a blank story to tell
    contentTable = Table(
        data,
        colWidths=[
            1.2 * inch,
            6.5 * inch])
    tblStyle = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONT', (0, 0), (-1, -1), 'Inconsolata'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')])
    contentTable.setStyle(tblStyle)
    story.append(contentTable)
    doc.build(
        story,
        onFirstPage=myPageWrapper(
            contact)
        )
    return pdfname


"""
    Draw the framework for the first page,
    pass in contact info as a dictionary
"""
def myPageWrapper(contact):
    # template for static, non-flowables, on the first page
    # draws all of the contact information at the top of the page
    def myPage(canvas, doc):
        canvas.saveState()  # save the current state
        canvas.setFont('InconsolataBold', 16)  # set the font for the name
        canvas.drawString(
            .4 * inch,
            HEIGHT - (.4 * inch),
            contact['name'])  # draw the name on top left page 1
        canvas.line(.4 * inch, HEIGHT - (.47 * inch), 
            WIDTH - (.4 * inch), HEIGHT - (.47 * inch))

        # restore the state to what it was when saved
        canvas.restoreState()
    return myPage

if __name__ == "__main__":
    contact = {
        'name': 'HOSPITAL',}
    data = {
        'pt_name': ' '.join(['PP']),
        'age': ' '.join(['19']),
        'gender': '<br/>'.join(['Male']),
        'mobile number': '<br/>'.join(['9679413821']),
        'visit date': [''.join(['24/12/2023',])],
        'department': [''.join(['Cardiology',])],
        'doctor name':  [''.join(['Dr. Dilip Todi'])],
        'doctor mail':  [''.join(['todi.dilip@gmail.com'])],
        }
    tblData = [
        ['Patient Name:', Paragraph(data['pt_name'], styles['Content'])],
        ['Age:', Paragraph(data['age'], styles['Content'])],
        ['Gender:', Paragraph(data['gender'], styles['Content'])],
        ['Mobile Number:', Paragraph(data['mobile number'], styles['Content'])],
        ['Visit Date:', [Paragraph(x, styles['Content']) for x in data['visit date']]],
        ['Department:', [Paragraph(x, styles['Content']) for x in data['department']]],
        ['Doctor:', [Paragraph(x, styles['Content']) for x in data['doctor name']]],
        ['Doctor Email:', [Paragraph(x, styles['Content']) for x in data['doctor mail']]],
        ]
    
    generate_print_pdf(tblData, contact)
