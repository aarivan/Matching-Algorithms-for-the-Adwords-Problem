import sys
import csv
import random
import math


# READ queries.txt
def queries():
	file = open('queries.txt','r')
	record = csv.reader(file)
	for rec in record:
		qry_list.append(rec[0])
	return qry_list


# GREEDY ALGORITHM
def greedy(qry_list, adv_budget, qry_bid):
	amount = 0
	for qry in qry_list:
		mbidder, mbid = '', 0.0
		for alist in qry_bid[qry]:
			if not alist[1] <= mbid:
				if not alist[1] >= adv_budget[alist[0]]: 
					mbidder, mbid = alist[0], alist[1]
		if mbidder!='':
			adv_budget[mbidder] -= mbid	
			amount += mbid
	return amount


# msvv ALGORITHM
def msvv(qry_list, unmodified_adv_budget, qry_bid, modified_adv_budget):
	amount = 0
	for qry in qry_list:
		mbidder, val = '', 0
		
		for alist in qry_bid[qry]:
			if not (alist[1] > modified_adv_budget[alist[0]]) :
			 	intValue = (1 - math.exp(((unmodified_adv_budget[alist[0]] - modified_adv_budget[alist[0]])/unmodified_adv_budget[alist[0]])-1))
			 	if (alist[1]*intValue) >= val :  
					mbidder, mbid, val = alist[0], alist[1], alist[1] * intValue
		if mbidder!='' :
			modified_adv_budget[mbidder] -= mbid	
			amount += mbid
	return amount


# BALANCE ALGORITHM
def balance(qry_list, adv_budget, qry_bid):
	amount = 0
	for qry in qry_list:
		mbidder, mbudget = '', 0.0
		for alist in qry_bid[qry]:
			if not (alist[1] > adv_budget[alist[0]]): 
				if not (adv_budget[alist[0]] <= mbudget): 
					mbudget, mbidder, mbid = adv_budget[alist[0]], alist[0], alist[1]
		if mbidder != '' :
			adv_budget[mbidder] -= mbid	
			amount += mbid
	return amount


random.seed(0)


# Check for valid arguments
if (len(sys.argv) != 2) or (sys.argv[1] not in ['greedy', 'msvv', 'balance']):
    print('Invalid Arguments Error: Enter - python adwords.py <algo> where <algo> = [greedy, msvv, balance]')
    sys.exit(1)

adv_budget, qry_bid, qry_list = {}, {}, []


# Reading queries.txt, bidder_dataset.csv 
file = open('bidder_dataset.csv','rb')
record = csv.reader(file)
next(record,None)
for rec in record:
	if rec[3] != '': adv_budget[rec[0]] = float(rec[3])


file = open('bidder_dataset.csv','rb')
record = csv.reader(file)
next(record,None)
for rec in record:
	if rec[1] in qry_bid:
		qry_bid[rec[1]].append([rec[0],float(rec[2])])
	else:
		qry_bid[rec[1]] = []
		qry_bid[rec[1]].append([rec[0],float(rec[2])])

qry_list = queries()


if sys.argv[1] == 'greedy':
	print greedy(qry_list,adv_budget.copy(),qry_bid.copy())
	amount, OPT = 0.0, 0.0
	for i in range(0, 100) :
		random.shuffle(qry_list)
		amount += greedy(qry_list, adv_budget.copy(), qry_bid.copy())
	amount /= 100
	
	for keys in adv_budget:
		OPT += adv_budget[keys]
	print (amount/OPT)

elif sys.argv[1] == 'msvv':	
	print msvv(qry_list,adv_budget.copy(),qry_bid.copy(),adv_budget.copy())
	amount, OPT = 0.0, 0.0
	for i in range(0, 100) :
		random.shuffle(qry_list)
		amount += msvv(qry_list, adv_budget.copy(), qry_bid.copy(),adv_budget.copy())
	amount /= 100

	for keys in adv_budget:
		OPT += adv_budget[keys]
	print (amount/OPT)

else:
	print balance(qry_list,adv_budget.copy(),qry_bid.copy())
	amount, OPT = 0.0, 0.0
	for i in range(0, 100) :
		random.shuffle(qry_list)
		amount += balance(qry_list, adv_budget.copy(), qry_bid.copy())
	amount /= 100
	
	for keys in adv_budget:
		OPT += adv_budget[keys]
	print (amount/OPT)
