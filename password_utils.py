# -*- coding: utf-8 -*-
"""
Random Password Generator of n-characters length (n is input by user)
"""

import random

class Password():
    alpha = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    num = "1234567890"
    sym = """!@#$%&*()_+-=[]<>."?/"""
    
    @staticmethod
    def generate_secure_random_password(n=12):
        chars = Password.alpha + Password.num + Password.sym
        sec_obj = random.SystemRandom()
        passwd = ""
        for i in range(n):
            passwd += sec_obj.choice(chars)
        return(passwd)
    
    @staticmethod
    def generate_secure_password(n=12):
        sec_obj = random.SystemRandom()
        if(n<7):
            passwd = Password.generate_secure_random_password(n)
        else:
            # n is being divided strategically into n1, n2, and n3, with the division proportion being random, such that each of alphabets, numbers and symbols occurs at least once, but their no of occurrences vary each time, with random proportion.
            n1 = random.randint(2,n-3)
            n2 = random.randint(1,n-n1-1)
            # n1 = int(n//2)                           
            # n2 = int(n1//2)+1                        
            n3 = n-n1-n2
            passwd = ""
            for i in range(n1): #Takes n1 number of characters from alphabet set alpha, and concatenates it to main string passwd
                passwd += sec_obj.choice(Password.alpha)
            for i in range(n2):   #Takes n2 number of characters from digit set num, and appends it to main string passwd
                passwd += sec_obj.choice(Password.num)
            for i in range(n3):   #Takes n3 number of characters from symbol set sym, and appends it to main string passwd
                passwd += sec_obj.choice(Password.sym)
            passwd = sec_obj.sample(passwd,n)           #Shuffles all the characters obtained in the string randomly, so that the alphabet then number then symbol sequence is intermixed
            passwd = "".join(passwd)                    #Joins all the characters in the list to form a string
        return(passwd)


  
