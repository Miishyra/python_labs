import os, csv, sys

from openpyxl import (
    Workbook,
)


def csv_to_xlsx(
    csv_path: str,
    xlsx_path: str,
) -> None:
    if not os.path.exists(csv_path):
        print("FileNotFoundError")
        sys.exit(1)

    if os.path.getsize(csv_path) == 0:
        print("ValueError")
        sys.exit(1)
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    with open(
        csv_path,
        "r",
        encoding="utf-8",
    ) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            ws.append(row)

    for column_cells in ws.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter
        for cell in column_cells:
            if cell.value:
                max_length = max(
                    max_length,
                    len(str(cell.value)),
                )
        ws.column_dimensions[column_letter].width = max(
            max_length + 2,
            8,
        )
    wb.save(xlsx_path)
