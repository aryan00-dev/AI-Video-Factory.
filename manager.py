import random

topics = [
    "Aloo roasting Samosa",
    "Chai roasting Coffee",
    "Smartphone roasting Landline",
    "Free Fire roasting PUBG",
    "Laptop roasting PC"
]

topic = random.choice(topics)

with open("current_topic.txt", "w", encoding="utf-8") as f:
    f.write(topic)

print(f"Manager Engine: Aaj ka topic hai - {topic}")
