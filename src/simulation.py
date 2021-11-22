from src.utils import harbor_active,choose_boat,choose_dock,find_ship_ready
from src.random_vars import exp,normal
import sys



class HarborState:
    def __init__(self) -> None:
        self.waitlist = []
        self.docks = [None]*3     #ship,time
        self.trailer = None     #(ship,time,dock) if empty(None,time)
        self.trailer_in_port = True


class Simulation:
    def __init__(self) -> None:
        self.harbor = HarborState()
        self.ship_times = {}     #total time that ship spends since arrival and departure
        self.ship_total_time = {}
        self.time = 0
        self.trailer_time_to_dock = sys.maxsize
        self.trailer_time_to_port = sys.maxsize
        t0 = exp(1/8) 
        self.arrival_time = t0
        self.dock_time = [sys.maxsize]*3 
        self.depart_dock_time = [sys.maxsize]*3
        self.ship_count = 0
        self.waiting_to_depart = []
        self.T = 24
        
    def run(self):
        while self.time < self.T or harbor_active(self.ship_times):  
             
            if self.arrival_time == sys.maxsize and self.time < self.T and not harbor_active(self.ship_times):
                break
            

            if (self.arrival_time == min(self.arrival_time,self.trailer_time_to_dock,self.trailer_time_to_port, min(self.dock_time),\
                min(self.depart_dock_time))):
                if self.time == 0 and self.arrival_time > self.T:
                    while self.arrival_time > self.T:
                        next_time_arrival = self.time +  exp(1/8)
                        self.arrival_time = next_time_arrival
                
                elif self.arrival_time < self.T:
                    self.ship_count = self.ship_count + 1
                    print('------Ship' ,self.ship_count,'arrived to port------')
                    self.time = self.arrival_time
                    boat = choose_boat()
                    load_time = 0
                    if boat == 'small':
                        load_time = normal(9,1)
                    elif boat == 'medium':
                        load_time = normal(12,2)
                    elif boat == 'large':
                        load_time = normal(18,3)
                
                    

                    self.harbor.waitlist.append(self.ship_count)
                #generating next arrival
                    self.ship_times[self.ship_count] = (self.arrival_time,None)
                    next_time_arrival = self.time +  exp(1/8)
                    self.arrival_time = next_time_arrival 
                else:
                    self.arrival_time = sys.maxsize
                #Checking where is the trailer
                if self.harbor.trailer is None:
                    chosen_dock = choose_dock(self.harbor.docks)
                    if chosen_dock is not None and len(self.harbor.waitlist)>0: 
                        ship = self.harbor.waitlist.pop(0)    #ordenar
                        self.harbor.trailer = (ship,load_time,chosen_dock)
                        if self.harbor.trailer_in_port:      #trailer empty and in port                
                            self.trailer_time_to_dock = self.time
                        else:
                            moving_trailertoport_time = exp(4)
                            self.trailer_time_to_dock = self.time + moving_trailertoport_time                   
                    elif self.harbor.trailer_in_port and len(self.waiting_to_depart)>0:
                        self.dock_time[0] = self.time + exp(4) 
                        
            #Going to dock Event
            elif (self.trailer_time_to_dock == min(self.arrival_time,self.trailer_time_to_dock,self.trailer_time_to_port, min(self.dock_time),\
                min(self.depart_dock_time))):
                self.time = self.trailer_time_to_dock
                self.trailer_time_to_dock = sys.maxsize
                ship,load_time,chosen_dock = self.harbor.trailer
                moving_time = exp(1/2)
                self.dock_time[chosen_dock] = self.time + moving_time
                self.harbor.trailer_in_port = False
                
                print('------Ship ',ship,' leaving for dock ',chosen_dock,'------')

            #Start to load Event
            elif (min(self.dock_time) == min(self.arrival_time,self.trailer_time_to_dock,self.trailer_time_to_port, min(self.dock_time),\
                min(self.depart_dock_time))):
                if self.harbor.trailer is not None:
                    ship,load_time,chosen_dock = self.harbor.trailer
                    print('------Ship ',ship,' loading in dock ',chosen_dock,'------')
                    self.time = self.dock_time[chosen_dock]
                    self.dock_time[chosen_dock] = sys.maxsize
                    self.harbor.trailer = None
                    self.trailer_time_to_dock = sys.maxsize
                    self.trailer_time_to_port = sys.maxsize
                    if len(self.waiting_to_depart) > 0:
                        ship_ready,indx = self.waiting_to_depart.pop(0)
                        to_port_time = exp(1)
                        self.trailer_time_to_port = self.time + to_port_time
                        self.harbor.trailer = (ship_ready,None,None)
                        self.harbor.docks[indx] = None
                    
                    self.harbor.docks[chosen_dock] = ship
                    self.depart_dock_time[chosen_dock] = self.time + load_time
                    
                else:
                    self.time = self.dock_time[0]
                    self.dock_time[0] = sys.maxsize
                    self.harbor.trailer_in_port = False
                    if len(self.waiting_to_depart) > 0:
                        ship_ready,indx = self.waiting_to_depart.pop(0)
                        to_port_time = exp(1)
                        self.trailer_time_to_port = self.time + to_port_time
                        self.harbor.trailer = (ship_ready,None,None)
                        self.harbor.docks[indx] = None

                 
            #Finish load, is depart time   
            elif ((min(self.depart_dock_time) == min(self.arrival_time,self.trailer_time_to_dock,self.trailer_time_to_port, min(self.dock_time),\
                min(self.depart_dock_time))) and (min(self.depart_dock_time) > self.time)):
                self.time = min(self.depart_dock_time)
                if self.harbor.trailer is None:
                    ship,indx = find_ship_ready(self.depart_dock_time,self.harbor.docks)
                    to_port_time = exp(1)
                    print('------Ship ',ship,' leaving to port------')
                    if not self.harbor.trailer_in_port:
                        self.trailer_time_to_port = self.time + to_port_time
                        self.harbor.trailer = (ship,None,None)
                        self.depart_dock_time[indx] = sys.maxsize
                        self.harbor.docks[indx] = None

                    else:
                        moving_trailertoport_time = exp(4)
                        self.trailer_time_to_port = self.time + moving_trailertoport_time + to_port_time 
                        self.harbor.trailer = (ship,None,None)
                        self.depart_dock_time[indx] = sys.maxsize
                        self.harbor.docks[indx] = None
                else:
                    ship,indx = find_ship_ready(self.depart_dock_time,self.harbor.docks)
                    self.waiting_to_depart.append((ship,indx))
                    self.depart_dock_time[indx] = sys.maxsize
            #Ship finished and leaved port
            elif (self.trailer_time_to_port == min(self.arrival_time,self.trailer_time_to_dock,self.trailer_time_to_port, min(self.dock_time),\
                min(self.depart_dock_time))):
                self.time = self.trailer_time_to_port
                self.trailer_time_to_port = sys.maxsize
                self.harbor.trailer_in_port = True
                ship,_,__= self.harbor.trailer
                self.harbor.trailer = None
                start,_ = self.ship_times[ship]
                self.ship_times[ship] = (start,self.time)
                total = self.ship_times[ship][1] - self.ship_times[ship][0] 
                self.ship_total_time[ship] = total
                
                print('------Ship ',ship,' leaves port, total time',total ,'------')
        
        return self.ship_total_time,self.ship_count
