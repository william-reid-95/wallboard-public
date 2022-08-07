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

pygame.draw.rect(background,(224,224,224),((1445,55),(405,75)))
background.blit(logo,(1455,60))

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
            self.offset_y = 650


        elif row_number >= 40: #second row of agents
            self.offset_x = (self.offset_x + win_x/2)-250
            self.offset_y = 988

    def update(self):
        #print(self.csv_row)# this updates live
        if row_number != 1:# if not first row (headings), change colour of row based on activity
            if self.csv_row[1] == " On contact":
                self.activity_colour = (51,255,255)#cyan
            elif self.csv_row[1] == " Available":
                self.activity_colour = (51,255,51)#green
            elif self.csv_row[1] == " Incoming":
                self.activity_colour = (51,255,51)#green
            elif self.csv_row[1] == " Outbound Call":
                self.activity_colour = (153,51,255)#purple
            elif self.csv_row[1] == " Training/Coaching":
                self.activity_colour = (255,255,51)#yellow
            elif self.csv_row[1] == " Meetings/Huddles":
                self.activity_colour = (255,255,51)#yellow
            elif self.csv_row[1] == " Projects (Internal)":
                self.activity_colour = (255,255,51)#yellow
            elif self.csv_row[1] == " Missed":
                self.activity_colour = (255,153,51)#orange
            elif self.csv_row[1] == " Ticketing/Research":
                self.activity_colour = (255,153,51)#orange
            elif self.csv_row[1] == " After contact work":
                self.activity_colour = (255,153,51)#orange
            elif self.csv_row[1] == " Short Break":
                self.activity_colour = (224,224,224)#light grey
            elif self.csv_row[1] == " Lunch Break":
                self.activity_colour = (224,224,224)#light grey
            elif self.csv_row[1] == " Comfort Break":
                self.activity_colour = (224,224,224)#dark grey
            elif self.csv_row[1] == " Offline Tasks":
                self.activity_colour = (255, 0, 255)#pink
            elif self.csv_row[1] == " System Down":
                self.activity_colour = (255, 0, 255)#pink
            elif self.csv_row[1] == " Offline":
                self.activity_colour = (255,51,51)#red
            else:
                self.activity_colour = (255,51,51)#red
                #TODO: ADD LOGIC TO DELETE ROW IF AGENT IS OFFLINE FOR > 10 MINUTES
                #flag_for_removal()


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
                self.duration_block.x_mag = self.block_height-50
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
                self.average_block = Block((self.row_x*5)-290+self.offset_x,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height-100, self.block_width,self.csv_row[6],self.activity_colour)
                self.average_block.draw()
            else:
                #UPDATE BLOCK
                self.average_block.x_pos = (self.row_x*5)-290+self.offset_x
                self.average_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.average_block.x_mag = self.block_height-100
                self.average_block.y_mag = self.block_width
                self.average_block.string = self.csv_row[6]
                self.average_block.colour = self.activity_colour
                self.average_block.draw()



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
        self.offset_y = -168

        self.name_block = None
        self.in_queue_block = None
        self.queued_block = None

        self.SLA_block = None


        row_list.append(self)


        self.offset_x = (self.offset_x + win_x/2+320)+50

        #TODO: logic to change colour based on queue volume

        if self.description == 'Queues':
            self.activity_colour = (150,150,150)
        else:
            self.activity_colour = (224,224,224)


    def update(self):
        if self.description == 'Queues':
            self.csv_row[3] = " In"
            self.csv_row[5] = " Total"
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
                self.in_queue_block = Block(self.row_x*1+self.offset_x,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height-100, self.block_width,self.csv_row[3],self.activity_colour)
                self.in_queue_block.draw()
            else:
                #UPDATE BLOCK
                self.in_queue_block.x_pos = self.row_x*1+self.offset_x
                self.in_queue_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.in_queue_block.x_mag = self.block_height-100
                self.in_queue_block.y_mag = self.block_width
                self.in_queue_block.string = self.csv_row[3]
                self.in_queue_block.colour = self.activity_colour
                self.in_queue_block.draw()

        if len(self.csv_row) >= 6:
            if self.queued_block == None:
                self.queued_block = Block(self.row_x*2+self.offset_x-100,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height-80, self.block_width,self.csv_row[5],self.activity_colour)
                self.queued_block.draw()
            else:
                #UPDATE BLOCK
                self.queued_block.x_pos = self.row_x*2+self.offset_x-100
                self.queued_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.queued_block.x_mag = self.block_height-80
                self.queued_block.y_mag = self.block_width
                self.queued_block.string = self.csv_row[5]
                self.queued_block.colour = self.activity_colour
                self.queued_block.draw()

        if len(self.csv_row) >= 10:
            if self.SLA_block == None:
                self.SLA_block = Block(self.row_x*3+self.offset_x-200,(self.row_y+self.gap)*self.row_number-self.offset_y, self.block_height-80, self.block_width,self.csv_row[9],self.activity_colour)
                self.SLA_block.draw()
            else:
                #UPDATE BLOCK
                self.SLA_block.x_pos = self.row_x*3+self.offset_x-200
                self.SLA_block.y_pos = (self.row_y+self.gap)*self.row_number-self.offset_y
                self.SLA_block.x_mag = self.block_height-80
                self.SLA_block.y_mag = self.block_width
                self.SLA_block.string = self.csv_row[9]
                self.SLA_block.colour = self.activity_colour
                self.SLA_block.draw()


