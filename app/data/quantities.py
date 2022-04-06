from unicodedata import name
from app.schemas import QuantityBase

available_quantities_list = []


# I did not implement all of the Quantities yet
total_flights = QuantityBase(name="number of flights", param="num", unit="number", decimal_places=0, summaryType="total")
pct_on_time = QuantityBase(name="% of flights on time", param="pct-on-time", unit="percent", decimal_places=1, summaryType="mean")
pct_cancelled = QuantityBase(name="% of flights cancelled", param="pct-cancelled", unit="percent", decimal_places=1, summaryType="mean")
available_quantities_list = [total_flights, pct_on_time, pct_cancelled]