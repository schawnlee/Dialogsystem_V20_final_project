# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

import random

class Room():
    def __init__(self, room_name="AN EMPTY ROOM", doors=[]):
        self.room_name = room_name
        self.doors = doors

    def get_doors(self):
        return self.doors

    def get_name(self):
        return self.room_name


map = {

    "OFFICE": [None, None, None, "MEETING ROOM"],
    "MEETING ROOM": [None, "OFFICE", "LAB", "CAFETERIA"],
    "LAB": ["MEETING ROOM", None, "AUDITORIUM", None],
    "AUDITORIUM": ["LAB", None, "MAIN ENTRANCE", None],
    "CAFETERIA": [None, "MEETING", None, "MAIN ENTRANCE"]

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




def office_event():
    paths = [" For emergency, there is nothing better then run STRAIGHT a way!", " Friday morning at 9:00, gathering for group picture infront of the entrance of the Cafeteria"]
    path = random.choice(paths)
    text = "Oh! This is Vlad's office, you find a note and it reads despite the bad light {}".format(path)
    return text

def cafe_event():
    foods = ["SANDWICH", "BANANA", "CHOCKLADBAL", "NODDLE BOX", "COFFEE", "ORANGE JUICE", "WATER", "COOKIES",
             "CINEMON BUN"]

    text = "You found some {}".format(random.choice(foods)) + " and took it, since you are thirsty and hungry, and you feel better!"
    return text

def event_scary():
    events = ["The light went suddenly out, it is completely dark", "These is some weird noise...", "You want to get out", "You are tired","You are missing your firends",
              "You promise your self not ever to oversleep"]
    text = random.choice(events)
    return text

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
            if random.random() < 0.5:
                if CURRENT_ROOM == "OFFICE":
                    dispatcher.utter_message(text=office_event())
                if CURRENT_ROOM == "CAFETERIA":
                    dispatcher.utter_message(text=cafe_event())
                else:
                    dispatcher.utter_message(text=event_scary())
            dispatcher.utter_message(text="You are now in {}".format(CURRENT_ROOM) + " Where do you want to go next?")

        else:
            dispatcher.utter_message(template = "utter_no_way_out")
        return [SlotSet("room", CURRENT_ROOM), SlotSet("direction", None)]