agent_list = []
queue_list = []


class Agent:
    def __init__(self, is_part_time,email,f_name,l_name):
        self.is_part_time = is_part_time
        self.email = email
        self.f_name = f_name
        self.l_name = l_name

        self.gui_row_instance = None

        agent_list.append(self)

    def agent_row(self, row_number, default_row_x, default_row_y, default_block_width, default_block_height, row):
        if self.gui_row_instance == None:#create row
            self.gui_row_instance = GUI_Row(row_number, default_row_x, default_row_y, default_block_width, default_block_height, row, False)
        else:#update existing row
            self.gui_row_instance.csv_row = row
            self.gui_row_instance.update()

def create_agents():

    agents_heading = Agent(False, 'Agents', 'Agents', ' ')
    # FIRST LETTER OF FIRST NAME, LAST NAME
    #bbiddle = Agent(False, 'brandon.biddle@dxc.com', 'Agents', ' ')
    nmcgrath = Agent(False, 'nmcgrath4@dxc.com', 'Nick', 'McGrath')
    lsumpton = Agent(False, 'liam.sumpton@dxc.com', 'Liam', 'Sumpton')
    ehall = Agent(False, 'erica.hall@dxc.com', 'Erica', 'hall')
    abrooks = Agent(False, 'andrew.brooks2@dxc.com', 'Andrew', 'brooks')
    anapalan = Agent(False, 'andrian.napalan@dxc.com', 'Andrian', 'Napalan')
    deastaway = Agent(False, 'daniel.eastaway@dxc.com', 'Daniel', 'Eastaway')
    rhazara = Agent(False, 'rohit.hazara@dxc.com', 'Rohit', 'Hazara')
    iibarra = Agent(False, 'ian.ibarra@dxc.com', 'Ian', 'Ibarra')
    klisson = Agent(False, 'kate.lisson@dxc.com', 'Kate', 'Lisson')
    lhenry = Agent(False, 'laura.henry@dxc.com', 'Laura', 'Henry')
    dfindlay = Agent(False, 'debra.findlay@dxc.com', 'Debra', 'Findlay')
    jyeoh = Agent(False, 'jef.yeoh@dxc.com', 'Jef', 'Yeoh')
    hthresher = Agent(False, 'harold.thresher2@dxc.com', 'Harold', 'Thresher')
    kwhishwilson = Agent(False, 'kate.whishwilson@dxc.com', 'Kate', 'Whish-Wilson')
    sdobber = Agent(False, 'stefan.dobber@dxc.com', 'Stefan', 'Dobber')
    tphoa = Agent(False, 'tiansoon.phoa@dxc.com', 'Tiansoon', 'Phoa')
    zye = Agent(False, 'zhongmin.ye@dxc.com', 'Zhongmin', 'Ye')
    cwu = Agent(False, 'chunyi.wu@dxc.com', 'Chunyi', 'Wu')
    jallentanner = Agent(False, 'jesse.allentanner@dxc.com', 'Jesse', 'Allen-Tanner')
    tkerslake = Agent(False, 'tyler.kerslake@dxc.com', 'Tyler', 'Kerslake')
    breid = Agent(False, 'bill.reid@dxc.com', 'Bill', 'Reid')
    jboost = Agent(False, 'joshua.boost@dxc.com', 'Boost', 'J')
    nmclean = Agent(False, 'nicholas.mclean2@dxc.com', 'Nicholas', 'Mclean')
    chamilton = Agent(False, 'chris.hamilton@dxc.com', 'Chris', 'Hamilton')
    xbrett = Agent(False, 'xander.brett@dxc.com', 'Xander', 'Brett')
    zli = Agent(False, 'zhipeng.li@dxc.com', 'Zhipeng', 'Li')
    hyoung = Agent(False, 'hugh.young@dxc.com', 'Hugh', 'Young')
    tsheppard = Agent(False, 'tanisha.sheppard@dxc.com', 'Tanisha', 'Sheppard')
    sknevett = Agent(False, 'seb.knevett@dxc.com', 'Seb', 'Knevett')
    uvazeele = Agent(False, 'ubadha.vazeele@dxc.com', 'Vaz', '')
    msu = Agent(False, 'majuan.su@dxc.com', 'Majuan', 'Su')
    mkumari = Agent(False, 'manosha.kumari@dxc.com', 'Manusha', 'Kumari')
    njackimowicz = Agent(False, 'nick.jackimowicz@dxc.com', 'Nick', 'Jakimowicz')
    ntafurt = Agent(False, 'nicolas.tafurt@dxc.com', 'Nic', 'Handsome')
    nshen = Agent(False, 'ningyuan.shen@dxc.com', 'Ningyuan', 'Shen')
    rbyard = Agent(False, 'rhys.byard@dxc.com', 'Rhys', 'Bryard')
    arobertshaw = Agent(False, 'amie.robertshaw@dxc.com', 'Amie', 'Robertshaw')
    dbridge = Agent(False, 'declan.bridge2@dxc.com', 'Declan', 'Bridge')
    ddermondy = Agent(False, 'duane.dermody2@dxc.com', 'Duane', 'Dermody')
    ochivers = Agent(False, 'owen.chivers2@dxc.com', 'Owen', 'Chivers')
    rsingh = Agent(False, 'robin.singh2@dxc.com', 'Robin', 'Singh')
    dbenson = Agent(False, 'daniel.benson@dxc.com', 'Daniel', 'Benson')
    dmcdougall2 = Agent(False, 'david.mcdougall2@dxc.com', 'David', 'McDougall')
    hxia = Agent(False, 'haifeng.xia@dxc.com', 'Haifeng', 'Xia')
    jveldhuis2 = Agent(False, 'jack.veldhuis2@dxc.com', 'Jack', 'Veldhuis')
    jrussell2 = Agent(False, 'joshua.russell2@dxc.com', 'Joshua', 'Russell')
    tmunster2 = Agent(False, 'tarryd.munster2@dxc.com', 'Tarryd', 'Munster')
    zobrien2 = Agent(False, 'zoe.obrien2@dxc.com', 'Zoe', 'Obrien')
    asalvatierra = Agent(False, 'adriana.salvatierra@dxc.com', 'Adriana', 'Salvatierra')
    jvaletich = Agent(False, 'jack.valetich@dxc.com', 'Jake', 'Valetich')
    dsingh9 = Agent(False, 'deepak.singh9@dxc.com', 'Deepak', 'Singh')
    ssmart = Agent(False, 'sophie.smart@dxc.com', 'Sophie', 'Smart')

