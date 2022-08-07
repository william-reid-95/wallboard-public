#statsGUI by William Reid 12/11/2021

import os
import sys
import csv
import pygame #as pyg

win_x, win_y = 1920, 1080

pygame.init()



pygame.display.set_caption('Wally the Wallboard')

window_surface = pygame.display.set_mode((win_x, win_y))

background = pygame.Surface((win_x, win_y))

background.fill(pygame.Color(0,0,0))

#print(pygame.font.get_fonts())

font = pygame.font.SysFont("calibri.ttf", 24)
icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)

logo = pygame.image.load(r"small.png")
### BODY

pygame.draw.rect(background,(224,224,224),((1375,55),(405,75)))
background.blit(logo,(1385,60))

class Block: # change to function
    def __init__(self,x_pos,y_pos,x_mag,y_mag,string,colour):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_mag = x_mag
        self.y_mag = y_mag
        self.string = string
        self.colour = colour # tuples (r,g,b,alpha (alpha optional))

    def draw(self):
        #draw rectangle
        pygame.draw.rect(background,self.colour,((self.x_pos,self.y_pos),(self.x_mag,self.y_mag)))

        #draw text
        self.text = font.render(self.string,True,(0,0,0)) #(0,0,0) is the colour of the font - black
        background.blit(self.text,(self.x_pos,self.y_pos+4))

row_list = []

class GUI_Row:
    def __init__(self,row_number, row_x, row_y, block_height, block_width, csv_row, is_queue):
        self.row_number = row_number # which row
        self.row_x = row_x # pos x
        self.row_y = row_y
        self.block_height = block_height
        self.block_width = block_width

        self.csv_row = csv_row
        self.is_queue = is_queue


        self.gap = 2
        self.offset_x = 30
        self.offset_y = 0

        self.agent_block = None
        self.activity_block = None
        self.duration_block = None
        self.in_block = None
        self.out_block = None
        self.average_block = None

        row_list.append(self)

        if is_queue: #offset for queue info
            self.offset_x = (self.offset_x + win_x/2+320)
            self.offset_y = 600


        elif row_number >= 40: #if not queue
            self.offset_x = (self.offset_x + win_x/2)-300
            self.offset_y = 988


    def update(self):
        #print(self.csv_row)# this updates live
        if row_number != 1:# not headings
            if row[1] == " On contact":
                self.activity_colour = (51,255,255)#cyan
            elif row[1] == " Available":
                self.activity_colour = (51,255,51)#green
            elif row[1] == " Outbound Call":
                self.activity_colour = (153,51,255)#purple
            elif row[1] == " Training/Coaching":
                self.activity_colour = (255,255,51)#yellow
            elif row[1] == " Ticketing/Research":
                self.activity_colour = (255,153,51)#orange
            elif row[1] == " After contact work":
                self.activity_colour = (255,153,51)#orange
            elif row[1] == " Short Break":
                self.activity_colour = (224,224,224)#light grey
            elif row[1] == " Lunch Break":
                self.activity_colour = (224,224,224)#light grey
            else:
                self.activity_colour = (255,51,51)#red
        else:# if first item i.e. headings, turn grey
            self.activity_colour = (150,150,150)
            self.csv_row[4] = "In"
            self.csv_row[5] = "Out"

        #THESE NEED TO BE FUNCTIONS AS ITS BASICALLY THE SAME THING HAPPENING 6 TIMES, but it does work :)
        if len(self.csv_row) >= 4:
            if self.agent_block == None:# this fixes infinite duplication bug but is a huge pain in this ass
                self.agent_block = Block(self.row_x*0+self.offset_x,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height, self.block_width,self.csv_row[3],self.activity_colour)
                self.agent_block.draw()
            else:
                #UPDATE BLOCK
                self.agent_block.x_pos = self.row_x*0+self.offset_x
                self.agent_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.agent_block.x_mag = self.block_height
                self.agent_block.y_mag = self.block_width
                self.agent_block.string = self.csv_row[3]
                self.agent_block.colour = self.activity_colour
                self.agent_block.draw()

        if len(self.csv_row) >= 2:
            if self.activity_block == None:
                self.activity_block = Block(self.row_x*1+self.offset_x,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height, self.block_width,self.csv_row[1],self.activity_colour)
                self.activity_block.draw()
            else:
                #UPDATE BLOCK
                self.activity_block.x_pos = self.row_x*1+self.offset_x
                self.activity_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.activity_block.x_mag = self.block_height
                self.activity_block.y_mag = self.block_width
                self.activity_block.string = self.csv_row[1]
                self.activity_block.colour = self.activity_colour
                self.activity_block.draw()

        if len(self.csv_row) >= 3:
            if self.duration_block == None:
                self.duration_block = Block(self.row_x*2+self.offset_x,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height, self.block_width,self.csv_row[2],self.activity_colour)
                self.duration_block.draw()
            else:
                #UPDATE BLOCK
                self.duration_block.x_pos = self.row_x*2+self.offset_x
                self.duration_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.duration_block.x_mag = self.block_height
                self.duration_block.y_mag = self.block_width
                self.duration_block.string = self.csv_row[2]
                self.duration_block.colour = self.activity_colour
                self.duration_block.draw()

        if len(self.csv_row) >= 5:
            if self.in_block == None:
                self.in_block = Block((self.row_x*3)-50+self.offset_x,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height-120, self.block_width,self.csv_row[4],self.activity_colour)
                self.in_block.draw()
            else:
                #UPDATE BLOCK
                self.in_block.x_pos = (self.row_x*3)-50+self.offset_x
                self.in_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.in_block.x_mag = self.block_height-120
                self.in_block.y_mag = self.block_width
                self.in_block.string = self.csv_row[4]
                self.in_block.colour = self.activity_colour
                self.in_block.draw()

        if len(self.csv_row) >= 6:
            if self.out_block == None:
                self.out_block = Block((self.row_x*4)-170+self.offset_x,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height-120, self.block_width,self.csv_row[5],self.activity_colour)
                self.out_block.draw()
            else:
                #UPDATE BLOCK
                self.out_block.x_pos = (self.row_x*4)-170+self.offset_x
                self.out_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.out_block.x_mag = self.block_height-120
                self.out_block.y_mag = self.block_width
                self.out_block.string = self.csv_row[5]
                self.out_block.colour = self.activity_colour
                self.out_block.draw()

        if len(self.csv_row) >= 7:
            if self.average_block == None:
                self.average_block = Block((self.row_x*5)-220+self.offset_x,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height, self.block_width,self.csv_row[6],self.activity_colour)
                #self.average_block.draw()
            else:
                #UPDATE BLOCK
                self.average_block.x_pos = (self.row_x*5)-220+self.offset_x
                self.average_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.average_block.x_mag = self.block_height
                self.average_block.y_mag = self.block_width
                self.average_block.string = self.csv_row[6]
                self.average_block.colour = self.activity_colour
                #self.duration_block.draw()



