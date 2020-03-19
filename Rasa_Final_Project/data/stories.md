## happy path
* greet
  - utter_greet
  
## tell a direction
* inform{"direction":"east"}
  - slot{"direction":"east"}
  - action_update

## repeat path  
* greet
  - utter_greet
* greet
  - utter_greet
* greet
  - action_restart

  

