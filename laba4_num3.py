import tomli_w
import pickle

def parse_schedule(filename):
    d, day, lesson = {}, None, None
    with open(filename, encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if s.startswith('day "'):
                day = s[5:-3]
                d[day] = {}
            elif s.startswith('lesson "'):
                lesson = s[8:-3]
                d[day][lesson] = {}
            elif '=' in s and day and lesson:
                k, v = s.split('=', 1)
                d[day][lesson][k.strip()] = v.strip().strip('"')
    return d


try:
    # 1. Чтение и парсинг  в словарь
    with open("schedule.hcl", "r", encoding="utf-8") as f:
        chl_text = f.read()
        schedule_dict = parse_schedule("schedule.hcl")
        print(f'Прочитанный файл (тип данных: {type(schedule_dict)}):\n{schedule_dict}')

    # 2. Сериализиция в байты
    pickled = pickle.dumps(schedule_dict)
    # print(f'Бинарный код: {pickled}')
    # print(f"Размер: {len(pickled)} байт")

    # 3. Десериализация
    restored = pickle.loads(pickled)
    # print(restored)
    # print(f"Десериализованные данные: {restored}")

    # 4. Конвертация с исп tomli_w
    toml_string = tomli_w.dumps(schedule_dict)
    # print("TOML строка:")
    # print(toml_string)
    with open("schedule1.toml", "w", encoding="utf-8") as toml_file:
        toml_file.write(toml_string)
finally:
    None



