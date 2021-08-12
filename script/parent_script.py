import os 
import time
import datetime
'''
fhand14 = os.popen('pwd')
output10 = fhand14.readlines()
fhand14.close()
output11 = output10[0].strip('\n')
'''
import copy_new_scripting2
import copy
'''
os.system('gcloud config configurations activate mainnet-config')
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/root/gcpcmdlineuser_mainnet.json'
os.system('gcloud auth activate-service-account anmol-bigtable-test@mainnet-beta.iam.gserviceaccount.com --key-file=/root/gcpcmdlineuser_mainnet.json')

file1 = open("SOL transaction data load into BQ - accounts.txt")
output = file1.readlines()
##print(output)       #['HWFzm33hjwjHQB24np1bbW6oPy1xo8kGVfBe2cQyYM7E\n', 'A5x1aLP7ribPDuRNXcMaTAzwnyn3mFqK5Xewen4Zk3q1\n']
print('check1')
file1.close()
for i in range(len(output)):
    output[i] = output[i].strip('\n')
    print(output[i])      #print single account at a time     HWFzm33hjwjHQB24np1bbW6oPy1xo8kGVfBe2cQyYM7E
    print('check2')
'''

##print(output)       #['HWFzm33hjwjHQB24np1bbW6oPy1xo8kGVfBe2cQyYM7E', 'A5x1aLP7ribPDuRNXcMaTAzwnyn3mFqK5Xewen4Zk3q1']
###print('check3')

print('Enter the account signature that you want to check')
fhand15 = open('Acc_to_check.txt')
OUTPUT = fhand15.readlines()
fhand15.close()
###print(OUTPUT)
#TIME_ = datetime.datetime.now()
if os.path.exists('list_of_sig.txt'):
    os.remove('list_of_sig.txt')
    print('removed the list_of_sig.txt')

