# BQ-Data-Load

This Script will be getting a Solana owned account/ list of Solana owned accounts as input and then it will be doing the following work:
1. **Fetching the list of historical transaction signatures for each account**
2. **Fetching the detail of each transaction signature, representing the details of every historical transaction that involved a Solana owned account**
3. **Load it into BigQuery**

_Basically, this script loads historical data related to solana owned accounts into the BigQuery table_


**Prerequisites:**
1. A `Schema File` in `.json` format to be passed it to the BigQuery Table
2. A `Source File` to read data from, in the `.json` format
3. A `Service Account` with Required Permissions

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
