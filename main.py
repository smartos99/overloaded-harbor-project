from src.simulation import Simulation

def run_several_simulations(n):
    average = 0
    for i in range(n):
        s = Simulation()
        ship_info,total = s.run()
        count = 0
        for ship in ship_info.keys():
            count+= ship_info[ship]
        average += count/total
    print('--------------------------------------')
    print('AVERAGE: ',average/n)
    print('--------------------------------------')
        

def main():
    
    s = Simulation()
    ship_info,total = s.run()
    count = 0
    for ship in ship_info.keys():
        count+= ship_info[ship]
    
    average = count/total
    print('--------------------------------------')
    print('AVERAGE: ',average)
    print('--------------------------------------')     
    #run_several_simulations(10)   
    
    
if __name__ == '__main__':
    main()
    
