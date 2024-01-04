import sys
import unittest

from plan_runner import *
from plugin_manager import *

class TestPlanRunner(unittest.TestCase):

    def setUp(self):
        file_path = 'plan-space_doc-auto_basic.yaml'

        with open(file_path, 'r') as file:
            self.basic_data = yaml.safe_load(file)

        self.plugin_manager = PluginManager()
        self.plugin_manager.register_plugin("test", TestPlugin)
        self.plugin_manager.register_plugin("fetch_document", FetchDocumentPlugin)
        self.plugin_manager.register_plugin("ocr_document", OCRDocumentPlugin)
        self.plugin_manager.register_plugin("extract_labels", ExtractLabelsPlugin)
        self.plugin_manager.register_plugin("apply_rules", ApplyRulesPlugin)
        self.plugin_manager.register_plugin("capture", CaptureDataPlugin)
        self.plugin_manager.register_plugin("storage", DataStoragePlugin)

    def test_basic_plan_runner_happy_path(self):

        self.plugin_manager.test_mode = False

        data = self.basic_data.copy()

        start_state = State(**data['PlanSpace']['StartState']['state'])
        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        planner = Planner(plan_space, mycostFn)

        current_state = copy.deepcopy(start_state)

        plan_runner = PlanRunner(planner, current_state, self.plugin_manager)

        plan_runner.current_state = current_state

        action_count = 0

        while not plan_runner.isGoalState():
            action = plan_runner.getNextStep()
            print("action: ", {action.name})
            plan_runner.executeAction(action)
            action_count += 1

        self.assertEqual(action_count, 6, "Plan cost is 6")

    def test_basic_plan_runner_respect_unexpected_state_change(self):


        self.plugin_manager.test_mode = False

        data = self.basic_data.copy()

        start_state = State(**data['PlanSpace']['StartState']['state'])
        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        planner = Planner(plan_space, mycostFn)

        current_state = copy.deepcopy(start_state)

        plan_runner = PlanRunner(planner, current_state, self.plugin_manager)

        plan_runner.current_state = current_state

        action_count = 0

        action = plan_runner.getNextStep()
        print("action: ", {action.name})
        plan_runner.executeAction(action)

        self.assertEqual(action.name, "fetch_document", "Action name is fetch_document")

        action = plan_runner.getNextStep()
        print("action: ", {action.name})

        self.assertEqual(action.name, "ocr_document", "Action name is ocr_document")

        plan_runner.executeAction(Action("capture", 1, [], []))  #unexpected state change

        action = plan_runner.getNextStep()

        self.assertEqual(action.name, "storage", "Action name is storage")

