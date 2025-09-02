import os

import PyPDF2


def merge_pdfs(pdfs_to_merge, output_file):
    merger = PyPDF2.PdfMerger()

    for pdf_file in pdfs_to_merge:
        merger.append(pdf_file)

    with open(output_file, "wb") as output:
        merger.write(output)

    print(f"Los PDFs se han unido correctamente en {output_file}")


def dividir(pdf_path):
    try:
        pdf_path = os.path.abspath(pdf_path)
        # Crear carpeta para las páginas divididas
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_folder = f"{base_name}_paginas"
        os.makedirs(output_folder, exist_ok=True)

        # Abrir el PDF
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            for i in range(num_pages):
                writer = PyPDF2.PdfWriter()
                writer.add_page(reader.pages[i])

                output_path = os.path.join(output_folder, f"pagina_{i+1}.pdf")
                with open(output_path, "wb") as output_pdf:
                    writer.write(output_pdf)

        print(f"Se han dividido las páginas en la carpeta: {output_folder}")
    except FileNotFoundError:
        print(
            f"Error: No se encontró el archivo PDF en la ruta especificada: {pdf_path}"
        )
    except Exception as e:
        print(f"Error al dividir el PDF: {e}")


def redimensionar(pdf_path):
    try:
        pdf_path = os.path.abspath(pdf_path)
        # Pedir al usuario las nuevas dimensiones en pulgadas
        new_width_in = float(
            input("Ingrese el nuevo ancho para redimensionar (en pulgadas): ")
        )
        new_height_in = float(
            input("Ingrese el nuevo alto para redimensionar (en pulgadas): ")
        )

        # Convertir pulgadas a puntos (1 pulgada = 72 puntos)
        new_width = new_width_in * 72
        new_height = new_height_in * 72

        # Abrir el PDF
        with open(pdf_path, "rb") as file:
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
            with open(output_path, "wb") as output_pdf:
                writer.write(output_pdf)

        print(f"Se ha redimensionado el PDF y guardado como: {output_path}")
    except FileNotFoundError:
        print(
            f"Error: No se encontró el archivo PDF en la ruta especificada: {pdf_path}"
        )
    except ValueError:
        print(
            "Error: Las dimensiones ingresadas no son válidas. Por favor ingrese números válidos."
        )
    except Exception as e:
        print(f"Error al redimensionar el PDF: {e}")





def agregar_en_posicion(pdf_base, pdf_insertar):
    try:
        # Mantener los archivos abiertos durante toda la operación
        with open(pdf_base, "rb") as file_base, open(pdf_insertar, "rb") as file_insertar:
            reader_base = PyPDF2.PdfReader(file_base)
            reader_insertar = PyPDF2.PdfReader(file_insertar)

            pdf_base_pages = [reader_base.pages[i] for i in range(len(reader_base.pages))]
            pdf_insertar_pages = [reader_insertar.pages[i] for i in range(len(reader_insertar.pages))]

            # Nuevo objeto para crear nuevo pdf
            pdf_nuevo = PyPDF2.PdfWriter()
            posicion_insertar = int(input("Digite la posicion donde quiere insertar: "))

            # Insertamos las paginas bases hasta la posicion deseada
            for i in range(posicion_insertar):
                pdf_nuevo.add_page(pdf_base_pages[i])

            # Insertamos las paginas del pdf que queremos insertar
            for pagina in pdf_insertar_pages:
                pdf_nuevo.add_page(pagina)

            # Continuar anadiendo el resto del pdf base
            for i in range(posicion_insertar, len(pdf_base_pages)):
                pdf_nuevo.add_page(pdf_base_pages[i])

            # Guardamos el pdf
            with open("pdf_combinado.pdf", "wb") as pdf_salida:
                pdf_nuevo.write(pdf_salida)

        print("PDF COMBINADO!")

    except Exception as e:
        print(f"[Error] ocurrio al agregar en posicion: {e}")


def mover_pagina(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            pages = [reader.pages[i] for i in range(num_pages)]

            # Pedir página a mover (1-based)
            pagina_mover = int(input(f"Ingrese el número de la página a mover (1-{num_pages}): ")) - 1
            if pagina_mover < 0 or pagina_mover >= num_pages:
                print("Número de página inválido.")
                return

            # Pedir posición destino (1-based)
            posicion_destino = int(input(f"Ingrese la posición destino (1-{num_pages}): ")) - 1
            if posicion_destino < 0 or posicion_destino >= num_pages:
                print("Posición destino inválida.")
                return

            # Extraer la página
            pagina = pages.pop(pagina_mover)

            # Insertar en la nueva posición
            pages.insert(posicion_destino, pagina)

            # Crear nuevo PDF
            writer = PyPDF2.PdfWriter()
            for page in pages:
                writer.add_page(page)

            # Guardar sobreescribiendo el archivo original
            with open(pdf_path, "wb") as output_pdf:
                writer.write(output_pdf)

            print(f"Se ha movido la página en el PDF: {pdf_path}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo PDF en la ruta especificada: {pdf_path}")
    except ValueError:
        print("Error: Ingrese números válidos para la página y posición.")
    except Exception as e:
        print(f"Error al mover la página: {e}")


def main():
    print("Seleccione la operación que desea realizar:")
    print("1. Unir PDFs")
    print("2. Dividir PDF por páginas")
    print("3. Redimensionar PDF")
    print("4. agregar PDF a otro")
    print("5. Mover página dentro de un PDF")
    opcion = input("Ingrese el número de la opción: ")

    if opcion == "1":
        pdf_files = []
        print(
            "Ingrese las rutas de los archivos PDF que desea unir (Presione Enter para finalizar):"
        )

        while True:
            user_input = input("Ruta del archivo PDF: ")

            if not user_input:  # Si no se proporciona una ruta, finalizar
                break

            pdf_files.append(user_input)

        if pdf_files:
            output_file = input(
                "Ingrese el nombre del archivo de salida para los PDFs unidos: "
            )
            merge_pdfs(pdf_files, output_file)
        else:
            print("No se han proporcionado archivos PDF para unir.")
    elif opcion == "2":
        pdf_path = input("Ingrese la ruta del PDF a dividir: ")
        dividir(pdf_path)
    elif opcion == "3":
        pdf_path = input("Ingrese la ruta del PDF a redimensionar: ")
        redimensionar(pdf_path)
    elif opcion == "4":
        pdf_base = input("Digite la ruta absoluta del pdf: \n")
        pdf_insertar = input("Digite la ruta absoluta del pdf: \n")
        agregar_en_posicion(pdf_base, pdf_insertar)
    elif opcion == "5":
        pdf_path = input("Ingrese la ruta del PDF: ")
        mover_pagina(pdf_path)
    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()
