import csv, json, sys, os


def json_to_csv(
    json_path: str,
    csv_path: str,
) -> None:
    if not os.path.exists(json_path):
        print("FileNotFoundError")
    if os.path.getsize(json_path) == 0:
        print("1ValueError")
        sys.exit(1)
    with open(
        json_path,
        "r",
        encoding="utf-8",
    ) as json_file:
        json_data = json.load(json_file)
        if not all(type(x) == dict for x in json_data):
            print("ValueError")
            sys.exit(1)
    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=json_data[0].keys(),
        )
        writer.writeheader()
        writer.writerows(json_data)


def csv_to_json(
    csv_path: str,
    json_path: str,
) -> None:
    if not os.path.exists(csv_path):
        print("FileNotFoundError")
        sys.exit(1)
    if os.path.getsize(csv_path) == 0:
        print("3ValueError")
        sys.exit(1)
    with open(
        csv_path,
        "r",
        encoding="utf-8",
    ) as csvfile:
        reader = csv.reader(csvfile)
        header = next(
            reader,
            None,
        )
        if not header:
            print("4ValueError")
            sys.exit(1)
        reader = csv.DictReader(csvfile)
        data = list(reader)
    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as jsonfile:
        json.dump(
            data,
            jsonfile,
            ensure_ascii=False,
            indent=4,
        )