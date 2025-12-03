import csv
from pathlib import Path
from typing import List, Tuple, Optional


# читаем содержимое текста из файла
def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    try:
        return Path(path).read_text(encoding=encoding)
    except FileNotFoundError:
        return "Файл не найден."
    except UnicodeDecodeError:
        return "Ошибка кодирования файла."


# запись данных в CSV файл
def write_csv(
    rows: list[tuple | list], path: str | Path, header: tuple[str, ...] | None = None
) -> None:
    p = Path(path)
    with p.open(
        "w", newline="", encoding="utf-8"
    ) as file:  # w открывает файл(если он есть) и стирает все или создает его(если нет)
        f = csv.writer(file)
        if header is None and rows == []:  # нет заголовка и данных
            file_c.writerow(("a", "b"))
        if header is not None:
            f.writerow(header)
        if rows != []:
            const = len(rows[0])
            for i in rows:
                if len(i) != const:
                    return ValueError
        f.writerows(rows)


def ensure_parent_dir(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


# использование функций
print(
    read_text(r"C:\Users\denis\python_labs\data\input.txt")
)  # чтение содержимого файла input.txt
write_csv(
    [("word", "count"), ("test", 3)], r"C:\Users\denis\python_labs\data\check.json"
)  # запись в check.csv
