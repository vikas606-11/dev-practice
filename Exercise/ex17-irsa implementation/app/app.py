import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

table = dynamodb.Table("irsa-demo-table")

# Put Item
table.put_item(
    Item={
        "id": "1",
        "name": "Vikas"
    }
)

print("PutItem Successful")

# Get Item
response = table.get_item(
    Key={
        "id": "1"
    }
)

print("GetItem Response:")
print(response.get("Item"))

# Update Item
table.update_item(
    Key={
        "id": "1"
    },
    UpdateExpression="SET #n = :value",
    ExpressionAttributeNames={
        "#n": "name"
    },
    ExpressionAttributeValues={
        ":value": "Cloud Engineer"
    }
)

print("UpdateItem Successful")