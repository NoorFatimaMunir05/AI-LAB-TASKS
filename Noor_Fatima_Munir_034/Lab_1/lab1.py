def rule(score, complete, attendance, income):
    if not complete:
        return "Hold", "Missing documents"
    if score < 70:
        return "Hold", "Score below 70"
    if attendance < 75:
        return "Hold", "Attendance below 75"
    if income > 50000:
        return "Hold", "Income above 50000"
    return "Review", "All conditions met"

def threshold(probability):
    return "Review" if probability >= 0.70 else "Hold"

cases = [
    ("pass", 82, True, 80, 40000, 0.81, "Review"),
    ("attendance_fail", 82, True, 70, 40000, 0.81, "Hold"),
    ("income_fail", 82, True, 80, 60000, 0.81, "Hold"),
    ("boundary", 70, True, 75, 50000, 0.70, "Review")
]
print("CASE | INPUT | EXPECTED | ACTUAL | REASON | PROBABILITY | DISAGREE")
for name, score, complete, attendance, income, probability, expected in cases:
    actual, reason = rule(score, complete, attendance, income)
    other = threshold(probability)
    print(name, (score, complete, attendance, income, probability), expected, actual, reason, other, actual != other, sep=" | ")
    assert actual == expected
print("EDGE CASES")
for case in [(91, False, 90, 30000, 0.88), (69, True, 80, 40000, 0.69)]:
    print(case, rule(*case[:4]), threshold(case[4]))
