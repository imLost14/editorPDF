import PyPDF2

def merge_pdfs(pdfs_to_merge, output_file):
    merger = PyPDF2.PdfMerger()

    for pdf_file in pdfs_to_merge:
        merger.append(pdf_file)

    with open(output_file, 'wb') as output:
        merger.write(output)

    print(f'Los PDFs se han unido correctamente en {output_file}')

def main():
    pdf_files = []
    print("Ingrese las rutas de los archivos PDF que desea unir (Presione Enter para finalizar):")

    while True:
        user_input = input("Ruta del archivo PDF: ")
        
        if not user_input:  # Si no se proporciona una ruta, finalizar
            break

        pdf_files.append(user_input)

    if pdf_files:
        output_file = input("Ingrese el nombre del archivo de salida para los PDFs unidos: ")

        merge_pdfs(pdf_files, output_file)
    else:
        print("No se han proporcionado archivos PDF para unir.")

if __name__ == "__main__":
    main()
