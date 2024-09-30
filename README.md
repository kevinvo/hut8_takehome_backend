# Assumptions made for profitability calculations.
1. Bitcoin Price $63,576
2. Hashprice (USD/TH/s/Day) - $0.045

# An explanation of how these assumptions impact the calculations.
1. If bitcoin price increases, it's more profitable to mine BTC. If it decreases, it's not as profitable.
2. Daily Revenue = Hashprice * Hashrate. When Hashprice increases, more money is made.

# How to run
1. source venv/bin/activate
2. pip install fastapi uvicorn
3. uvicorn main:app --reload