def sqrt(n):
    lastGuess=n
    while True:
        nextGuess=(lastGuess+n/lastGuess)/2
        if abs(nextGuess-lastGuess)<=0.0001:
            break
        else:
            lastGuess=nextGuess
    return nextGuess
    

