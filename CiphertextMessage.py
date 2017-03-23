import string

#This program uses the Caesar Cipher method of encryption
#Scroll to the bottom of the page to see how it is tested

#you can create a hidden message by : plaintext = PlaintextMessage('hello', 2)
#Where 2 is the number of letters shifted

#you can see when you use CiphertextMessage that you no longer need the shift
#This is because the program tries all 26 possible outputs and chooses the best
#translation

def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string(fileName):
    """
    Returns: a story in encrypted text.
    """
    f = open(fileName, "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

def save_story_string(fileName,storyString):
    """
    Returns: your encrpyted text
    """
    f = open(fileName, "w")
    print(storyString,file=f)
    f.close()


def decrypt_story(storyString):
    #Loads story from file and decrypts it
    aStory = get_story_string(storyString)
    aMessage = CiphertextMessage(aStory)
    aTuple = aMessage.decrypt_message()
    return aTuple

def encrypt_story(storyString,shift):
    aStory = get_story_string(storyString)  
    aMessage = PlaintextMessage(aStory,shift)
    save_story_string("output.txt", aMessage.get_message_text_encrypted())
    print("Story Saved to output.txt")
    
class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        letters = string.ascii_lowercase + string.ascii_uppercase
        letterDic = {}
        middle = len(letters)//2
        #increment string of ascii character and apply shift
        for i in range(0,middle):
            #if we have gone past the lenth of the characters start at beginning
            if i + shift < middle:
                letterDic[letters[i]] = letters[i+shift] 
                letterDic[letters[i + middle]] = letters[i + middle + shift]
            else:
                letterDic[letters[i]] = letters[i - middle + shift]
                letterDic[letters[i + middle]] = letters[i + middle - middle + shift]
        return letterDic
        
                
        

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        #get message without altering
        theMessage = self.get_message_text()
        newMessage = ''
        mDict = self.build_shift_dict(shift)
        #Create new message using the dictionary, skipping letters not inside
        for i in theMessage:
            if i in mDict:
                newMessage += mDict[i]
            else:
                newMessage += i
        return newMessage

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less 
        code is repeated
        '''
        Message.__init__(self, text)
        self.text = text
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(self.get_shift())
        
    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class
        
        Returns: a COPY of self.encrypting_dict
        '''
        return dict(self.encrypting_dict)

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        PlaintextMessage.__init__(self, self.get_message_text(), shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        #Break up the text by the spaces
        best = 0
        currentScore = 0
        holdS = 0
        for s in range(0,26+1):
            newMessage = self.apply_shift(s)
            textList = newMessage.split(' ')
            #now step through list
            for w in textList:
                if is_word(self.valid_words, w):
                    currentScore += 1
            #now if that decode was best
            if currentScore >= best:
                best = currentScore
                holdS = s
            #reset some terms
            currentScore = 0
        #now apply the best version

        bestMessage = self.apply_shift(holdS)
        return (holdS, bestMessage)
            

#Example test case (PlaintextMessage)
#==============================================================================
plaintext = PlaintextMessage('hello', 2)
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.get_message_text_encrypted())
     
#Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq')
print('Expected Output:', (24, 'hello'))
print('Actual Output:', ciphertext.decrypt_message())

#Example now decipher a story
print(decrypt_story("story.txt"))

encrypt_story("plainStory.txt",5)#reads story and shifts by number 
#==============================================================================
