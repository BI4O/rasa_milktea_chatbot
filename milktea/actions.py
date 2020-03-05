# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message("Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCharge(Action):

    def name(self) -> Text:
        return "action_charge"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 价格表
        price1 = {
            "奶茶":5,
            "咖啡":6,
            "卡布奇诺":10
        }
        price2 = {
            "中":1,
            "大":1.5,
            "特大":2
        }

        # 提取饮料种类，规格
        type = tracker.get_slot("type")
        size = tracker.get_slot("size")
        if size not in ['中','大','特大']:
            dispatcher.utter_message("不好意思，只有中杯、大杯和特大杯")
            return []
        price = price1[type] * price2[size]

        dispatcher.utter_message("您的%s杯%s一共%s元" % (size, type, price))

        return []
