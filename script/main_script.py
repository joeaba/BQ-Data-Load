import os
import re 
import time
import datetime
import setup_credential
import helper_script
fhand15 = open('acc_to_check.txt')
OUTPUT = fhand15.readlines()
fhand15.close()
if os.path.exists('list_of_sig.txt'):
    os.remove('list_of_sig.txt')

for x in OUTPUT:
    setup_credential.mainnet_cred()
    x = x.strip('\n')
    if not(os.path.exists("last_transac.txt")):
        fhand5 = open("last_transac.txt",'a')
        fhand5.close()

    fhand5 = open("last_transac.txt")
    output2 = fhand5.readlines()
    fhand5.close()

    accountFound = False

    for row in output2:
        row = row.strip('\n')
        row = row.split(',')
        if x.strip('\n') == row[0]:
            accountFound = True
            pass

    if not accountFound:
        FHAND1 = os.popen('solana-ledger-tool bigtable transaction-history -l . '+x)
        output3 = FHAND1.readlines()
        FHAND1.close()
        FHAND2 = open("list_of_sig.txt",'w')
        for detail_ in output3:
            FHAND2.write(detail_)
        FHAND2.close()

        row = x + "," + detail_
        fhand = open("last_transac.txt",'a')
        fhand.write(row)
        fhand.close()
    else:
        print('The Account is Already existing in the last_transaction.txt file')
        fhand5 = open("last_transac.txt")
        output9 = fhand5.readlines()
        fhand5.close()
        for row in output9:
            row = row.strip('\n')
            row = row.split(',')
            if row[0] == x:
                last_txn_recorded = row[1]
                fhand4 = os.popen('solana-ledger-tool bigtable transaction-history --before ' + last_txn_recorded + ' -l . ' + x)
                time.sleep(4)
                output1 = fhand4.readlines()
                fhand4.close()
                if len(output1) > 0:
                    fhand3 = open('list_of_sig.txt','w')
                    for sig in output1:
                        fhand3.write(sig)
                    fhand3.close()

                    fin = open("last_transac.txt")
                    data = fin.readlines()
                    fin.close()
                    fin = open("last_transac.txt", "w", newline='')
                    for data_strip in data:
                        data_strip = data_strip.replace(last_txn_recorded, output1[-1].strip('\n'))	
                        fin.write(data_strip)
                    fin.close()
                else:
                    if not (os.path.exists('list_of_sig.txt')):
                        fhand3b = open('list_of_sig.txt','w')
                        fhand3b.close()
                    break 
    
    file1 = open("list_of_sig.txt")
    fhand6 = open('sig_details.json','w')
    output2 = file1.readlines()
    file1.close()
    for sig2_ in output2:
        
        fhand5 = os.popen('curl -X POST -H "Content-Type: application/json" -d \'{"jsonrpc":"2.0", "id":1, "method":"getConfirmedTransaction","params":["'+sig2_.strip("\n")+'","json"]}\' https://api.mainnet-beta.solana.com')
        time.sleep(4)
        output3 = fhand5.readlines()
        fhand5.close()

        for detail_ in output3:
            detail_ = detail_.strip('\n')
            fhand6.write(detail_+'|')

    fhand6.close()
    if not(os.path.exists('sig_details.json')):
        fhand5 = open('sig_details.json','w')
        fhand5.close()
    fhand7 = open('sig_details.json')
    output4 = fhand7.readlines()
    fhand7.close()
    for details_ in output4:
        details_ = details_.split('|')
        for z in details_:
            fhandle1 = open('single_sig.json', 'w')
            fhandle1.write(z)
            fhandle1.close()

            setup_credential.default_cred()
            fhand1 = os.popen('pwd')
            output10 = fhand1.readlines()
            fhand1.close()
            output11 = output10[0].strip('\n')
            fhandle3 = os.popen('bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON bigtable.main_py ./single_sig.json ./bq_load.json')
            time.sleep(7)
            fhandle3.close()
helper_script.make_copy()
fhandle_4 = os.popen('bq query \--destination_table principal-lane-200702:bigtable.main_uuid \--append_table \--use_legacy_sql=false "SELECT \'GENERATE_UUID()\' AS uuid, * FROM bigtable.main_py"')
time.sleep(30)
fhandle_4.close()

fhandle_4 = os.popen('bq query \--destination_table principal-lane-200702:history.transaction_main \--append_table \--use_legacy_sql=false "SELECT sig.slot AS slot, sig.signature AS signature, uid.account_key AS account, ROUND(CAST(pre.balance_pre / 1000000000 AS FLOAT64),8) AS balance_pre, ROUND(CAST(pst.balance_post / 1000000000 AS FLOAT64),8) balance_post, ROUND(CAST((pst.balance_post - pre.balance_pre) / 1000000000 AS FLOAT64),8) AS amount, MAX(sig.blocktime) AS blocktime FROM ( SELECT ROW_NUMBER() OVER (PARTITION BY uuid) AS rank, Uuid, account_key AS account_key FROM bigtable.main_uuid CROSS JOIN UNNEST (result.transaction.message.accountKeys) AS account_key ) uid LEFT JOIN ( SELECT ROW_NUMBER() OVER (PARTITION BY uuid) AS rank, uuid, balance_pre AS balance_pre FROM bigtable.main_uuid CROSS JOIN UNNEST (result.meta.preBalances) AS balance_pre ) pre ON pre.uuid = uid.uuid AND pre.rank = uid.rank LEFT JOIN ( SELECT ROW_NUMBER() OVER (PARTITION BY uuid) AS rank, Uuid, balance_post AS balance_post FROM bigtable.main_uuid CROSS JOIN UNNEST (result.meta.postBalances) AS balance_post ) pst ON pst.uuid = uid.uuid AND pst.rank = uid.rank LEFT JOIN ( SELECT * FROM ( SELECT ROW_NUMBER() OVER (PARTITION BY uuid) AS rank,uuid,result.blocktime AS blocktime,result.slot AS slot,signature AS signature, FROM bigtable.main_uuid CROSS JOIN UNNEST (result.transaction.signatures) AS signature) WHERE rank = 1) sig ON sig.uuid = uid.uuid GROUP BY 1,2,3,4,5,6"')
time.sleep(30)
fhandle_4.close()

