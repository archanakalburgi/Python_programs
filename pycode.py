def reading_last_item(line):
    print(line)

flptr=open("/Users/archana/learn-code/git-what/ledger.txt","r")
for i in flptr:
    reading_last_item(i)
flptr.close()

# sum=0
# price=[]

# for i in flptr:
#     if flptr=Total:
#         price.append()

# print(sum)

# Date,Name, Item, Total
# 15-02-2020, ABVS, Rice, 10
# 15-02-2020,ABVS, Bali, 10
# 18-02-2020,ABVS, Bali, -10
# 20-02-2020,ABVS, soap, 230



# awk -F ',' '{print $4}' ledger.txt | tail -n 5 | awk '{n += $1}; END {print n}'

# example = "15-02-2020, ABVS, Rice, 10"
# 1, Extract 4th column
# 2. Totol/number -> number

# list = total
# sum(list)