create_agents()


class Queue:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.amount = 0

        self.gui_queue_instance = None

        queue_list.append(self)

    def queue_row(self, row_number, default_row_x, default_row_y, default_block_width, default_block_height, row):
        if self.gui_queue_instance == None:#create row
            self.gui_queue_instance = GUI_Row_Queue(row_number, default_row_x, default_row_y, default_block_width, default_block_height, row, self.description)
        else:#update existing row
            self.gui_queue_instance.csv_row = row
            self.gui_queue_instance.update()

def create_queues():
    # queue headings
    queue_heading = Queue('Queue','Queues')
    queue_total = Queue('Summary','Total')

    # queues
    queue_Pwd = Queue('CBA Desktop Pwd','Password')

    queue_hardware_new = Queue('CBA Desktop Hardware New','Desktop New')
    queue_hardware = Queue('CBA Desktop Hardware Existing','Desktop Existing')
    queue_hidden = Queue('CBA Desktop Hidden','Desktop Hidden')

    queue_commSee_new = Queue('CBA Desktop CommSee New','CommSee New')
    queue_commSee = Queue('CBA Desktop CommSee Existing','CommSee Existing')

    queue_apps_new = Queue('CBA Desktop Business Apps New','Bank Apps New')
    queue_apps = Queue('CBA Desktop Business Apps Existing','Bank Apps Existing')

    



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

