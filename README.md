# Sim-Trading-Analysis
Simulated FX Post-Trade Analysis Project:

This project uses Plotly and Pandas to calculate/chart Buys and Sells (from _trades.csv files), Bids and Asks (from _md.csv files), Aggregate Mark-Out curves, and Mark-to-Market PnL curves for four different hypothetical FX instruments (BTA, GMMA, LMDA, and ZTA) over 48hrs in 100 ms intervals.

See Python code in Sim_Trading.py. The market dataset (_md.csv files) for each of the four hypothetical instruments is large (>1.7M rows of bid/ask prices for the 100 millisecond horizon ticks), and has been compressed and attached as .zip files.

Example Output for BTA:
<img width="1494" alt="Screenshot 2024-03-11 at 6 07 06 PM" src="https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/13393726-7ed5-4eec-94db-0a70b2d5fcfd">

BTA 1-hr lookback, bid and ask curves + buy and sells:
<img width="1286" alt="Screenshot 2024-03-11 at 2 40 05 PM" src="https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/eb9fc09f-32fa-46ed-8c6a-307d5cdbee5f">
BTA Aggregate Markout Curve:
![image](https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/33f0b164-e3b2-4848-8cd2-8d847beb48a5)

LMMDA 1-hr lookback, bid and ask curves + buy and sells:
![image](https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/bf752fa2-1f72-48b8-b6a9-17253cc39b9b)
LMDA Aggregate Markout Curve:
![image](https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/805b0bb8-04d2-4c47-bac0-bce8c7bdbaf9)

GMMA 1-hr lookback, bid and ask curves + buy and sells:
![image](https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/e9faaa4a-9e3c-40f0-91dc-e6f16f9dde0d)
GMMA Aggregate Markout Curve:
![image](https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/f0255a6b-38e1-405c-8fdd-2d073af70f2a)


ZTA 1-hr lookback, bid and ask curves + buy and sells:
![image](https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/dd3be76d-6e19-49c2-b3d0-019c1718406d)
ZTA Aggregate Markout Curve:
![image](https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/22b6df2d-a76a-492c-a6fd-af5626a67eed)
