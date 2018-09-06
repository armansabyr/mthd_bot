BOT: "t.me/method_mercurybot", https://github.com/armansabyr/mthd_bot
change token in config.py file
change url to method.kz (tested in localhost)

REQUESTS to:
url + /api/v1/adduser   - Initialzing the user's chat_id, Params are (chat_id, phone)
url + /api/v1/tasks     - List of available tasks
url + /api/v1/get_results   - request for inputs/outputs of the exact task to test
url + /api/v1/submit   - Submit


MODELS:
new: Task
     Task has many tests
     Test (inputs and outputs)
     GroupTask (for saving the date and completed students)
     GroupTask has_one task
                has manu users(completed)

old: Group has many group_tasks
