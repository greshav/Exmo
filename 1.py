import requests, json, time

fees_limit = 'https://exmo.me/ctrl/feesAndLimits'

sleep_time = 1
amount = 100
fltr = ('PRQ_BTC', 'BTT_BTC', 'PTI_BTC')
percent = 0.0							#  минимальный процент от сделки
fees = 1.004
fee_lim = {}							#1.004
a = []


def fees_limit(dct):
    '''
    lst - global list to save array of pairs
    return [{pair:[min quantity, taker fee, maker fee]}, ...}
    '''
    r = requests.get('https://exmo.me/ctrl/feesAndLimits')
    resp = json.loads(r.text)['data']['limits']
    for s in resp:
        nm = s['pair'].replace('/', '_')
        dct[nm] = [float(s['min_q']), float(s['taker']) / 100 + 1, float(s['maker']) /100 + 1]

def get_ticker():
    r = requests.get('https://api.exmo.me/v1/ticker/')
    return json.loads(r.text)

def get_list():
	global obj
	r = requests.get('https://api.exmo.me/v1/ticker/')
	obj = json.loads(r.text)
	global arr
	try:
		arr
	except NameError:
		arr = list(set([o for o in obj])  - set(fltr))  # Все пары

def get_cur(pair, tp):
	r = requests.get("https://api.exmo.com/v1.1/order_book?pair=" + pair + "&limit=1")
	obj = json.loads(r.text)
	if tp == 'buy':
		return(obj[pair]['ask'][0][1])
	elif tp == 'sell':
		return(obj[pair]['bid'][0][2])

def split_pairs():
	all_cur = []
	for n in range(len(arr)): # делим все пары
		q = arr[n].split('_')
		a.append(q)
		all_cur.append(q[0])
		all_cur.append(q[1])
		global all_curr
		all_curr = sorted(set(all_cur))  # Все пары

def all_pairs(a):
    v = []
    global all_curr
    for num in all_curr:
        s = create_list(num, a)
        if len(s) != 0:
            v.extend(s)
    return v

def trade_pairs(dic):
    arr1 = []
    if dic != None:
        for n in range(len(dic)):
            if dic[n][0] + '_' + dic[n][1] in arr:
                pair1 = dic[n][0] + '_' + dic[n][1]
                tmp2 = amount * float(obj[pair1]['buy_price']) / fee_lim[pair1][1]
            else:
                pair1 = dic[n][1] + '_' + dic[n][0]
                tmp2 = amount / float(obj[pair1]['sell_price']) / fee_lim[pair1][1]
            if dic[n][1] + '_' + dic[n][2] in arr:
                pair2 = dic[n][1] + '_' + dic[n][2]
                tmp3 = tmp2 * float(obj[pair2]['buy_price']) / fee_lim[pair2][1]
            else:
                pair2 = dic[n][2] + '_' + dic[n][1]
                tmp3 = tmp2 / float(obj[pair2]['sell_price']) / fee_lim[pair2][1]
            if dic[n][2] + '_' + dic[n][3] in arr:
                pair3 = dic[n][2] + '_' + dic[n][3]
                tmp4 = tmp3 * float(obj[pair3]['buy_price']) / fee_lim[pair3][1] # продаём
            else:
                pair3 = dic[n][3] + '_' + dic[n][2]
                tmp4 = tmp3 / float(obj[pair3]['sell_price']) / fee_lim[pair3][1]	# покупаем
            if tmp4 > amount + percent:
                #tmp5 = get_cur(tmp4_4, tmp5_t)
                arr1.append([tmp4, n])
                tmp6 = "%.2f" % (tmp4 - amount)
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
    else:
        return []


fees_limit(fee_lim)
get_list()
split_pairs()
#cr = create_list('BTC', arr)
cr = all_pairs(arr) 
while True:
	print('Waiting..')
	start_time = time.time()
	get_list()
	trade_pairs(cr)
	print("--- %0.4s seconds " % (time.time() - start_time))
	time.sleep(sleep_time)
    
def main():
	pass

if __name__=="__main__":
    main()
