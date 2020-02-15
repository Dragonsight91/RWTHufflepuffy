# handle the $feature command
async def handle_feat(mongo_client, message):
    words = str(message.content).split(" ")
    action = words[0:2] + [" ".join(words[3:])]
    if action[2] == "add":
        await feat_add(mongo_client, action[3])
    print(action)

async def feat_add(mongo_client, message):
    pass
async def purge_feat():
    pass