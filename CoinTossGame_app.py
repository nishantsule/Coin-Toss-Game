# Import useful packages
import sys
import numpy as np
from collections import deque
from bokeh.plotting import figure 
from bokeh.layouts import row, column, widgetbox
from bokeh.models.widgets import Slider, Div, Button, TextInput
from bokeh.events import ButtonClick
from bokeh.server.server import Server
from bokeh.models import Label

# Defines a class for the coin toss game ES28
class CoinToss:
    
    # Initializing variables
    # Arguments: number of games to simulate, sequence of head/tail to end the game
    def __init__(self, number_of_games, endgame):
        self.numgames = number_of_games
        self.endgamelen = len(endgame)
        self.endgame = endgame
        self.reset()
        self.check_endgame()
        
    # Reset all the counters
    def reset(self):
        self.counter = np.zeros(self.numgames)
        
    # Check if endgame is correctly inputted    
    def check_endgame(self):
        if self.endgame.strip('HT'):
            sys.exit('ERROR: Endgame can only be a string containing Hs and/or Ts')
                
    # Run the coin toss game    
    def run(self):        
        # Initialize a queue for the current sequence
        curr_seq = deque('', self.endgamelen)
        endgame_reached = False
        # Start looping through number of games 
        for i in range(self.numgames):
            while not endgame_reached:
                # Update counter for current game
                self.counter[i] += 1
                # Check if coin toss resulted in a Head or a Tail
                if np.random.random_sample() < 0.5:
                    curr_seq.append('H')
                else:
                    curr_seq.append('T')
                # Check if the current sequence is equal to the endgame
                check = sum(cs == eg for (cs, eg) in zip(curr_seq, self.endgame))
                if check == self.endgamelen:
                    endgame_reached = True
                    curr_seq.clear()
            endgame_reached = False
        
    # Plot the distribution of number of tosses required to end the game
    def plot_counts(self, r, lb):
        hist, edges = np.histogram(self.counter, density=False, bins=50)
        r.data_source.data['top'] = hist
        r.data_source.data['left'] = edges[:-1]
        r.data_source.data['right'] = edges[1:]
        lb.text = 'Endgame reached in ~' + str(np.around(np.mean(self.counter), decimals=1)) + ' games'


def modify_doc(doc):
 
    p1 = figure(plot_width=500, plot_height=300,
               title='Histogram of Coin Toss Game simulation for Player 1', 
               tools='', background_fill_color='#fafafa')
    r1 = p1.quad(top=[], bottom=0, left=[], right=[], fill_color="navy", 
           line_color="white", alpha=0.5)
    lb1 = Label(x=120, y=120, x_units='screen', y_units='screen',
               text='', render_mode='css',
               background_fill_color='white', background_fill_alpha=0.5)
    lbwinloss1 = Label(x=200, y=90, x_units='screen', y_units='screen',
                       text='',  render_mode='css',
                       background_fill_color='white', background_fill_alpha=0.5)
    p1.y_range.start = 0
    p1.add_layout(lb1)
    p1.add_layout(lbwinloss1)
    p1.xaxis.axis_label = 'Number of tosses to reach endgame'
    p1.yaxis.axis_label = 'counts'
    p1.toolbar.logo = None
    p2 = figure(plot_width=500, plot_height=300,
               title='Histogram of Coin Toss Game simulation for Player 2', 
               tools='', background_fill_color='#fafafa')
    r2 = p2.quad(top=[], bottom=0, left=[], right=[], fill_color="navy", 
           line_color="white", alpha=0.5)
    lb2 = Label(x=120, y=120, x_units='screen', y_units='screen',
               text='', render_mode='css',
               background_fill_color='white', background_fill_alpha=0.5)
    lbwinloss2 = Label(x=200, y=90, x_units='screen', y_units='screen',
                       text='', render_mode='css',
                       background_fill_color='white', background_fill_alpha=0.5)
    p2.y_range.start = 0
    p2.add_layout(lb2)
    p2.add_layout(lbwinloss2)
    p2.xaxis.axis_label = 'Number of tosses to reach endgame'
    p2.yaxis.axis_label = 'counts'
    p2.toolbar.logo = None
    number_of_games = Slider(title='Number of Games', value=500, start=1, end=5000, step=1)
    endgame1 = TextInput(value="HT", title='Player 1 Endgame:')
    endgame2 = TextInput(value="HH", title='Player 2 Endgame:')
    startbutton = Button(label='Start', button_type='success')
    texttitle = Div(text='''<b>BAYSIAN MIND: SIMULATING A COIN TOSSING GAME</b>''', width=1000)
    textdesc = Div(text='''This app simulates a coin tossing game where two players pick a sequence of head/tail occurances. 
                   A coin is tossed until the chosen sequences occur and the game ends and the player who picked the 
                   endgame sequence that occurs first wins. So, the objective is to chose an endgame that will end the 
                   game with the least number of tosses. The app simulates a given number of coin toss games with the 
                   chosen endgame sequences. The average number of tosses required to win is computed and its distribution 
                   is plotted.''', width=1000)
    textrel = Div(text='''Learn more about our Bayesian mind and how it affects technology, ethics, and society in <b>ES 28</b>''', width=1000)
    textdisp = Div(text='''<b>Note: </b> Enter a sequence of Capital H's and T's to represent heads and tails, respectively. 
                   Please only enter Capitol H and T, entering any other letter will return an error and stop the app. Also, 
                   for a fair comparision the players should enter the same number of letters in their sequence''', width=600)

    def check_winner(c1, c2):
        if np.mean(c1.counter) < np.mean(c2.counter):
            lbwinloss1.text = 'You Win!'
            lbwinloss2.text = 'You lose!'
            lbwinloss1.text_color = 'green'
            lbwinloss2.text_color = 'red'
        else:
            lbwinloss1.text = 'You Lose!'
            lbwinloss2.text = 'You Win!'
            lbwinloss1.text_color = 'red'
            lbwinloss2.text_color = 'green'

    # Start the coin tossing game simulation
    def start_tossing(event):
        ng = number_of_games.value
        eg1 = endgame1.value
        eg2 = endgame2.value
        c1 = CoinToss(ng, eg1)
        c1.run()
        c1.plot_counts(r1, lb1)
        c2 = CoinToss(ng, eg2)
        c2.run()
        c2.plot_counts(r2, lb2)
        check_winner(c1, c2)

    # Setup callbacks
    startbutton.on_event(ButtonClick, start_tossing)
    # Setup layout and add to document 

    doc.add_root(column(texttitle, textdesc, number_of_games, textdisp, row(endgame1, endgame2), 
                 startbutton, row(p1, p2), textrel))

server = Server({'/': modify_doc}, num_procs=1)
server.start()
 
if __name__=='__main__':
    print('Opening Bokeh application on http://localhost:5006/')
    server.io_loop.add_callback(server.show, '/')
    server.io_loop.start()


