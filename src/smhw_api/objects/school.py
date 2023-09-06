from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .subjects import Subject
from .tools import convert_datetime


@dataclass(slots=True)
class _SchoolPremiumFeatures:
    welfare_notes: bool
    white_label_enabled: bool
    custom_theme_enabled: bool
    collins_content: bool
    sanctions: bool
    on_call_enabled: bool


@dataclass(slots=True)
class _CollinsSettings:
    public_calendar_advert: bool
    teacher_class_task_advert: bool
    parent_class_task_advert: bool
    student_class_task_advert: bool


@dataclass(slots=True)
class PublicSchool:
    "Used for when searching for schools."
    id: int
    name: str
    address: str
    town: str
    post_code: str
    subdomain: str
    is_active: bool
    brand_color: str | None


@dataclass(slots=True)
class School:
    """The class "School" contains attributes related to a school, such as its ID, name, address, and
    employee and student IDs, as well as a list of subjects and a boolean indicating whether the school
    has praise points enabled.
    """

    id: int
    name: str
    subdomain: str
    address: str
    town: str
    post_code: str
    country: str
    phone_number: Any
    email: str
    website: str
    twitter: str
    facebook: str
    instagram: str
    school_phase_name: str
    latitude: int
    longitude: int
    created_at: datetime
    updated_at: datetime
    logo_url: str
    logo_name: str
    premium_features: _SchoolPremiumFeatures
    prospectus_url: str
    prospectus_name: str
    homepage_background_image_name: str
    homepage_background_image_url: str
    homepage_zones: bool
    homepage_active: bool
    homepage_background: str
    student_zone_root_id: int
    school_zone_root_id: int
    parent_zone_root_id: int
    links: dict  # may be used?
    employee_ids: list[int]
    collins_settings: _CollinsSettings
    brand_color: str
    only_positive_kudos_enabled: bool
    is_discussion_enabled: bool
    share_classroom_enabled: bool
    share_task_to_teams_enabled: bool
    notice_types_enabled: bool
    domains_for_email_import: str
    domain = str  # domains_for_email_import
    school_private_info_id: int
    time_zone: str
    registration_group_ids: list[int]
    has_o365_integration: bool
    active_directory_enabled: bool
    google_enabled: bool
    google_drive_uploads_disabled: bool
    dropbox_uploads_disabled: bool
    one_drive_uploads_disabled: bool
    hide_session_marks: bool
    hide_lesson_marks: bool
    satchel_classes_homework_ad: bool
    root_directory_id: int
    school_praise_info_id: int
    is_active: bool
    import_external_type: str
    imports_enabled: bool
    attendance_settings_id: int
    class_group_ids: list[int]
    seating_label_ids: list[int]
    import_photos_type: str
    early_access_enabled: bool
    account_switch_enabled: bool
    praise_points: bool  # if school has praise_points enabled
    kudos: bool
    kudos_import: bool
    kudos_writeback: bool
    smart_seating: bool
    core: bool
    homework: bool
    timetables: bool
    attendance: bool
    attendance_import_sessions: bool
    attendance_writeback_sessions: bool
    attendance_import_lessons: bool
    attendance_writeback_lessons: bool
    assessment: bool
    detentions: bool
    detentions_writeback: bool
    documents: bool
    xod_documents: bool
    contact_scope_consented: bool
    address_scope_consented: bool
    show_staff_codes_for_public: bool
    referred_incidents_enabled: bool
    partners_page_enabled: bool
    sanction_rule_ids: list[int]
    classroom_emails_scope_enabled: bool
    student_ids: list[int]
    parent_ids: list[int]
    pulse_promo: bool
    announcement_category_ids: list[int]
    subjects: list[Subject]

    def __post_init__(self):
        self.created_at = convert_datetime(self.created_at)
        self.updated_at = convert_datetime(self.updated_at)


@dataclass(slots=True)
class PublicSchoolSearch:
    schools: list[PublicSchool]
    selection_count: int
    offset: int
