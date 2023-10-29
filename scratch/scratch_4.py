import datetime
import yfinance as yf
import plotext as plt

plt.date_form('d/m/Y')

start =datetime.datetime.now()-datetime.timedelta(50)
print(f"{start=}")
end = plt.today_datetime()
print(f"{end=}")
data = yf.download('goog', start, end)

dates = plt.datetimes_to_strings(data.index)

plt.candlestick(dates, data)

plt.title("Google Stock Price CandleSticks")
plt.horizontal_line(139)
plt.xlabel("Date")
plt.ylabel("Stock Price $")
plt.show()
