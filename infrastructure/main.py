from aws_cdk import App
from dynamodb import DynamoDBStack
from lambdas import LambdaStack


app = App()

dynamodb_stack = DynamoDBStack(app, "DynamoDBStack")
lambda_stack = LambdaStack(
    app,
    "LambdaStack",
    table_name=dynamodb_stack.table.table_name,
)

app.synth()
