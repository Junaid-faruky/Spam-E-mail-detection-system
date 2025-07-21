class DriverStateAnalyzer:
    def __init__(self):
        self.blink_rate = 0
        self.head_position = "center"
        self.steering_behavior = "stable"

    def analyze_state(self):
        if self.blink_rate > 20:
            return "Alert: High blink rate detected! Potential drowsiness."
        elif self.head_position != "center":
            return f"Alert: Head position is {self.head_position}. Potential distraction."
        elif self.steering_behavior == "erratic":
            return "Alert: Erratic steering behavior detected! Potential loss of control."
        else:
            return "Driver state is normal."

    def simulate_input(self, blink_rate, head_position, steering_behavior):
        self.blink_rate = blink_rate
        self.head_position = head_position
        self.steering_behavior = steering_behavior
        return self.analyze_state()


# Main program
if __name__ == "__main__":
    analyzer = DriverStateAnalyzer()

    test_cases = [
        {"blink_rate": 25, "head_position": "center", "steering_behavior": "stable"},
        {"blink_rate": 15, "head_position": "left", "steering_behavior": "stable"},
        {"blink_rate": 10, "head_position": "center", "steering_behavior": "erratic"},
        {"blink_rate": 10, "head_position": "center", "steering_behavior": "stable"},
    ]

    for i, case in enumerate(test_cases):
        print(f"Test Case {i + 1}: {case}")
        result = analyzer.simulate_input(
            case["blink_rate"], case["head_position"], case["steering_behavior"]
        )
        print("Analysis Result:", result)
        print("-" * 40)
