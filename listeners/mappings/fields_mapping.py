import logging
from typing import Union, List, Dict, Set

from common.type_hints import JSONType
from listeners.mappings.user_info_fields import UserInfoFields


class FieldsMapping:

    def __init__(self,
                 user_id_col: str,
                 first_name_col: str,
                 last_name_col: str,
                 email_col: str,
                 can_access_platform: str,
                 manager_id_col: str,
                 manager_email_col: str,
                 departments_ordered_cols: List[str],
                 city_col: str,
                 country_col: str,
                 business_unit_col: str,
                 extra_data_cols: Set[str],
                 ):
        self.fields_mappings: Dict[UserInfoFields, str] = {
            UserInfoFields.USER_ID: user_id_col,
            UserInfoFields.FIRST_NAME: first_name_col,
            UserInfoFields.LAST_NAME: last_name_col,
            UserInfoFields.EMAIL: email_col,
            UserInfoFields.CAN_ACCESS_PLATFORM: can_access_platform,
            UserInfoFields.MANAGER_ID: manager_id_col,
            UserInfoFields.MANAGER_EMAIL: manager_email_col,
            UserInfoFields.DEPARTMENT: departments_ordered_cols,
            UserInfoFields.CITY: city_col,
            UserInfoFields.COUNTRY: country_col,
            UserInfoFields.BUSINESS_UNIT: business_unit_col,
            UserInfoFields.EXTRA_DATA: extra_data_cols
        }

    GRADE_ATTR = "Grade level"
    LEADER_ATTR = "People_Leader"

    def get(self, field: UserInfoFields, user_data: JSONType) -> Union[str, int, bool, List[str], JSONType]:
        try:
            if field == UserInfoFields.DEPARTMENT or field == UserInfoFields.EXTRA_DATA:
                if field not in self.fields_mappings:
                    return []
                dep_or_extra = list()
                for mapped_field in self.fields_mappings[UserInfoFields.DEPARTMENT]:
                    if mapped_field in user_data:
                        dep_or_extra.append(user_data[mapped_field])
                    else:
                        logging.warning(f'{mapped_field=} not in {user_data=}')
                return dep_or_extra
            if field == UserInfoFields.CAN_ACCESS_PLATFORM:
                if self.GRADE_ATTR not in user_data or self.LEADER_ATTR not in user_data:
                    logging.warning(f'{self.GRADE_ATTR} or {self.LEADER_ATTR} not in {user_data=}')
                    return None
                grade = int(user_data[self.GRADE_ATTR])
                leader = user_data[self.LEADER_ATTR] == 'Y'
                return grade >= 6 and leader
            if field in self.fields_mappings:
                mapped_field = self.fields_mappings[field]
                if mapped_field in user_data:
                    return user_data[mapped_field]
                else:
                    logging.warning(f'{mapped_field=} not in {user_data=}')
        except Exception as e:
            logging.exception(e)
            logging.error(f'could not extract {field=} from {user_data=}')
        logging.warning(f'returning None for {field=}, from {user_data=}')
        return None
