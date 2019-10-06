import sys
import requests
import time




def funcGuessWord(wordit, listOfWords, token, hangManGame, letterFreq, usedLetters):
    words = hangManGame['state'].split()
    word = words[wordit].lower()
    while '_' in word:
        print(word)

        for key in letterFreq: # reset all remaining possible letters to count 0
            letterFreq[key] = 0
            print (key)

        for posWord in listOfWords: # go through all words remaining in list
            valid = True

            if len(posWord) == len(word):# if the size of the possible word is equal to size of the word we are guessing
                for x in range(len(word)): # iterate through word we are guessing and check that all known letters match
                    if word[x] != '_' and word[x] != posWord[x]:
                        valid = False
                        break
                if valid: # if they match check if all unknown letters are not already guessed
                    for x in range(len(word)):
                        if word[x] == '_':
                            if posWord[x] in usedLetters:
                                valid = False
                                break

            else:
                valid = False

            if not valid: # if any condition is not satisfied remove the word from the list so we do not hit it again
                listOfWords.remove(posWord)

            if valid: # if constraints are satisfied find the first unknown letter in our word and increment the
                # corresponding letter in the possible word
                for x in range(len(posWord)):
                    if word[x] == '_':
                        letterFreq[posWord[x]] = letterFreq[posWord[x]] + 1
                print(posWord)

        max = -1
        letter = '_'

        #go through all keys and take the max and guess that one
        for key in letterFreq:
            if letterFreq[key] > max:
                letter = key
                max = letterFreq[key]
        letterFreq.pop(letter)
        usedLetters.append(letter)
        print(token)
        print(letter)
        while 1:
            hangManGame = requests.post('http://gallows.hulu.com/play?code=atalpade@umich.edu&token=%s&guess=%s' % (str(token), str(letter)))
            if hangManGame.status_code == 200:
                break
            time.sleep(5)  # Delays for 5 seconds. You can also use a float value.
        hangManGame = hangManGame.json()
        print(hangManGame)
        words = hangManGame['state'].split()
        word = words[wordIt].lower()
        if hangManGame['status'] == "DEAD" or hangManGame['status'] == 'FREE':
            return hangManGame
            break
    return hangManGame


if __name__ == "__main__":
    print('%s will run %d games' % (sys.argv[1], int(sys.argv[2])))
games = int(sys.argv[2])
listOfW = [line.rstrip('\n') for line in open("1-1000.txt")]
for i in range(games):
    letterFreq = {'e': 0, 't': 0, 'a': 0, 'o': 0, 'i': 0, 'n': 0, 's': 0, 'r': 0, 'h': 0, 'l': 0, 'd': 0, 'c': 0,
                  'u': 0, 'm': 0, 'f': 0, 'p': 0, 'g': 0, 'w': 0, 'y': 0, 'b': 0, 'v': 0, 'k': 0, 'x': 0, 'j': 0,
                  'q': 0, 'z': 0}
    usedLetters = []
    response = requests.get('http://gallows.hulu.com/play?code=atalpade@umich.edu')
    hangManGame = response.json()
    token = hangManGame['token']
    words = hangManGame['state'].split()
    wordIt = 0
    while (hangManGame['status'] != "DEAD" or hangManGame['status'] != 'FREE') and wordIt != len(words):
        listOfWords = listOfW.copy()
        print(len(listOfWords))
        hangManGame = funcGuessWord(wordIt, listOfWords, token, hangManGame, letterFreq, usedLetters)
        wordIt=wordIt+1
    print("success!")


# func to Parse string out to words put words in list
# Pass in one word to func which will guess letters based on the most common letter for the word thus far
# go on to next word and continue
