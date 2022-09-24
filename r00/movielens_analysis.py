import os
import sys
import urllib
import requests
from bs4 import BeautifulSoup as bs
import json
import pytest
from collections import Counter, defaultdict
import functools
from datetime import datetime
import re


class InvalidCsv(Exception):
	pass


class CsvParser:
	def __init__(self, filename, sep=',', header=True):
		self.filename = filename
		self.sep = sep
		self.header = header
		self.columns = []
		self.count_features = None

	def open_csv(self):
		with open(self.filename, 'r') as fd:
			if self.header:
				self.columns = next(fd).strip('\n').split(',')
				self.count_features = len(self.columns)
			else:
				self.columns = range(int(1e6))
			for row in fd:
				yield row.strip()

	def read_csv(self):
		for row in self.open_csv():
			row_dict = {}
			flag = False
			column_idx = 0
			for obj in row.strip('\n').split(self.sep):
				try:
					row_dict[self.columns[column_idx]] = row_dict.get(
						self.columns[column_idx], '') + obj.strip('"')
				except IndexError:
					print('Invalid CSV')
					sys.exit()

				if obj.count('"') == 1:
					flag = not flag

				if flag:
					row_dict[self.columns[column_idx]] += self.sep
				else:
					column_idx += 1
			if self.count_features is None:
				self.count_features = len(row_dict)
			if len(row_dict) != self.count_features:
				print('Invalid CSV')
				sys.exit()
			yield row_dict


