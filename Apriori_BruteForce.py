# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 16:11:58 2021

@author: patel
"""
import csv
import time

def getSupport(set_transactions, s):
    supp = 0
    
    for trans in set_transactions:
        if s.issubset(trans):
            supp+=1
    return supp

def Brute_Generate_Itemsets(lst, n):
    if n == 0: 
        return [[]] 
      
    final_lst =[] 
    for i in range(0, len(lst)): 
          
        t = lst[i] 
        remain = lst[i + 1:] 
          
        for p in Brute_Generate_Itemsets(remain, n-1): 
            final_lst.append([t]+p) 
              
    return final_lst

def Apriori_Generate_Itemsets(lst, n, remove_set):
    if n == 0: 
        return [[]] 
      
    final_lst =[] 
    for i in range(0, len(lst)): 
          
        t = lst[i] 
        remain = lst[i + 1:] 
          
        for p in Apriori_Generate_Itemsets(remain, n-1, remove_set): 
            is_super = False
            tmp = [t] + p
            tmp_set = set(tmp)
            for r in remove_set:
                if tmp_set.issuperset(r):
                    is_super = True
            if not is_super:
                final_lst.append([t]+p) 
              
    return final_lst

def getPermutations(it, r=None):
    tuple_items = tuple(it)
    n = len(tuple_items)
    
    if r is None:
        r = n
    
    if r > n:
        return
    
    index = list(range(n))
    c = list(range(n, n-r, -1))
    
    yield tuple(tuple_items[i] for i in index[:r])
    
    while n:
        for i in reversed(range(r)):
            c[i] -= 1
            if c[i] == 0:
                index[i:] = index[i+1:] + index[i:i+1]
                c[i] = n - i
            else:
                j = c[i]
                index[i], index[-j] = index[-j], index[i]
                yield tuple(tuple_items[i] for i in index[:r])
                break
        else:
            return
        

def apriori(min_support, min_confidence, db_file):
    list_transactions = []
    item_count ={}
    with open(db_file, mode='r', encoding='utf-8-sig') as csv_file:
        num_rows = 0
        for row in csv.reader(csv_file):
            num_rows+=1
            line = row[0].split(", ")
            list_transactions.append(line)
            for word in line:
                if word in item_count:
                    item_count[word.strip()] += 1
                else:
                    item_count[word.strip()] = 1
                    
        min_support *= num_rows
        
        set_transactions = set(frozenset(i) for i in list_transactions)
       
        remove = []
        freq_items = []
        for item in item_count:
            if item_count[item] >= min_support:
                freq_items.append(item)
            else:
                remove.append(item)
        
        
        freq_itemset = set(frozenset(freq_items))
        remove_itemset = set(frozenset(remove))
        
        for i in range(2, len(freq_items)):
            check_freq = False
            temp = Apriori_Generate_Itemsets(freq_items, i, remove_itemset)
            temp_set=set(frozenset(j) for j in temp)
            for s in temp_set:
                supp = getSupport(set_transactions, s)
                if supp >= min_support:
                    item_count[s] = supp
                    freq_itemset.add(s)
                    check_freq = True
                else:
                    remove_itemset.add(s)
            if check_freq == False:
                break
                        
  
        rule_set = set()
        for comb in freq_itemset:
            if type(comb) != str:
                perms = list(getPermutations(comb, len(comb)))
                for perm in perms:
                    if len(perm)>2:
                        for i in range(1, len(perm)):
                            A = frozenset(sorted(perm))
                            C = frozenset(sorted(perm[i:]))
                            if i >1:
                                B = frozenset(sorted(perm[0:i]))
                            else:
                                B = perm[0]
                            if A in item_count and B in item_count:
                                numerator = item_count[A]
                                denominator = item_count[B]
                                conf =  ((numerator/denominator)*100) 
                                if conf >= min_confidence:
                                    rule_set.add(str(B) + " --> " + str(C) + " Confidence: " + str(conf))

                    else:
                        A = frozenset(perm)
                        B = perm[0]
                        if A in item_count and B in item_count:
                                numerator = item_count[A]
                                denominator = item_count[B]
                                conf =  ((numerator/denominator)*100) 
                                if conf >= min_confidence:
                                    rule_set.add(str(B) + " --> " + str(perm[1]) + " Confidence: "+ str(conf))
                                    
        print("\nAPRIORI ASSOCIATION RULES:")
        for rule in rule_set:
            print(rule)
        

def brute_force(min_support, min_confidence, db_file):
    list_transactions = []
    item_count ={}
    with open(db_file, mode='r', encoding='utf-8-sig') as csv_file:
        num_rows = 0
        for row in csv.reader(csv_file):
            num_rows += 1
            line = row[0].split(", ")
            list_transactions.append(line)
            for word in line:
                if word in item_count:
                    item_count[word.strip()] += 1
                else:
                    item_count[word.strip()] = 1
                    
        min_support *= num_rows
                    
        set_transactions = set(frozenset(i) for i in list_transactions)

        items = []
        for item in item_count:
            items.append(item)

                

        
        freq_itemset = set()
        
        for i in range(2, len(items)):
            check_freq = False
            temp = Brute_Generate_Itemsets(items, i)
            temp_set=set(frozenset(j) for j in temp)
            for s in temp_set:
                supp = getSupport(set_transactions, s)
                if supp >= min_support:
                    item_count[s] = supp
                    freq_itemset.add(s)
                    check_freq = True
            if check_freq == False:
                break
                    
        rule_set = set()
        for comb in freq_itemset:
            if type(comb) != str:
                perms = list(getPermutations(comb, len(comb)))
                perms.sort()
                for perm in perms:
                    if len(perm)>2:
                        for i in range(1, len(perm)):
                            A = frozenset(sorted(perm))
                            C = frozenset(sorted(perm[i:]))
                            if i >1:
                                B = frozenset(sorted(perm[0:i]))
                            else:
                                B = perm[0]
                            if A in item_count and B in item_count:
                                numerator = item_count[A]
                                denominator = item_count[B]
                                conf =  ((numerator/denominator)*100) 
                                if conf >= min_confidence:
                                    rule_set.add(str(B) + " --> " + str(C) + " Confidence: " + str(conf))

                    else:
                        A = frozenset(perm)
                        B = perm[0]
                        if A in item_count and B in item_count:
                                numerator = item_count[A]
                                denominator = item_count[B]
                                conf =  ((numerator/denominator)*100) 
                                if conf >= min_confidence:
                                    rule_set.add(str(B) + " --> " + str(perm[1]) + " Confidence: "+ str(conf))
        
        print("\n\nBRUTE FORCE ASSOCIATION RULES")
        for rule in rule_set:
            print(rule)
        
if __name__=="__main__":
    # Get user input to determine min confidence and database
    support    = input("What would you like the minimum support to be? (Enter whole number like 20) ")
    confidence = input("What would you like the minimum confidence to be? (Enter whole number like 30) ")
    db_num     = input("What database would you like to access? (Enter number between 1 and 5) ")
    
    # Find the min support and confidence based off the number of transactions
    min_support = int(support)/100
    min_confidence = int(confidence)
    
    
    db_file = "Database" + str(db_num) + ".csv" 
    
    # Run Apriori method with given support. confidence, and database
    start = time.time()
    apriori(min_support, min_confidence, db_file)
    end = time.time()
    
    print("\nAPRIORI RUN TIME: " + str(end-start) + " seconds\n")
    
    print("____________________________________________________________________")
    
    # Run Brute Force method with given support, confidence, and database
    start = time.time()
    brute_force(min_support, min_confidence, db_file)
    end = time.time()
    
    print("\nBRUTE FORCE RUN TIME: " + str(end-start) + " seconds")
        

