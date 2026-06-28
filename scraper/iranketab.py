import requests
from bs4 import BeautifulSoup


def scraper_iranketab():
    url = "https://www.iranketab.ir/tag/209-bestsellers"

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup.find_all(["article", "div", "li"]):
        text = tag.get_text(" ", strip=True)

        if len(text) > 50 and ("تومان" in text or "ریال" in text):
            print("=" * 80)
            print(tag.prettify()[:4000])
            break

    books = []

    cards = soup.select(".product-card, .book-card, .product-box, .col-md-3")[:10]

    for rank, card in enumerate(cards, start=1):
        title = ""
        author = ""
        price = ""
        link = ""

        title_tag = (
            card.select_one(".product-name")
            or card.select_one(".title")
            or card.select_one("h2")
            or card.select_one("h3")
            or card.select_one("a")
        )

        if title_tag:
            title = title_tag.get_text(strip=True)

        author_tag = (
            card.select_one(".author")
            or card.select_one(".product-author")
            or card.select_one(".authors")
        )

        if author_tag:
            author = author_tag.get_text(strip=True)

        price_tag = (
            card.select_one(".price")
            or card.select_one(".product-price")
            or card.select_one(".new-price")
        )

        if price_tag:
            price = price_tag.get_text(" ", strip=True)

        link_tag = card.select_one("a[href]")

        if link_tag:
            href = link_tag["href"]

            if href.startswith("/"):
                link = "https://www.iranketab.ir" + href
            else:
                link = href

        books.append(
            {
                "rank": rank,
                "title": title,
                "author": author,
                "price": price,
                "link": link,
            }
        )

    return books
