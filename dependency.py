from stanfordnlp import jsonrpc
from stanfordnlp import corenlp
from simplejson import loads, dumps
import logging
import os


class StanfordParser(object):
	def _load_cache(self, f):
		for line in f:
			cache_line = loads(line)
			self.cache.update(cache_line)

	def __init__(self, cache_filename="cache/parser_cache.txt"):
		#self.parser = corenlp.StanfordCoreNLP(corenlp_path=os.path.abspath("stanford-corenlp-full-2014-08-27"))
		self.cache_filename = cache_filename
		self.cache = {} # str -> dependencies

		if os.path.exists(self.cache_filename):
			with open(self.cache_filename, 'r') as f:
				self._load_cache(f)

		self.out_file = open(cache_filename, 'a', 1)
		self.server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),
                           jsonrpc.TransportTcpIp(addr=("localhost", 8091), timeout=5.0))


	def parse(self, text):
		return loads(self.server.parse(text))

	def dependencies(self, text):
		dep = []

		if text in self.cache:
			# return cached result if there
			return self.cache[text]
		else:
			# get result and update cache
			parse_result = self.parse(text)
			for sentence in parse_result.get("sentences", []):
				dep += sentence.get(u'dependencies')

			cache_line = {text: dep}
			self.cache.update(cache_line)
			self.out_file.write(dumps(cache_line)+"\n")
		return dep