def get_days_difference(prev_date, curr_date):
    prev_date, curr_date = str(prev_date), str(curr_date)
    days_difference = (
        (int(curr_date[:4]) - int(prev_date[:4])) * 365
        + (int(curr_date[4:6]) - int(prev_date[4:6])) * 30
        + int(curr_date[6:8])
        - int(prev_date[6:8])
    ) + 2
    return days_difference


def reverse_score(score):
    score = str(score)
    reversed_score = []
    sets = score.split(" ")
    for set in sets:
        games = set.split("-")
        reversed_score.append("-".join(games[::-1]))
    return " ".join(reversed_score)
