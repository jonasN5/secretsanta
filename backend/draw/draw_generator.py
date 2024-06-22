import random

from draw.models import Draw, Participant, DrawPair, User


def find_hamiltonian_cycle(
        participants: list[Participant],
        constraints: dict[Participant, set[Participant]]) -> list[Participant] or None:
    """
    Find a Hamiltonian cycle in a graph with the given participants and constraints.
    A detailed explanation can be found here: https://binary-machinery.github.io/2021/02/03/secret-santa-graph.html
    :param participants: list of participants
    :param constraints: dictionary of a set of Participants that are blacklisted for each Participant
    :return: a list of participants representing the Hamiltonian cycle
    """

    class ResTreeNode:
        def __init__(self, participant: Participant):
            self.used_participants = set()
            self.cur_part = participant

        def __str__(self):
            return str(self.cur_part) + " (" + str(self.used_participants) + ")"

    res = []
    iteration = 0
    while True:
        iteration += 1
        constraints_len = 0
        if len(res) > 0:
            cur_user_id_node = res[-1]
            constraint_user_ids = constraints.get(cur_user_id_node.cur_part, set())

            if len(constraint_user_ids) or len(cur_user_id_node.used_participants):
                # move constrained and used ids to the end of the list
                index = 0
                scan_max = len(participants)
                while index < scan_max:
                    if (participants[index] in constraint_user_ids or participants[index]
                            in cur_user_id_node.used_participants):
                        participants.append(participants.pop(index))
                        scan_max -= 1
                        constraints_len += 1
                    else:
                        index += 1

        max_index = len(participants) - constraints_len
        need_go_back = max_index == 0
        if not need_go_back:
            index = random.randint(0, max_index - 1)
            user_id = participants.pop(index)
            res.append(ResTreeNode(user_id))

            if len(participants) == 0:
                cur_user_id_node = res[-1]
                constraint_user_ids = constraints.get(cur_user_id_node.cur_part, set())
                if res[0].cur_part in constraint_user_ids:
                    need_go_back = True
                else:
                    break

        if need_go_back:
            # return one step back
            if len(res) == 1:
                # no way to go back anymore, there is no solution
                return None

            cur_node = res.pop()
            participants.append(cur_node.cur_part)
            res[-1].used_participants.add(cur_node.cur_part)

    return [node.cur_part for node in res]


def generate_draw(participants: list[Participant], owner: User) -> Draw:
    """
    Generate a Draw instance from a list of participants.
    :param participants: list of participants
    :param owner: owner of the draw
    :return: a saved Draw instance
    """
    cycle = find_hamiltonian_cycle(list(participants), {p: {b for b in p.blacklisted.all()} for p in participants})

    draw = Draw.objects.create(owner=owner)
    # Generate a pair for each vertex in the cycle.
    pairs = []
    for i in range(len(cycle)):
        pairs.append(DrawPair(
            santa=cycle[i],
            santee=cycle[(i + 1) % len(cycle)],
            draw=draw,
        ))
    DrawPair.objects.bulk_create(pairs)
    return draw
