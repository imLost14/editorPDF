import docx
import PyPDF2

def convert_docx_to_pdf(docx_file, pdf_file):
  """
  Convierte un documento Word en PDF.

  Args:
    docx_file: La ruta al archivo Word.
    pdf_file: La ruta al archivo PDF de salida.

  Returns:
    None.
  """

  # Cargamos el documento Word.
  doc = docx.Document(docx_file)

  # Creamos un objeto PDF.
  pdf = PyPDF2.PdfFileWriter()

  # Iteramos sobre las páginas del documento Word.
  for page in doc.pages:
    # Agregamos la página al documento PDF.
    pdf.addPage(page._element)

  # Escribimos el documento PDF.
  with open(pdf_file, "wb") as f:
    pdf.write(f)

  

if __name__ == "__main__":
  # Rutas a los archivos Word y PDF.
  docx_file = input("Ingresa la ruta del archivo word")
  pdf_file = input("ruta del archivo de salida")

  # Convertimos el documento Word en PDF.
  convert_docx_to_pdf(docx_file, pdf_file)