class Movies(CsvParser):
	"""
	Analyzing data from movies.csv
	"""

	def __init__(self, path_to_the_file):
		"""
		Put here any fields that you think you will need.
		"""
		super().__init__(path_to_the_file)

	def is_valid_file(self):
		return set(self.columns) == set('movieId,title,genres'.split(','))

	def read_csv(self):
		for film_info in super(Movies, self).read_csv():
			if not self.is_valid_file():
				print(f'Invalid parse CSV {self.filename}')
				sys.exit()
			yield film_info

	def get_first_film_info(self):
		for film_info in super(Movies, self).read_csv():
			return film_info

	def dist_by_release(self):
		"""
		The method returns a dict where the keys are years and the values are counts.
		You need to extract years from the titles. Sort it by counts descendingly.
		"""
		release_years = Counter()
		for film_info in self.read_csv():
			try:
				year = int(re.findall(r'\((\d{4})\)', film_info['title'])[-1])
			except IndexError:
				continue
			release_years[year] += 1
		return dict(release_years.most_common())

	def dist_by_genres(self):
		"""
		The method returns a dict where the keys are genres and the values are counts.
	Sort it by counts descendingly.
		"""
		genres = Counter()
		for film_info in self.read_csv():

			for genre in self._get_film_genre(film_info):
				genres[genre] += 1
		return dict(genres.most_common())

	@staticmethod
	def _get_film_genre(film_info: dict):
		if film_info['genres'] == '(no genres listed)':
			return []
		return film_info['genres'].split('|')

	def most_genres(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are the number of genres of the movie. Sort it by numbers descendingly.
		"""
		movies = Counter()
		for film_info in self.read_csv():
			movies[film_info['title']] = len(self._get_film_genre(film_info))
		return dict(movies.most_common()[:n])


def mean(values):
	if len(values) == 0:
		return float('nan')
	return sum(values) / len(values)


def median(values):
	if len(values) == 0:
		return float('nan')
	items = sorted(values)
	if len(items) % 2 == 1:
		return items[len(items) // 2]
	return (items[len(items) // 2 - 1] + items[len(items) // 2]) / 2


def var(values):
	if not len(values):
		return float('nan')
	mean_value = mean(values)
	squared_diff = [(value - mean_value) ** 2 for value in values]
	return sum(squared_diff) / len(squared_diff)


class Ratings(CsvParser):
	"""
	Analyzing data from ratings.csv
	"""

	def __init__(self, path_to_the_file, path_to_movies_file):
		"""
		Put here any fields that you think you will need.
		"""
		super().__init__(path_to_the_file)
		self.filename_movies = path_to_movies_file
		self.movies = self.Movies(self, path_to_movies_file)

	def get_users(self):
		return Ratings.Users(self, self.filename_movies)

	def get_movies(self):
		return Ratings.Movies(self, self.filename_movies)

	def is_valid_file(self):
		return set(self.columns) == set('userId,movieId,rating,timestamp'.split(','))

	def read_csv(self):
		for film_info in super(Ratings, self).read_csv():
			if not self.is_valid_file():
				print(f'Invalid parse CSV {self.filename}')
				sys.exit()
			yield film_info

	class Movies(Movies):
		def __init__(self, rating, movies_filename):
			super().__init__(movies_filename)
			self.rating = rating
			self.movies_id2name = {}

		def init_mapping_movies(self):
			for film_info in self.read_csv():
				self.movies_id2name[film_info['movieId']] = film_info['title']

		def dist_by_year(self):
			"""
			The method returns a dict where the keys are years and the values are counts.
			Sort it by years ascendingly. You need to extract years from timestamps.
			"""
			ratings_by_year = Counter()
			for film_info in self.rating.read_csv():
				ratings_by_year[datetime.fromtimestamp(int(film_info['timestamp'])).year] += 1
			return dict(ratings_by_year.most_common()[::-1])

		def dist_by_rating(self):
			"""
			The method returns a dict where the keys are ratings and the values are counts.
			Sort it by ratings ascendingly.
			"""
			ratings_distribution = Counter()
			for film_info in self.rating.read_csv():
				ratings_distribution[float(film_info['rating'])] += 1
			return dict(ratings_distribution.most_common()[::-1])

		def top_by_num_of_ratings(self, n):
			"""
			The method returns top-n movies by the number of ratings.
			It is a dict where the keys are movie titles and the values are numbers.
			Sort it by numbers descendingly.
			"""
			self.init_mapping_movies()
			if n == -1:
				n = len(self.movies_id2name)
			top_movies = Counter()
			for film_info in self.rating.read_csv():
				top_movies[self.movies_id2name[film_info['movieId']]] += 1
			return dict(top_movies.most_common()[:n])

		def top_by_ratings(self, n, metric='average'):
			"""
			The method returns top-n movies by the average or median of the ratings.
			It is a dict where the keys are movie titles and the values are metric values.
			Sort it by metric descendingly.
			The values should be rounded to 2 decimals.
			"""
			assert metric in ('average', 'median')
			top_movies = self._groupby_rating_by_film()
			if n == -1:
				n = len(self.movies_id2name)
			if metric == 'average':
				top_movies = [(title, mean(ratings))
				for title, ratings in top_movies.items()]
			else:
				top_movies = [(title, median(ratings))
				for title, ratings in top_movies.items()]

			return dict(
				map(lambda x: (x[0], round(x[1], 2)),
					sorted(top_movies, key=lambda x: x[1], reverse=True)[:n]))

		def _groupby_rating_by_film(self):
			self.init_mapping_movies()
			top_movies = defaultdict(list)
			for film_info in self.rating.read_csv():
				top_movies[self.movies_id2name[film_info['movieId']]].append(
				float(film_info['rating']))
			return top_movies

		def top_controversial(self, n):
			"""
			The method returns top-n movies by the variance of the ratings.
			It is a dict where the keys are movie titles and the values are the variances.
			Sort it by variance descendingly.
			The values should be rounded to 2 decimals.
			"""
			if n == -1:
				n = len(self.movies_id2name)
			top_movies = self._groupby_rating_by_film()
			top_movies = [(title, var(ratings))
			for title, ratings in top_movies.items()]

			return dict(
				map(lambda x: (x[0], round(x[1], 2)),
				sorted(top_movies, key=lambda x: x[1], reverse=True)[:n]))

	class Users(Movies):
		"""
		In this class, three methods should work.
		The 1st returns the distribution of users by the number of ratings made by them.
		The 2nd returns the distribution of users by average or median ratings made by them.
		The 3rd returns top-n users with the biggest variance of their ratings.
		Inherit from the class Movies. Several methods are similar to the methods from it.
		"""

		def _groupby_rating_by_film(self):
			self.init_mapping_movies()
			top_movies = defaultdict(list)
			for film_info in self.rating.read_csv():
				top_movies[film_info['userId']].append(
				float(film_info['rating']))
			return top_movies

		def dist_by_rating(self):
			ratings_distribution = Counter()
			for film_info in self.rating.read_csv():
				ratings_distribution[film_info['userId']] += 1
			return dict(ratings_distribution.most_common()[::-1])

		def dict_by_ratings(self, metric='average'):
			return super().top_by_ratings(-1, metric)

		def top_controversial(self, n):
			return super().top_controversial(n)


class Tags:
    """
    Analyzing data from tags.csv
    """
    first_line_list = ["userId","movieId","tag","timestamp"]
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        f = open(path_to_the_file, "r")
        self.userId = list()
        self.movieId = list()
        self.tag = list()
        self.timestamp = list()
        first_line = True
        elem_count = len(self.first_line_list)
        for line in f:
            if first_line:
                word_list = line[0:-1].split(",")
                if word_list != self.first_line_list:
                    raise Exception("Wrong file")
                first_line = False
            else:
                word_list = line.split(",")
                if len(word_list) != elem_count:
                    raise Exception(f"Wrong file:\n Line \'{line}\' should have {elem_count} elements")
                self.userId.append(word_list[0])
                self.movieId.append(word_list[1])
                self.tag.append(word_list[2])
                self.timestamp.append(word_list[3])
        f.close()


    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict
 where the keys are tags and the values are the number of words inside the tag.
 Drop the duplicates. Sort it by numbers descendingly.
        """
        if n < 1:
            n = -1
        big_tags = set(map(lambda x: (x,len(x.split(" "))), self.tag))
        big_tags = list(big_tags)
        big_tags.sort(key=lambda i: i[1], reverse=True)
        big_tags = dict(big_tags[0:n])
        return big_tags

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        if n < 1:
            n = -1
        big_tags = set(map(lambda x: (x,len(x)), self.tag))
        big_tags = list(big_tags)
        big_tags.sort(key=lambda i: i[1], reverse=True)
        big_tags = list(map(lambda x: x[0], big_tags[0:n]))
        return big_tags

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        most_words_list = self.most_words(n)
        tags_key = most_words_list.keys()
        longest_list = self.longest(n)
        big_tags = list(set(tags_key).intersection(set(longest_list)))
        return big_tags

    def most_popular(self, n):
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        if n < 1:
            n = -1
        popular_tags = list(set(Counter(self.tag).items()))
        popular_tags.sort(key=lambda i: i[1], reverse=True)
        popular_tags = dict(popular_tags[0:n])
        return popular_tags

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        unique_tags = set(self.tag)
        tags_with_word = list(filter(lambda x: x.find(word) >= 0, unique_tags))
        tags_with_word.sort()
        return tags_with_word

class Links:
    """
    Analyzing data from links.csv
    """
    first_line_list = ["movieId","imdbId","tmdbId"]
    limit_films = 5
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        f = open(path_to_the_file, "r")
        self.movieId = list()
        self.imdbId = list()
        self.tmdbId = list()
        first_line = True
        elem_count = len(self.first_line_list)
        for line in f:
            if first_line:
                word_list = line[0:-1].split(",")
                if word_list != self.first_line_list:
                    raise Exception("Wrong file")
                first_line = False
            else:
                word_list = line[0:-1].split(",")
                if len(word_list) != elem_count:
                    raise Exception(f"Wrong file:\n Line \'{line}\' should have {elem_count} elements")
                self.movieId.append(word_list[0])
                self.imdbId.append(word_list[1])
                self.tmdbId.append(word_list[2])
        f.close()

    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """
        imdb_info = list()
        for movie in list_of_movies:
            tmp_dict = dict()
            if movie in self.movieId:
                tmp_dict["movieId"] = movie
                imdbId = self.imdbId[self.movieId.index(movie)]
                url = "http://www.imdb.com/title/tt" + imdbId + "/"
                response = requests.get(url).text
                soup = bs(response, 'html.parser')

                blocks = soup.find_all('li', class_="ipc-metadata-list__item")
                for block in blocks:
                    if block.text.find('Director') >= 0 and "Director" in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Director'] = group
                    elif block.text.find('Writers') >= 0 and "Writers" in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Writers'] = group
                    elif block.text.find('Stars') >= 0 and "Stars" in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Stars']= group
                    elif block.text.find('Runtime') >= 0 and "Runtime" in list_of_fields:
                        group = [group.text for group in block.find_all('div')]
                        tmp_dict['Runtime']= group
                    elif block.text.find('Production companies') >= 0 and 'Production companies' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Production companies']= group
                    elif block.text.find('Budget') >= 0 and 'Budget' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        for budget in group:
                            budget_int = int(''.join([c for c in budget.replace(',', '') if c.isdigit()]))
                        tmp_dict['Budget']= [budget_int]
                    elif block.text.find('Gross worldwide') >= 0 and 'Gross worldwide' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Gross worldwide']= group
                    elif block.text.find('Gross worldwide') >= 0 and 'Cumulative Worldwide Gross' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        for gross in group:
                            gross_int = int(''.join([c for c in gross.replace(',', '') if c.isdigit()]))
                        tmp_dict['Cumulative Worldwide Gross']= [gross_int]
                    elif block.text.find('Genres') >= 0 and 'Genres' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Genres']= group
                    elif block.text.find('Also known as') >= 0 and 'Titles' in list_of_fields:
                        group = [group.text for group in block.find_all('li')]
                        tmp_dict['Titles']= group

                tmp_list = list()
                for i in list_of_fields:
                    if i in tmp_dict.keys():
                        tmp_list.append(tmp_dict[i])
                    else:
                        tmp_list.append([" -1"])
                imdb_info.append([movie, *tmp_list])

        imdb_info.sort(key=lambda i: int(i[0]), reverse=True)
        return imdb_info

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        movie_id_list = self.get_movie_selection_id(n)
        directors = dict()
        info = self.get_imdb(movie_id_list, ["Director"])
        for direct_list in info:
            for direct in direct_list[0]:
                if direct in directors.keys():
                    directors[direct] += 1
                else:
                    directors[direct] = 1
        directors = list(directors.items())
        directors.sort(key=lambda i: i[1], reverse=True)

        return dict(directors[0:n])

    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        movie_id_list = self.get_movie_selection_id(n)
        budgets = dict()
        info = self.get_imdb(movie_id_list, ["Titles", 'Budget'])
        for budget_list in info:
            budgets[budget_list[1][0]] = budget_list[2][0]
        budgets = list(budgets.items())
        budgets_sort = budgets.copy()
        for i, (movies_name, budget) in enumerate(budgets_sort):
            if budget == ' -1':
                budget_int = -1
            else:
                budget_int = budget
            budgets_sort[i] = (movies_name, budget_int)
        budgets_sort.sort(key=lambda i: i[1], reverse=True)
        return dict(budgets_sort[0:n])

    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        movie_id_list = self.get_movie_selection_id(n)
        profits = dict()
        info = self.get_imdb(movie_id_list, ["Titles", 'Cumulative Worldwide Gross', 'Budget'])
        for profit_list in info:
            profits[profit_list[1][0]] = float(profit_list[2][0]) - float(profit_list[3][0])
        profits = list(profits.items())
        profits.sort(key=lambda i: i[1], reverse=True)
        return dict(profits[0:n])

    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
        Sort it by runtime descendingly.
        """
        movie_id_list = self.get_movie_selection_id(n)
        runtimes = dict()
        info = self.get_imdb(movie_id_list, ["Titles", 'Runtime'])
        for runtime_list in info:
            runtimes[runtime_list[1][0]] = runtime_list[2][0]
        runtimes = list(runtimes.items())
        runtimes.sort(key=lambda i: i[1], reverse=True)
        return dict(runtimes[0:n])

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it.
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        movie_id_list = self.get_movie_selection_id(n)
        costs = dict()
        info = self.get_imdb(movie_id_list, ["Titles", 'Budget', 'Runtime'])
        for cost_list in info:
            time = cost_list[3][0]
            if time.find('hour') >= 0:
                time_min = float(time[0: time.find('hour')]) * 60
                if time.find('min') >= 0:
                    time_min += float(time[time.find('hour') + 5::].lstrip().split(" ")[0])
            else:
                time_min = float(time.split(' ')[0])
            budget = cost_list[2][0]
            if not isinstance(budget, int):
                budget = -1
            costs[cost_list[1][0]] = budget / time_min
        costs = list(costs.items())
        costs.sort(key=lambda i: i[1], reverse=True)
        return dict(costs[0:n])

    def get_movie_selection_id(self, n:int):
        if n < 1:
            n = len(self.movieId)
        tmp_set = set(self.movieId)
        movie_id = list()
        for i in range(0, n):
            movie_id.append(tmp_set.pop())
        return movie_id


class Tests:
	def setup_class(self):
		self.movies = Movies('movies.csv')
		self.rating = Ratings('ratings.csv', 'movies.csv')
		self.tags = Tags('tags.csv')
		self.links = Links('links.csv')

	def test_movies_dist_by_release(self):
		result = self.movies.dist_by_release()
		assert (isinstance(result, dict) and
				(set(map(type, result.values())) == {int} and
				 set(map(type, result.keys())) == {int}) and
				sorted(result.values(), reverse=True) == list(result.values()))

	def test_movies_dist_by_genres(self):
		result = self.movies.dist_by_genres()
		assert (isinstance(result, dict) and
				(set(map(type, result.values())) == {int} and
				set(map(type, result.keys())) == {str}) and
				sorted(result.values(), reverse=True) == list(result.values()))

	def test_movies_most_genres(self):
		result = self.movies.most_genres(10)
		assert (isinstance(result, dict) and
				(set(map(type, result.values())) == {int} and
				set(map(type, result.keys())) == {str}) and
				sorted(result.values(), reverse=True) == list(result.values()))

	def test_rating_dist_by_year(self):
		result = self.rating.get_movies().dist_by_year()
		assert (isinstance(result, dict) and
				(set(map(type, result.values())) == {int} and
				set(map(type, result.keys())) == {int}) and
				sorted(result.values(), reverse=False) == list(result.values()))

	def test_rating_dist_by_rating(self):
		result = self.rating.get_movies().dist_by_rating()
		assert (isinstance(result, dict) and
				(set(map(type, result.values())) == {int} and
				set(map(type, result.keys())) == {float}) and
				sorted(result.values(), reverse=False) == list(result.values()))

	def test_rating_top_by_num_of_ratings(self):
		result = self.rating.get_movies().top_by_num_of_ratings(10)
		assert (isinstance(result, dict) and
				(set(map(type, result.values())) == {int} and
				set(map(type, result.keys())) == {str}) and
				sorted(result.values(), reverse=True) == list(result.values()))

	def test_rating_top_by_ratings(self):
		for metric in ['average', 'median']:
			result = self.rating.get_movies().top_by_ratings(500, metric)
			assert (isinstance(result, dict) and
					(set(map(type, result.values())) == {float} and
					set(map(type, result.keys())) == {str}) and
					sorted(result.values(), reverse=True) == list(result.values()))

	def test_rating_top_controversial(self):
		result = self.rating.get_movies().top_controversial(10)
		assert (isinstance(result, dict) and
				(set(map(type, result.values())) == {float} and
				set(map(type, result.keys())) == {str}) and
				sorted(result.values(), reverse=True) == list(result.values()))

	def test_tags_most_words(self):
		result = self.tags.most_words(10)
		assert (isinstance(result, dict) and
				(set(map(type, result.values())) == {int} and
				set(map(type, result.keys())) == {str}) and
				sorted(result.values(), reverse=True) == list(result.values()))

	def test_tags_longest(self):
		big_tags = Counter()
		for tag_s in self.tags.read_csv():
			for tag_list in self.tags.get_tags(tag_s):
				big_tags[tag_list] = len(tag_list)
		result = self.tags.longest(10)
		print(sorted(dict(big_tags).items(), reverse=True, key=lambda x: x[1])[:10])
		assert (isinstance(result, list) and
				set(map(type, result)) == {str} and
				[el[0] for el in sorted(dict(big_tags).items(),
					reverse=True, key=lambda x: x[1])[:10]] == list(result))

	def test_tags_most_words_and_longest(self):
		result = self.tags.most_words_and_longest(1000)
		assert (isinstance(result, list) and
			set(map(type, result)) == {str})

	def test_tags_most_popular(self):
		result = self.tags.most_popular(10)
		assert (isinstance(result, dict) and
			(set(map(type, result.values())) == {int} and
			set(map(type, result.keys())) == {str}) and
			sorted(result.values(), reverse=True) == list(result.values()))

	def test_tags_with(self):
		result = self.tags.tags_with('Netflix')
		assert (isinstance(result, list) and
			set(map(type, result)) == {str} and
			sorted(result, reverse=False) == list(result))

	def test_tags_most_words(self):
		top_n = self.tags.most_words(10)
		assert isinstance(top_n, dict)
		assert len(top_n) == 10
		longes_key = "Something for everyone in this one... saw it without and plan on seeing it with kids!"
		assert top_n[longes_key] == 16

	def test_tags_longest(self):
		top_n = self.tags.longest(10)
		assert isinstance(top_n, list)
		assert isinstance(top_n[0], str)
		assert len(top_n) == 10
		longes_key = "Something for everyone in this one... saw it without and plan on seeing it with kids!"
		assert len(top_n[0]) == 85 and top_n[0] == longes_key

	def test_tags_most_words_and_longest(self):
		top_n = self.tags.most_words_and_longest(10)
		assert isinstance(top_n, list)
		assert isinstance(top_n[0], str)
		assert len(top_n) <= 10
		longes_key = "Something for everyone in this one... saw it without and plan on seeing it with kids!"
		assert longes_key in top_n

	def test_tags_most_popular(self):
		top_n = self.tags.most_popular(10)
		assert isinstance(top_n, dict)
		assert len(top_n) == 10
		popular_key = "In Netflix queue"
		assert top_n[popular_key] == 131

	def test_tags_with_word(self):
		top_n = self.tags.tags_with("ab")
		assert isinstance(top_n, list)
		assert isinstance(top_n[0], str)
		assert len(top_n) == 26
		assert top_n[0].find("ab") >= 0

	def test_get_imdb(self):
		result = self.links.get_imdb(['1', '2', '3', '4', '5'], ['movieId', 'Director', 'Genre', 'Stars'])
		assert (isinstance(result, list) and
			set(map(type, result)) == {list} and
			sorted(result, reverse=True, key=lambda x: x[0]) == list(result))

	def test_top_directors(self):
		self.links.get_imdb(['1', '2', '3', '4', '5'], ['movieId', 'Director', 'Genre', 'Stars'])
		result = self.links.top_directors(3)
		assert (isinstance(result, dict) and
			set(map(type, result)) == {str})

	def test_links_get_imdb(self):
		info_list = self.links.get_imdb(["1", "2"], ["movieId"])
		assert isinstance(info_list, list)
		assert isinstance(info_list[0], list)
		assert int(info_list[0][0]) > int(info_list[1][0])

	def test_links_top_directors(self):
		top_n = self.links.top_directors(3)
		assert isinstance(top_n, dict)

	def test_links_most_expensive(self):
		top_n = self.links.most_expensive(3)
		assert isinstance(top_n, dict)

	def test_links_most_profitable(self):
		top_n = self.links.most_profitable(3)
		assert isinstance(top_n, dict)

	def test_links_longest(self):
		top_n = self.links.longest(3)
		assert isinstance(top_n, dict)

	def test_links_top_cost_per_minute(self):
		top_n = self.links.top_cost_per_minute(3)
		assert isinstance(top_n, dict)

	def test_links_get_movie_selection_id(self):
		top_n = self.links.get_movie_selection_id(3)
		assert isinstance(top_n, list)
		assert isinstance(top_n[0], str)
		assert len(top_n) == 3

if __name__ == '__main__':
	links = Links("links.csv")
	top_n = links.top_cost_per_minute(200)
