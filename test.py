import os

sessions = next(os.walk('sessions/'), (None, None, []))[2]

def find_letter(letter, lst):
    for word in lst:
        if letter in word:
            str = word
    print(str)
    return any(letter in word for word in lst)

if find_letter('309424939', sessions) == True:
    print('Крут')
print(sessions)