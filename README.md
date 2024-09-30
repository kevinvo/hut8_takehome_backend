# Assumptions made for profitability calculations.
1. Bitcoin Price $63,576
2. Hashprice (USD/TH/s/Day) - $0.045

# An explanation of how these assumptions impact the calculations.
1. If bitcoin price increases, it's more profitable to mine BTC. If it decreases, it's not as profitable.
2. Daily Revenue = Hashprice * Hashrate. When Hashprice increases, more money is made.

# How to run
1. pip install -r requirements.txt
2. uvicorn main:app --reload