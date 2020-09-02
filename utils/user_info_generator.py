import json

from utils.user_info_fields import UserInfoFields
from utils.fields_mapping import FieldsMapping


class UserInfoGenerator:
    MANDATORY_FIELDS = [
        UserInfoFields.USER_ID,
        UserInfoFields.EMAIL,
        UserInfoFields.FIRST_NAME,
        UserInfoFields.LAST_NAME,
        UserInfoFields.CITY
    ]
    NON_MANDATORY_FIELDS = [
        UserInfoFields.CAN_ACCESS_PLATFORM,
        UserInfoFields.MANAGER_EMAIL,
        UserInfoFields.MANAGER_ID,
        UserInfoFields.DEPARTMENT,
        UserInfoFields.COUNTRY,
        UserInfoFields.BUSINESS_UNIT,
        UserInfoFields.EXTRA_DATA,
    ]

    @classmethod
    def generate_from_json(cls, user_data: json, mapping: FieldsMapping) -> json:
        user_info = dict()
        for field in cls.MANDATORY_FIELDS:
            user_info[field] = mapping.get(field, user_data)
        for field in cls.NON_MANDATORY_FIELDS:
            if field in mapping:
                user_info[field] = mapping.get(field, user_data)
        return user_info
