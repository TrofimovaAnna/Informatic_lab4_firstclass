import time
 
start_time = time.time()
 
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



# десериализация dict - toml строка
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


# основной код

counter = 0
while counter < 100:
    counter += 1
    if __name__ == '__main__':
        try:
            with open("schedule.chl", "r", encoding="utf-8") as f:
                chl_text = f.read()
                schedule_dict = parse_schedule("schedule.chl")
            
            new_dict = str(schedule_dict)
            binary_bits = text_to_bits(new_dict)
            
            restored_tomb_string = text_from_bits(binary_bits)
            schedule_dict = eval(restored_tomb_string)
            
            toml_string = dict_to_toml(schedule_dict)
        finally:
            None
 
end_time = time.time() 
execution_time = end_time - start_time  
 
print(f"Время выполнения программы: {execution_time} секунд")

# Время выполнения программы: 0.09927725791931152 секунд

