import sys, argparse

sys.path.append(r"C:\Users\denis\python_labs\src\lib")
sys.path.append(r"C:\Users\denis\python_labs\src\lab6")
from csv_xlsx import (
    csv_to_xlsx,
)
from json_csv import (
    json_to_csv,
    csv_to_json,
)
from cli_text import (
    check_file,
)


def cli_convert():
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    sub = parser.add_subparsers(
        dest="cmd",
        required=True,
    )

    p1 = sub.add_parser("json2csv")
    p1.add_argument(
        "--in",
        dest="input",
        required=True,
        help="Входной JSON файл",
    )
    p1.add_argument(
        "--out",
        dest="output",
        required=True,
        help="Выходной CSV файл",
    )

    p2 = sub.add_parser("csv2json")
    p2.add_argument(
        "--in",
        dest="input",
        required=True,
        help="Входной CSV файл",
    )
    p2.add_argument(
        "--out",
        dest="output",
        required=True,
        help="Выходной JSON файл",
    )

    p3 = sub.add_parser("csv2xlsx")
    p3.add_argument(
        "--in",
        dest="input",
        required=True,
        help="Входной CSV файл",
    )
    p3.add_argument(
        "--out",
        dest="output",
        required=True,
        help="Выходной XLSX файл",
    )

    args = parser.parse_args()

    try:
        if args.cmd == "json2csv":
            if not check_file(args.input):
                print(f"Ошибка: Файл {args.input} не существует или недоступен")
                sys.exit(1)

            json_to_csv(
                args.input,
                args.output,
            )
            print(f"Успешно: JSON -> CSV")

        elif args.cmd == "csv2json":
            if not check_file(args.input):
                print(f"Ошибка: Файл {args.input} не существует или недоступен")
                sys.exit(1)

            csv_to_json(
                args.input,
                args.output,
            )
            print(f"Успешно: CSV -> JSON")

        elif args.cmd == "csv2xlsx":
            if not check_file(args.input):
                print(f"Ошибка: Файл {args.input} не существует или недоступен")
                sys.exit(1)

            csv_to_xlsx(
                args.input,
                args.output,
            )
            print(f"Успешно: CSV -> XLSX")

        else:
            print("Ошибка: Неизвестная команда")
            sys.exit(1)

        return 0

    except Exception as e:
        print(f"Ошибка при конвертации: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(cli_convert())