fhandle_4 = os.popen('bq query \--destination_table principal-lane-200702:history.transaction_frto \--append_table \--use_legacy_sql=false "SELECT blocktime, slot, hst.signature AS signature, hst.account AS account, CASE WHEN amount < 0 THEN hst.account ELSE neg.account END AS account_from, CASE WHEN amount > 0 THEN hst.account ELSE pos.account END AS account_to,amount FROM history.transaction_main hst LEFT JOIN (SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY signature ORDER BY amount DESC) AS rank, signature, account FROM history.transaction_main) WHERE rank = 1) pos ON pos.signature = hst.signature LEFT JOIN ( SELECT * FROM ( SELECT ROW_NUMBER() OVER (PARTITION BY signature ORDER BY amount ASC) AS rank, signature,account FROM history.transaction_main) WHERE rank = 1) neg ON neg.signature = hst.signature"')
time.sleep(30)
fhandle_4.close()


os.system('chmod +x write-all-stake-accounts.sh')

os.system('./write-all-stake-accounts.sh &')
time.sleep(17)
setup_credential.default_cred()
list1= []
with os.popen('ls | sort') as fhandle3:
    output12 = fhandle3.readlines()
    for output in output12:
        list1.append(output)
        #print(output)
        #print (list1)
    for index,ip in enumerate(list1,1):
        value1 = "-" + str(index)
        #print("list1 is : ",list1[int(value1)])
        list1[int(value1)] = list1[int(value1)].strip('\n')
        #print('list1[int(value1)] is: ',list1[int(value1)])
        output13 = re.search('^stake_accounts-.*csv$',list1[int(value1)])
        print("output13 is : ", output13)
        if output13:
            output15 = list1[int(value1)]
            break
            
# with os.popen('ls | sort') as fhandle3:
#     output12 = fhandle3.readlines()
#     for index,ip in enumerate(output12):
#         output12[index] = output12[index].strip('\n')
#         print('output12[index] is: ',output12[index])
#         output13 = re.search('^stake_accounts-.*csv$',output12[index])
#         if output13:
#             os.system('rm '+ip)

# os.system('rm stake_accounts-\b[0-9]{4}\b-\b[0-9]{2}-\b[0-9]{2}[-._]([01]?\d|2[0-3]):([0-5]?\d):([0-5]?\d).csv')
# os.system('./write-all-stake-accounts.sh &')
# time.sleep(10)
# setup_credential.default_cred()
# with os.popen('ls | sort') as fhandle3:
#     output12 = fhandle3.readlines()
#     for index,ip in enumerate(output12):
#         output12[index] = output12[index].strip('\n')
#         print('output12[index] is: ',output12[index])
#         output13 = re.search('^stake_accounts-.*csv$',output12[index])
#         if output13:
#             output15 = output12[index]


# os.system('./write-all-stake-accounts.sh &')
# time.sleep(10)
# setup_credential.default_cred()
# with os.popen('pwd') as fhand1:
#     output11 = fhand1.readline()
#     output11 = output11[0].strip('\n')
#     with os.popen('ls') as fhandle3:
#         output12 = fhandle3.readlines()
#         for index,ip in enumerate(output12):
#             output12[index] = output12[index].strip('\n')
#             output13 = re.search('^stake_accounts-.*csv$',output12[index])
#             if output13:
#                 output15 = ip

fhandle_4 = os.popen ('bq load --autodetect --source_format=CSV bigtable.lockup ./'+ output15)
time.sleep(15)
fhandle_4.close()
print('query is starting')
os.system(' bq query \--destination_table principal-lane-200702:bigtable.history \--use_legacy_sql=false "SELECT DATE(TIMESTAMP_SECONDS(blocktime)) AS datestamp, TIMESTAMP_SECONDS(blocktime) AS timestamp, EXTRACT(YEAR FROM TIMESTAMP_SECONDS(blocktime)) AS year_number, EXTRACT(MONTH FROM TIMESTAMP_SECONDS(blocktime)) AS month_number, hst.slot AS slot, hst.signature AS signature,hst.account AS account, CASE WHEN lck.date_lockup IS NOT NULL THEN CAST(lck.date_lockup AS STRING) WHEN lck.date_lockup IS NULL THEN \'None\' ELSE \'Unknown\' END AS date_lockup, account_from, account_to, IFNULL(amount,0) AS amount FROM (SELECT \'parameter\' AS join_parameter, blocktime, slot, signature, account, account_from,account_to, amount FROM history.transaction_frto) hst LEFT JOIN (SELECT account_address AS account, MAX(lockup_timestamp) AS date_lockup FROM bigtable.lockup WHERE lockup_timestamp IS NOT NULL GROUP BY 1 ) lck ON lck.account = hst.account_to"')
time.sleep(80)
