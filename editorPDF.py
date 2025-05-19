import PyPDF2
import os

def merge_pdfs(pdfs_to_merge, output_file):
    merger = PyPDF2.PdfMerger()

    for pdf_file in pdfs_to_merge:
        merger.append(pdf_file)

    with open(output_file, 'wb') as output:
        merger.write(output)

    print(f'Los PDFs se han unido correctamente en {output_file}')

def dividir(pdf_path):
    try:
        pdf_path = os.path.abspath(pdf_path)
        # Crear carpeta para las páginas divididas
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_folder = f"{base_name}_paginas"
        os.makedirs(output_folder, exist_ok=True)

        # Abrir el PDF
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            for i in range(num_pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(reader.pages[i])

                output_path = os.path.join(output_folder, f'pagina_{i+1}.pdf')
                with open(output_path, 'wb') as output_pdf:
                    writer.write(output_pdf)

        print(f'Se han dividido las páginas en la carpeta: {output_folder}')
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo PDF en la ruta especificada: {pdf_path}")
    except Exception as e:
        print(f"Error al dividir el PDF: {e}")

def redimensionar(pdf_path):
    try:
        pdf_path = os.path.abspath(pdf_path)
        # Pedir al usuario las nuevas dimensiones en pulgadas
        new_width_in = float(input("Ingrese el nuevo ancho para redimensionar (en pulgadas): "))
        new_height_in = float(input("Ingrese el nuevo alto para redimensionar (en pulgadas): "))

        # Convertir pulgadas a puntos (1 pulgada = 72 puntos)
        new_width = new_width_in * 72
        new_height = new_height_in * 72

        # Abrir el PDF
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            for page in reader.pages:
                # Obtener tamaño original
                media_box = page.mediabox
                orig_width = float(media_box.width)
                orig_height = float(media_box.height)

                # Calcular factores de escala
                scale_x = new_width / orig_width
                scale_y = new_height / orig_height

                # Aplicar transformación de escala al contenido
                page.scale(scale_x, scale_y)

                # Ajustar el tamaño de la página
                page.mediabox.upper_right = (new_width, new_height)

                writer.add_page(page)

            # Guardar el PDF redimensionado
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_path = f"{base_name}_redimensionado.pdf"
            with open(output_path, 'wb') as output_pdf:
                writer.write(output_pdf)

        print(f'Se ha redimensionado el PDF y guardado como: {output_path}')
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo PDF en la ruta especificada: {pdf_path}")
    except ValueError:
        print("Error: Las dimensiones ingresadas no son válidas. Por favor ingrese números válidos.")
    except Exception as e:
        print(f"Error al redimensionar el PDF: {e}")

def main():
    print("Seleccione la operación que desea realizar:")
    print("1. Unir PDFs")
    print("2. Dividir PDF por páginas")
    print("3. Redimensionar PDF")
    opcion = input("Ingrese el número de la opción: ")

    if opcion == '1':
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
    elif opcion == '2':
        pdf_path = input("Ingrese la ruta del PDF a dividir: ")
        dividir(pdf_path)
    elif opcion == '3':
        pdf_path = input("Ingrese la ruta del PDF a redimensionar: ")
        redimensionar(pdf_path)
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()
