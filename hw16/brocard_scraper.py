from typing import Any, List
from curl_cffi import requests
from parsel import Selector

from databases import Session, Parfume

PARFUME_URL = "https://www.brocard.ua/ua/category/aromati-dlya-nogo/versace-327/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


class Price(float):
    def __new__(cls, value: str):
        clean_value = value.replace(" ", "").replace(",", ".")
        return super().__new__(cls, clean_value)


def scrape_data() -> List[tuple[Any]]:
    data = []
    response = requests.get(PARFUME_URL, headers=HEADERS, timeout=10)
    print(response.status_code)
    sel = Selector(text=response.text)
    products = sel.css("div.product-list-item:not(.out-of-stock)")
    for product in products:
        name = product.css(".product-name::text").get()
        brand = product.css(".product-brand::text").get()
        price_old = Price(product.css(".old-price .wysiwyg::text").get(""))
        price = Price(product.css(".special-price .wysiwyg::text").get(""))
        picture = product.css("img::attr(src)").get()
        print(name, brand, price_old, price)
        data.append(
            {
                "name": brand,
                "brand": name,
                "price_old": price_old,
                "price": price,
                "picture": picture,
            }
        )
    return data


def main():
    parfumes = scrape_data()
    with Session() as session:
        parfumes_to_db = [Parfume(**parfume) for parfume in parfumes]
        session.add_all(parfumes_to_db)
        session.commit()


if __name__ == "__main__":
    main()
