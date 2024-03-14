import bisect
import itertools
import math
from operator import itemgetter
import pandas as pd
import plotly.graph_objects as go
from datetime import time
import numpy as np
from tqdm import tqdm
from plotly.subplots import make_subplots

# CSVs to DFs - Change File Paths Here -
bta_md_df = pd.read_csv('/Users/benjoergens/Desktop/BTAUSD_md.csv')
bta_trades_df = pd.read_csv('/Users/benjoergens/Desktop/BTAUSD_trades.csv')
gmma_md_df = pd.read_csv('/Users/benjoergens/Desktop/GMMAUSD_md.csv')
gmma_trades_df = pd.read_csv('/Users/benjoergens/Desktop/GMMAUSD_trades.csv')
lmda_md_df = pd.read_csv('/Users/benjoergens/Desktop/LMDAUSD_md.csv')
lmda_trades_df = pd.read_csv('/Users/benjoergens/Desktop/LMDAUSD_trades.csv')
zta_md_df = pd.read_csv('/Users/benjoergens/Desktop/ZTAUSD_md.csv')
zta_trades_df = pd.read_csv('/Users/benjoergens/Desktop/ZTAUSD_trades.csv')
horizon_ticks_df = pd.read_csv('/Users/benjoergens/Desktop/horizon_ticks.csv')
horizon_ticks_lst = horizon_ticks_df['h_ticks'].tolist()


