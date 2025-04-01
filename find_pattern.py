import sys
import re
import time

FROMTECH_FILEPATH = r"C:\programming\Vovan\FromTech_voicemail.txt"
AUTORESPONDER_FILEPATH = r"C:\programming\Vovan\autoresponder.txt"
RESULT_FILE_FILEPATH = r"C:\programming\Vovan\result_file.txt"


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000
        print(f"Время выполнения функции '{func.__name__}': {elapsed_time:.4f} мс")
        return result

    return wrapper


def read_files(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:

            file_list = []
            for string in file:
                string = string.strip()
                file_list.append(string)

            return file_list
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        sys.exit()


def delete_end_strings_in_list(file_list):  # удаление из файла ::"True", возврат modify_file

    without_str_ends_fromtech_list = []
    for row in file_list:
        if row.endswith('::"true"'):
            row = row[:-8]
            without_str_ends_fromtech_list.append(row)
    return without_str_ends_fromtech_list


def compile_regexes(string_list):  # Компилируем список с регулярными выражениями

    if not string_list:
        return None

    compiled_regexes = [re.compile(regex) for regex in string_list]
    return compiled_regexes


@timer
def search_for_matches(compiled_regexes_list, string, without_str_ends_fromtech_list):  # Поиск совпадений
    start_time = time.perf_counter()
    result = None

    for i, compiled_regular in enumerate(compiled_regexes_list):
        if compiled_regular.search(string):
            end_time = time.perf_counter()
            elapsed_time = (end_time - start_time) * 1000
            result = f"{string}|{without_str_ends_fromtech_list[i]}|{elapsed_time:.6f} мс\n"
            break

    if result is None:
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000
        result = f"{string}|'Нет совпадений'| {elapsed_time:.6f} мс\n"

    return result


def search_function(autoresponder_list, compiled_regexes_list,
                    without_str_ends_fromtech_list):  # поиск совпадения строки с рег.выр.

    result_list = []

    if compiled_regexes_list is None or without_str_ends_fromtech_list is None:
        print("Ошибка: Нет компилированных регулярных выражений или измененных строк для поиска")
        return

    for string in autoresponder_list:
        if not string:
            continue

        result_string = search_for_matches(compiled_regexes_list, string, without_str_ends_fromtech_list)
        result_list.append(result_string)

    return result_list


def wright_file(string_list):  # Запись результатов в файл
    try:
        with open(RESULT_FILE_FILEPATH, 'w', encoding='utf-8') as file:
            for row in string_list:
                file.write(row)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit()


def main_function():

    fromtech_list = read_files(FROMTECH_FILEPATH)

    autoresponder_list = read_files(AUTORESPONDER_FILEPATH)

    without_str_ends_fromtech_list = delete_end_strings_in_list(fromtech_list)

    compiled_regexes_list = compile_regexes(without_str_ends_fromtech_list)

    result_list = search_function(autoresponder_list, compiled_regexes_list, without_str_ends_fromtech_list)

    wright_file(result_list)


if __name__ == "__main__":

    main_function()