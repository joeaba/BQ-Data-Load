import os

os.system('gcloud config configurations activate xxx')
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/xxx/xxx/gcpxxxlineuserxxx.json'
os.system('gcloud auth activate-service-account xxx@xxx.iam.gserviceaccount.com --key-file=/xxx/xxx.json')

file1 = open("SOL transaction data load into BQ - accounts.txt")
output = file1.readlines()
file1.close()
for i in range(len(output)):
    output[i] = output[i].strip('\n')
    
x = input('Enter the account signature that you want to check')
if not(os.path.exists('last transaction details.txt')):
    fhand5 = open('last transaction details.txt','a')
    fhand5.close()

fhand5 = open('last transaction details.txt')
output2 = fhand5.readlines()
fhand5.close()

count_pos = 0
accountFound = False

for row in output2:
    row = row.strip('\n')
    row = row.split(',')
    if x.strip('\n') == row[0]:
        accountFound = True

if not accountFound:
    FHAND1 = os.popen('solana-ledger-tool bigtable transaction-history -l . '+x)
    output3 = FHAND1.readlines()
    FHAND1.close()
    FHAND2 = open('list_of_signature.txt','w')
    #Writing to the "signature list" file
    for detail_ in output3:
        FHAND2.write(detail_)
        print('printing detail_')
        print(detail_)

    FHAND2.close()
    row = x + "," + detail_
    fhand = open("last transaction details.txt",'a')
    fhand.write(row)
    fhand.close()

else:
    fhand5 = open('last transaction details.txt')
    output9 = fhand5.readlines()
    fhand5.close()
    for row in output9:
        row = row.strip('\n')
        row = row.split(',')
        if row[0] == x:
            last_txn_recorded = row[1]
        fhand4 = os.popen('solana-ledger-tool bigtable transaction-history --before ' + last_txn_recorded + ' -l . ' + x)
        output1 = fhand4.readlines()
        fhand4.close()
        if len(output1) > 0:
            fhand3 = open('list_of_signature.txt','w')
            # Writing to the "list of signatures" file
            for sig in output1:
                fhand3.write(sig)
            fhand3.close()


            print('check15')
            fin = open("last transaction details.txt", "rt")
            #read file contents to string
            data = fin.read()
            #replace all occurrences of the required string
            data = data.replace(last_txn_recorded, output1[-1])
            #close the input file
            fin.close()
            #open the input file in write mode
            fin = open("last transaction details.txt", "w", newline='')
            #overrite the input file with the resulting data
            fin.write(data)


file1 = open("list_of_signature.txt")
output2 = file1.readlines()

for sig2_ in output2:
    fhand5 = os.popen('curl -X POST -H "Content-Type: application/json" -d \'{"jsonrpc":"2.0", "id":1, "method":"getConfirmedTransaction","params":["'+sig2_.strip("\n")+'","json"]}\' https://api.mainnet-beta.solana.com')
    output2 = fhand5.readlines()
    fhand5.close()
    fhand6 = open('signature_details.json','w')
    #Writing to the "signature details" file
    for detail_ in output2:
        fhand6.write(detail_)
    fhand6.close()
    
if not(os.path.exists('signature_details.json')):
    fhand5 = open('signature_details.json','w')
    fhand5.close()
fhand7 = open('signature_details.json')
output3 = fhand7.readlines()
fhand7.close()
for details_ in output3:
    #   print(details_)
    os.system('gcloud config configurations activate xxx-config')
    fhandle1 = open('single_signature_detail.json', 'w')
    fhandle1.write(details_)
    fhandle1.close()
    os.system('gcloud config configurations activate xxx')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/xxx/gcpxxxlineuserxxx.json'
    os.system('gcloud auth activate-service-account xxx@xxx.iam.gserviceaccount.com --key-file=/xxx/gcpxxxlineuser.json')
    os.popen('bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON xxx.xxx /home/xxx/xxx/xxx/solana/xxx/xxxx/solana-release/xxx/single_signature_detail.json /xxx/xxx.json')
    #print("BigQuery load number counter1="+ str(counter1))
    #print("BigQuery load number counter2="+ str(counter2))

file1.close()
