import obj_comparison
from utils import Roadmap, Category, Issue
import time
import requests

WEBHOOK_URL = "https://discordapp.com/api/webhooks/825435452256550922/VW8rXr0vWCXiI9GzF2iP12v_87OMrndekWOcH-0gODu5J4FIsypXYTLcfGjVrXQ_gnql"

last_roadmap = None

while True:
    print("Checking roadmap...")
    if last_roadmap is None:
        print("First time, sleeping...")
        last_roadmap = Roadmap('https://zarpgaming.com/index.php/roadmap')
    else:
        new_roadmap = Roadmap('https://zarpgaming.com/index.php/roadmap')
        if obj_comparison.deep_equals(last_roadmap, new_roadmap):
            print("No changes")
        else:
            print("Changes")

            new_issues = []

            for c, category in enumerate(new_roadmap.categories):
                new_str = category.name

                print(category.name)
                for issue in category.issues:
                    if issue.id not in [i.id for i in last_roadmap.categories[c].issues]:
                        new_str += "\n\t" + str(issue)
                        print("\t" + str(issue))
                
                if new_str != category.name:
                    new_issues.append(new_str)

            #notify discord
            if len(new_issues) > 0:
                print("Sending notification")
                payload = {
                    "content": "New issues: " + ", ".join([str(i) for i in new_issues])
                }
                requests.post(WEBHOOK_URL, json=payload)


            last_roadmap = new_roadmap
        print("Done, sleeping...")
    time.sleep(60 * 60) #sleep for an hour