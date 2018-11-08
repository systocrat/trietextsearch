import time
from collections import defaultdict


class Node(object):
	def __init__(self, char, parent=None):
		self.char = char
		self.parent = parent
		self.children = {}

	def consume_word(self, word):
		node = self

		for c in word:
			if c in node.children:
				node = node.children[c]
			else:
				new_node = Node(c, node)
				node.children[c] = new_node
				node = new_node

	def lookup(self, c):
		return self.children.get(c, None)

	def list_words(self):
		stack = [(self.char, [self])]

		all_paths = []

		while stack:
			vertex, path = stack.pop()

			if len(path[-1].children) == 0:
				all_paths.append(path)
			else:
				for char in path[-1].children.keys():
					child_node = path[-1].children[char]
					stack.append((char, path + [child_node]))

		return [
			''.join([
				n.char
				for n in path
			])
			for path in all_paths
		]

	def get_word(self):
		word = []

		node = self
		while node:
			word.append(node.char)
			node = node.parent

		return ''.join(word[::-1])


trie_root = Node('')

words = [
	'zebra',
	'abacus',
	'hotdog',
]

for word in words:
	trie_root.consume_word(word)

with open('words_alpha.txt', 'r') as f:
	big_text = f.read()

search_tree = defaultdict(list)


def contains_any(text, trie):
	search_index = defaultdict(list)

	for i, char in enumerate(text):
		if i in search_index:
			indexed_nodes = search_index[i]

			for node in indexed_nodes:
				if len(node.children) == 0:
					return True, node.get_word()

				potential_new_index_node = node.lookup(char)

				if potential_new_index_node:
					search_index[i + 1].append(potential_new_index_node)

			del search_index[i]

		potential_sub_node = trie.lookup(char)

		if potential_sub_node:
			search_index[i + 1].append(potential_sub_node)

	return False, None


def contains_any_test():
	print('Running contains_any')

	start = time.time()

	contains, word = contains_any(big_text, trie_root)

	end = time.time() - start

	print(f'Word contained: {word}')
	print(f'Seconds for contains_any: {end}')


def in_test():
	print('Running IN test')

	start = time.time()

	found = False
	for word in words:
		if word in big_text:
			found = True
			print(f'Word contained: {word}')
			break

	if not found:
		print('Word contained: None')

	end = time.time() - start

	print(f'Seconds for in test: {end}')


contains_any_test()
in_test()
