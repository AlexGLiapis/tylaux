answer = input('Enter a word:\n')

print('Word length is ', len(answer))

guess = input('Enter a guess:\n')

guessct = 0
while guess != answer:
    
    dblchk = ''
    if(guessct > 0):
        print(guessct, ' turns taken. ', end='')
        guess = input('Try again:\n')
    guessct+=1 
    if len(guess) != len(answer):
        guess = input('Guess is not the same length as answer. Try again:\n')
        guessct-=1
    else:
        for x, y in zip(answer, guess):
            if x == y:
                print(y, ' is green')
            else:
                dblchk = dblchk + y
                
        for x in answer:
            for y in dblchk:
                if x==y:
                    print(y, ' is yellow')
                    dblchk = dblchk.replace(y,'',1)
        for x in dblchk:
            print(x, ' is black')