class GUI_Row_Queue:
    def __init__(self,row_number, row_x, row_y, block_height, block_width, csv_row, description):
        self.row_number = row_number # which row
        self.row_x = row_x # pos x
        self.row_y = row_y
        self.block_height = block_height
        self.block_width = block_width

        self.csv_row = csv_row
        self.description = description

        self.gap = 2
        self.offset_x = 140
        self.offset_y = -140

        self.name_block = None
        self.in_queue_block = None

        row_list.append(self)


        self.offset_x = (self.offset_x + win_x/2+320)

        #logic to change colour based on queue volume



        if self.description == 'Title':
            self.activity_colour = (150,150,150)
        else:
            self.activity_colour = (224,224,224)


    def update(self):

        #THESE NEED TO BE FUNCTIONS AS ITS BASICALLY THE SAME THING HAPPENING 6 TIMES, but it does work :)
        if len(self.csv_row) >= 1:
            if self.name_block == None:# this fixes infinite duplication bug but is a huge pain in this ass
                self.name_block = Block(self.row_x*0+self.offset_x,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height, self.block_width,self.description,self.activity_colour)
                self.name_block.draw()
            else:
                #UPDATE BLOCK
                self.name_block.x_pos = self.row_x*0+self.offset_x
                self.name_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.name_block.x_mag = self.block_height
                self.name_block.y_mag = self.block_width
                self.name_block.string = self.description
                self.name_block.colour = self.activity_colour
                self.name_block.draw()

        if len(self.csv_row) >= 4:
            if self.in_queue_block == None:
                self.in_queue_block = Block(self.row_x*1+self.offset_x,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height, self.block_width,self.csv_row[3],self.activity_colour)
                self.in_queue_block.draw()
            else:
                #UPDATE BLOCK
                self.in_queue_block.x_pos = self.row_x*1+self.offset_x
                self.in_queue_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.in_queue_block.x_mag = self.block_height
                self.in_queue_block.y_mag = self.block_width
                self.in_queue_block.string = self.csv_row[3]
                self.in_queue_block.colour = self.activity_colour
                self.in_queue_block.draw()

