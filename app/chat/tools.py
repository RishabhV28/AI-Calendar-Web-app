TOOLS=[
    {
        "type": "function",
        "function":{
            "name": "create_event",
            "description": "Create a calendar event for the user.",
            "paramenters":{
                "type": "object",
                "properties":{
                "title": {"type": "string"},
                "date": {'type':'string', "description": "The date exactly as the user said it,e.g. 'tomorrow', 'next friday'"},
                "time": {"type":"string","description":"24-hour HH:MM, e.g. '12:00'"},
                "duration_minutes":{"type":"integer", "description":"Defaults to 60 if user didn't say"},
            },
            "required":["title","date","time"],

            },
        },
    },
    {
        "type":"function",
        "function":{
            "name": "list_events",
            "description":"List the user's events on a given day.",
            "parameters":{
                "type":"object",
                "properties":{
                    "date":{"type":"string","description":"The date as the user said it, e.g. 'today','tomorrow'"},

                },
                "required":["date"],
            },
        },
    },
]