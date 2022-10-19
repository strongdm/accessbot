import re
from grant_request_type import GrantRequestType
from .base_grant_helper import BaseGrantHelper
from ..exceptions import PermissionDeniedException
from ..util import VALID_TIME_UNITS, convert_duration_flag_to_timedelta
from readabledelta import readabledelta


class ResourceGrantHelper(BaseGrantHelper):
    def __init__(self, bot):
        self.__bot = bot
        self.__admin_ids = bot.get_admin_ids()
        self.__sdm_service = bot.get_sdm_service()
        super().__init__(bot, self.__sdm_service, self.__admin_ids, GrantRequestType.ACCESS_RESOURCE, 'AUTO_APPROVE_TAG', 'AUTO_APPROVE_ALL')

    def check_permission(self, sdm_object, sdm_account, searched_name):
        account_grant_exists = self.__sdm_service.account_grant_exists(sdm_object, sdm_account.id)
        if not self.__bot.config['ALLOW_RESOURCE_ACCESS_REQUEST_RENEWAL'] and account_grant_exists:
            raise PermissionDeniedException("You already have access to that resource!")

    def get_all_items(self):
        return self.__sdm_service.get_all_resources()

    def get_item_by_name(self, name, execution_id = None):
        return self.__get_resource(name, execution_id)

    def get_operation_desc(self):
        return "access"

    def can_try_fuzzy_matching(self):
        return self.__bot.config['ENABLE_RESOURCES_FUZZY_MATCHING']

    def __get_resource(self, resource_name, execution_id):
        role_name = self.__bot.config['CONTROL_RESOURCES_ROLE_NAME']
        if role_name and not self.__is_resource_in_role(resource_name, role_name):
            self.__bot.log.info("##SDM## %s GrantHelper.__get_resource resource not in role %s", execution_id, role_name)
            raise Exception("Access to this resource not available. Please contact your strongDM admins.")
        return self.__sdm_service.get_resource_by_name(resource_name)

    def __is_resource_in_role(self, resource_name, role_name):
        sdm_resources_by_role = self.__sdm_service.get_all_resources_by_role(role_name)
        return any(r.name == resource_name for r in sdm_resources_by_role)

    def get_flags_validators(self):
        return {
            'reason': self.reason_flag_validator,
            'duration': self.duration_flag_validator,
        }

    def reason_flag_validator(self, value: str):
        if len(value) == 0:
            raise Exception('You need to enter a valid reason after the "--reason" flag.')
        if self.__bot.config['REQUIRED_FLAGS'] is not None:
            self.__verify_reason_template_match(value)
        return True

    def duration_flag_validator(self, value: str):
        match = re.match(r'^\d+[a-zA-Z]?$', value)
        if not match:
            raise Exception('You need to enter a valid duration, e.g. 60m, 2h, etc.')
        short_time_unit = self.get_short_time_unit_from_duration(value)
        if short_time_unit is None:
            formatted_valid_time_units = ', '.join(VALID_TIME_UNITS.keys())
            raise Exception(f'You need to enter a valid duration unit. Valid units are: {formatted_valid_time_units}.')
        duration = int(re.search(r'\d+', value).group())
        if duration == 0:
            raise Exception('You need to enter a duration greater than zero.')
        duration_limit = self.__bot.config['GRANT_TIMEOUT_LIMIT']
        if duration_limit is not None:
            duration_timedelta = convert_duration_flag_to_timedelta(value)
            duration_limit_timedelta = convert_duration_flag_to_timedelta(f"{duration_limit}m")
            if duration_timedelta > duration_limit_timedelta:
                raise Exception(f"You need to enter a duration lesser or equals to {readabledelta(duration_limit_timedelta)}")
        return True

    def __verify_reason_template_match(self, value):
        reason_template_match = re.match(r'reason:/(.*)/', self.__bot.config['REQUIRED_FLAGS'])
        if reason_template_match is not None:
            template = reason_template_match.group(1)
            try:
                reason_template = re.compile(template)
            except:
                raise Exception('A reason template was defined, but it\'s invalid')
            if reason_template.match(value) is None:
                raise Exception(f'You need to provide a valid reason following the template: /{template}/.')
        return True

    def get_short_time_unit_from_duration(self, duration):
        time_unit_match = re.search(r'[a-zA-Z]', duration)
        short_time_unit = time_unit_match.group() if time_unit_match else 'm'
        if not VALID_TIME_UNITS.get(short_time_unit):
            return None
        return short_time_unit
