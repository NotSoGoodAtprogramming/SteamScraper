from urllib import request 
from bs4 import BeautifulSoup
from pprint import pprint as pp
import re as regex

def userMenu(steam_games):
	browsing = True
	
	while browsing:
		print("\n============TOP SELLING STEAM GAMES=================")
		print("Options: Type the corrisponding number")
		print("1) See all titles")
		print("2) See all prices")
		print("3) See all release date")
		print("4) See all ratings")
		print("\n\nTo see see full list type f\n\n\n")
		print("For all information on a specific title type the index number the next screen type \"N\" to get to the next screen")

		userinp = input("~ ")

		try:
			if userinp == "q":
				browsing = False
			elif userinp == "1":
				for title in range(1, len(steam_games["titles"]) + 1):
					print(title, ":", steam_games["titles"][title - 1])
			elif userinp == "2":
				for price in range(1, len(steam_games["prices"]) + 1):
					print(price, ":", steam_games["prices"][price - 1])
			elif userinp == "3":
				for date in range(1, len(steam_games["release_date"]) + 1):
					print(date, ":", steam_games["release_date"][date - 1])
			elif userinp == "4":
				for rates in range(1, len(steam_games["ratings"]) + 1):
					print(rates, ":", steam_games["ratings"][rates - 3])
			elif userinp == "f":
				for games in range(1, len(steam_games["titles"]) + 1):
					print("\n==================================================")
					print(" Title:", steam_games["titles"][games - 1],'\n',
						"Prices:", steam_games["prices"][games - 1], '\n',
						"Ratings:", steam_games["ratings"][games - 1], '\n',
						"Release Date:", steam_games["release_date"][games - 1], '\n')
			elif userinp == "N":
				try:
					print("Type the index number of the title")
					indx = input("~ ")
					if indx == len(steam_games["titles"]):
						print()
				except Exception as E:
					print(E)
			else:
				print("Try another option please..")
		except Exception as E:
			print(E)


def main():
	url = "https://store.steampowered.com/search/?filter=topsellers"
	urlOBJ = request.Request(url)
	html = request.urlopen(urlOBJ).read()
	soup = BeautifulSoup(html, 'html.parser')
	steam_games = {} #dictionary to store all the information so users can navigate it

	"""
	Retrieving all the Game's title's, release date's, prices, and ratings
	"""
	game_titles = []
	game_release_date = []
	game_prices = []
	game_ratings = []
	
	for games in soup.find_all("div", {"class" : "leftcol large"}):
		for GAMES in games.find_all("div", {"class" : "responsive_search_name_combined"}):
			game_titles.append(GAMES.span.text)
			game_prices.append(GAMES.find("div", {"class" : "col search_price_discount_combined responsive_secondrow"}).text.strip())
			game_release_date.append(GAMES.find_all("div", {"class" : "col search_released responsive_secondrow"})[0].text)
			for rates in GAMES.find_all("span"):
				game_ratings.append(rates.attrs)
	
	steam_games["titles"] = game_titles
	steam_games["prices"] = game_prices
	steam_games["release_date"] = game_release_date
	steam_games["ratings"] = game_ratings
	
	"""Removes \n from steam prices and re-enters them into the steam_games["prices"] catalog"""
	game_prices_list = []
	for items in range(len(steam_games["prices"])):
		if "\n" in steam_games["prices"][items]:
			game_prices_list.append(steam_games["prices"][items].replace("\n", ' '))
		else:
			game_prices_list.append(steam_games["prices"][items])
	steam_games["prices"] = game_prices_list #steam prices function ends here


	"""Takes the steam reviews and puts them into a list for the steam_games["ratings"] catalog"""
	game_ratings = []
	for rates in range(1, len(steam_games["ratings"]) + 1):
		if "data-tooltip-html" in steam_games["ratings"][rates - 1]:
			game_ratings.append(steam_games["ratings"][rates - 1]["data-tooltip-html"])
	steam_games["ratings"] = game_ratings

	userMenu(steam_games)

if __name__ == '__main__':
	main()