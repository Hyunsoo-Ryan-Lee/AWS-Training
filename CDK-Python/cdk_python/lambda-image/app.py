import json
import pandas as pd




def handler(event, context):
    df = pd.read_csv("titanic.csv")
    cols = df.columns
    print(cols)
    return {
        'statusCode': 200,
        'body': json.dumps(f"hello everyone!\n\n{cols}")
    }