# BQ-Data-Load

This Script will be getting a Solana owned account/ list of Solana owned accounts as input and then it will be doing the following work:
1. **Fetching the list of historical transaction signatures for each account**
2. **Fetching the detail of each transaction signature, representing the details of every historical transaction that involved a Solana owned account**
3. **Load it into BigQuery**

_Basically, this script loads historical data related to solana owned accounts into the BigQuery table_


**Prerequisites:**
1. A `Schema File` named as `bq_load` in `.json` format to be passed it to the BigQuery Table
2. A `Source File` named as `Acc_to_check` to read Accounts to be checked, in the `.txt` format
3. A `Service Account` with Required Permissions (i.e., BigTable Read, BigQuery Write) and its `Credentials` key file
4. The `Script File` named as `Main_Script.py`, `Setup_Credential.py`, `Helper_Script.py` at one place

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

(a). Need to create a service account with necessary permissions (i.e., BigTable Read, BigQuery Write) and then create and save a key file of it
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
export $PATH=PATH:/[LOCATION_OF_APPLICATIONS-EXE_FILE]
```
Example:
If for solana-ledger-tool the location is **`/home/[USER]/.local/share/solana/install/release/xxx/xxlxxexx/solana-release/bin/solana-ledger-tool`** then the path will be
```bash
export $PATH=PATH:/home/[USER]/.local/share/solana/install/release/xxx/xxlxxexx/solana-release/bin
```
If for solana-ledger-tool the location is **`/home/[USER]/.local/share/solana/install/releases/xxxxx/solana-release/bin/google-cloud-sdk/bin/gcloud`**
```bash
export $PATH=PATH:/home/[USER]/.local/share/solana/install/releases/xxxxx/solana-release/bin/google-cloud-sdk/bin
```
Note:
To find path for a .exe use `find / -iname [NAME_OF_EXE]`

Example:

`find / -iname solana-ledger-tool`

3. Use the parameters like key's file-name and the service-account-emailid used to create that key, and replace the corresponding reference inside the file named as Setup_Credential.py.

Example:

```bash
cred = str(output11) + '/[KEY-FILE-NAME.json]'
```
```bash
gcloud auth activate-service-account [EMAILID-OF-SERVICE-ACCOUNT]
```

4. Change the permissions of the file named as `write-all-stake-accounts.sh` by running the command 
```bash
chmod +x write-all-stake-accounts.sh
```
