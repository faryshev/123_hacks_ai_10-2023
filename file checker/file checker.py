import re
import json

# Ваш текст
text =  open("example.txt", "r")

# Определите регулярные выражения для извлечения данных
document_form_pattern = r'Типовая межотраслевая форма № (\S+)'
document_number_pattern = r'ТРЕБОВАНИЕ-НАКЛАДНАЯ №\s+(\d+)'
code_okud_pattern = r'Форма по ОКУД\n(\d+)'
code_okpo_pattern = r'по ОКПО\n(\d+)'
code_3_pattern = r'структурное\nподразделение\n(\d+)'
document_organization_pattern = r'Организация\n(.+)'
document_department_pattern = r'подразделение\n(.+)'
date_pattern = r'Дата\nсоста-\nвления\n(\d+\.\d+\.\d+)'
operation_code_pattern = r'Код вида\nоперации\n(\d+)'
sender_subtable_pattern = r'Отправитель\n(.*?)\n-\n(.*?)'
recipient_subtable_pattern = r'Получатель\n(.*?)\n-\n(.*?)'
account_pattern = r'Корреспондирующий счет\n(\d+)'
analytical_accounting_code_pattern = r'код аналити-\nческого учета\n(.+)'
accounting_unit_pattern = r'Учетная\nединица\nвыпуска\nпродукции\n\(работ,\nуслуг\)\n(.+)'
through_pattern = r'Через кого ПД (.+)'
requestee_pattern = r'Затребовал (.+)'
corresponding_account_pattern = r'(\d+)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)'
released_position_pattern = r'Отпустил\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)'
received_position_pattern = r'Получил\n-\n(.*?)\n-\n(.*?)\n-\n(.*?)'
sales_document_pattern = r'Документа сбыта: (\d+)'
material_document_pattern = r'Документа материала: (\d+)'
accounting_document_pattern = r'Бухгалтерский документ: (\d+)'

# Функция для извлечения значения с проверкой наличия совпадений
def extract_with_check(pattern, text, index=1):
    match = re.search(pattern, text)
    return match.group(index) if match else None

# Извлекаем данные с проверкой наличия совпадений
document_form = extract_with_check(document_form_pattern, text)
document_number = extract_with_check(document_number_pattern, text)
code_okud = extract_with_check(code_okud_pattern, text)
code_okpo = extract_with_check(code_okpo_pattern, text)
code_3 = extract_with_check(code_3_pattern, text)
document_organization = extract_with_check(document_organization_pattern, text)
document_department = extract_with_check(document_department_pattern, text)
date = extract_with_check(date_pattern, text)
operation_code = extract_with_check(operation_code_pattern, text)

sender_subtable_match = re.search(sender_subtable_pattern, text, re.DOTALL)
recipient_subtable_match = re.search(recipient_subtable_pattern, text, re.DOTALL)

sender_department = extract_with_check(sender_subtable_pattern, text, 1)
sender_service_number = extract_with_check(sender_subtable_pattern, text, 2)
recipient_department = extract_with_check(recipient_subtable_pattern, text, 1)
recipient_service_number = extract_with_check(recipient_subtable_pattern, text, 2)
account = extract_with_check(account_pattern, text)
analytical_accounting_code = extract_with_check(analytical_accounting_code_pattern, text)
accounting_unit = extract_with_check(accounting_unit_pattern, text)
through = extract_with_check(through_pattern, text)
requestee = extract_with_check(requestee_pattern, text)

# Извлечение данных для таблицы накладной
invoice_table_match = re.search(corresponding_account_pattern, text, re.DOTALL)
corresponding_account = {
    "corresponding_account": extract_with_check(corresponding_account_pattern, text, 1),
    "material_value_number": extract_with_check(corresponding_account_pattern, text, 2),
    "material_value_service_number": extract_with_check(corresponding_account_pattern, text, 3),
    "characteristic": extract_with_check(corresponding_account_pattern, text, 4),
    "serial_number": extract_with_check(corresponding_account_pattern, text, 5),
    "service_number": extract_with_check(corresponding_account_pattern, text, 6),
    "network_number": extract_with_check(corresponding_account_pattern, text, 7),
    "measurement_units_code": extract_with_check(corresponding_account_pattern, text, 8),
    "measurement_units_name": extract_with_check(corresponding_account_pattern, text, 9),
    "quantity_requested": extract_with_check(corresponding_account_pattern, text, 10),
    "quantity_given": extract_with_check(corresponding_account_pattern, text, 11),
    "price": extract_with_check(corresponding_account_pattern, text, 12),
    "price_except_NAT": extract_with_check(corresponding_account_pattern, text, 13),
    "warehouse_number": extract_with_check(corresponding_account_pattern, text, 14),
    "location": extract_with_check(corresponding_account_pattern, text, 15),
    "traced_product_registration_number": extract_with_check(corresponding_account_pattern, text, 16),
}

# Извлечение данных для таблицы "Отпустил"
released_table_match = re.search(released_position_pattern, text, re.DOTALL)
released_position = {
    "position": extract_with_check(released_position_pattern, text, 1),
    "signature": extract_with_check(released_position_pattern, text, 2),
    "signature_description": extract_with_check(released_position_pattern, text, 3),
}

# Извлечение данных для таблицы "Получил"
received_table_match = re.search(received_position_pattern, text, re.DOTALL)
received_position = {
    "position": extract_with_check(received_position_pattern, text, 1),
    "signature": extract_with_check(received_position_pattern, text, 2),
    "signature_description": extract_with_check(received_position_pattern, text, 3),
}

sales_document = extract_with_check(sales_document_pattern, text)
material_document = extract_with_check(material_document_pattern, text)
accounting_document = extract_with_check(accounting_document_pattern, text)

data = {
    "document": {
        "document_form": document_form,
        "document_number": document_number,
        "document_codes": {
            "code_OKUD": code_okud,
            "code_OKPO": code_okpo,
            "code_3": code_3
        },
        "document_organization": document_organization,
        "document_department": document_department,
        "shipping_table": {
            "date": date,
            "operation_code": operation_code,
            "sender_subtable": {
                "department": sender_department,
                "service_number": sender_service_number
            },
            "recipient_subtable": {
                "department": recipient_department,
                "service_number": recipient_service_number
            },
            "account": account,
            "analytical_accounting_code": analytical_accounting_code,
            "accounting_unit": accounting_unit
        },
        "through": through,
        "requestee": requestee,
        "invoice_table": corresponding_account,
        "released": released_position,
        "received": received_position,
        "sales_document": sales_document,
        "material_document": material_document,
        "accounting_document": accounting_document
    }
}

json_data = json.dumps(data, ensure_ascii=False, indent=4)

print(json_data)