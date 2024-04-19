# Sim-Trading-Analysis
Simulated FX Post-Trade Analysis Project:

This project uses Plotly and Pandas to calculate/chart Buys and Sells (from _trades.csv files), Bids and Asks (from _md.csv files), Aggregate Mark-Out curves, and Mark-to-Market PnL curves for four different hypothetical FX instruments (BTA, GMMA, LMDA, and ZTA) over 48hrs in 100 ms intervals.

See Python code in Sim_Trading.py. The market dataset (_md.csv files) for each of the four hypothetical instruments is large (>1.7M rows of bid/ask prices for the 100 millisecond horizon ticks), and has been compressed and attached as .zip files.

Example Output for BTA:
<img width="1494" alt="Screenshot 2024-03-11 at 6 07 06 PM" src="https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/13393726-7ed5-4eec-94db-0a70b2d5fcfd">

<img width="1047" alt="Screenshot 2024-04-19 at 10 28 51 AM" src="https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/d685f191-8a42-440b-b4f5-9c4332b06b9b">

<img width="1047" alt="Screenshot 2024-04-19 at 10 27 57 AM" src="https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/7220c008-c52c-4bee-a050-e1dc048f1bde">

<img width="1047" alt="Screenshot 2024-04-19 at 10 28 28 AM" src="https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/5284c9d3-f13e-4b1c-97b6-99480a89bf23">

<img width="1047" alt="Screenshot 2024-04-19 at 10 29 14 AM" src="https://github.com/benjoergens/Sim-Trading-Analysis/assets/59835387/cba3caa4-1603-4a8e-9ae2-2127ea8fa721">
