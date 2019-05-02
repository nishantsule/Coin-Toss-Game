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
        lb.text = 'Average games to reach endgame = ' + str(np.around(np.mean(self.counter), decimals=1))


def modify_doc(doc):
 
    p1 = figure(plot_width=500, plot_height=300,
               title='Histogram of counts to reach endgame', 
               tools='', background_fill_color='#fafafa')
    r1 = p1.quad(top=[], bottom=0, left=[], right=[], fill_color="navy", 
           line_color="white", alpha=0.5)
    lb1 = Label(x=300, y=150, x_units='screen', y_units='screen',
               text='', render_mode='css',
               background_fill_color='white', background_fill_alpha=0.5)
    #lbwinloss1 = Label(x=400, y=100, x_units='screen', y_units='screen',
    #                   text='', text_color='', render_mode='css')
    p1.y_range.start = 0
    p1.add_layout(lb1)
    #p1.add_layout(lbwinloss1)
    p1.xaxis.axis_label = 'Number of tosses to reach endgame'
    p1.yaxis.axis_label = 'counts'
    p2 = figure(plot_width=500, plot_height=300,
               title='Histogram of counts to reach endgame', 
               tools='', background_fill_color='#fafafa')
    r2 = p2.quad(top=[], bottom=0, left=[], right=[], fill_color="navy", 
           line_color="white", alpha=0.5)
    lb2 = Label(x=300, y=100, x_units='screen', y_units='screen',
               text='', render_mode='css',
               background_fill_color='white', background_fill_alpha=0.5)
    #lbwinloss2 = Label(x=400, y=100, x_units='screen', y_units='screen',
    #                   text='', text_color='', render_mode='css')
    p2.y_range.start = 0
    p2.add_layout(lb2)
    #p2.add_layout(lbwinloss2)
    p2.xaxis.axis_label = 'Number of tosses to reach endgame'
    p2.yaxis.axis_label = 'counts'

    number_of_games = Slider(title='Number of Games', value=200, start=1, end=5000, step=1)
    endgame1 = TextInput(value="HTH", title='Player 1 Endgame:')
    endgame2 = TextInput(value="HHH", title='Player 2 Endgame:')
    startbutton = Button(label='Start', button_type='success')

    def check_winner(c1, c2):
        if np.mean(c1.counter) > np.mean(c2.counter):
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
        #check_winner(c1, c2)

    # Setup callbacks
    startbutton.on_event(ButtonClick, start_tossing)
    # Setup layout and add to document 

    doc.add_root(column(row(number_of_games), row(endgame1, endgame2), startbutton, row(p1, p2)))

server = Server({'/': modify_doc}, num_procs=1)
server.start()
 
if __name__=='__main__':
    print('Opening Bokeh application on http://localhost:5006/')
    server.io_loop.add_callback(server.show, '/')
    server.io_loop.start()


