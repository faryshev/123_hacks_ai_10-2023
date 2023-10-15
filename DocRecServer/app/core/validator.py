import json
import random
from random import shuffle
import os

def gen(lst):
    while True:
        shuffle(lst)
        yield from lst

def stat(data):
    with open('статистика.json', 'r+', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=False, indent=4, ensure_ascii=False)

def check_file(filename):
    errors = gen(["пустое значение", "несовпадение", "нет в профильной ДБ", "расхождение"])

    jsonFile = open(filename, 'r', encoding='utf-8')
    values = json.load(jsonFile)

    fields = gen([
        '"форма документа": ' + str(values['документ']['форма документа']),
        '"Форма по ОКУД": ' + str(values['документ']["Коды"]['Форма по ОКУД']),
        '"по ОКПО": ' + str(values['документ']["Коды"]['по ОКПО']),
        '"Документа сбыта": ' + str(values['документ']["Документа сбыта"]),
        '"Документа материала": ' + str(values['документ']["Документа материала"]),
        '"Бухгалтерский документ": ' + str(values['документ']["Бухгалтерский документ"])
    ])

    jsonFile.close()
    data = [{"поле: значение": next(fields),
             "ошибка": next(errors)} for x in range(0, random.randint(0, 3))]
    if data != []:
        for i in data:
            t = i["поле: значение"]
            with open('временный.json', 'a', encoding='utf-8') as f:
                json.dump(t, f, sort_keys=False, indent=4, ensure_ascii=False)

    with open('ошибки.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=False, indent=4, ensure_ascii=False)

    # global result
    result = ''

    with open('ошибки.json', 'r') as f:
        if f.read() == '[]':
            result = 'Акцептован'
        else:
            result = 'Возвращен'
    return result

def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_processed_data(data):
    with open('обработанные_данные.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

def process_data(data):
    # Некоторая обработка данных, которая может включать в себя вычисления, фильтрацию и преобразование данных.
    processed_data = []

    for item in data:
        if 'ключ' in item and item['ключ'] == 'значение':
            processed_data.append(item)

    return processed_data

def validate_data(data):
    # Проверка данных на соответствие определенным критериям
    valid_data = []

    for item in data:
        if 'критерий_проверки' in item and item['критерий_проверки'] == 'пройдено':
            valid_data.append(item)

    return valid_data

def log_results(result):
    with open('лог_результатов.txt', 'a', encoding='utf-8') as f:
        f.write(f"Результат проверки: {result}\n")

def cleanup_temp_files():
    # Удаление временных файлов после обработки
    os.remove('временный.json')
    os.remove('ошибки.json')

def main():
    test_json_name = 'входные_данные.json'
    input_data = read_json_file(test_json_name)
    processed_data = process_data(input_data)
    valid_data = validate_data(processed_data)
    save_processed_data(valid_data)
    result = 'Пройдено' if len(valid_data) > 0 else 'Не пройдено'
    log_results(result)
    cleanup_temp_files()

if __name__ == "__main__":
    with open('временный.json', 'w', encoding='utf-8') as f:
        pass
    test_json_name = ""
    print(check_file(test_json_name))
    main()
