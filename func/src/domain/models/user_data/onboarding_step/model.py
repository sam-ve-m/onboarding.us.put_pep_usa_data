class UserOnboardingStep:
    __expected_step_br = "finished"
    __expected_step_us = "politically_exposed"

    def __init__(self, step_br: str, step_us: str):
        self.step_br = step_br
        self.step_us = step_us

    def is_in_correct_step(self):
        is_correct_step_br = self.step_br == self.__expected_step_br
        is_correct_step_us = self.step_us == self.__expected_step_us
        are_steps_ok = is_correct_step_br and is_correct_step_us
        return are_steps_ok
