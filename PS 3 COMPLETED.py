# 6.0001 Problem Set 3
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
# Name          : <Mahir KAYA>



import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


WORDLIST_FILENAME = "words.txt"
#==============================================================================
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq




# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word=word.lower()
    first_element=0
    
    for k in word:
        if k!="*":
            first_element+=SCRABBLE_LETTER_VALUES[k]                
    second_element=(7*(len(word))-3*(n-len(word)))
    if second_element<1:
        
        second_element=1
    score=second_element*first_element
    return score


# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    s=''
    for letter in hand.keys():
        for j in range(hand[letter]):
             s+=letter+' '     
        return s

                       
def anti_display(hand):
    anti_hand={}
    alphabet=string.ascii_letters
    for t in hand:
        
        if t in alphabet or t=='*': 
            if hand.count(t)>1:
                anti_hand.update({t:hand.count(t)})
            else:
                anti_hand.update({t:1})
    return anti_hand        
# Make sure you understand how this function works and what it does!

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    hand2=display_hand(hand)
    s=random.choice(hand2)
    while s not in VOWELS:
        s=random.choice(hand2)
    
    if hand[s]<=1:
        
        del hand[s]
        hand.update({'*':1})
    else:
        hand[s]=hand[s]-1
        hand.update({'*':1})
    hand=display_hand(hand)
    if calculate_handlen(anti_display(hand))!=n:
        print('ERROR')
    return (hand)

def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    hand2=hand.copy()
    word=word.lower()
    
    for e in word:
        if e in hand2:
            hand2[e]=hand2[e]-1  
            if hand[e]<=0:
                hand[e]=0
    
    return(hand2)


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word=word.lower()
    index=word.find('*')
    words_with_joker=[]
    art=''
    art2=[]
    art3=[]
    passed_words=[]
    if '*' not in hand:
        if word in word_list:

            for t in word:
                if t in hand:
                    if word.count(t)<=hand[t]:
                        art2.append(t)
            result2=all(elem in art2 for elem in word)
            if result2:
                return True
            else:
                
                return False
#end of part 1
    
    if '*'  in hand:
        if '*' not in word:
            if word in word_list:

                for t in word:
                    if t in hand:
                        if word.count(t)<=hand[t]:
                            art3.append(t)
            result3=all(elem in art3 for elem in word)
            if result3:
                return True
            else:
                
                return False    
    
    if "*" in hand:
        if "*" in word:
            for e in VOWELS:
                if e!='*':
                    word=list(word)
                    word[index]=e
                    word=''.join(word)
                    words_with_joker.append(word)
    for s in words_with_joker:
    
        if s in word_list:
            passed_words.append(s)
    if len(passed_words)==0:
        return False
    else:
        
        for t in passed_words:
            if t in word_list:
                for s in t:
                    if s!=t[index]:
                        if s in hand:
                            if word.count(s)<=hand[s]:
                                art+=s
                            word=list(word)
    
    word[index]=''
    word=''.join(word)  
    result=all(elem in art for elem in word)

    if result:

        return True
    else:
        return False

