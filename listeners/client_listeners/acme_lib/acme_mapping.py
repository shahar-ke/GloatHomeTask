from utils.fields_mapping import FieldsMapping


class AcmeMapping(FieldsMapping):

    def __init__(self):
        super().__init__(user_id_col="UserId",
                         first_name_col="First_name",
                         last_name_col="Last_name",
                         email_col="Email_Id",
                         manager_id_col="Manager_userId",
                         manager_email_col="Manager_email",
                         departments_ordered_cols=["Department level 1", "Department level 2", "Department level 3"],
                         city_col="City",
                         country_col="Country",
                         business_unit_col="Business_unit",
                         extra_data_cols={"Grade level", "People_Leader", "Title", "Division", "Location"})
