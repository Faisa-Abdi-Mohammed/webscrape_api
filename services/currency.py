import requests
from bs4 import BeautifulSoup


def gbp_to_sek(gbp: float, rate: float) -> float:
    # Konverterar pund till kronor
    return round(gbp * rate, 2)


def get_gbp_sek_rate() -> float:
    """
    Hämtar aktuell växelkurs GBP -> SEK via web scraping.
    Om något går fel används en fallback-kurs.
    """

    fallback_rate = 13.0  # används om scraping misslyckas

    try:
        url = "https://www.x-rates.com/calculator/?from=GBP&to=SEK&amount=1"
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Växelkursen ligger i span med class ccOutputRslt
        rate_text = soup.select_one("span.ccOutputRslt").get_text(strip=True)


        rate_value = float(rate_text.split(" ")[0])

        return rate_value

    except Exception:
        return fallback_rate