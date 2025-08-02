import os
import re
from datetime import datetime

MIGRATIONS_DIR = "app/alembic/versions"
CREATE_DATE_PATTERN = re.compile(r"Create Date:\s+([\d\-]+\s+[\d:\.]+)")
ALREADY_RENAMED_PATTERN = re.compile(r"^\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}_")


def rename_migrations(folder: str):
    for filename in os.listdir(folder):
        if filename == "__init__.py" or not filename.endswith(".py"):
            continue

        if ALREADY_RENAMED_PATTERN.match(filename):
            continue

        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        match = CREATE_DATE_PATTERN.search(content)
        if not match:
            continue

        try:
            date_str = match.group(1)
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            print(f"Date error at: {filename}")
            continue

        prefix = dt.strftime("%Y_%m_%d_%H_%M_%S")
        new_name = f"{prefix}_{filename}"
        new_path = os.path.join(folder, new_name)
        os.rename(filepath, new_path)


if __name__ == "__main__":
    rename_migrations(MIGRATIONS_DIR)