for x in OUTPUT:
    print('check3')
    copy_new_scripting2.mainnet_cred()
    ###print(x)
    x = x.strip('\n')
    #x = input('Enter the account signature that you want to check')

    ###counter1 = 0
    if not(os.path.exists('last transac.txt')):
        print('check4')
        fhand5 = open('last transac.txt','a')
        fhand5.close()

    fhand5 = open('last transac.txt')
    print('check5')
    output2 = fhand5.readlines()
    print("initial output of last trx file is ", output2)
    fhand5.close()

    accountFound = False

    for row in output2:
        print('check5b')
        row = row.strip('\n')
        row = row.split(',')
        print(row)
        if x.strip('\n') == row[0]:
            ###print(row)
            accountFound = True
            break

    if not accountFound:
        print('check6')
        FHAND1 = os.popen('solana-ledger-tool bigtable transaction-history -l . '+x)
        output3 = FHAND1.readlines()
        ##print(output3)
        ###print('check7')
        FHAND1.close()
        FHAND2 = open("list_of_sig.txt",'w')
        #Writing to the "signature list" file
        for detail_ in output3:
            #print('check8')
            FHAND2.write(detail_)
            ###print('printing detail_')
            #print(detail_)
        FHAND2.close()

        ###print('check9')
        row = x + "," + detail_
        fhand = open("last transac.txt",'a')
        print('check10')
        fhand.write(row)
        fhand.close()
    else:
        print('The Account is Already existing in the last transaction')
        fhand5 = open('last transac.txt')
        output9 = fhand5.readlines()
        fhand5.close()
        #count_pos = 0
        print(output9)
        for row in output9:
            row = row.strip('\n')
            row = row.split(',')
            ###print(row)              #list = [account + element]
            print("second")
            if row[0] == x:
                last_txn_recorded = row[1]
                print(row[1])
                print("third")
                fhand4 = os.popen('solana-ledger-tool bigtable transaction-history --before ' + last_txn_recorded + ' -l . ' + x)
                time.sleep(4)
                print('check13')
                output1 = fhand4.readlines()
                print('output1 is ',output1)
                fhand4.close()
                if len(output1) > 0:
                    fhand3 = open('list_of_sig.txt','w')
                    print('check14a')
                    # Writing to the "list of signatures" file
                    for sig in output1:
                        print('check14')
                        #sig = sig.strip('\n')
                        print(sig)
                        fhand3.write(sig)
                    fhand3.close()

                    print('check15')
                    #last_txn_recorded = row[1]
                    fin = open("last transac.txt")
                    #read file contents to string
                    data = fin.read()
                    for data_strip in data:
                        #replace all occurrences of the required string
                        data_strip = data_strip.replace(last_txn_recorded, output1[-1])
                        #close the input file
                        fin.close()
                        #open the input file in write mode
                        fin = open("last transac.txt", "w", newline='')
                    #overrite the input file with the resulting data
                        fin.write(data_strip)
                        fin.close()
                        #copy.make_copy()
                        print('data to be writeen on file last is',data_strip)
                    break
                else:
                    print('check15b')
                    if not (os.path.exists('list_of_sig.txt')):
                        print('check15c')
                        fhand3b = open('list_of_sig.txt','w')
                        fhand3b.close()
                    print('list is empty')
                    break 
    
    file1 = open("list_of_sig.txt")
    fhand6 = open('sig_details.json','w')
    ###print('check16')
    output2 = file1.readlines()
    file1.close()
    print('output to be written on the bq for account',x ,'is ',output2)
    for sig2_ in output2:
        print('check17')
        
        fhand5 = os.popen('curl -X POST -H "Content-Type: application/json" -d \'{"jsonrpc":"2.0", "id":1, "method":"getConfirmedTransaction","params":["'+sig2_.strip("\n")+'","json"]}\' https://api.mainnet-beta.solana.com')
        time.sleep(4)
        output3 = fhand5.readlines()
        fhand5.close()

        for detail_ in output3:
            detail_ = detail_.strip('\n')
            print('check18')
            print(detail_)
            fhand6.write(detail_+'|')

    fhand6.close()
    ##print(detail_)
    ##print("checkcheck")
    ###print('check19')
    ##print(detail_)
    if not(os.path.exists('sig_details.json')):
        ###print('check4')
        fhand5 = open('sig_details.json','w')
        fhand5.close()
    fhand7 = open('sig_details.json')
    output4 = fhand7.readlines()
    fhand7.close()
    for details_ in output4:
        print('check20')
        ##print(details_)
        details_ = details_.split('|')
        for z in details_:
            fhandle1 = open('single_sig.json', 'w')
            fhandle1.write(z)
            fhandle1.close()
            #print(z)
            print("check21")

        #importing data from another script
            copy_new_scripting2.default_cred()
            ###print("Now loading the main__py")
            fhand1 = os.popen('pwd')
            output10 = fhand1.readlines()
            fhand1.close()
            output11 = output10[0].strip('\n')
            ###print(output11)fhand1.close()            
            ###print(output11)
            fhandle3 = os.popen('bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON bigtable.main_py '+output11+'/single_sig.json '+output11+'/bq_load.json')
            time.sleep(7)
            ###print("loading has been complete for the main__py")
            fhandle3.close()
    #break    
    ###print("Now, loading the main_uuid")
copy.make_copy()
fhandle_4 = os.popen('bq query \--destination_table principal-lane-200702:bigtable.main_uuid \--append_table \--use_legacy_sql=false "SELECT \'GENERATE_UUID()\' AS uuid, * FROM bigtable.main_py"')
time.sleep(30)
fhandle_4.close()


