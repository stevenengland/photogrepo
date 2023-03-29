from pytest_mock import MockerFixture

from app.photos.services import photo_consumer_service


def test_consume_copies_file_to_destination(mocker: MockerFixture) -> None:
    pcs = photo_consumer_service.PhotoConsumerService2()
    pcs.print_something()
