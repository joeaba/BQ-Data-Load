import os
import sys

fhand1 = os.popen('pwd')
output10 = fhand1.readlines()
output11 = output10[0].strip('\n')
print(output11)

os.system('gcloud config configurations activate mainnet-config')
cred = str(output11) + '/gcpcmdlineuser_mainnet.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= cred
os.system('gcloud auth activate-service-account anmol-bigtable-test@mainnet-beta.iam.gserviceaccount.com --key-file='+ cred)

file1 = open("SOL transaction data load into BQ - accounts.txt")
output = file1.readlines()
print(output)       #['HWFzm33hjwjHQB24np1bbW6oPy1xo8kGVfBe2cQyYM7E\n', 'A5x1aLP7ribPDuRNXcMaTAzwnyn3mFqK5Xewen4Zk    3q1\n']
print('check1')
file1.close()
for i in range(len(output)):
    output[i] = output[i].strip('\n')
    print(output[i])      #print single account at a time     HWFzm33hjwjHQB24np1bbW6oPy1xo8kGVfBe2cQyYM7E
    print('check2')
print (output)
def default_cred():
    os.system('gcloud config configurations activate default')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=cred
    os.system('gcloud auth activate-service-account gcp-service-account@principal-lane-200702.iam.gserviceaccount.com --key-file='+cred)
def mainnet_cred():
    os.system('gcloud config configurations activate mainnet-config')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=cred
    os.system('gcloud auth activate-service-account anmol-bigtable-test@mainnet-beta.iam.gserviceaccount.com --key-file='+cred)