agent_list = []
queue_list = []


class Agent:
    def __init__(self, is_part_time,email):
        self.is_part_time = is_part_time
        self.email = email

        self.gui_row_instance = None

        agent_list.append(self)

    def agent_row(self, row_number, default_row_x, default_row_y, default_block_width, default_block_height, row):
        if self.gui_row_instance == None:#create row
            self.gui_row_instance = GUI_Row(row_number, default_row_x, default_row_y, default_block_width, default_block_height, row, False)
        else:#update existing row
            self.gui_row_instance.csv_row = row
            self.gui_row_instance.update()

def create_agents():

    agents_heading = Agent(False, 'Agents')
    # FIRST LETTER OF FIRST NAME, LAST NAME
    jpalmer = Agent(False, 'jpalmer42@dxc.com')
    #eknight = Agent(False, 'edward.knight@dxc.com')
    slarge = Agent(False, 'scott.large@dxc.com')
    tlovell = Agent(False, 'tlovell5@dxc.com')
    cparsell = Agent(False, 'cparsell@dxc.com')
    akrasuljak = Agent(False, 'akrasuljak@dxc.com')
    jcourtney = Agent(False, 'jack.courtney2@dxc.com')
    nmcgrath = Agent(False, 'nmcgrath4@dxc.com')
    ahuynh = Agent(False, 'ahuynh25@dxc.com')
    bbiddle = Agent(False, 'brandon.biddle@dxc.com')
    lsumpton = Agent(False, 'liam.sumpton@dxc.com')
    ehall = Agent(False, 'erica.hall@dxc.com')
    abrooks = Agent(False, 'andrew.brooks2@dxc.com')
    anapalan = Agent(False, 'andrian.napalan@dxc.com')
    deastaway = Agent(False, 'daniel.eastaway@dxc.com')
    rhazara = Agent(False, 'rohit.hazara@dxc.com')
    iibarra = Agent(False, 'ian.ibarra@dxc.com')
    klisson = Agent(False, 'kate.lisson@dxc.com')
    lhenry = Agent(False, 'laura.henry@dxc.com')
    dfindlay = Agent(False, 'debra.findlay@dxc.com')
    jyeoh = Agent(False, 'jef.yeoh@dxc.com')
    hthresher = Agent(False, 'harold.thresher2@dxc.com')
    kwhishwilson = Agent(False, 'kate.whishwilson@dxc.com')
    sdobber = Agent(False, 'stefan.dobber@dxc.com')
    tphoa = Agent(False, 'tiansoon.phoa@dxc.com')
    zye = Agent(False, 'zhongmin.ye@dxc.com')
    cwu = Agent(False, 'chunyi.wu@dxc.com')
    jallentanner = Agent(False, 'jesse.allentanner@dxc.com')
    tkerslake = Agent(False, 'tyler.kerslake@dxc.com')
    breid = Agent(False, 'bill.reid@dxc.com')
    jboost = Agent(False, 'joshua.boost@dxc.com')
    nmclean = Agent(False, 'nicholas.mclean2@dxc.com')
    chamilton = Agent(False, 'chris.hamilton@dxc.com')
    xbrett = Agent(False, 'xander.brett@dxc.com')
    zli = Agent(False, 'zhipeng.li@dxc.com')
    hyoung = Agent(False, 'hugh.young@dxc.com')
    tsheppard = Agent(False, 'tanisha.sheppard@dxc.com')
    sknevett = Agent(False, 'seb.knevett@dxc.com')
    uvazeele = Agent(False, 'ubadha.vazeele@dxc.com')
    msu = Agent(False, 'majuan.su@dxc.com')
    mkumari = Agent(False, 'manosha.kumari@dxc.com')
    njackimowicz = Agent(False, 'nick.jackimowicz@dxc.com')
    ntafurt = Agent(False, 'nicolas.tafurt@dxc.com')
    nshen = Agent(False, 'ningyuan.shen@dxc.com')
    rbyard = Agent(False, 'rhys.byard@dxc.com')
    arobertshaw = Agent(False, 'amie.robertshaw@dxc.com')
    xander_b = Agent(False, 'declan.bridge2@dxc.com')
    dbridge = Agent(False, 'duane.dermody2@dxc.com')
    ochivers = Agent(False, 'owen.chivers2@dxc.com')
    rsingh = Agent(False, 'robin.singh2@dxc.com')
    acooper = Agent(False, 'acooper27@dxc.com')
    dbenson = Agent(False, 'daniel.benson@dxc.com')
    dmcdougall2 = Agent(False, 'david.mcdougall2@dxc.com')
    hxia = Agent(False, 'haifeng.xia@dxc.com')
    jveldhuis2 = Agent(False, 'jack.veldhuis2@dxc.com')
    jrussell2 = Agent(False, 'joshua.russell2@dxc.com')
    tmunster2 = Agent(False, 'tarryd.munster2@dxc.com')
    zobrien2 = Agent(False, 'zoe.obrien2@dxc.com')
    asalvatierra = Agent(False, 'adriana.salvatierra@dxc.com')
    jvaletich = Agent(False, 'jack.valetich@dxc.com')
    dsingh9 = Agent(False, 'deepak.singh9@dxc.com')
    ssmart = Agent(False, 'sophie.smart@dxc.com')

