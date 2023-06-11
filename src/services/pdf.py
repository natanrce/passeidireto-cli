import pdfkit

from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader

class PdfService:
  def merge_pdf_and_save(self, pdf_buffer, output_name):
    """Merge all pages into a single PDF file
    """
    result_pdf = PdfFileWriter()
    
    for buffer in pdf_buffer:
      pdf_content = PdfFileReader(stream=buffer)

      for page in range(pdf_content.getNumPages()):
        result_pdf.addPage(pdf_content.getPage(page))

    result_pdf.write(output_name)

  def get_single_file_buffer(self, html_content):
    """Get single PDF page
    """
    options = {
      'encoding': 'utf-8',
      'enable-local-file-access': True,
      'page-size': 'A4',
      'minimum-font-size': '48'
    }

    pdf_file = pdfkit.from_string(
      html_content, 
      False, 
      options, 
      css='./styles/style.css'
    )
    
    return BytesIO(pdf_file)
  
  def get_all_pages_buffer(self, html_pages):
    """Get all pdf pages in array
    """
    return list(map(self.get_single_file_buffer, html_pages))
  