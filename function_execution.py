def get_course_info(nrc, request):
    requested_info = {}

    if request == "teacher":
        requested_info["teacher"] = "Juan Perez"
    elif request == "department":
        requested_info["department"] = "Computer Science"
    elif request == "subject":
        requested_info["subject"] = "Programming"
    elif request == "group":
        requested_info["group"] = "1"
    elif request == "name":
        requested_info["name"] = "Programming 1"
    elif request == "available places":
        requested_info["available places"] = "10"
    elif request == "enrolled amount":
        requested_info["enrolled amount"] = "20"
    elif request == "schedule":
        requested_info["schedule"] = "Monday 10:00 - 12:00"
    elif request == "all":
        requested_info["teacher"] = "Juan Perez"
        requested_info["department"] = "Computer Science"
        requested_info["subject"] = "Programming"
        requested_info["group"] = "1"
        requested_info["name"] = "Programming 1"
        requested_info["available places"] = "10"
        requested_info["enrolled amount"] = "20"
        requested_info["schedule"] = "Monday 10:00 - 12:00"

    return str(requested_info)
