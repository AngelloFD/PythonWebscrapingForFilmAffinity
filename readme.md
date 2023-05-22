# Webscraping with Python and BeautifulSoup for reviews on FilmAffinity
This script was created out of boredom and to practice webscraping with Python and BeautifulSoup. It scrapes the reviews of a movie on FilmAffinity and saves them in a .csv and json file.

## Getting Started
### Prerequirements and installation
Preferabily, you'd want to use a virtual enviroment to install the required packages. You can create one with:
```
python -m venv venv
```
What you will need to install to run the script its all in the requirements.txt file. You can install them with:
```
pip install -r requirements.txt
```
### Usage
To run the script you will need to run the following command:
```
python webscraping.py
```
**Important: If you execute the script as it is right now, it will scrape the reviews from the titles.csv file stored in the testdata folder which is part of the [Paramount+ Movies and TV Shows](https://www.kaggle.com/datasets/dgoenrique/paramount-movies-and-tv-shows?select=titles.csv).**

## TODOs
- [ ] Add UI
- [ ] Ask for user input for the csv file path and the name of the column where the titles are stored.
- [ ] Scrape from different languages of the site.

## License
This project is licensed under the GNU GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details
