import datetime
import os

import rich
from dotenv import load_dotenv

import bimay

load_dotenv()


if __name__ == "__main__":
    bm = bimay.bimay(token=os.getenv("TOKEN"), roleId=os.getenv("ROLEID"))
    today = bm.get_schedule_date(datetime.datetime.now())
    rich.print("Today's Schedule:\n")
    for i in range(len(today)):
        class_title = today[i]["content"]
        classSessionId = today[i]["customParam"]["classSessionId"]
        classId = today[i]["customParam"]["classId"]
        session_details = bm.get_class_session_detail(classSessionId)
        startDateTime = datetime.datetime.strptime(
            session_details["dateStart"], "%Y-%m-%dT%H:%M:%S"
        )
        endDateTime = datetime.datetime.strptime(
            session_details["dateEnd"], "%Y-%m-%dT%H:%M:%S"
        )

        duration = (endDateTime - startDateTime).seconds // 60
        duration_hours = duration // 60
        duration_minutes = duration % 60
        duration_string = ""
        if duration_hours > 0:
            duration_string += str(duration_hours) + " hours "
        if duration_minutes > 0:
            duration_string += str(duration_minutes) + " minutes"

        delivery_mode = session_details["deliveryMode"]
        if delivery_mode == "GSLC":
            mode = "[green][GSLC][/]"
        else:
            mode = "[red][VC][/]"
        _class = f"[cyan][{today[i]['title']}][/cyan]"
        rich.print(
            f"{mode}{_class}[yellow][Session {session_details['sessionNumber']}][/]\n[bold]{class_title}[/]"
        )
        rich.print(
            f"{startDateTime.strftime('%I:%M %p')} - {endDateTime.strftime('%I:%M %p')}\nduration:{duration_string}"
        )
        rich.print(f"Topic: {session_details['topic']}")
        for subtopic in session_details["courseSubTopic"]:
            rich.print(f"\t-{subtopic}")

        if session_details["joinUrl"] in ("", None):
            url = (
                "https://newbinusmaya.binus.ac.id/lms/course/"
                + classId
                + "/session/"
                + classSessionId
            )
            text = "Session URL"
        else:
            url = session_details["joinUrl"]
            text = "Zoom URL"
        rich.print(f"[bold blue][link={url}]{text}[/link][/]")
        print("-----------")
