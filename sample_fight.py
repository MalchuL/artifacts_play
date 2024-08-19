import argparse
import logging
import time

from dynaconf import settings

from src.playground.characters.character import Character
from src.playground.characters.remote.rest_api_character import RestApiCharacter
from src.rest_api_client.client import AuthenticatedClient

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--character", default=None)
parser.add_argument("--task")
args = parser.parse_args()

task_position = {"fight": (0, 1),
                 "harvest": (2, 0)}

cur_action = args.task
assert cur_action in task_position

if __name__ == '__main__':
    char_name = args.character or settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    print("items", character.inventory.items)
    print("equip" ,character.inventory.equipment)
    print("stats" ,character.stats)
    character.wait_until_ready()
    task_pos = task_position[cur_action]
    if tuple(character.position) != tuple(task_pos):
        character.move(*task_pos)
        character.wait_until_ready()
    for _ in range(15 * 60):

        if character.inventory.is_inventory_full():
            BANK_POS = [4, 1]
            character.move(*BANK_POS)
            character.wait_until_ready()
            for items in character.inventory.items:
                character.deposit_item(item=items.item, amount=items.quantity)
                character.wait_until_ready()

            character.move(*task_pos)
            character.wait_until_ready()

        if character.character_quest.is_task_completed() or character.character_quest.get_current_task() is None:
            print("-"*20)
            print(character.character_quest.get_current_task())
            print("-" * 20)
            cur_pos = character.position
            TASK_POS = [1, 2]
            character.move(*TASK_POS)
            character.wait_until_ready()
            if character.character_quest.get_current_task() is not None:
                character.character_quest.complete_task()
                character.wait_until_ready()

            character.character_quest.accept_new_task()
            character.wait_until_ready()

            character.move(*cur_pos)
            character.wait_until_ready()

        try:
            if cur_action == "fight":
                print("fight results", character.fight())
                character.wait_until_ready()
            elif cur_action == "harvest":
                character.harvest()
                character.wait_until_ready()

        except Exception as e:
            logger.error(e, stack_info=True)
            time.sleep(1)


            character.wait_until_ready()


