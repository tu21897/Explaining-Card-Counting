# add_ci.col.py - Tu Nguyen 2022
#
# ----------------------------------
#
# This file adds a confidence interval column to a csv 
#

# Imports
import numpy as np
import pandas as pd
import scipy.stats as sp
import statistics as st

# count system to corresponding index
DATA = ['hi_lo', 'hi_opt1', 'hi_opt2',
             'omega2', 'zen_count',
             'halves', 'wong_halves', 'silver_fox', 
             'revere_point_count','canfield_expert'] 

def main():
    for i in range(len(DATA)):
        # The read csv file
        read = 'docs/data/counting_' + DATA[i] + '_data.csv'
        # The write csv file
        write = 'docs/data/counting_' + DATA[i] + '_data.csv'
        # The csv file with as a data frame
        df = pd.read_csv(read)
        # Suppress numpy float sci form
        np.set_printoptions(suppress=True)
        sessWR = np.array(df['Session winrate (W/L x(Base))'])
        lifeWR = np.array(df['Lifetime winrate (W/L x(Base))'])
        sessCI = [(0,0)]
        lifeCI = [(0,0)]
        for i in range(2, len(sessWR) + 1):
            sessCI.append(sp.t.interval(0.95, len(sessWR[:i]) - 1, loc=np.mean(sessWR[:i]), scale=sp.sem(sessWR[:i])))
        for i in range(2, len(lifeWR) + 1):
            lifeCI.append(sp.t.interval(0.95, len(lifeWR[:i]) - 1, loc=np.mean(lifeWR[:i]), scale=sp.sem(lifeWR[:i])))
        
        df['Session CI Left'] = [sessCI[i][0] for i in range(len(sessCI))]
        df['Session CI Right'] = [sessCI[i][1] for i in range(len(sessCI))]
        df['Lifetime CI Left'] = [lifeCI[i][0] for i in range(len(lifeCI))]
        df['Lifetime CI Right'] = [lifeCI[i][1] for i in range(len(lifeCI))]
        df['Lifetime Mean'] = [df['Lifetime winrate (W/L x(Base))'][0]] + [st.mean(df['Lifetime winrate (W/L x(Base))'][:i+1]) for i in range(1, len(lifeWR))]

        df.to_csv(write, float_format='%.3f', index=False)


if __name__ == "__main__":
    main()