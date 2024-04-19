# Sim-Trading-Analysis
Simulated FX Post-Trade Analysis Project:

This project uses Plotly and Pandas to calculate/chart Buys and Sells (from _trades.csv files), Bids and Asks (from _md.csv files), Aggregate Mark-Out curves, and Mark-to-Market PnL curves for four different hypothetical FX instruments (BTA, GMMA, LMDA, and ZTA) over 48hrs in 100 ms intervals.

See Python code in Sim_Trading.py. The market dataset (_md.csv files) for each of the four hypothetical instruments is large (>1.7M rows of bid/ask prices for the 100 millisecond horizon ticks), and has been compressed and attached as .zip files.

Example Output for BTA:
<img width="1494" alt="Screenshot 2024-03-11 at 6 07 06 PM" src="https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/13393726-7ed5-4eec-94db-0a70b2d5fcfd">

BTA 1-hr Buys/Sells and Bid/Ask Curve Look-Back:
<img width="1009" alt="Screenshot 2024-04-19 at 10 35 31 AM" src="https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/6f2ce7f6-0b62-408a-a6c4-32a026779663">

BTA 1-hr Agg. Mark-Out Curve Look-Back:
<img width="1095" alt="Screenshot 2024-04-19 at 10 36 03 AM" src="https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/b33b2ffb-35c3-4cff-8144-f6508db43e71">
