import time
import tomli_w
import pickle
 
start_time = time.time()  
 

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

counter = 0
while counter < 100:
    counter += 1
    if __name__ == '__main__':
        try:
            # 1. Чтение и парсинг chl в словарь
            with open("schedule.chl", "r", encoding="utf-8") as f:
                chl_text = f.read()
                schedule_dict = parse_schedule("schedule.chl")

            pickled = pickle.dumps(schedule_dict)

            restored = pickle.loads(pickled)

            toml_string = tomli_w.dumps(schedule_dict)
            # print("TOML строка:")
            # print(toml_string)
        finally:
            None

 
end_time = time.time() 
execution_time = end_time - start_time  
 
print(f"Время выполнения программы: {execution_time} секунд")


# Время выполнения программы: 0.06343865394592285 секунд
