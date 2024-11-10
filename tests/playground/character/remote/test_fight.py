
def test_fight(character):
    character.wait_until_ready()
    character.move(0,1)  # Chicken position
    character.wait_until_ready()
    character.fight()


def test_rest(character):
    character.wait_until_ready()
    character.rest()

