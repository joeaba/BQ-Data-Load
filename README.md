# BQ-Data-Load

This Script will be getting a Solana owned account/ list of Solana owned accounts as input and then it will be doing the following work:
1. **Fetching the list of historical transaction signatures for each account**
2. **Fetching the detail of each transaction signature, representing the details of every historical transaction that involved a Solana owned account**
3. **Load it into BigQuery**

_Basically, this script loads historical data related to solana owned accounts into the BigQuery table_


**Prerequisites:**
1. A `Schema File` in `.json` format to be passed it to the BigQuery Table
2. A `Source File` to read data from, in the `.json` format
3. A `Service Account` with Required Permissions and the `key` file related to it

## 1. Fetching the list of historical transaction signatures for each account

```bash
$ solana-ledger-tool bigtable transaction-history -l . [SOLANA_OWNED_ACCOUNT]
```

Output: List of transaction signatures 

```bash
xxxxxuQfUxaxx2xLx9xxxmxxxxxRxQxxxpx3xSxxxHxxx3x4x3xUxxxxexcxTxyxMxExxxzx
xyxxxPxtx6xexRxwxWxxxZxgxxxfx8xZxXxkxSxxxYxxxLxxxBxmxQ7xxx3VyFxrxXxkxxxx
xxxxxxxhxxxxhxxxx32xxxxxxxixmxxxxx3xxxx2xnxxmxxxx1xxyx8xxxrxex8xxxxx-xxx
```
## 2. Fetching the detail of each transaction signature

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"jsonrpc":xxxxxx, "id":xxxxx, "method":"getConfirmedTransaction", "params":["[TRANSACTION_SIGNATURE]","json"]}' https://api.mainnet-beta.solana.com
```

Output: Detail of each transaction signature

```bash
{"jsonrpc":"xxxx.xxxx","result":{"blockTime":xxxxxxxxxxx,"meta":{"err":xxxxxxx,"fee":xxxxxx,"innerInstructions":[],"logMessages":["Program xxxxxxxxxxxxxxxx invoke [x]","Program xxxxxxxxxxxx success"],"postBalances":[xxxx,xxxxx,xxxx],"postTokenBalances":[],"preBalances":[xxxx,xxxx,xxxx],"preTokenBalances":[],"rewards":[],"status":{xxx:xxx}},"slot":xxxx,"transaction":{"message":{"accountKeys":[xxx,xxxx,xxxx],"header":{"numReadonlySignedAccounts":xxx,"numReadonlyUnsignedAccounts":xxxx,"numRequiredSignatures":xxxx},"instructions":[{"accounts":[xxxxx,xxxxx],"data":xxxxxxxx,"programIdIndex":xxxxxxx}],"recentBlockhash":xxxxxxxxxxxxxxxxxxxxxx},"signatures":[xxxxxxxxxxxxxxxxxxxxxxxxxxxxx]}},"id":xxxx}
```

## 3. Load it into BigQuery

```bash
$ bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON [DATASET_NAME].[BIG_QUERY_TABLE_NAME] [SOURCE_FILE_LOCATION.json] .[SCHEMA_FILE_LOCATION.json]
```

## How to run data-load script 

Steps:
1. Install the **`gcloud`** executable and set it in **`PATH`**
2. Install the **`python 3.x`** and set it in **`PATH`**
3. Install the **`solana-ledger-tool`** executable and set it in **`PATH`**

Then Run the script using **`python3 [SCRIPT_FILENAME.PY]`**

## Steps followed to get the scripting file to run: 

1. Setup the gcloud credentials:

(a). Need to create a service account with necessary permissions and then create and save a key file of it
```bash
gcloud iam service-accounts create SERVICE_ACCOUNT_ID \
    --description="DESCRIPTION" \
    --display-name="DISPLAY_NAME"
````

(b). Optional: To grant your service account an IAM role on your project

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:SERVICE_ACCOUNT_ID@PROJECT_ID.iam.gserviceaccount.com" \
    --role="ROLE_NAME"
```

(c). Optional: To allow users to impersonate the service account,

```bash
gcloud iam service-accounts add-iam-policy-binding \
    SERVICE_ACCOUNT_ID@PROJECT_ID.iam.gserviceaccount.com \
    --member="user:USER_EMAIL" \
    --role="roles/iam.serviceAccountUser"
```
(d). To Create a new key file
```bash
gcloud iam service-accounts keys create KEY_FILE \ 
--iam-account=SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com
```

Output: A Service account is created and its key file is now downloaded to your machine.

2. To setup PATH for gcloud, solana-ledger-tool

```bash
export $PATH=PATH:/[LOCATION_OF_EXE_FILE]
```
Example:
If for solana-ledger-tool the location is **`/home/xxxxxx/.local/xxx/solana-release/xxx/xxlxxexx/release-xxxxxxx/xxxx/xxxxx/bin/solana-ledger-tool`** then the path will be
```bash
export $PATH=PATH:/home/xxxxxx/.local/xxx/solana-release/xxx/xxlxxexx/release-xxxxxxx/xxxx/xxxxx/bin
```
If for solana-ledger-tool the location is **`/home/xxxxxx/.local/xxx/xxx/gcloud-sdk/xxx/xxxx/xxxx/xxx/bin/gcloud`**
```bash
export $PATH=PATH:/home/xxxxxx/.local/xxx/gcloud-sdk/xxx/xxxx/xxxx/xxx/bin
```
Note:
To find path for a .exe use `find / -iname [NAME_OF_EXE]`

Example:

`find / -iname solana-ledger-tool`

3. To setup environment variable and authorising the service account, have to pass the `location` of `.json` file that contains the key credentials inside the script file

```bash
$ import os
$ os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/xxx/xxx/xxx.json'
$ os.system('gcloud auth activate-service-account xxxxx@xxxxx.iam.gserviceaccount.com --key-file=/xxx/xxx/xxx.json')
``` 
