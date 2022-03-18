import pytest

from project.dao.models import Director


class TestDirectorsView:
    url = "/directors/"

    @pytest.fixture
    def director(self, db):
        d = Director(name="Тим Бёртон")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture()

    @pytest.fixture
    def director_dao_service(self, director):
        with patch("project.services.directors_service.DirectorDAO") as mock:
            mock.return_value = Mock(
                get_one_by_id=Mock(return_value=DirectorSchema().dump(director)),
                get_all=Mock(return_value=DirectorSchema(many=True).dump([director])),
                get_by_limit=Mock(return_value=DirectorSchema(many=True).dump([director]))
            )
            yield mock

    def test_get_directors(self, client, director):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json == [
            {"id": director.id, "name": director.name},
        ]

    def test_director_pages(self, client, director):
        response = client.get("/directors/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1


class TestGenreView:
    url = "/directors/{director_id}"

    @pytest.fixture
    def director(self, db):
        d = Director(name="Владимир Бортко")
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_director(self, client, director):
        response = client.get(self.url.format(director_id=director.id))
        assert response.status_code == 200
        assert response.json == {"id": director.id, "name": director.name}

    def test_genre_not_found(self, client):
        response = client.get(self.url.format(director_id=1))
        assert response.status_code == 404
