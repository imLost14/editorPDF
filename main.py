import PyPDF2
import os
from pynput import keyboard


def merge_pdfs(pdfs_to_merge, output_file): #dos parametros, la union de los pdfs y el resultado de la union
    merger = PyPDF2.PdfFileMerger()

    #Agregar los pdsfs al merge en el orden deseado
    for pdf_file in pdfs_to_merge:
        merger.append(pdf_file)

        #guardar el pdf resultante en el archivo de salida
        with open(output_file, 'wb') as output:
            merger.write(output)

        print(f'los PDFs se han unido correctamente {output_file}')


def main():
    pdf_files = []
    print("Ingrese las rutas de los archivos pdf que desea unir (Ctrl + T para finalizar):")

    while True:
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('t'):
            break

        user_input = input("Ruta del archivo PDF: ")
        pdf_files.append(user_input)


    if pdf_files:
        output_file = input("Ingrese el nombre del archivo de salida para los PDFs unidos: ")
        merge_pdfs(pdf_files, output_file)

    else:
        print("No se ha proporcionado archivos para unir")


if __name__ == "__main__":
    main()   