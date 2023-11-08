from datetime import datetime
from typing import Any, Dict, List, Optional

from elementary.monitor.alerts.alert import AlertModel

DBT_TEST_TYPE = "dbt_test"


class TestAlertModel(AlertModel):
    def __init__(
        self,
        id: str,
        test_unique_id: str,
        elementary_unique_id: str,
        test_name: str,
        severity: str,
        table_name: str,
        test_type: str,
        test_sub_type: str,
        test_results_description: str,
        test_results_query: str,
        test_short_name: str,
        alert_class_id: str,
        model_unique_id: str,
        test_description: Optional[str] = None,
        other: Optional[Dict] = None,
        test_params: Optional[Dict] = None,
        test_rows_sample: Optional[List[Dict]] = None,
        column_name: Optional[str] = None,
        detected_at: Optional[datetime] = None,
        database_name: Optional[str] = None,
        schema_name: Optional[str] = None,
        owners: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        subscribers: Optional[List[str]] = None,
        status: Optional[str] = None,
        suppression_interval: Optional[int] = None,
        timezone: Optional[str] = None,
        report_url: Optional[str] = None,
        alert_fields: Optional[List[str]] = None,
        elementary_database_and_schema: Optional[str] = None,
        integration_params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(
            id,
            alert_class_id,
            model_unique_id,
            detected_at,
            database_name,
            schema_name,
            owners,
            tags,
            subscribers,
            status,
            suppression_interval,
            timezone,
            report_url,
            alert_fields,
            elementary_database_and_schema,
            integration_params,
        )
        self.table_name = table_name
        self.test_type = test_type
        self.test_sub_type = test_sub_type
        self.test_results_description = test_results_description.capitalize()
        self.test_results_query = test_results_query.strip()
        self.test_short_name = test_short_name
        self.other = other or {}
        self.test_params = test_params or {}
        self.test_rows_sample = test_rows_sample or []
        self.column_name = column_name
        self.test_unique_id = test_unique_id
        self.elementary_unique_id = elementary_unique_id
        self.test_name = test_name
        self.severity = severity
        self.test_description = test_description
        self.error_message = self.test_results_description

    @property
    def table_full_name(self) -> str:
        table_full_name_parts = [
            name
            for name in [self.database_name, self.schema_name, self.table_name]
            if name
        ]
        return ".".join(table_full_name_parts).lower()

    @property
    def test_display_name(self) -> str:
        return self.display_name(self.test_name)

    @property
    def test_sub_type_display_name(self) -> str:
        return self.display_name(self.test_sub_type)

    @property
    def is_elementary_test(self) -> bool:
        return self.test_type != DBT_TEST_TYPE

    @staticmethod
    def display_name(str_value: str) -> str:
        return str_value.replace("_", " ").title()

    @property
    def data(self) -> Dict:
        return dict(
            id=self.id,
            alert_class_id=self.alert_class_id,
            model_unique_id=self.model_unique_id,
            detected_at=self.detected_at,
            database_name=self.database_name,
            schema_name=self.schema_name,
            owners=self.owners,
            tags=self.tags,
            subscribers=self.subscribers,
            status=self.status,
            suppression_interval=self.suppression_interval,
            test_unique_id=self.test_unique_id,
            elementary_unique_id=self.elementary_unique_id,
            test_name=self.test_name,
            test_display_name=self.test_display_name,
            severity=self.severity,
            table_name=self.table_name,
            table_full_name=self.table_full_name,
            test_type=self.test_type,
            test_sub_type=self.test_sub_type,
            test_sub_type_display_name=self.test_sub_type_display_name,
            test_results_description=self.test_results_description,
            test_results_query=self.test_results_query,
            test_short_name=self.test_short_name,
            test_description=self.test_description,
            other=self.other,
            test_params=self.test_params,
            test_rows_sample=self.test_rows_sample,
            column_name=self.column_name,
        )

    @property
    def concise_name(self):
        if self.is_elementary_test:
            return f"{self.test_short_name or self.test_name} - {self.test_sub_type_display_name}"
        else:
            return f"{self.test_short_name or self.test_name}"