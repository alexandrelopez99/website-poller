from time import sleep
from random import uniform
from bs4 import BeautifulSoup
from requests import get, RequestException

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
TIMEOUT = 10
JITTER_FACTOR = 0.1

def check_site_title(url):
    try:
        r = get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT}
        )
        r.raise_for_status()
    except RequestException:
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    title_text = soup.title.get_text(strip=True)
    return title_text

def main():
    print("\n---------------------------------------------------------------")
    url = input("Enter full URL: ")
    wait_base = int(input("Enter polling interval time (in seconds): "))
    wait_max_jitter = wait_base*JITTER_FACTOR

    print("Starting website monitor. Press Ctrl+C to quit.\n")

    while True:
        title = check_site_title(url)
        if title is None:
            print(f"Website {url} not reachable.")
        else:
            print(f"Website title: {title}")

        wait = wait_base + uniform(-wait_max_jitter, wait_max_jitter)
        print(f"Polling again in {wait:.3f} seconds...\n")
        sleep(wait)

if __name__ == "__main__":
    main()