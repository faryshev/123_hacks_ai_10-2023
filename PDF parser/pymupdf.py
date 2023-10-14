import fitz  # Это PyMuPDF

# Укажите путь к вашему PDF-файлу
pdf_file_path = "example.pdf"


# Открываем PDF-файл
pdf_document = fitz.open(pdf_file_path)

# Проходим по каждой странице PDF и извлекаем текст
for page_number in range(len(pdf_document)):
    page = pdf_document[page_number]
    page_text = page.get_text()

    # Выводим текст текущей страницы
    print(f"Страница {page_number + 1}:\n")
    print(page_text)

# Закрываем PDF-документ
pdf_document.close()