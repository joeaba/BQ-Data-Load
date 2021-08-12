import os
import sys
fhand1 = os.popen('pwd')
output10 = fhand1.readlines()
output11 = output10[0].strip('\n')
fhand1.close()

os.system('gcloud config configurations activate mainnet-config')
cred = str(output11) + '/gcpcmdlineuser_mainnet.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= cred
os.system('gcloud auth activate-service-account anmol-bigtable-test@mainnet-beta.iam.gserviceaccount.com --key-file='+ cred)

def default_cred():
    fhand1 = os.popen('pwd')
    output10 = fhand1.readlines()
    output11 = output10[0].strip('\n')
    os.system('gcloud config configurations activate default')
    cred = str(output11) + '/gcpcmdlineuser.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=cred
    os.system('gcloud auth activate-service-account gcp-service-account@principal-lane-200702.iam.gserviceaccount.com --key-file='+cred)
def mainnet_cred():
    fhand1 = os.popen('pwd')
    output10 = fhand1.readlines()
    output11 = output10[0].strip('\n')
    os.system('gcloud config configurations activate mainnet-config')
    cred = str(output11) + '/gcpcmdlineuser_mainnet.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=cred
