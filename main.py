import requests, json, time

fees_limit = 'https://exmo.me/ctrl/feesAndLimits'

sleep_time = 10
tmp1 = 100
fltr = ['PRQ_BTC', 'ONE_BTC']
percent = 1							#  минимальный процент от сделки
fees = 1.001
  							#1.004
a = []
all_curr = []

def get_list():
	global obj
	r = requests.get('https://api.exmo.me/v1/ticker/')
	obj = json.loads(r.text)
	global arr
	arr = list(set([o for o in obj])  - set(fltr))

def get_cur(pair, tp):
	r = requests.get("https://api.exmo.com/v1.1/order_book?pair=" + pair + "&limit=1")
	obj = json.loads(r.text)
	if tp == 'buy':
		return(obj[pair]['ask'][0][1])
	elif tp == 'sell':
		return(obj[pair]['bid'][0][2])

def split_pairs():
	tmp = set()
	for n in range(len(arr)): # делим все пары
		q = arr[n].split('_')
		a.append(q)
		tmp.add(q[0])
		tmp.add(q[1])
	else:
		return sorted(tmp)

def all_pairs(lst, lst2):
	for num in lst:
		v = create_list(num, lst2)
		trade_pairs(v)

def trade_pairs(dic):
	arr1 = []
	if dic != None:
		for n in range(len(dic)):
			try:
				tmp2 = tmp1 * float(obj[dic[n][0] + '_' + dic[n][1]]['buy_price']) / fees
				tmp2_2 = str(dic[n][0]) + '_' + str(dic[n][1])
				#print("%0.10f" % tmp2)
			except KeyError:
				tmp2 = tmp1 / float(obj[dic[n][1] + '_' + dic[n][0]]['sell_price']) / fees
				tmp2_2 = obj[dic[n][1] + '_' + dic[n][0]]
				#print("%0.10f" % tmp2)
			try:
				tmp3 = tmp2 * float(obj[dic[n][1] + '_' + dic[n][2]]['buy_price']) / fees
				tmp3_3 = obj[dic[n][1] + '_' + dic[n][2]]
				#print("%0.10f" % tmp3)
			except KeyError:
				tmp3 = tmp2 / float(obj[dic[n][2] + '_' + dic[n][1]]['sell_price']) / fees
				tmp3_3 = obj[dic[n][2] + '_' + dic[n][1]]
				#print("%0.10f" % tmp3)
			try:
				tmp4 = tmp3 * float(obj[dic[n][2] + '_' + dic[n][3]]['buy_price']) / fees # продаём
				tmp4_4 = str(dic[n][2]) + '_' + str(dic[n][3])
				tmp5_t = 'sell'
				#print("%0.10f" % tmp4)
			except KeyError:
				tmp4 = tmp3 / float(obj[dic[n][3] + '_' + dic[n][2]]['sell_price']) / fees	# покупаем
				tmp4_4 = str(dic[n][3]) + '_' + str(dic[n][2])
				tmp5_t = 'buy'
				#print("%0.10f" % tmp4)
			if tmp4 > tmp1 + percent: # and fltr not in dic[n]:
				#tmp5 = get_cur(tmp4_4, tmp5_t)
				arr1.append([tmp4, n])
				tmp6 = "%.2f" % (tmp4 - tmp1)
				print(*dic[n], tmp6 + "%", sep=' -> ')
		return(arr1)

def create_list(pay_pair, dics):
	b = []
	c = []
	e = []
	for z in range(len(a)):# находим первую пару
		if a[z][0] == pay_pair:
			b.append(a[z])
		elif a[z][1] == pay_pair:
			b.append([a[z][1], a[z][0]])
	for k in range(len(b)): # находим вторую пару
		for h in range(len(a)):
			if a[h][0] == b[k][1] and b[k][0] != a[h][1]:
				c.append([b[k][0], b[k][1], a[h][1]])
			elif a[h][1] == b[k][1] and b[k][0] != a[h][0]:
				c.append([b[k][0], b[k][1], a[h][0]])
	for j in range(len(c)):  # находим третью пару
		for l in range(len(a)):
			if a[l][1] == c[j][2] and a[l][0] == pay_pair:
				e.append([c[j][0], c[j][1], c[j][2], a[l][0]])
			elif a[l][0] == c[j][2] and a[l][1] == pay_pair:
				e.append([c[j][0], c[j][1], c[j][2], a[l][1]])
	if len(e) != 0:
		return(e)


get_list()
all_curr = split_pairs()
#print(all_curr)
while True:
	print('Waiting..')
	start_time = time.time()
	get_list()
	all_pairs(all_curr, arr)
	#trade_pairs(create_list('USDT', arr))
	print("--- %0.4s seconds " % (time.time() - start_time))
	time.sleep(sleep_time)





#get_cur('BTC_USD', 'sell')
#a = create_list('HB', arr)
#trade_pairs(a)
#for x in c:
#	print(x)
#print(a)
#print("%0.10f" % (trade_pairs(a)))

#
def main():
	pass

if __name__=="__main__":
    main()