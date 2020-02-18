import sys

async def factorize(n):
	res=1
	if(n>=1):
		res = n*factorize(n-1)
	return res

async def get_permutations(word):
	# get the word
	chars = list(word)

	# get the permutations
	perms = await factorize(len(chars))

	# group unique characters
	groups = dict(zip(chars, [0 for x in chars]))

	# count all character groups
	for char in chars:
		groups[char] += 1

	# correct permutations for doubles
	for group in groups.keys():
		perms = perms/ await factorize(groups[group])
	return {
		"perms": int(perms),
		"groups": groups
	}

