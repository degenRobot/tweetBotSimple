from generateResponse import generateResponse
from fireScrape import getInfo
from context import gtmInfo
#prompt = "Now draft some tweets about Rise Chain"

message = f"""
- Draft some tweets (use information in the <context> tag)
(make sure to stay in character & use instructions in the <style> tag - although be creative & potentially break the rules if you can MAKE IT BETTER)

"""

# url = "https://www.paradigm.xyz/2024/06/reth-prod"
# url = "https://feed.defillama.com/"
# topic = getInfo(url)
#load topic.txt
with open("topic.txt", "r") as file:
    topic = file.read()

# message = context + message

out = generateResponse(message, topic = topic)
print(out)
