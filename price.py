import typing as t
from datetime import datetime, timedelta, date
import simplejson
from marshmallow import Schema, fields
from marshmallow.validate import Range


# HELPERS
def today() -> date:
    return datetime.now().date()


def today_minus_15_days() -> date:
    today = datetime.now()
    minus_15 = today - timedelta(days=15)
    return minus_15.date()


# SCHEMAS
class ValidationMessage(Schema):
    message = fields.Dict()


class ValidationErrorSchema(Schema):
    errors = fields.Nested(ValidationMessage)


class PopDetailsRequest(Schema):
    start_date = fields.Date(
        missing=today_minus_15_days,
        # format="YYYY-MM-DD",
        description="Inclusive date to start search from. Default 15 days ago",
    )
    end_date = fields.Date(
        missing=today,
        # format="YYYY-MM-DD",
        description="Inclusive date to end search. Default Today",
    )
    page = fields.Integer(missing=1, desciption="for paginating results")
    max_per_page = fields.Integer(
        missing=3000, validate=Range(max=3000), description="max results per page"
    )


class PopDetailsResponse(Schema):
    date = fields.Str(required=True, example="2022-02-02")
    media_paid_brand = fields.Str(
        required=True,
        example="Clorox",
    )
    player_paid_brand = fields.Str(required=True, example="Clorox")
    store_number = fields.Str(required=True, example="6350")
    plays = fields.Int(required=True, example=372)
    media_name = fields.Str(
        required=True, example="Clorox_CleanUpCleanerAndBleach_360x1920P_20NOV21.mp4"
    )
    media_length = fields.Int(required=True, example=57)
    media_program_goal = fields.Str(example="Product Benefit")
    # total_media_air_time = fields.Int(
    #     required=True,
    #     example=44010
    # )
    player_in_store_category_location = fields.Str(
        required=True, example="Window Treatments"
    )
    player_form_factor = fields.Str(required=True, example="Vertical Video Banner")
    player_orientation = fields.Str(example="Landscape")
    player_agnostic_floorplan_location = fields.Str(
        example="Aisle 1 for electric shades"
    )
    advertised_product_category_3 = fields.Str(example="028-004-CLEANING")
    sku_1_primary = fields.Str(example="518238")
    sku_2 = fields.Str(example="1001805909")
    sku_3 = fields.Str(example="1000031996")


class PopDetailsListResponse(PopDetailsRequest):
    total_count = fields.Integer()
    current_page_count = fields.Integer()
    # see nested field yet
    proof_list = fields.List(fields.Nested(PopDetailsResponse))


class ImpressionRequest(Schema):
    start_date = fields.Date(
        missing=today_minus_15_days,
        # format="YYYY-MM-DD",
        description="Inclusive date to start search from. Default 15 days ago",
    )
    end_date = fields.Date(
        missing=today,
        # format="YYYY-MM-DD",
        description="Inclusive date to end search. Default Today",
    )
    page = fields.Integer(missing=1, desciption="for paginating results")
    max_per_page = fields.Integer(
        missing=1000, validate=Range(max=3000), description="max results per page"
    )


# This is a example of the field I mentioned
class UserSchema(Schema):
    name = fields.String()
    email = fields.String()
    created_at = fields.DateTime()
    since_created = fields.Method("get_days_since_created")

    def get_days_since_created(self, obj):
        return dt.datetime.now().day - obj.created_at.day
