# Write your code here
import random

class game():
    
    command_set = ['scissors', 'rock', 'paper']
    
    def __init__(self):
        print('Enter your name:')
        input_name = input()
        print(f'Hello, {input_name}')
        # set user name
        self.user_name = input_name
        self.rating = 0
        self.rules =[]
        # read the file
        with open('rating.txt', 'r') as f:
            line = f.readline()
            while line:
                (name, score) = line.strip().split()
                # found user in list?
                if name == input_name:
                    self.rating = int(score)
                line = f.readline()
            f.close()

    def define_rules(self):
        rules = input()
        self.rules = rules.strip().split(",")
        print("Okay, let's start")
        #call play method
        self.play()


    
    def play(self):
        # play default rules
        if len(self.rules) == 1:
            self.rps()
        # play customized rules
        else:
            self.customized()

    def customized(self):
        #print('play with customized rules')
        #play customized rules
        while True:
            command = input()
            if command in self.rules:
                self.interaction_with_custommized(command)
            elif command == '!exit':
                # exit the game
                print('Bye!')
                break
            elif command == '!rating':
                print(f'Your rating: {self.rating}')
            else:
                print('Invalid input')

    def interaction_with_custommized(self,command):
        # get the command index in rules
        idx = self.rules.index(command)
        # init a new list to order the option
        order = []
        # add last half
        order = order + self.rules[idx + 1:]
        # add the option in front of the command
        order = order + self.rules[0:idx]

        # computer ge a random choice
        computer_option = random.choice(self.rules)
        #print(f'win set {order[0:int(len(order)/2+1)]}')
        #print(f'lose set {order[int(len(order)/2 + 1):]}')
        # draw
        if command == computer_option:
            print(f'There is a draw {command}')
            # add 50 point
            self.rating = self.rating + 50
        elif order.index(computer_option) >= (0.5 *len(order)):
            print(f'Well done. The computer chose {computer_option} and failed')
            # add 100 point
            self.rating = self.rating + 100
        else:
            print(f'Sorry, but the computer chose {computer_option}')

    def rps(self):
        #print('play with customized rules')
        #play rps
        #decided the result in this round
        while True:
            command = input()
            if command in game.command_set:
                self.interaction(command)
            elif command == '!exit':
                 # exit the game
                print('Bye!')
                break
            elif command == '!rating':
                print(f'Your rating: {self.rating}')
            else:
                print('Invalid input')
        
    def interaction(self, command):
        # result [0,3)
        result = random.random()*3
        
        if result < 1:
            self.player_win(command)
        elif (result >= 1) and (result < 2 ):
            self.draw(command)
        else:
            self.player_loss(command)
    
    def player_win(self,command):
        if command == 'scissors':
            print('Well done. The computer chose paper and failed')
        elif command == 'rock':
            print('Well done. The computer chose scissors and failed')
        elif command == 'paper':
            print('Well done. The computer chose rock and failed')      
        # add 100 point
        self.rating = self.rating + 100 
            
    def draw(self,command):
        if command == 'scissors':
            print('There is a draw (scissors)')
        elif command == 'rock':
            print('There is a draw (rock)')
        elif command == 'paper':
            print('There is a draw (paper)')   
        # add 100 point
        self.rating = self.rating + 50          
    

    def player_loss(self,command):
        if command == 'scissors':
            print('Sorry, but the computer chose rock')
        elif command == 'rock':
            print('Sorry, but the computer chose paper')
        elif command == 'paper':
            print('Sorry, but the computer chose scissors')       
                
play = game()
play.define_rules()
