def isCustomerWinner(codeList, shoppingCart):
    codeListGroupPointer = 0
    shoppingCartPointer = 0
    while codeListGroupPointer < len(codeList) and shoppingCartPointer < len(shoppingCart):
        if len(codeList[codeListGroupPointer]) > len(shoppingCart) - shoppingCartPointer:
            return False
        match = all(True if a == 'anything' else a == b for a, b in zip(
            codeList[codeListGroupPointer],
            shoppingCart[shoppingCartPointer:shoppingCartPointer + len(codeList[codeListGroupPointer]) + 1]
        ))
        if match:
            shoppingCartPointer += len(codeList[codeListGroupPointer])
            codeListGroupPointer += 1
        else:
            shoppingCartPointer += 1
    return codeListGroupPointer == len(codeList)

print(isCustomerWinner([['apple', 'apple'], ['banana', 'anything', 'banana']], ['orange', 'apple', 'apple', 'banana', 'orange', 'banana']))
print(isCustomerWinner([['apple', 'apple'], ['banana', 'anything', 'banana']], ['banana', 'orange', 'banana', 'apple', 'apple']))
print(isCustomerWinner([['apple', 'apple'], ['banana', 'anything', 'banana']], ['apple', 'banana', 'apple', 'banana', 'orange', 'banana']))
print(isCustomerWinner([['apple', 'banana','apple', 'banana', 'coconut']], ['apple', 'banana', 'apple', 'banana', 'apple', 'banana']))
print(isCustomerWinner([['apple', 'orange'], ['orange', 'banana', 'orange']], ['apple', 'orange', 'banana', 'orange', 'orange', 'banana', 'orange', 'grape']))
print(isCustomerWinner([['apple', 'apple'], ['banana', 'anything', 'banana']], ['apple', 'apple', 'banana', 'banana']))
print(isCustomerWinner([['apple', 'apple'], ['apple', 'anything', 'banana']], ['apple', 'apple', 'banana', 'banana']))
print(isCustomerWinner([['apple', 'apple'], ['apple', 'anything', 'banana']], ['apple', 'apple', 'apple', 'apple', 'banana']))
print(isCustomerWinner([['apple', 'apple'], ['apple', 'banana']], ['apple', 'apple', 'apple', 'banana']))
print(isCustomerWinner([["anything", "apple" ], ["banana", "anything", "banana"]], ["orange", "grapes", "apple", "orange", "orange", "banana", "apple", "banana", "banana"]))
print(isCustomerWinner([['anything']], ['apple', 'apple', 'apple', 'banana']))




def largestItemAssociation(pairs):
    groups = []
    for pair in pairs:
        found = False
        for group in groups:
            if pair[0] in group or pair[1] in group:
                group.update(pair)
                found = True
                break
        if not found:
            groups.append(set(pair))
    return sorted(list(max(groups, key=len)))

print(largestItemAssociation([[1, 2], [3, 4], [4, 5]]))
print(largestItemAssociation([[1, 2], [3, 4], [4, 5], [2, 6]]))



def find_unique_substrings(s, k):
    results = set()
    for i in range(len(s) - k):
        sample = s[i:i+k]
        if len(set(sample)) == k:
            results.add(sample)
    print(results)

find_unique_substrings('abcabc', 3)
find_unique_substrings('awaglknagawunagwkwagl', 4)




def count_keywords(k, keywords, reviews):
    counts = {word.lower(): 0 for word in keywords}
    for review in reviews:
        unseen_keywords = set(counts.keys())
        for word in review.split():
            for keyword in unseen_keywords:
                processed_word = ''.join(filter(str.isalpha, word)).lower()
                if keyword == processed_word:
                    counts[keyword] += 1
                    unseen_keywords.remove(keyword)
                    break

    results = sorted([(value, key) for key, value in counts.items()], key=lambda item: (-item[0], item[1]))
    return [r[1] for r in results[:k]]

k = 2
keywords = ["anacell", "cetracular", "betacellular"]
reviews = [
  "Anacell provides the best services in the city",
  "betacellular has awesome services",
  "Best services provided by anacell, everyone should use anacell",
]
print(count_keywords(k, keywords, reviews))


k = 2
keywords = ["anacell", "betacellular", "cetracular", "deltacellular", "eurocell"]
reviews = [
  "I love anacell Best services; Best services provided by anacell",
  "betacellular has great services",
  "deltacellular provides much better services than betacellular",
  "cetracular is worse than anacell",
  "Betacellular is better than deltacellular.",
]
print(count_keywords(k, keywords, reviews))
