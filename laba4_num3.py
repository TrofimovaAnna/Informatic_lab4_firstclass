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


# основной код

if __name__ == '__main__':
    try:
        # 1.чтение и парсинг HCL в словарь
        with open("schedule.chl", "r", encoding="utf-8") as f:
            chl_text = f.read()
            schedule_dict = parse_schedule("schedule.chl")
            print(f'Прочитанный файл (тип данных: {type(schedule_dict)}):\n{schedule_dict}')

        # 2.сериализуем в байты
        pickled = pickle.dumps(schedule_dict)
        # print(f'Бинарный код: {pickled}')
        # print(f"Размер: {len(pickled)} байт")

        # 3.восстанавливаем
        restored = pickle.loads(pickled)
        # print(restored)
        # print(f"Десериализованные данные: {restored}")

        # 4.конвертация в формат toml с помощью tomli_w
        toml_string = tomli_w.dumps(schedule_dict)
        print("TOML строка:")
        print(toml_string)
    finally:
        None





