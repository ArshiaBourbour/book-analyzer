import os
from datetime import datetime

import pandas as pd

from scraper.iranketab import scraper_iranketab
from scraper.book30 import scraper_book30
from scraper.digikala import scraper_digikala


def save_data(name, data):
    os.makedirs("data", exist_ok=True)

    columns = ["rank", "title", "author", "price", "link"]

    df = pd.DataFrame(data, columns=columns)

    path = f"data/{name}.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")

    print(f"Saved: {path}")


def main():
    print(f"Scraping started at {datetime.now()}")

    scrapers = {
        "iranketab": scraper_iranketab,
        "30book": scraper_book30,
        "digikala": scraper_digikala,
    }

    for name, scraper in scrapers.items():
        try:
            data = scraper()
            save_data(name, data)
            print(f"{name}: {len(data)} books saved")
        except Exception as e:
            print(f"{name}: {e}")

    print("Done!")


if __name__ == "__main__":
    main()
