import sys
import unittest
import yaml


from planner import *

class TestPlanner(unittest.TestCase):

    def setUp(self):
        file_path = 'plan-space_doc-auto_basic.yaml'

        with open(file_path, 'r') as file:
            self.basic_data = yaml.safe_load(file)

        file_path = 'plan-space_doc-auto_advanced.yaml'

        with open(file_path, 'r') as file:
            self.advanced_data = yaml.safe_load(file)

        file_path = "plan-space_taco-order_ai-generated.yaml"

        with open(file_path, 'r') as file:
            self.taco_data = yaml.safe_load(file)

        file_path = "plan-space_taco-order_advanced_ai-generated.yaml"

        with open(file_path, 'r') as file:
            self.taco_advanced_data = yaml.safe_load(file)

    def mycostFn(self, state, action):
        return action.cost

    def print_plan(self, plan, msg=""):
        print("\nPLAN ", msg, ":\n")
        for step, p in enumerate(plan, start=1):
            print(f"PLAN STEP {step}:", {'action': p.name, 'cost': p.cost})
        print("Total Plan Cost: ", sum([step.cost for step in plan]))

    def test_01_basic_planner_happy_path(self):
        data = self.basic_data.copy()
        # Test 1: Basic Plan Space
        start_state = State(**data['PlanSpace']['StartState']['state'])
        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        planner = Planner(plan_space, self.mycostFn)
        plan = aStarSearch(planner)

        self.print_plan(plan, "Basic")

        self.assertEqual(sum([step.cost for step in plan]), 6, "Plan cost is 6")

    def test_02_basic_planner_goal_state_already_true(self):
        data = self.basic_data.copy()
        # Test 1: Basic Plan Space
        start_state = State(**data['PlanSpace']['StartState']['state'])
        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        start_state["document_processed"] = True

        planner = Planner(plan_space, self.mycostFn)
        plan = aStarSearch(planner)

        self.print_plan(plan, "Goal State already True")
        self.assertEqual(sum([step.cost for step in plan]), 0, "Plan cost is zero")

    def test_03_basic_planner_first_action_already_true(self):
        data = self.basic_data.copy()
        # Test 1: Basic Plan Space
        start_state = State(**data['PlanSpace']['StartState']['state'])
        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        start_state["document_fetched"] = True

        planner = Planner(plan_space, self.mycostFn)
        plan = aStarSearch(planner)

        self.print_plan(plan, "First action already true")
        self.assertEqual(sum([step.cost for step in plan]), 5, "Plan cost is 5")

    def test_04_advanced_planner_happy_path(self):
        data = self.advanced_data.copy()
        # Test 1: Advanced Plan Space
        start_state = State(**data['PlanSpace']['StartState']['state'])
        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        planner = Planner(plan_space, self.mycostFn)
        plan = aStarSearch(planner)

        self.print_plan(plan, "Advanced")

        self.assertEqual(sum([step.cost for step in plan]), 10, "Plan cost is 10")

    def test_05_advanced_planner_pre_condition_with_greater_than(self):
        """
            This test exercises the pre-condition with a greater than operator
            and tests that an alternative plan is generated when the state changes, in this case
            the document size is greater than 100.
        """

        data = self.advanced_data.copy()
        # Test 1: Advanced Plan Space
        start_state = State(**data['PlanSpace']['StartState']['state'])

        start_state["document_size"] = 100

        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        planner = Planner(plan_space, self.mycostFn)
        plan = aStarSearch(planner)

        self.print_plan(plan, "Advanced")

        self.assertEqual(sum([step.cost for step in plan]), 109, "Plan cost is 109")
        self.assertEqual(sum([1 for step in plan]), 6, "Plan steps is 6")



    def test_06_taco_planner_happy_path(self):
        """
        This plan space was generated with the following prompt:

        using the following planning style, create a plan space with state variables and actions for an online ordering system for a taco restaurant

        (copied the plan-space_doc-auto_basic.yaml file)
        """

        data = self.taco_data.copy()
        # Test 1: Taco Plan Space
        start_state = State(**data['PlanSpace']['StartState']['state'])
        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        planner = Planner(plan_space, self.mycostFn)
        plan = aStarSearch(planner)

        self.print_plan(plan, "Taco Plan")

        self.assertEqual(sum([step.cost for step in plan]), 7, "Plan cost is 7")

    def test_07_taco_advanced_planner_ai_generated(self):
        """
               This plan space was generated with the following prompt:

               modify the plan space to offer both pickup or delivery

        """

        data = self.taco_advanced_data.copy()
        # Test 1: Taco Plan Space
        start_state = State(**data['PlanSpace']['StartState']['state'])
        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        planner = Planner(plan_space, self.mycostFn)
        plan = aStarSearch(planner)

        self.print_plan(plan, "Taco Advanced Plan with both pickup and delivery options")

        self.assertEqual(sum([step.cost for step in plan]), 7, "Plan cost is 7")

    def test_07_taco_advanced_planner_delivery_chosen_ai_generated(self):


        data = self.taco_advanced_data.copy()
        # Test 1: Taco Plan Space
        start_state = State(**data['PlanSpace']['StartState']['state'])
        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        start_state["delivery_option_chosen"] = True

        planner = Planner(plan_space, self.mycostFn)
        plan = aStarSearch(planner)

        self.print_plan(plan, "Taco Advanced Plan - Delivery Chosen")

        self.assertEqual(sum([step.cost for step in plan]), 7, "Plan cost is 7")

if __name__ == '__main__':
    unittest.main()