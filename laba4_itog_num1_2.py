# --- Функции для бинарного преобразования строки ---
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    if not bits:
        return ''
    n = int(bits, 2)
    byte_length = (len(bits) + 7) // 8
    return n.to_bytes(byte_length, 'big').decode(encoding, errors)

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



# --- десериализация dict → .toml строка ---
def dict_to_toml(schedule_dict):
    lines = []
    for day_name, lessons in schedule_dict.items():
        lines.append(f"[day.{day_name}]")
        lines.append("")
        for lesson_id, attrs in lessons.items():
            lines.append(f"[day.{day_name}.lesson.{lesson_id}]")
            for key, value in attrs.items():
                safe_value = str(value).replace('"', '\\"')
                lines.append(f'{key} = "{safe_value}"')
            lines.append("")
    if lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


# === ОСНОВНОЙ КОД ===

if __name__ == '__main__':
    try:
        # 1. Чтение и парсинг .chl → словарь
        with open("schedule.chl", "r", encoding="utf-8") as f:
            chl_text = f.read()
            schedule_dict = parse_schedule("schedule.chl")
            print(f'Прочитанный файл (тип данных: {type(schedule_dict)}):\n{schedule_dict}')

        # 2. Сериализация (перевод в бинарный код)
        new_dict = str(schedule_dict)
        binary_bits = text_to_bits(new_dict)
        print(f'Бинарный код:\n{binary_bits}')

        # 3. Десериализация (восстановление бинарного коде в словарь)
        restored_tomb_string = text_from_bits(binary_bits)
        schedule_dict = eval(restored_tomb_string)
        print(f'Десериализованные данные (тип данных: {type(schedule_dict)}):\n{schedule_dict}')

        # 4. Конвертация в формат toml
        toml_string = dict_to_toml(schedule_dict)
        print(toml_string)
    finally:
        None



