import time
 
start_time = time.time()
 
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


def dict_to_xml(data):
    def escape(text):
        return text.replace('&', '&amp;').replace('<', '<').replace('>', '>')

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<schedule>')

    for day, lessons in data.items():
        xml.append(f'  <day name="{escape(day)}">')
        for slot, info in lessons.items():
            xml.append(f'    <lesson slot="{escape(slot)}">')
            for key, value in info.items():
                xml.append(f'      <{key}>{escape(str(value))}</{key}>')
            xml.append('    </lesson>')
        xml.append('  </day>')

    xml.append('</schedule>')
    return '\n'.join(xml)

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
            
            toml_string = dict_to_xml(schedule_dict)
            # print('Формат xml')
            # print(toml_string)
        finally:
            None
 
end_time = time.time() 
execution_time = end_time - start_time 
 
print(f"Время выполнения программы: {execution_time} секунд")


# Время выполнения программы: 0.07166457176208496 секунд
