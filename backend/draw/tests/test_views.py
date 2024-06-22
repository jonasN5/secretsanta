from http import HTTPMethod

from common.tests.utils import ViewTestBase
from draw.models import Participant, Draw
from draw.tests.mock.models.draw import draw1_userA
from draw.tests.mock.models.participant import participant1_userA, participant2_userA, participant0_userA
from draw.tests.mock.models.user import userA


class TestParticipantsViewSet(ViewTestBase):

    def build_model(self, model):
        return {
            'id': model.id,
            'username': model.username,
            'email': model.email,
            'blacklisted': list(model.blacklisted.values_list('id', flat=True)),
        }

    def test_get(self):
        response = self.run(f'/participants/', HTTPMethod.GET)
        expected = [
            self.build_model(participant) for participant in
            [participant0_userA, participant1_userA, participant2_userA]
        ]

        assert response.status_code == 200, response.json()
        assert expected == response.json()

    def test_get_object(self):
        participant = participant1_userA
        response = self.run(f'/participants/{str(participant.id)}/', HTTPMethod.GET)
        expected = self.build_model(participant)
        assert response.status_code == 200, response.json()
        assert expected == response.json(), response.json()

    def test_delete_object(self):
        participant = participant1_userA
        response = self.run(f'/participants/{str(participant.id)}/', HTTPMethod.DELETE)
        assert response.status_code == 204, response.json()

    def test_patch_object(self):
        participant = participant1_userA
        data = {'username': 'new_username', 'blacklisted': [participant2_userA.id]}
        response = self.run(f'/participants/{str(participant.id)}/', HTTPMethod.PATCH, data)
        expected = self.build_model(participant)
        expected['username'] = 'new_username'
        expected['blacklisted'] = [participant2_userA.id]
        assert response.status_code == 200, response.json()
        assert expected == response.json(), response.json()

    #
    def test_post(self):
        data = {'username': 'some_username', 'email': 'new_valid_email@email.com', 'blacklisted': []}
        response = self.run('/participants/', HTTPMethod.POST, data)
        assert response.status_code == 201, response.json()

        expected = self.build_model(Participant(
            id=response.json()['id'],
            username=data['username'],
            email=data['email'],
        ))

        assert expected == response.json()


class TestDrawView(ViewTestBase):

    def build_model(self, model):
        return {
            'id': model.id,
            'owner': model.owner_id,
            'created_at': model.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'pairs': [{'santa': pair.santa_id, 'santee': pair.santee_id} for pair in model.pairs.all()],
        }

    def test_get(self):
        response = self.run(f'/draws/', HTTPMethod.GET)
        draws = [draw1_userA]
        expected = {
            'count': len(draws),
            'next': None,
            'previous': None,
            'results': [
                self.build_model(draw) for draw in draws
            ]
        }

        assert response.status_code == 200, response.json()
        assert expected == response.json()

    def test_post(self):
        # Get the initial count of draws
        initial_count = Draw.objects.filter(owner=userA).count()
        response = self.run(f'/draws/', HTTPMethod.POST)
        assert response.status_code == 201, response.json()

        # The draw should have been created
        assert initial_count + 1 == Draw.objects.filter(owner=userA).count()
        # We should get the latest draw in response
        draw = Draw.objects.order_by('-created_at').first()
        expected = self.build_model(draw)
        assert expected == response.json(), response.json()