###print("Now, loading the transaction_main")
fhandle_4 = os.popen('bq query \--destination_table principal-lane-200702:history.transaction_main \--append_table \--use_legacy_sql=false "SELECT sig.slot AS slot, sig.signature AS signature, uid.account_key AS account, ROUND(CAST(pre.balance_pre / 1000000000 AS FLOAT64),8) AS balance_pre, ROUND(CAST(pst.balance_post / 1000000000 AS FLOAT64),8) balance_post, ROUND(CAST((pst.balance_post - pre.balance_pre) / 1000000000 AS FLOAT64),8) AS amount, MAX(sig.blocktime) AS blocktime FROM ( SELECT ROW_NUMBER() OVER (PARTITION BY uuid) AS rank, Uuid, account_key AS account_key FROM bigtable.main_uuid CROSS JOIN UNNEST (result.transaction.message.accountKeys) AS account_key ) uid LEFT JOIN ( SELECT ROW_NUMBER() OVER (PARTITION BY uuid) AS rank, uuid, balance_pre AS balance_pre FROM bigtable.main_uuid CROSS JOIN UNNEST (result.meta.preBalances) AS balance_pre ) pre ON pre.uuid = uid.uuid AND pre.rank = uid.rank LEFT JOIN ( SELECT ROW_NUMBER() OVER (PARTITION BY uuid) AS rank, Uuid, balance_post AS balance_post FROM bigtable.main_uuid CROSS JOIN UNNEST (result.meta.postBalances) AS balance_post ) pst ON pst.uuid = uid.uuid AND pst.rank = uid.rank LEFT JOIN ( SELECT * FROM ( SELECT ROW_NUMBER() OVER (PARTITION BY uuid) AS rank,uuid,result.blocktime AS blocktime,result.slot AS slot,signature AS signature, FROM bigtable.main_uuid CROSS JOIN UNNEST (result.transaction.signatures) AS signature) WHERE rank = 1) sig ON sig.uuid = uid.uuid GROUP BY 1,2,3,4,5,6"')
time.sleep(30)
fhandle_4.close()
###print("Now, loading the transaction__forto")
fhandle_4 = os.popen('bq query \--destination_table principal-lane-200702:history.transaction_frto \--append_table \--use_legacy_sql=false "SELECT blocktime, slot, hst.signature AS signature, hst.account AS account, CASE WHEN amount < 0 THEN hst.account ELSE neg.account END AS account_from, CASE WHEN amount > 0 THEN hst.account ELSE pos.account END AS account_to,amount FROM history.transaction_main hst LEFT JOIN (SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY signature ORDER BY amount DESC) AS rank, signature, account FROM history.transaction_main) WHERE rank = 1) pos ON pos.signature = hst.signature LEFT JOIN ( SELECT * FROM ( SELECT ROW_NUMBER() OVER (PARTITION BY signature ORDER BY amount ASC) AS rank, signature,account FROM history.transaction_main) WHERE rank = 1) neg ON neg.signature = hst.signature"')
time.sleep(30)
fhandle_4.close()
###print("Now, loading the history")
fhandle_4 = os.popen('bq query \--destination_table principal-lane-200702:history.history \--use_legacy_sql=false "SELECT DATE(TIMESTAMP_SECONDS(blocktime)) AS datestamp, TIMESTAMP_SECONDS(blocktime) AS timestamp, EXTRACT(YEAR FROM TIMESTAMP_SECONDS(blocktime)) AS year_number, EXTRACT(MONTH FROM TIMESTAMP_SECONDS(blocktime)) AS month_number, hst.slot AS slot, hst.signature AS signature,hst.account AS account, CASE WHEN lck.date_lockup IS NOT NULL THEN CAST(lck.date_lockup AS STRING) WHEN lck.date_lockup IS NULL THEN \'None\' ELSE \'Unknown\' END AS date_lockup, account_from, account_to, IFNULL(amount,0) AS amount FROM (SELECT \'parameter\' AS join_parameter,blocktime,slot, signature, account, account_from,account_to, amount FROM history.transaction_frto) hst LEFT JOIN ( SELECT account, MAX(date_lockup) AS date_lockup FROM bigtable.lockup WHERE date_lockup IS NOT NULL GROUP BY 1 ) lck ON lck.account = hst.account_to"')
time.sleep(3)
fhandle_4.close()
file1.close()