agents_csv_path = r"New_Agents.csv"
queue_csv_path = r"Queue.csv"

clock = pygame.time.Clock()

refresh_time = 4 # seconds
tick_rate = 6 #ticks per second
timer = 0

agent_reader_copy = []

while is_running:

    clock.tick(tick_rate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window_surface.blit(background, (0, 0))
    pygame.draw.rect(background,(1+(5*timer),20,100),((40,1050),(72*(timer+1),40)))

    if timer >= (tick_rate * refresh_time):
        timer = 0

        if(agents_enabled):
            #print("- opening agents.csv file success = " + str(os.access(agents_csv_path, os.R_OK)))
            if os.access(agents_csv_path, os.R_OK):
                try:
                    with open(agents_csv_path, newline='') as f:
                        reader = csv.reader(f)
                        agent_reader_copy.clear()
                        for row in reader:
                            agent_reader_copy.append(row)
                except:
                    print("- cannot read agents.csv, file being updated\n" )

            row_number = 1
            if len(agent_reader_copy) >= 2:
                for agent in agent_list:
                    found_row = False
                    for row in agent_reader_copy:
                        if row[0] == agent.email: #if email adress in row matches agent email
                            #create or update agent's GUI row
                            found_row = True
                            agent.agent_row(row_number, default_row_x, default_row_y, default_block_width, default_block_height, row)
                            break

                    if found_row == False:
                        agent.agent_row(row_number, default_row_x, default_row_y, default_block_width, default_block_height, ["NULL_EMAIL"," Offline"," 00:00:00"," " + agent.l_name + " " + agent.f_name," -"," -"," 00:00:00"])
                    row_number += 1
            else:
                print("no info in New_Agents")

        if(queue_enabled):
            #print("- opening queue.csv file success = " + str(os.access(queue_csv_path, os.R_OK)))
            if os.access(queue_csv_path, os.R_OK):
                try:
                    with open(queue_csv_path, newline='') as f:
                        queue_reader = csv.reader(f)
                        # next(reader) uncomment to remove headings

                        #add all relevant queues to short list
                        for queue_row in queue_reader:
                            for queue in queue_list:
                                if queue_row[0] == queue.name:

                                    queue.queue_row(queue_list.index(queue)+1, queue_default_row_x, default_row_y, queue_default_block_width, default_block_height, queue_row)

                except:
                    print("- cannot read queue.csv, file being updated\n" )


    timer += 1
    #print(str(timer) + " / " +str(tick_rate * refresh_time))

    pygame.display.update()

    #print(len(row_list))
