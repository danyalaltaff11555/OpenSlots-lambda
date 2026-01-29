from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Duration,
)
from constructs import Construct


class LambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, table_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        common_props = {
            "runtime": _lambda.Runtime.PYTHON_3_11,
            "timeout": Duration.seconds(30),
            "environment": {"DYNAMODB_TABLE": table_name},
        }

        self.booking_handler = _lambda.Function(
            self,
            "BookingHandler",
            handler="src/handlers/booking_handler.handler",
            code=_lambda.Code.from_asset("."),
            **common_props,
        )

        self.availability_handler = _lambda.Function(
            self,
            "AvailabilityHandler",
            handler="src/handlers/availability_handler.handler",
            code=_lambda.Code.from_asset("."),
            **common_props,
        )

        self.payment_handler = _lambda.Function(
            self,
            "PaymentHandler",
            handler="src/handlers/payment_handler.handler",
            code=_lambda.Code.from_asset("."),
            **common_props,
        )

        self.org_handler = _lambda.Function(
            self,
            "OrganizationHandler",
            handler="src/handlers/organization_handler.handler",
            code=_lambda.Code.from_asset("."),
            **common_props,
        )

        self.staff_handler = _lambda.Function(
            self,
            "StaffHandler",
            handler="src/handlers/staff_handler.handler",
            code=_lambda.Code.from_asset("."),
            **common_props,
        )

        self.api = apigw.RestApi(self, "BookingApi", rest_api_name="Booking API")

        bookings = self.api.root.add_resource("bookings")
        bookings.add_method("POST", apigw.LambdaIntegration(self.booking_handler))
        bookings.add_method("GET", apigw.LambdaIntegration(self.booking_handler))

        booking_id = bookings.add_resource("{id}")
        booking_id.add_method("GET", apigw.LambdaIntegration(self.booking_handler))
        booking_id.add_method("PATCH", apigw.LambdaIntegration(self.booking_handler))
        booking_id.add_method("DELETE", apigw.LambdaIntegration(self.booking_handler))

        availability = self.api.root.add_resource("availability")
        availability.add_method(
            "GET", apigw.LambdaIntegration(self.availability_handler)
        )

        orgs = self.api.root.add_resource("orgs")
        orgs.add_method("POST", apigw.LambdaIntegration(self.org_handler))

        org_id = orgs.add_resource("{id}")
        org_id.add_method("GET", apigw.LambdaIntegration(self.org_handler))
        org_id.add_method("PATCH", apigw.LambdaIntegration(self.org_handler))

        staff = self.api.root.add_resource("staff")
        staff.add_method("POST", apigw.LambdaIntegration(self.staff_handler))
        staff.add_method("GET", apigw.LambdaIntegration(self.staff_handler))

        staff_id = staff.add_resource("{id}")
        staff_id.add_method("GET", apigw.LambdaIntegration(self.staff_handler))
        staff_id.add_method("PATCH", apigw.LambdaIntegration(self.staff_handler))
        staff_id.add_method("DELETE", apigw.LambdaIntegration(self.staff_handler))
