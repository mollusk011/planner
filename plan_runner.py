
from planner import *
from plugin_manager import *
from plugin_interface import *
from plugins.doc_auto_plugins import *

import copy
import yaml

"""
    Planner Runner:

    Wraps a planner and provides a method to execute the plan.
    
    TODO:
    - add a run id
    - persist the plan to a file
    - add meta data to a run like time and date for every action
    - persist the run meta data to some kind of storage

"""


class PlanRunner:
    def __init__(self, planner = None, current_state=None, plugin_manager=None):
        self.current_state = current_state
        self.plugin_manager = plugin_manager
        self.planner = planner
        self.plan = self.planner.createPlan()
        self.run_id = 0

    def  getNextStep(self):
        return self.planner.getNextStep(self.current_state)

    def mycostFn(self, state, action):
        return action.cost

    def isGoalState(self):
        return self.planner.isGoalState(self.current_state)

    def executeAction(self, action):

        plugin_class = self.plugin_manager.get_plugin(action.name)

        if self.plugin_manager.plugin_exists(action.name):
            plugin_class = self.plugin_manager.get_plugin(action.name)
            plugin_instance = plugin_class()
            plugin_instance.run(self.current_state)
        else:
            print(f"No plugin found for action: {action.name}")

#PLACEHOLDER cost function. Ignore for now.
def mycostFn(state, action):
    return action.cost






