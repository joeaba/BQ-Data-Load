import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/xxxx/xxxxx.json'
os.system('gcloud auth activate-service-account xxxxxx@xxxxxxx.iam.gserviceaccount.com --key-file=/xxxx/xxxx/xxxxx.json')

signatures = ['xxxxxxxxxxxxx','xxxxxxxxxxxx','xxxxxxxxxxxxx']
for element in signatures:
    fhand4 = os.popen('./solana-ledger-tool bigtable transaction-history -l . '+element)
    output1 = fhand4.readlines()
    fhand3 = open('list_of_signature.txt','a')

    # Writing to the "list of signatures" file
    for sig in output1:
        fhand3.write(sig)

        sig = sig.split("\n")[0]
        fhand5 = os.popen('curl -X POST -H "Content-Type: application/json" -d \'{"jsonrpc":"2.0", "id":1, "method":"getConfirmedTransaction","params":["'+sig+'","json"]}\' https://api.mainnet-beta.solana.com')
        output2 = fhand5.readlines()
        fhand6 = open('signature_details.json','a')

        #Writing to the "signature details" file
        for detail_ in output2:
            fhand6.write(detail_)
os.system('gcloud auth activate-service-account xxxxxx@xxxxxxx.iam.gserviceaccount.com --key-file=/xxxx/xxxxx/xxxxxx.json')
fhand7 = open('signature_details.json')
output3 = fhand7.readlines()
fhandle = open('single_signature_detail.json','w')

for details_ in output3:
    fhandle.write(details_)
    os.popen('bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON xxxxxxx.xxxx /xxxx/xxxx/xxxx/xxxx/xxxx.json /xxxx.json')


fhand3.close()
fhand4.close()
fhand5.close()
fhand6.close()
fhand7.close()
fhandle.close()
