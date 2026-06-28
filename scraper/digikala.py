import requests
from bs4 import BeautifulSoup


def scraper_digikala():
    url = "https://www.digikala.com/best-selling/"

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    classes = set()

    for tag in soup.find_all(True):
        cls = tag.get("class")
        if cls:
            classes.add(" ".join(cls))

    for c in sorted(classes):
        print(c)
    books = []

    cards = soup.select(
        "article, .product-list_ProductList__item, .styles_VerticalProductCard__wrapper"
    )[:10]

    for rank, card in enumerate(cards, start=1):
        title = ""
        author = ""
        price = ""
        link = ""

        title_tag = (
            card.select_one("h3")
            or card.select_one("h2")
            or card.select_one("[data-cro-id='product-title']")
            or card.select_one("a")
        )

        if title_tag:
            title = title_tag.get_text(strip=True)

        author_tag = (
            card.select_one(".author")
            or card.select_one(".product-author")
            or card.select_one(".subtitle")
        )

        if author_tag:
            author = author_tag.get_text(strip=True)

        price_tag = (
            card.select_one("[data-testid='price-final']")
            or card.select_one(".price")
            or card.select_one(".text-subtitle-strong")
        )

        if price_tag:
            price = price_tag.get_text(" ", strip=True)

        link_tag = card.select_one("a[href]")

        if link_tag:
            href = link_tag["href"]

            if href.startswith("/"):
                link = "https://www.digikala.com" + href
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
