# Planner
    
    Planner Domain Model

    Summary:
    Plan Space (YAML file) -- has --> State Definitions and Actions
    Plan Space -- is input to --> Planner
    Planner -- creates --> Plan
    
    Plan Space: 
    - A set of actions that can be performed to achieve a goal.  
    - A start state that represents the the starting state of the plan space. 
    - A goal state that represents the desired state of the plan space.
    - YAML defined.
    - EXAMPLE: https://github.com/milan-at-kms/planner/blob/master/plan-space_doc-auto_basic.yaml
    
    Action:
    - A set of preconditions that must be met before an action can be performed.
    - A set of post effects that are the result of performing an action.
    - A cost that represents the cost of performing an action.
    
    State:
    - A set of variables that represent the current state of the world.  
    - These variables can be used to determine if an action can be performed.
    
    Planner:
    - Creates plans by searching through the plan space to find a sequence of actions that will achieve the goal state.
    - Uses a cost function to determine the cost of a plan.
    - If there are multiple plans that achieve the goal state, the planner will return the plan with the lowest cost.
    - createPlan Uses the A* search algorithm to find the lowest cost plan.
    
    Plan
    - A sequence of actions that achieve the goal state.
    - The cost of a plan is the sum of the cost of each action in the plan.

## Clone the Repository
    
    git clone https://github.com/milan-at-kms/planner.git
    cd planner
    

## Installation
    
    pip install -r requirements.tx
    

## Usage
  ```
  python -m unittest -v test_planner
  ```

## Example Test Output
  ```
  test_05_advanced_planner_pre_condition_with_greater_than (test_planner.TestPlanner)
This test exercises the pre-condition with a greater than operator ...
PLAN  Advanced :

PLAN STEP 1: {'action': 'fetch_document', 'cost': 5}
PLAN STEP 2: {'action': 'ocr_large_document', 'cost': 100}
PLAN STEP 3: {'action': 'extract_labels_in_batch', 'cost': 1}
PLAN STEP 4: {'action': 'apply_rules', 'cost': 1}
PLAN STEP 5: {'action': 'capture', 'cost': 1}
PLAN STEP 6: {'action': 'storage', 'cost': 1}
Total Plan Cost:  109
ok
```

