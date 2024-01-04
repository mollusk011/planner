
from copy import deepcopy

import heapq

"""
    Planner Domain Model:
    
    Plan Space: 
    - A set of actions that can be performed to achieve a goal.  
    - A start state that represents the the starting state of the plan space. 
    - A goal state that represents the desired state of the plan space.
    - YAML defined.
    
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

"""

class State:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, State):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

class Action:
    def __init__(self, name, cost, pre_conditions, post_effects):
        self.name = name
        self.cost = cost
        self.pre_conditions = pre_conditions
        self.post_effects = post_effects

class PlanSpace:
    def __init__(self, StartState, GoalState, Actions):
        self.start_state = StartState
        self.goal_state = [GoalState['state']]
        self.actions = [Action(**action['Action']) for action in Actions]



class Planner:

    def __init__(self, plan_space, costFn):
        self.start_state = plan_space.start_state
        self.goal_state = plan_space.goal_state
        self.costFn = costFn
        self.actions = plan_space.actions

    def getStartState(self):
        return self.start_state


    def isGoalState(self, state):
        for _state in self.goal_state:
            if not eval(_state):
                return False
        return True


    def getNextStep(self, state):
        self.start_state = state
        plan = self.createPlan()
        action = plan[0]
        return action

    """
    Returns a list of succeeding (ie. following) actions based on the current state.
    It uses the 'post_effects' of the action to simulate the effect of the action on the current state.       
    """
    def getSuccessors(self, current_state):
        successors = []
        for action in self.actions:
            if self.checkPreconditions(action, current_state):
                state = deepcopy(current_state)
                for effect in action.post_effects:
                    exec(effect)
                cost = self.costFn(state, action)
                successors.append((state, action, cost))
        return successors

    def checkPreconditions(self, action, state):
        for precondition in action.pre_conditions:
            if not eval(precondition):
                return False
        return True

    def heuristic(self, state):
        return 0
    def createPlan(self):
        # Typical A* implementation
        
        heuristic = self.heuristic

        closed = set()

        # from util import PriorityQueue
        fringe = PriorityQueue()

        STATE = 0
        ACT = 1
        COST = 2
        DATA = 3

        node = self.getStartState()
        plan = []
        plan_cost = []

        fringe.push((node, plan, plan_cost), heuristic(self.getStartState()))

        while True:
            if fringe.isEmpty():
                return []
                break

            popped = fringe.pop()
            node = popped[0]
            plan = popped[1]
            plan_cost = popped[2]

            if self.isGoalState(node):
                return plan
                break

            if not node in closed:
                closed.add(node)
                children = self.getSuccessors(node)

                for child in children:
                    sum_plan_cost = sum(plan_cost)
                    # child[ACT][DATA] = child[STATE]
                    fringe.push((child[STATE], plan + deepcopy([child[ACT]]),
                                 plan_cost + [child[COST]]),
                                heuristic(child[STATE]) + sum(plan_cost + [child[COST]])
                                )  # according to comments priorityqueue prioritizes the lowest priority. depth will make the deepest node the hightest priority





class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.

      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        # FIXME: restored old behaviour to check against old results better
        # FIXED: restored to stable behaviour
        entry = (priority, self.count, item)
        # entry = (priority, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        #  (_, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

