# Write your code here
class cofee_machine():
    def __init__(self):
        self.water= 400
        self.milk = 540
        self.beans= 120
        self.cups = 9
        self.money = 550
    
    def machine_set(self):
        print('Write how many ml of water do you want to add:')
        self.water+= int(input())
        print('Write how many ml of milk do you want to add:')    
        self.milk+= int(input())
        print('Write how many grams of coffee beans do you want to add:')
        self.beans+= int(input())
        print('Write how many disposable cups of coffee do you want to add:')
        self.cups+= int(input())
    
    def resource_check(self, water_need, mike_need, beans_need):
        # return False if no enough resource
        if self.water < water_need:
            print('Sorry, not enough water!')
            return False
        elif self.milk <mike_need:
            print('Sorry, not enough milk!')
            return False
        elif self.beans < beans_need:
            print('Sorry, not enough coffee beans!')
            return False
        elif self.cups < 1:
            print('Sorry, not enough disposable cups!')
            return False
        # return True id enough resource
        else:
            print('I have enough resources, making you a coffee!')
            return True
    
    def buy(self):
        print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
        command = input()
        if (command == '1') and (self.resource_check(250,0,16)): 
            # epresso
            self.water -= 250
            self.beans -= 16
            self.money += 4
            self.cups -= 1
        elif (command == '2') and (self.resource_check(350,75,20)):
            # latter
            self.water -= 350
            self.milk -= 75
            self.beans -=20
            self.money +=7
            self.cups -= 1
        elif (command == '3') and (self.resource_check(200,100,12)):
            #cappuccino
            self.water -= 200
            self.milk -= 100
            self.beans -= 12
            self.money += 6
            self.cups -= 1
        elif command == 'back':
            return
        
        #need a cup for every coffee
        
                
    def take(self):
        print(f'I gave you ${self.money}')
        self.money = 0
        
    def current_state(self):
        print('The coffee machine has:')
        print(f'{self.water} of water')
        print(f'{self.milk} of milk')
        print(f'{self.beans} of coffee beans')
        print(f'{self.cups} of disposable cups')
        print(f'{self.money} of money') 
        
    def capticy_confirm(self):
        max_cups = min(int(self.water/200),int(self.milk/50),int(self.beans/15))
        print('Write how many cups of coffee you will need:')
        num=int(input())
            
        if max_cups==num:
            print('Yes, I can make that amount of coffee')
        elif max_cups>num:
            print(f'Yes, I can make that amount of coffee (and even {max_cups-num} more than that)')
        else:
            print(f'No, I can make only {max_cups} cups of coffee')
    
    def interactive(self,command):   
        # take command 
        if command == 'fill':
            self.machine_set()
        elif command == 'buy':
            self.buy()
        elif command== 'take':
            self.take()   
        elif command == 'remaining':
            # show current state
            self.current_state()
        
def require_coffee(): 
    print('Write how many cups of coffee you will need:')
    
    num=int(input())
    water= 200*num
    milk = 50*num
    beans=15*num
    
    print(f'For {num} cups of coffee you will need:)')
    print(f'{water} ml of water')
    print(f'{milk} ml of milk')
    print(f'{beans} g of coffee beans')
    
def stage3_test():
    machine = cofee_machine()
    machine.machine_set()
    machine.capticy_confirm()

def stage5_test():
    machine = cofee_machine()
    while True:
        command = input()
        if command == 'exit':
            break
        else:
            machine.interactive(command)
            
#require_coffee()

stage5_test()