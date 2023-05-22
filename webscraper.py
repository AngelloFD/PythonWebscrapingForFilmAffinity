import csv
import json
from datetime import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup


cache = {}


def get(url):
    """
    Get the response from the given url. If the url is already in the cache, return the cached response.
    Otherwise, make the request and save the response in the cache.\n
    Arguments:
        url: The url to get the response from.

    Returns:
        The response from the given url.
    """
    if url in cache:
        return cache[url]
    else:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers)
            sleep(10)
            cache[url] = response
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            return None


def remove_accents(text):
    translation_table = str.maketrans("áéíóúüñ", "aeiouun")
    return text.translate(translation_table)


def get_show_urls(titles_csv):
    """
    Get the show urls from the given csv file.\n
    Arguments:
        titles_csv: The path to the csv file containing the titles.

    Returns:
        A list of show ids.
    """
    titles = []
    release_years = []
    with open(titles_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            titles.append(row["title"])
            release_years.append(row["release_year"])

    shows = []
    for title, release_year in zip(titles, release_years):
        search_url = f'https://www.filmaffinity.com/en/search.php?stext={title.replace(" ", "+")}&stype=title'
        page = get(search_url)
        if page.url != search_url and page.url.split("/")[4].find("film") != -1:
            show_id = page.url.split("/")[4]
            shows.append(show_id)
            print(f"Instantly found. Show ID: {show_id}, Title: {title}")
        elif page.url == search_url:
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find_all("div", class_="se-it mt")
            found = False
            for result in results:
                result_title = result.find("div", class_="mc-title").text.strip()
                if result_title == title:
                    result_url = result.find("a")["href"]
                    shows.append(result_url.split("/")[4])
                    found = True
                    print(
                        f"Found by name. Show ID: {result_url.split('/')[4]}, Title: {title}"
                    )
                    break
            if not found:
                for result in results:
                    result_year = result.find("div", class_="ye-w").text.strip()
                    if result_year == release_year:
                        result_url = result.find("a")["href"]
                        shows.append(result_url.split("/")[4])
                        print(
                            f"Found by year. Show ID: {result_url.split('/')[4]}, Title: {title}"
                        )
                        break
                else:
                    print(f"Not found. Title: {title}")
        else:
            print(f"Not found. Title: {title}")
    return shows


def get_reviews(shows):
    """
    Get the reviews for the given shows.\n
    Arguments:
        shows: A list of show ids.
    Returns:
        A list of dictionaries containing the reviews.
    """
    data = []
    for show in shows:
        page_number = 1
        while True:
            url = f"https://www.filmaffinity.com/es/reviews/{page_number}/{show}.html"
            page = get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            reviews = soup.find_all("div", class_="review-text1")
            ratings = soup.find_all("div", class_="user-reviews-movie-rating")
            genres_element = soup.find("span", class_="genres")
            genres = (
                [a.text for a in genres_element.find_all("a")] if genres_element else []
            )
            for review, rating in zip(reviews, ratings):
                review_text = remove_accents(review.text.strip())
                if review_text:
                    print(
                        f"Show ID: {show}, Review: {review_text}, Rating: {rating.text.strip()}"
                    )
                    data.append(
                        {
                            "metadata": {
                                "source": "FilmAffinity",
                                "timestamp": datetime.now().isoformat(),
                                "format": "JSON",
                                "tags": ["review"] + genres,
                            },
                            "Show ID": show,
                            "Review": review_text,
                            "Rating": rating.text.strip(),
                        }
                    )
            pager = soup.find("div", class_="pager")
            next_page = pager.find_all("a")[-1] if pager else None
            if next_page and next_page.text == ">>":
                page_number += 1
            else:
                break
    return data


def save_data(data):
    with open("reviews.json", "w") as f:
        json.dump(data, f, indent=4)

    with open("reviews.csv", mode="w") as csv_file:
        fieldnames = ["metadata", "Show ID", "Review", "Rating"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    # TODO: User input for csv file path
    titles_csv = "testdata/titles.csv"
    shows = get_show_urls(titles_csv)
    data = get_reviews(shows)
    save_data(data)


if __name__ == "__main__":
    main()
