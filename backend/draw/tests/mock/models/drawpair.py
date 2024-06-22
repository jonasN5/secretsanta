from draw.models import DrawPair
from draw.tests.mock.models.draw import draw1_userA
from draw.tests.mock.models.participant import participant0_userA, participant1_userA, participant2_userA

drawpair1_draw1 = DrawPair(
    santa=participant0_userA,
    santee=participant1_userA,
    draw=draw1_userA,
)

drawpair2_draw1 = DrawPair(
    santa=participant1_userA,
    santee=participant2_userA,
    draw=draw1_userA,
)

drawpair3_draw1 = DrawPair(
    santa=participant2_userA,
    santee=participant0_userA,
    draw=draw1_userA,
)
models = [drawpair1_draw1, drawpair2_draw1, drawpair3_draw1]
