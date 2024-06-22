import pytest

from draw.draw_generator import find_hamiltonian_cycle, generate_draw
from draw.tests.mock.models.participant import *


@pytest.mark.django_db
@pytest.mark.parametrize('participants, blacklists', [
    ([participant0_userA, participant1_userA, participant2_userA],
     {}),
    ([participant0_userA, participant1_userA, participant2_userA],
     {participant0_userA: {participant1_userA}}),
])
def test_find_hamiltonian_cycle_should_find_cycle(participants, blacklists):
    # We'll look for a cycle 10 times to validate the algorithm
    for _ in range(10):
        # Use copies to avoid modifying the original data
        cycle = find_hamiltonian_cycle(participants.copy(), blacklists.copy())
        assert cycle is not None
        assert len(cycle) == 3
        # Check that all participants are in the cycle exactly once
        assert all(p in cycle for p in participants)
        # Check that no blacklisted participant comes after the participant in the cycle
        for i, p in enumerate(cycle):
            for b in p.blacklisted.all():
                assert b not in cycle[i + 1:]


def test_find_hamiltonian_cycle_should_not_find_cycle():
    participants = [participant0_userA, participant1_userA, participant2_userA]
    blacklists = {participant0_userA: {participant1_userA, participant2_userA}}
    assert find_hamiltonian_cycle(participants, blacklists) is None


@pytest.mark.django_db
def test_generate_draw_should_create_draw():
    participants = [participant0_userA, participant1_userA, participant2_userA]
    owner = userA
    draw = generate_draw(participants, owner)
    assert draw is not None
