

def get_days_difference(prev_date, curr_date):
    prev_date, curr_date = str(prev_date), str(curr_date)
    days_difference = (
                (int(curr_date[:4]) - int(prev_date[:4]))
                * 365
                + (
                    int(curr_date[4:6])
                    - int(prev_date[4:6])
                )
                * 30
                + int(curr_date[6:8])
                - int(prev_date[6:8])
            )
    return days_difference