class Grapher:
    def __init__ (self, select_md_df, select_trades_df, select_instrument_name):

        # Find max elapsed md time in hrs
        self.md_ts_ms = select_md_df['ts_ms'].tolist()
        self.min_md_ms = min(self.md_ts_ms)
        self.max_md_hrs_elapsed = round((max(self.md_ts_ms) - self.min_md_ms) / 3600000)
        self.elapsed_hr_increments = []
        for i in range(0, self.max_md_hrs_elapsed+1):
            self.elapsed_hr_increments.append(i)
        self.corresponding_ms_increments = []
        self.elapsed_three_hr_increments = []
        self.elapsed_three_hr_labels = []
        for i in self.elapsed_hr_increments:
            self.corresponding_ms_increments.append((i*3600000) + self.min_md_ms)
            if i % 3 == 0:
                if i == 48:
                    datetime = time(i - 48)
                elif i > 23:
                    datetime = time(i - 24)
                else:
                    datetime = time(i)
                hour = datetime.hour
                self.elapsed_three_hr_increments.append(hour)
                self.elapsed_three_hr_labels.append(i)
            else:
                self.elapsed_three_hr_increments.append('')
                self.elapsed_three_hr_labels.append('')

        # Bids and asks
        self.bids = select_md_df['bid'].tolist()
        self.asks = select_md_df['ask'].tolist()
        self.min_bid = min(self.bids)
        self.max_ask = max(self.asks)

        # Trade data
        self.trades_ts_ms = select_trades_df['ts_ms']
        self.trade_ts_ms_lst = select_trades_df['ts_ms'].tolist()
        self.trade_ids = select_trades_df['trade_id'].tolist()
        self.trade_sizes = select_trades_df['size']

        # ID-sorted trade data
        self.ts_trades = select_trades_df.sort_values('trade_id')

        # Separate buys and sells
        self.buy_px = []
        self.sell_px = []
        self.pos_sizes = []
        for ind in select_trades_df.index:
            if select_trades_df['side'][ind] == 'B':
                self.buy_px.append(select_trades_df['px'][ind])
                self.sell_px.append('')
            else:
                self.sell_px.append(select_trades_df['px'][ind])
                self.buy_px.append('')

        # Negate sell positions for aggregate position (agg_pos) calcs
        for ind in self.ts_trades.index:
            if select_trades_df['side'][ind] == 'B':
                self.pos_sizes.append(select_trades_df['size'][ind])
            else:
                self.pos_sizes.append(select_trades_df['size'][ind] * -1)

        # Round up the trade times to match md_ts_ms (round up b/c positions should only change post trade)
        self.ordered_times = self.ts_trades['ts_ms'].tolist()
        self.rnd_ordered_times = []
        for i in self.ordered_times:
            self.rnd_ordered_times.append(int(math.ceil(i / 100.0)) * 100)

        self.ordered_px = self.ts_trades['px'].tolist()
        self.side = select_trades_df['side'].tolist()
        self.size = select_trades_df['size'].tolist()
        self.instrument_name = select_instrument_name

        # Calculate cumulative agg_pos_sizes
        agg_pos_sizes = list(itertools.accumulate(self.pos_sizes))
        # Dictionaries for faster lookups
        md_dict = dict(zip(select_md_df['ts_ms'], zip(select_md_df['bid'], select_md_df['ask'])))
        agg_pos_dict = dict(zip(self.rnd_ordered_times, agg_pos_sizes))
        # Initialize mark-to-market data list
        mtm_data = []
        # Find smallest key in agg_pos_dict
        smallest_key = min(agg_pos_dict.keys())
        # Find corresponding agg_pos_sizes values for each ts_ms_value
        for ts_ms_value in tqdm(select_md_df['ts_ms'], colour='blue',
                                desc='Processing ' + self.instrument_name + ' Aggregate Position Sizes'):
            # Find corresponding agg_pos_sizes value
            if ts_ms_value < smallest_key:
                agg_pos_size = 0
            else:
                keys = list(agg_pos_dict.keys())
                index = bisect.bisect_left(keys, ts_ms_value)
                if index > 0:
                    nearest_key = keys[index - 1]
                    agg_pos_size = agg_pos_dict[nearest_key]
                else:
                    # Where no key is less than or equal to ts_ms_value
                    agg_pos_size = 0
            # Store 'ts_ms', 'bids', 'asks', and agg_pos_sizes values
            bid, ask = md_dict.get(ts_ms_value, (None, None))
            mtm_data.append([ts_ms_value, bid, ask, agg_pos_size])

        # Calculate mark-to-market PnL
        mtm_pnl_data = [[mtm_data[0][0], 0]]  # Initialize with zero PnL for the first timestamp
        for i in tqdm(range(1, len(mtm_data)), colour='blue',
                      desc='Computing ' + self.instrument_name + ' MTM PnL Curve'):
            prev_agg_pos_size = mtm_data[i - 1][3]
            # Mark to mid, or mark to bid/ask? Practically, it may be easier to mark to mid and add on reserve
            # for bid-offer (as many banks/fx traders do), especially if dealing with complex derivatives.
            # Here, given simple long/short positions, and the availability of bids/asks, mark to bid/ask should provide
            # more realistic and 'conservative' mtm_pnl figures.
            if prev_agg_pos_size > 0:
                mtm_pnl = prev_agg_pos_size * (mtm_data[i][1] - mtm_data[i - 1][1])
            elif prev_agg_pos_size < 0:
                mtm_pnl = prev_agg_pos_size * (mtm_data[i][2] - mtm_data[i - 1][2])
            else:
                mtm_pnl = 0
            mtm_pnl_data.append([mtm_data[i][0], mtm_pnl + mtm_pnl_data[-1][1]])
        self.mtm_pnl = list(map(itemgetter(1), mtm_pnl_data))
        '''pnl_sum = 0
        pnl_count = 0
        for i in range(len(self.mtm_pnl)):
            pnl_sum += self.mtm_pnl[i]
            pnl_count += 1
        pnl_mean = pnl_sum/pnl_count
        dif_sum = 0
        for i in range(len(self.mtm_pnl)):
            dif_sqrs = (self.mtm_pnl[i] - pnl_mean) ** 2
            dif_sum += dif_sqrs
        print(dif_sum)
        print(pnl_count)
        vol = math.sqrt(dif_sum / pnl_count)
        print('Strat vol: ', vol)'''

        # Calculate margin curve
        # Create df with trade times and buy/sell_px columns
        trades_ms_px = pd.DataFrame({'trade_id': self.trade_ids, 'ts_ms': self.trade_ts_ms_lst, 'buy_px': self.buy_px,
                                     'sell_px': self.sell_px})
        trades_ms_px.sort_values(by='ts_ms', inplace=True)

        select_md_dict = {ts_ms: (bid, ask) for ts_ms, bid, ask in
                          zip(select_md_df['ts_ms'], select_md_df['bid'], select_md_df['ask'])}

        # Create method to round to last horizon tick (used to find bid/sell at last horizon tick)
        def round_down(x):
            return int(math.floor(x / 100.0)) * 100

        # Initialize time horizon margin dictionary
        th_margin_dict = {}
        # Calculate total number of iterations for tqdm progress bar
        total_iterations = len(trades_ms_px) * len(horizon_ticks_lst)
        # Calculate margin for each nth interval
        with tqdm(total=total_iterations, colour='blue',
                  desc='Computing ' + self.instrument_name + ' Aggregate Markout Curve') as pbar:
            for trade_id, ts_ms, buy_px, sell_px in trades_ms_px.itertuples(index=False):
                for j in horizon_ticks_lst:
                    new_trade_horizon = j + ts_ms
                    rnd_nth = round_down(new_trade_horizon)
                    nth_bid, nth_ask = select_md_dict.get(rnd_nth, (None, None))
                    if nth_bid is not None and nth_ask is not None:
                        margin = float(sell_px) - nth_ask if buy_px == '' else float(buy_px) - nth_ask
                        th_margin_dict[new_trade_horizon] = th_margin_dict.get(new_trade_horizon, 0) + margin
                    pbar.update(1)  # Update the progress bar for each iter
        self.th_margin_df = pd.DataFrame(list(th_margin_dict.items()),
                                         columns=['th', 'agg_margin']).sort_values(by='th')
        self.th_margin_df.reset_index(inplace=True, drop=True)

    # Plot all curves and buy/sell markers
    def plot_md_trades(self):
        print('Plotting ' + self.instrument_name + ' chart...')
        fig = go.Figure()
        fig = make_subplots(specs=[[{'secondary_y': True}]])
        fig['layout']['yaxis2']['showgrid'] = False
        fig.add_trace(go.Scatter(x=self.th_margin_df['th'],
                                 y=self.th_margin_df['agg_margin'],
                                 hovertext=self.th_margin_df['th'].astype(str),
                                 hovertemplate='<b>Agg Markout</b>: %{y}' + '<br><b>Timestamp</b>: %{hovertext}',
                                 name='Agg Markout',
                                 line=dict(color='rgb(93, 252, 138)', width=2)), secondary_y=True)
        fig.add_trace(go.Scatter(x=self.md_ts_ms,
                                 y=self.mtm_pnl,
                                 hovertext=self.md_ts_ms,
                                 hovertemplate='<b>MTM PnL</b>: %{y}' + '<br><b>Timestamp</b>: %{hovertext}',
                                 name='MTM PnL',
                                 line=dict(color='rgb(250, 255, 112)', width=2)))
        fig.add_trace(go.Scatter(x=self.md_ts_ms,
                                 y=self.bids,
                                 hovertext=self.md_ts_ms,
                                 hovertemplate='<b>Bid</b>: %{y}' + '<br><b>Timestamp</b>: %{hovertext}',
                                 name='Bids',
                                 line=dict(color='rgb(0, 191, 255)', width=2)))
        fig.add_trace(go.Scatter(x=self.md_ts_ms,
                                 y=self.asks,
                                 hovertext=self.md_ts_ms,
                                 hovertemplate='<b>Ask</b>: %{y}' + '<br><b>Timestamp</b>: %{hovertext}',
                                 name='Asks',
                                 line=dict(color='rgb(220, 208, 255)', width=2)))
        fig.add_trace(go.Scatter(x=self.trades_ts_ms,
                                 y=self.buy_px,
                                 mode='markers',
                                 customdata=np.stack((self.trades_ts_ms, self.trade_ids, self.trade_sizes), axis=-1),
                                 hovertemplate='<b>Buy Px</b>: %{y}' + '<br><b>Timestamp</b>: %{customdata[0]}'
                                               + '<br><b>Trade ID</b>: %{customdata[1]}'
                                               + '<br><b>Trade Size</b>: %{customdata[2]}',
                                 name='Buys',
                                 line=dict(color='green', width=6),
                                 marker=dict(symbol="triangle-up", size=12)))
        fig.add_trace(go.Scatter(x=self.trades_ts_ms,
                                 y=self.sell_px,
                                 mode='markers',
                                 customdata=np.stack((self.trades_ts_ms, self.trade_ids, self.trade_sizes), axis=-1),
                                 hovertemplate='<b>Sell Px</b>: %{y}' + '<br><b>Timestamp</b>: %{customdata[0]}'
                                               + '<br><b>Trade ID</b>: %{customdata[1]}'
                                               + '<br><b>Trade Size</b>: %{customdata[2]}',
                                 name='Sells',
                                 line=dict(color='red', width=6),
                                 marker=dict(symbol="triangle-down", size=12)))
        fig.update_layout(template='plotly_dark',
                          plot_bgcolor='rgb(13, 14, 15)',
                          paper_bgcolor='black',
                          title=(self.instrument_name + ' Market Data and Trades'),
                          title_x=0.065,
                          xaxis=dict(rangeselector=dict(buttons=list(
                              [dict(label="1hr look-back", step='hour', stepmode="backward"),
                               dict(step="all")]), bgcolor='black', bordercolor='white', borderwidth=1),
                              rangeslider=dict(
                                  visible=True, yaxis=dict(
                                      range=[self.min_bid, self.max_ask]), bgcolor='rgb(28, 31, 33)'), type='date'),
                          yaxis=dict(fixedrange=False),
                          xaxis2=dict(range=[self.min_bid, self.max_ask]),
                          legend_title='Click to Toggle')
        fig.update_xaxes(title_text='Time Elapsed (hrs)',
                         gridcolor='rgb(28, 31, 33)',
                         ticks='outside',
                         tickcolor='white',
                         tickvals=self.corresponding_ms_increments,
                         ticktext=self.elapsed_three_hr_labels)
        fig.update_yaxes(title_text='Price / MTM PnL (USD)',
                                    gridcolor='rgb(28, 31, 33)',
                                    tickprefix='$',
                                    ticks='outside',
                                    tickcolor='white',
                                    secondary_y=False)
        fig.update_yaxes(title_text='Agg. Markout (USD)',
                                    gridcolor='rgb(28, 31, 33)',
                                    tickprefix='$',
                                    ticks='outside',
                                    tickcolor='white',
                                    secondary_y=True)
        fig.show()


# Instantiate all graphs
#bta_graph = Grapher(bta_md_df, bta_trades_df, 'BTA')
#gmma_graph = Grapher(gmma_md_df, gmma_trades_df, 'GMMA')
#lmda_graph = Grapher(lmda_md_df, lmda_trades_df, 'LMDA')
zta_graph = Grapher(zta_md_df, zta_trades_df, 'ZTA')

# Plot all graphs
#bta_graph.plot_md_trades()
#gmma_graph.plot_md_trades()
#lmda_graph.plot_md_trades()
zta_graph.plot_md_trades()

