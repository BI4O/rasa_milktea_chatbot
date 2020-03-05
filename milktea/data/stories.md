## only greet 
* greet
  - utter_greet
  - utter_ask_order_what

## order naicha
* order{"type": "奶茶"}
  - slot{"type": "奶茶"}
  - utter_ask_size
* inform_size{"size": "大"}
  - slot{"size": "大"}
  - utter_affirm
* confirm
  - action_charge
  - utter_goodbye

## order kafei
* order{"type": "咖啡"}
  - slot{"type": "咖啡"}
  - utter_ask_size
* inform_size{"size": "中"}
  - slot{"size": "中"}
  - utter_affirm
* confirm
  - action_charge
  - utter_goodbye

## order kafei2
*  order{"type": "咖啡", "size": "大"}
  - slot{"type": "咖啡", "size": "大"}
  - utter_affirm
* confirm
  - action_charge
  - utter_goodbye

## order naicha2
* order{"type": "奶茶", "size": "特大"}
  - slot{"type": "奶茶", "size": "特大"}
  - utter_affirm
* confirm
  - action_charge
  - utter_goodbye
