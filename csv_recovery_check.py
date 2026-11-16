
import csv
import sys
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation

FIELDS = [
    "transaction_id", "date", "category",
    "description", "amount"
]

def check_csv(filename):
    path = Path(filename)

    if not path.is_file():
        print("CSV missing. Restore or re-upload:", filename)
        return False

    try:
        with path.open("r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != FIELDS:
                print("Invalid CSV column headings.")
                return False

            ids = set()
            count = 0

            for line, row in enumerate(reader, start=2):
                if None in row or any(
                    row.get(field) is None or
                    not row[field].strip()
                    for field in FIELDS
                ):
                    print("Missing or malformed value at line", line)
                    return False

                transaction_id = row["transaction_id"].strip().upper()

                if transaction_id in ids:
                    print("Duplicate ID:", transaction_id)
                    return False

                ids.add(transaction_id)

                try:
                    datetime.strptime(row["date"], "%d/%m/%Y")
                    amount = Decimal(row["amount"])
                    if not amount.is_finite():
                        raise ValueError("Non-finite amount")
                except (ValueError, InvalidOperation):
                    print("Invalid date or amount at line", line)
                    return False

                count += 1

        print("CSV validation successful.")
        print("Records checked:", count)
        return True

    except (OSError, UnicodeError, csv.Error) as error:
        print("Unable to read CSV:", error)
        return False

if __name__ == "__main__":
    filename = (
        sys.argv[1] if len(sys.argv) > 1
        else "MIT103_A3_Revised_T3_2026_Sample_Transactions.csv"
    )
    sys.exit(0 if check_csv(filename) else 1)
