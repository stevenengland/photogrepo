from datetime import datetime

import pytest
import time_machine

from app.common.services.file_name_generator_service import (
    FileNameGeneratorService,
)

iso8601_test_str = "2022-10-01"


@pytest.fixture(scope="function", name="fngs")
def file_name_generator_service() -> FileNameGeneratorService:
    fngs = FileNameGeneratorService()
    return fngs  # noqa: WPS331


@time_machine.travel(datetime.fromisoformat(iso8601_test_str))
def test_file_name_generator_should_create_correct_date_postfix_when_date_is_given(
    fngs: FileNameGeneratorService,
):
    assert (
        fngs.create_with_date_postfix("test1.tar.gz") == "test1_20221001000000.tar.gz"
    )
