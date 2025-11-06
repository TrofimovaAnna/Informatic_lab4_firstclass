def text_to_bits(text):
    bits = bin(int.from_bytes(text.encode('utf-8', errors='surrogatepass'), 'big'))[2:]
    len_bytes = (len(bits) + 7) // 8
    return bits.zfill(8 * len_bytes)

def text_from_bits(bits):
    if not bits:
        return ''
    int_bytes = int(bits, 2)
    byte_length = (len(bits) + 7) // 8
    return int_bytes.to_bytes(byte_length, 'big').decode('utf-8', errors='surrogatepass')

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


# десериализация dict в toml  
def dict_toml(schedule_dict):
    lines = []
    for day_name, lessons in schedule_dict.items():
        for lesson_id, attrs in lessons.items():
            lines.append(f"[{day_name}.{lesson_id}]")
            for key, value in attrs.items():
                safe_value = str(value).replace('"', '\\"')
                lines.append(f'{key} = "{safe_value}"')
            lines.append("")
    if lines and lines[-1] == "":
        del lines[-1]
    return "\n".join(lines)


# Основной код
try:
    # 1.Чтение и парсинг hcl в словарь
    with open("schedule.hcl", "r", encoding="utf-8") as f:
        chl_text = f.read()
        schedule_dict = parse_schedule("schedule.hcl")
        print(f'Прочитанный файл (тип данных: {type(schedule_dict)}):\n{schedule_dict}')

    # 2.Сериализация - перевод в бинарный код
    new_dict = str(schedule_dict)
    binary_bits = text_to_bits(new_dict)
    print(f'Бинарный код:\n{binary_bits}')

    # 3.Десериализация - восстановление бинарного коде в словарь
    restored_tomb_string = text_from_bits(binary_bits)
    schedule_dict = eval(restored_tomb_string)
    print(f'Десериализованные данные (тип данных: {type(schedule_dict)}):\n{schedule_dict}')

    # 4.Конвертация в toml
    toml_string = dict_toml(schedule_dict)
    # print(toml_string)

    with open("schedule.toml", "w", encoding="utf-8") as f:
        f.write(toml_string)
finally:
    None



