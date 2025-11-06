import time
import tomli_w
import pickle
 
start_time = time.time()  # время начала выполнения
 

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


# ОСНОВНОЙ КОД 


counter = 0
while counter < 100:
    counter += 1
    if __name__ == '__main__':
        try:
            # 1. Чтение и парсинг chl в словарь
            with open("schedule.chl", "r", encoding="utf-8") as f:
                chl_text = f.read()
                schedule_dict = parse_schedule("schedule.chl")
                # print(f'Прочитанный файл (тип данных: {type(schedule_dict)}):\n{schedule_dict}')

            # 2. Сериализуем в байты
            pickled = pickle.dumps(schedule_dict)
            # print(f'Бинарный код: {pickled}')
            # print(f"Размер: {len(pickled)} байт")

            # 3. Восстанавливаем
            restored = pickle.loads(pickled)
            # print(restored)
            # print(f"Десериализованные данные: {restored}")

            # 4. Конвертация в формат toml с помощью tomli_w
            toml_string = tomli_w.dumps(schedule_dict)
            # print("TOML строка:")
            # print(toml_string)
        finally:
            None

 
end_time = time.time()  # время окончания выполнения
execution_time = end_time - start_time  # вычисляем время выполнения
 
print(f"Время выполнения программы: {execution_time} секунд")

# Время выполнения программы: 0.06343865394592285 секунд