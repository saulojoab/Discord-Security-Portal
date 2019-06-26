#coding:utf-8

import discord
import json

with open("credentials.json", encoding='utf-8-sig') as json_file:
    cred = json.load(json_file)


class MyClient(discord.Client):
    # When the bot logs in.
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    # When someone sends a message.
    async def on_message(self, message):
        """
        This method handles every message event.
        :param message:
        :return:
        """
        if str(message.author) == "DSPBot#3929":
            return;
        print('Message from {0.author}: {0.content}'.format(message))
        # If the message starts with the bot prefix.
        if message.content.startswith("=dsb"):
            # We remove the command part.
            messageStr = message.content.replace("=dsb ", "");

            # We turn the message into a list of words.
            words = messageStr.split(" ")

            # Infraction verification
            if (words.__len__() == 4 and words[0] == "infraction"):
                await self.Infraction(words, message);

    async def Infraction(self, commandList, message):
        """
        This method handles the infraction reports.
        :param commandList:
        :param message:
        :return:
        """
        # If someone tries to register an infraction against our bot.
        if (commandList[2] == "<@593308038476201999>"):
            await message.channel.send("Ha ha ha. You're so silly :stuck_out_tongue:");
            return;

        # Loggin info.
        print(str(message.author) + " is registering an Infraction! Details:");
        print("- Infraction: " + commandList[1]);
        print("- User: " + commandList[2]);
        print("- Gravity: " + commandList[3]);

        # Logging info to user.
        await message.channel.send(":robot: Hello, " + str(message.author) + "! Your report has been registered. Details: ");
        await message.channel.send("- Infraction: " + commandList[1] + "\n- "
                                   "User: " + commandList[2] + "\n- Gravity: " + commandList[3]);

client = MyClient()
client.run(str(cred["bottoken"]))

if __name__ == "__main__":
    print()