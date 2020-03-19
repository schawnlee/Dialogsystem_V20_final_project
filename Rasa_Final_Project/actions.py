# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

class Room():
    def __init__(self, room_name="AN EMPTY ROOM", doors=[]):
        self.room_name = room_name
        self.doors = doors

    def get_doors(self):
        return self.doors

    def get_name(self):
        return self.room_name


map = {

    "OFFICE": [None, None, "OFFICE", "MEETING ROOM"],
    "MEETING ROOM": [None, "OFFICE", "LAB", "CAFE"],
    "LAB": ["MEETING ROOM", None, "AUDITORIUM", None],
    "AUDITORIUM": ["LAB", None, "MAIN ENTRANCE", None],
    "CAFE": [None, "MEETING", None, "MAIN ENTRANCE"]

}

mapping = {"WEST": 0, "NORTH": 1, "EAST": 2, "SOUTH": 3}

universe = []
for room_name, doors in map.items():
    room = Room(room_name, doors)
    universe.append(room)


def change_room(room_name, direction):
    current_room = Room()
    for room in universe:
        if room_name == room.get_name():
            current_room = room
            i = mapping[direction]
            return current_room.get_doors()[i]




from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class Update(Action):

     def name(self) -> Text:
         return "action_update"

     def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        CURRENT_ROOM = tracker.get_slot("room")
        DIRECTION = tracker.get_slot("direction").upper()

        if CURRENT_ROOM == "MAIN ENTRANCE":
            dispatcher.utter_message(template = "utter_goodbye")
        elif change_room(CURRENT_ROOM,DIRECTION):
            CURRENT_ROOM = change_room(CURRENT_ROOM,DIRECTION)
            dispatcher.utter_message(text="You are now in {}".format(CURRENT_ROOM))
        else:
            dispatcher.utter_message(template = "utter_no_way_out")
        return [SlotSet("room", CURRENT_ROOM), SlotSet("direction", None)]
