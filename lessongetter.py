from datetime import datetime , timedelta

from MagisterPy import *
class LessonGetter():
    def __init__(self):
        pass
from datetime import datetime

class LessonGetter():
    def __init__(self):
        pass

    def extract_lessons_from_response(self, json):
        formatted_lessons = []
        
        for lesson in json:
            try:
                # Get start and end time from the JSON
                start_time_str = lesson["Start"]
                end_time_str = lesson["Einde"]

                # Optional: Truncate to handle longer datetime precision (e.g., 7 digits in milliseconds)
                start_time_str = start_time_str[:26] + 'Z' if len(start_time_str) > 26 else start_time_str
                end_time_str = end_time_str[:26] + 'Z' if len(end_time_str) > 26 else end_time_str

                # Convert strings to datetime objects
                start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S.%fZ") +timedelta(hours=1)  # Convert to datetime object
                end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S.%fZ") +timedelta(hours=1)  # Convert to datetime object

                # Get lesson name and location
                if lesson["Vakken"]:
                    lesson_name = lesson["Vakken"][0]["Naam"]
                else:
                    lesson_name = "Uitgevallen"
                location = lesson["Lokatie"]

                # Format the lesson data to include lesson name, location, and formatted time
                lesson_data = {
                    "lesson": lesson_name,  # Lesson name
                    "location": location,   # Location of the lesson
                    "time": f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"  # Time range in HH:MM format
                }

                formatted_lessons.append(lesson_data)

            except KeyError as e:
                print(f"Missing key: {e}")
            except ValueError as e:
                print(f"Error parsing date: {e}")

        return formatted_lessons
    def extract_lessons_from_date(self,session:MagisterSession,date):
        
        date_string = date

        # Convert the string to a datetime object
        date_object = datetime.strptime(date_string, "%a %b %d %H:%M:%S %Y")
        
        # Format the datetime object into the desired format
        formatted_date = date_object.strftime(r"%Y-%m-%d")
        
        #session.get_schedule(_from,)
        
        response_schedule = session.get_schedule(formatted_date,formatted_date,with_changes=False)

        formatted_schedule = self.extract_lessons_from_response( response_schedule)


        return formatted_schedule


