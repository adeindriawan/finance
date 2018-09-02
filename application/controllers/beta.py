import pandas as pd
# https://stackoverflow.com/questions/50394873/import-pandas-datareader-gives-importerror-cannot-import-name-is-list-like
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

def calculate(code, start, end):
	yf.pdr_override()
	stock_history = pdr.get_data_yahoo(code, start=start, end=end)['Adj Close']
	index_history = pdr.get_data_yahoo('^JKSE', start=start, end=end)['Adj Close']

	stock_dict = stock_history.to_dict()
	index_dict = index_history.to_dict()

	stock_dates = [*stock_dict]
	index_dates = [*index_dict]

	#menyaring tanggal yang ada di list tanggal saham, tapi tidak ada di list tanggal bursa
	not_in_index_date = list(filter(lambda x: x not in stock_dates, index_dates))
    #menyaring tanggal yang ada di list tanggal bursa, tapi tidak ada di list tanggal saham
	not_in_stock_date = list(filter(lambda x: x not in index_dates, stock_dates))
    #menggabungkan kedua list tersebut
	try:
		filtered_dates = not_in_index_date + not_in_stock_date

    	#menyaring nilai-nilai pada dictionary bursa dengan menghapus data yang tidak terdapat pada dictionary saham
		for key in filtered_dates:
			if key in index_dict:
				del index_dict[key]

	    #menyaring nilai-nilai pada dictionary saham dengan menghapus data yang tidak terdapat pada dictionary bursa
		for key in filtered_dates:
			if key in stock_dict:
				del stock_dict[key]

	except TypeError: # berarti not_in_index_date & not_in_stock_date kosong
		pass

    #buat list harga penutupan bursa dari dictionary bursa yang sudah disaring
	index_closing_values = list(index_dict.values())

    #buat list harga penutupan saham dari dictionary saham yang sudah disaring
	stock_closing_values = list(stock_dict.values())

    #buat list yang merangkum return bursa harian selama periode yang dipilih
	index_return = []

    #menghitung return bursa harian dalam satu periode yang telah dipilih dengan menggunakan loop dan menambahkan setiap hasilnya ke dalam list returnBursa
	num = 0
	for i in range(0, len(index_closing_values) - 1):
		daily_index_return = (index_closing_values[num] / index_closing_values[num + 1]) - 1
		index_return.append(daily_index_return)
		num = num + 1

    #buat list yang merangkum return saham harian selama periode yang telah dipilih
	stock_return = []

    #menghitung return saham harian dalam satu periode yang telah dipilih dengan menggunakan loop dan menambahkan setiap hasilnya ke dalam list returnSaham
	num = 0
	for i in range(0, len(stock_closing_values) - 1):
		daily_stock_return = (stock_closing_values[num] / stock_closing_values[num + 1]) - 1
		stock_return.append(daily_stock_return)
		num = num + 1

    #menghitung nilai rata-rata return saham dan bursa selama periode yang dipilih
	avg_stock_return = sum(stock_return) / len(stock_return)
	avg_index_return = sum(index_return) / len(index_return)

    # menghitung nilai beta dengan persamaan regresi linier
	sigma_a = 0
	for i in range(0, len(stock_return)):
		sigma_a += ((index_return[i] - avg_index_return) * (stock_return[i] - avg_stock_return))

	sigma_b = 0
	for i in range(0, len(stock_return)):
		sigma_b += ((index_return[i] - avg_index_return) ** 2)

	beta_value = sigma_a / sigma_b

	return str(beta_value)