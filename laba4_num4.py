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



try:
    with open("schedule.hcl", "r", encoding="utf-8") as f:
        chl_text = f.read()
        schedule_dict = parse_schedule("schedule.hcl")
        print(f'Прочитанный файл (тип данных: {type(schedule_dict)}):\n{schedule_dict}')

    new_dict = str(schedule_dict)
    binary_bits = text_to_bits(new_dict)
    print(f'Бинарный код:\n{binary_bits}')

    restored_tomb_string = text_from_bits(binary_bits)
    schedule_dict = eval(restored_tomb_string)
    print(f'Десериализованные данные (тип данных: {type(schedule_dict)}):\n{schedule_dict}')

    # xml_string = dict_to_xml(schedule_dict)
    # print('Формат xml')
    # print(xml_string)

    xml_content = dict_to_xml(schedule_dict)

    with open("schedule.xml", "w", encoding="utf-8") as xml_file:
        xml_file.write(xml_content)
        
    print('XML файл: schedule.xml')
finally:
    None