def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """

        
    result=0
    for t in hand:
        result+=hand[t]

    return result
total_score=0

def play_hand(hand, word_list,total_score):
    

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    print('Current hand:', hand)
    a= input("enter a word or '!!' to indicate that you are finished:")
    hand=anti_display(hand)
    while a!="!!":

       
            if is_valid_word(a, hand, word_list)==True:
                x=get_word_score(a, calculate_handlen(hand))
                hand=update_hand(hand, a)
                print('current hand:', display_hand(hand))
    
                total_score+=x
                
                
                
                if len(display_hand(hand))==0:
                    print(a+' '+'earned'+' '+ str(x)+' '+ 'points.' )
                    
                    print('ran out of letters. Total score:', total_score)
                    break
                else:    
                    print('current hand:', display_hand(hand))
                    print('total score:', total_score)
                    a=input("enter a word or '!!' to indicate that you are finished:")
                    
            else:
                
                hand=update_hand(hand,a)
                print('Current hand:',display_hand(hand))
                if len(display_hand(hand))==0:
                    print('ran out of letters. Total score:', total_score)
                    break
                else:    
                    a=input('That is not a valid word, please choose another:')
            
    if a=='!!':
        print('END OF HAND')
        return(total_score)
    return(total_score)

    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
#    alphabet=string.ascii_lowercase
#    print(alphabet)
#    alphabet2=list(alphabet)
#    alphabet2.remove(letter)
#
#
#    alphabet=''.join(alphabet2)
#    print(alphabet)           
    alphabet=string.ascii_lowercase
    alphabet=alphabet.replace(letter,'')
    for t in alphabet:
        if t in hand:
            alphabet=alphabet.replace(t,'')
    x=random.choice(alphabet)
            
    if letter in hand:

        hand=display_hand(hand)
        for t in hand:
            
            
            if t==letter:
                hand=hand.replace(letter,x)
        hand=anti_display(hand)
        return(display_hand(hand))
    else:
        hand=hand
        return(display_hand(hand))
            
total_score_overall=0
def play_game(word_list, total_score_overall):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    a=input('Enter a total number of hands:')
    a=int(a)
    HAND_SIZE=input('Please enter hand size:')
    HAND_SIZE=int(HAND_SIZE)
    hand=deal_hand(HAND_SIZE)     
    
    
    hand2=anti_display(hand)
    print(hand)
    substituer=input('Would you like a substitute letter:')
#    while substituer!='yes' or 'no':
##        print('please enter yes or no:')
#        substituer=input('Would you like a substitute letter:')
#    if substituer=='yes':
#            break
#        if substituer=='no':
#            break
        
    if substituer=='yes':
        
        s10=input('Which letter would you like to replace:')
        hand=substitute_hand(hand2,s10)
        k=0
        while k<a:
            
            total_score_overall+=play_hand(hand, word_list,total_score) 
            t=input('would you like to replay the hand?')
            if t=='no':
                k+=1
            if t=='yes':
                k=k
            print('k:',k)
            if k>=a:
                return 'total score overall:',total_score_overall
            
            
            
            while t=='yes':
                    if k>=a:
                        return 'total score overall:',total_score_overall
                    hand=hand
                    
                    
                    total_score_overall+=play_hand(hand, word_list, total_score)
                    print('total score overall:', total_score_overall)
                    
                    if t=='no':
                        k+=1    
                    t=input('would you like to replay the hand?')
                    if t=='no':
                        k+=1
            while t=='no':
                    if k>=a:
                        return 'total score overall:',total_score_overall  
                    hand=deal_hand(HAND_SIZE)
                    print('current hand:', hand)
                    
                    r=input('Would you like a substitute letter:')
                    if r=='yes':
                        s4=input('which letter would you like to replace:')
                        hand=substitute_hand(anti_display(hand),s4)
                    

                    total_score_overall+=play_hand(hand, word_list, total_score)
                    print(total_score_overall)

                    t=input('would you like to replay the hand?')    
                    if t=='no':
                        k+=1
            while t!='yes' and t!='no':
                k=k
                print('Please enter yes or no')
                t=input('would you like to replay the hand?')


    if substituer=='no':

                   
        


        s=0
        while s<a:
            
            total_score_overall+=play_hand(hand, word_list,total_score) 
            t=input('would you like to replay the hand?')
            if t=='no':
                s+=1
            if t=='yes':
                s=s
            print('s:',s)
            if s>=a:
                return 'total score overall:',total_score_overall
            
            
            
            while t=='yes':
                    if s>=a:
                        return 'total score overall:',total_score_overall
                    hand=hand
                    
                    
                    total_score_overall+=play_hand(hand, word_list, total_score)
                    print('total score overall:', total_score_overall)
                    print(s)

                    t=input('would you like to replay the hand?')
                    if t=='no':
                        s+=1
            while t=='no':
                    if s>=a:
                        return 'total score overall:',total_score_overall    
                    hand=deal_hand(HAND_SIZE)
                    print('current hand:', hand)
                    
                    r=input('Would you like a substitute letter:')
                    if r=='yes':
                        s2=input('which letter would you like to replace:')
                        hand=substitute_hand(anti_display(hand),s2)
                    

                    total_score_overall+=play_hand(hand, word_list, total_score)
                    print(total_score_overall)

                    t=input('would you like to replay the hand?')    
                    if t=='no':
                        s+=1
            while t!='yes' and t!='no':
                s=s
                print('Please enter yes or no')
                t=input('would you like to replay the hand?')



                

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    print(play_game(word_list, total_score_overall)) 
#
