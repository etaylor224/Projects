
from budget_db import db_create, db_exists
import pybudgetConsole


def main():
    if not db_exists:
        db_create()

    row = pybudgetConsole.row
    if row == "1":
        pybudgetConsole.add_entries()
    else:
        pybudgetConsole.read_entries()

if __name__ == "__main__":
    main()
