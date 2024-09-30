from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalculationInput(BaseModel):
    electricity_cost: float = Field(..., description="Electricity cost must be a float and cannot be null")
    hash_rate: float = Field(..., description="Hash rate must be a float and cannot be null (in TH/s)")
    initial_investment: float = Field(..., description="Initial investment must be a float and cannot be null")
    power_consumption: float = Field(..., description="Power consumption must be a float and cannot be null (in kW)")

HASHPRICE_IN_USD_PER_TH_PER_DAY = 0.045  # Current Hashprice in USD/TH/s/Day
BITCOIN_PRICE_IN_USD = 63_576  # Current cost per Bitcoin in USD
DAYS_IN_MONTH = 30  # Approximate number of days in a month
DAYS_IN_YEAR = 365  # Approximate number of days in a year

@app.post("/calculate/")
def calculate(input_data: CalculationInput):
    if any(value is None for value in input_data.__dict__.values()):
        raise HTTPException(status_code=400, detail="All parameters must be provided and cannot be null.")
    
    # Access the input data
    electricity_cost = input_data.electricity_cost
    hash_rate = input_data.hash_rate
    initial_investment = input_data.initial_investment
    power_consumption = input_data.power_consumption

    # Cost calculations
    daily_cost = power_consumption * 24 * electricity_cost
    monthly_cost = daily_cost * DAYS_IN_MONTH  # Approximate 30 days in a month
    yearly_cost = daily_cost * DAYS_IN_YEAR

    # Revenue calculations in USD
    daily_revenue_usd = hash_rate * HASHPRICE_IN_USD_PER_TH_PER_DAY
    monthly_revenue_usd = daily_revenue_usd * DAYS_IN_MONTH
    yearly_revenue_usd = daily_revenue_usd * DAYS_IN_YEAR

    # Revenue calculations in BTC
    daily_revenue_btc = daily_revenue_usd / BITCOIN_PRICE_IN_USD
    monthly_revenue_btc = monthly_revenue_usd / BITCOIN_PRICE_IN_USD
    yearly_revenue_btc = yearly_revenue_usd / BITCOIN_PRICE_IN_USD

    # Profit calculations in USD
    daily_profit_usd = daily_revenue_usd - daily_cost
    monthly_profit_usd = monthly_revenue_usd - monthly_cost
    yearly_profit_usd = yearly_revenue_usd - yearly_cost

    # Break-even timeline (in days)
    if daily_profit_usd > 0:
        breakeven_timeline_days = initial_investment / daily_profit_usd
        breakeven_timeline = f"{breakeven_timeline_days:.2f} days"
    else:
        breakeven_timeline_days = -1
        breakeven_timeline = -1

    # Cost to mine 1 BTC
    if daily_revenue_btc > 0:
        cost_to_mine_1_btc = daily_cost / daily_revenue_btc
    else:
        cost_to_mine_1_btc = None  # Undefined if no BTC is mined

    return {
        "dailyCost": daily_cost,
        "monthlyCost": monthly_cost,
        "yearlyCost": yearly_cost,
        "dailyRevenueUSD": daily_revenue_usd,
        "monthlyRevenueUSD": monthly_revenue_usd,
        "yearlyRevenueUSD": yearly_revenue_usd,
        "dailyRevenueBTC": daily_revenue_btc,
        "monthlyRevenueBTC": monthly_revenue_btc,
        "yearlyRevenueBTC": yearly_revenue_btc,
        "dailyProfitUSD": daily_profit_usd,
        "monthlyProfitUSD": monthly_profit_usd,
        "yearlyProfitUSD": yearly_profit_usd,
        "breakevenTimeline": breakeven_timeline,
        "breakevenTimelineDays": breakeven_timeline_days,
        "costToMine": cost_to_mine_1_btc
    }