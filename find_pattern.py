import os
import re
import time

PROJECT_FOLDERPATH = r"C:\programming\Vovan"
AUTORESPONDER_FILEPATH = r"C:\programming\Vovan\autoresponder.txt"
RESULT_FILE_FILEPATH = r"C:\programming\Vovan\result_file.txt"


def file_modification(file):   # удаление из файла ::"True", возврат modify_file

    modify_file = []

    try:
        with open(os.path.join(PROJECT_FOLDERPATH, file), 'r', encoding='utf-8') as orig_file:
            for line in orig_file:
                line = line.rstrip()
                if line.endswith('::"true"'):
                    line = line[:-8]
                modify_file.append(line)

    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None

    return modify_file


def file_compiletion(modified_file_list):   # компилируем список с рег. выраж.

    if modified_file_list is None:
        return None

    compiled_regexes = [re.compile(regex) for regex in modified_file_list]
    return compiled_regexes


def search_for_matches(compiled_regexes, modified_file_list):   # поиск совпадения строки с рег.выр.

    if compiled_regexes is None or modified_file_list is None:
        print("Ошибка: Нет компилированных регулярных выражений или измененных строк для поиска.")
        return

    try:
        with open(AUTORESPONDER_FILEPATH, 'r', encoding='utf-8') as autoresponder, \
             open(RESULT_FILE_FILEPATH, 'w', encoding='utf-8') as result_file:

            for string in autoresponder:
                start_time = time.perf_counter()
                string = string.strip()
                if not string:
                    continue
                match_found = False
                for i, compiled_regular in enumerate(compiled_regexes):
                    if compiled_regular.search(string):
                        end_time = time.perf_counter()
                        elapsed_time = (end_time - start_time)*1000
                        result_file.write(f"{string}|{modified_file_list[i]}|{elapsed_time:.6f} мс\n")
                        match_found = True
                        break
                    # else:
                    #     end_time = time.perf_counter()
                    #     elapsed_time = (end_time - start_time)*1000
                if not match_found:
                    result_file.write(f"{string}|'Нет совпадений'|: {elapsed_time:.6f} мс\n")

    except FileNotFoundError:
        print("Один из файлов не найден.")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


if __name__ == "__main__":

    modified_file = file_modification("FromTech_voicemail.txt")

    compiled_regexes = file_compiletion(modified_file)

    search_for_matches(compiled_regexes, modified_file)

