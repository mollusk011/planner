import sys
import unittest
import yaml


from planner import *

class TestPlanner(unittest.TestCase):

    def setUp(self):
        file_path = 'plan-space_protocols-basic.yaml'

        with open(file_path, 'r') as file:
            self.basic_data = yaml.safe_load(file)


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
        plan = planner.createPlan()

        self.print_plan(plan, "Basic")

        #self.assertEqual(sum([step.cost for step in plan]), 5, "Plan cost is 5")

        self.assertGreater(len(plan), 0, "Plan has at least one step")


    def test_01_basic_planner_is_tenant(self):
        data = self.basic_data.copy()
        # Test 1: Basic Plan Space
        start_state = State(**data['PlanSpace']['StartState']['state'])
        plan_space = PlanSpace(start_state, data['PlanSpace']['GoalState'], data['PlanSpace']['Actions'])

        planner = Planner(plan_space, self.mycostFn)

        start_state["is_tenant"] = True

        plan = planner.createPlan()

        self.print_plan(plan, "Basic")

        #self.assertEqual(sum([step.cost for step in plan]), 5, "Plan cost is 5")

        self.assertGreater(len(plan), 0, "Plan has at least one step")

if __name__ == '__main__':
    unittest.main()