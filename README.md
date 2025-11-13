## Лабораторная работа 5
### Задание A — JSON ↔ CSV
```python
import json
import csv
from pathlib import Path

def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON-файл в CSV."""
    if Path(json_path).suffix != '.json' or Path(csv_path).suffix != '.csv':
        raise TypeError("Неверное расширение файла")
    
    with open(json_path, encoding="utf-8") as f: 
        data = json.load(f)
    
    if not data or not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    
    # Собираем все уникальные ключи из всех объектов
    fieldnames = sorted({key for item in data for key in item.keys()})
    
    with open(csv_path, "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        # Заполняем отсутствующие поля пустыми строками
        for item in data:
            row = {field: item.get(field, '') for field in fieldnames}
            writer.writerow(row)

def csv_to_json(csv_path: str, json_path: str) -> None:
    """Преобразует CSV в JSON (список словарей)."""
    if Path(csv_path).suffix != '.csv' or Path(json_path).suffix != '.json':
        raise TypeError("Неверное расширение файла")
    
    with open(csv_path, 'r', encoding='utf-8', newline='') as cf:
        reader = csv.DictReader(cf)
        lt_rows = list(reader)
        
    if not lt_rows:
        raise ValueError("CSV файл пуст или содержит только заголовок")
    
    with open(json_path, 'w', encoding='utf-8') as jf:
        json.dump(lt_rows, jf, ensure_ascii=False, indent=2)

json_to_csv('C:/Users/denis/python_labs/data/samples/people.json', 'C:/Users/denis/python_labs/data/out/people_from_json.csv')
csv_to_json('C:/Users/denis/python_labs/data/samples/people.csv', 'C:/Users/denis/python_labs/data/out/people_from_csv.json')

```
![Картинка 1](img\lab5\exA1.png)
![Картинка 1](img\lab5\exA2/png)
![Картинка 1](img\lab5\exA3.png)
![Картинка 1](img\lab5\exA4.png) 

### Задание B — CSV → XLSX

```python
from openpyxl import Workbook
import csv
from pathlib import Path

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """Конвертирует CSV в XLSX."""
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV файл не найден: {csv_path}")
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    
    try:
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            if not rows:
                raise ValueError("CSV файл пуст")
            
            for row in rows:
                ws.append(row)
            
            # Автоширина колонок
            for column in ws.columns:
                if column:  # Проверяем что колонка не пустая
                    mx = max(len(str(cell.value)) for cell in column)
                    ws.column_dimensions[column[0].column_letter].width = max(mx + 2, 8)
        
        wb.save(xlsx_path)
        
    except csv.Error as e:
        raise ValueError(f"Ошибка чтения CSV: {e}")
    
csv_to_xlsx('C:/Users/denis/python_labs/data/samples/cities.csv', 'C:/Users/denis/python_labs/data/out/cities.xlsx')
csv_to_xlsx('C:/Users/denis/python_labs/data/samples/people.csv', 'C:/Users/denis/python_labs/data/out/people.xlsx')    
```
![Картинка 1](img\lab5\exB1.png)
![Картинка 1](img\lab5\exB2.png)