create_agents()


class Queue:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.amount = 0

        self.gui_queue_instance = None

        queue_list.append(self)
        print("added " + self.name)

    def queue_row(self, row_number, default_row_x, default_row_y, default_block_width, default_block_height, row):
        if self.gui_queue_instance == None:#create row
            self.gui_queue_instance = GUI_Row_Queue(row_number, default_row_x, default_row_y, default_block_width, default_block_height, row, self.description)
        else:#update existing row
            self.gui_queue_instance.csv_row = row
            self.gui_queue_instance.update()

def create_queues():
    # queue headings
    queue_heading = Queue('Queue','Title')
    queue_total = Queue('Total','NULL')

    # queues
    queue_Pwd = Queue('CBA Desktop Pwd','Password')
    queue_Hardware = Queue('CBA Desktop Hardware New','Desktop')
    queue_CommSee = Queue('CBA Desktop CommSee New','CommSee')
    queue_Apps = Queue('CBA Desktop Business Apps New','Bank Apps')

create_queues()

default_row_x = 180
default_row_y = 24

default_block_width = 180
default_block_height = 24

queue_default_row_x = 160
queue_default_block_width = 160

is_running = True

queue_enabled = True
agents_enabled = True

agents_csv_path = r"Agents.csv"
queue_csv_path = r"Queue.csv"

clock = pygame.time.Clock()

refresh_time = 4 # seconds
tick_rate = 6 #ticks per second
timer = 0

while is_running:
    clock.tick(tick_rate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window_surface.blit(background, (0, 0))
    pygame.draw.rect(background,(1+(5*timer),20,100),((20,1000),(72*(timer+1),40)))

    if timer >= (tick_rate * refresh_time):
        timer = 0


        if(agents_enabled):
            #print("- opening agents.csv file success = " + str(os.access(agents_csv_path, os.R_OK)))
            if os.access(agents_csv_path, os.R_OK):
                try:
                    with open(agents_csv_path, newline='') as f:
                        reader = csv.reader(f)
                        # next(reader) uncomment to remove headings
                        row_number = 1
                        for row in reader:
                            for agent in agent_list:
                                if row[0] == agent.email: #if email adress in row matches agent email

                                    #create or update agent's GUI row
                                    agent.agent_row(row_number, default_row_x, default_row_y, default_block_width, default_block_height, row)

                            row_number += 1

                except:
                    print("- cannot read agents.csv, file being updated\n" )



        if(queue_enabled):
            #print("- opening queue.csv file success = " + str(os.access(queue_csv_path, os.R_OK)))
            if os.access(queue_csv_path, os.R_OK):
                try:
                    with open(queue_csv_path, newline='') as f:
                        queue_reader = csv.reader(f)
                        # next(reader) uncomment to remove headings
                        queue_row_number = 1
                        for queue_row in queue_reader:
                            for queue in queue_list:
                                if queue_row[0] == queue.name:
                                    # print("match found for queue: " + str(queue_row_number) + " - " + queue.name)
                                    queue.queue_row(queue_row_number, queue_default_row_x, default_row_y, queue_default_block_width, default_block_height, queue_row)

                            #logic for bliting queue info
                            queue_row_number += 1

                except:
                    print("- cannot read queue.csv, file being updated\n" )


    timer += 1
    print(str(timer) + " / " +str(tick_rate * refresh_time))

    pygame.display.update()

    #print(len(row_list))
