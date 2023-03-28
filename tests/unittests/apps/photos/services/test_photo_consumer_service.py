from pytest_mock import MockerFixture

from app.photos.services import photo_consumer_service


def test_consume_copies_file_to_destination(mocker: MockerFixture) -> None:
    # mocked_copy = mocker.patch("app.photos.services.photo_consumer_service.shutil.copy2")

    pcs = photo_consumer_service.PhotoConsumerService2(name="test")
    # mocker.patch.object(pcs.file_system_service, )
    pcs.print_something()
