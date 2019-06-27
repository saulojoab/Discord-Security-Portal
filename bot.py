#coding:utf-8

import discord
import json
import apiHandler

with open("credentials.json", encoding='utf-8-sig') as json_file:
    cred = json.load(json_file)

with open("badwords.json", encoding='utf-8-sig') as json_file:
    bad_words = json.load(json_file);


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
            if (words.__len__() > 3 and words[0] == "infraction"):
                await self.Infraction(words, message);
            if (words[0] == "say" and words.__len__() > 1):
                await self.Say(words, message);
            else:
                await message.channel.send("Im sorry? I have no idea what you said... :sob:");

    async def Say(self, commandList, message):
        """
        This method makes the bot say something.
        :param commandList:
        :param message:
        :return:
        """
        # Forming the phrase the user wants the bot to say.
        phrase = "";
        for idx, i in enumerate(commandList):
            if (idx > 0):
                phrase += i + " "
            elif (commandList.__len__() == idx):
                phrase += i;

        # Checking for bad words.
        for i in phrase.split(" "):
            for w in bad_words:
                if (i == w):
                    print("Bad word! Nonono!");
                    await message.channel.send("Hey!! :angry:\nDon't make me say bad words!");
                    return;

        print(str(message.author) + " asked the bot to say '" + message.content + "'.");
        # Sending the message.
        await message.channel.send(phrase);


    async def Infraction(self, commandList, message):
        """
        This method handles the infraction reports.
        :param commandList:
        :param message:
        :return:
        """
        # If someone tries to register an infraction against our bot.
        if (commandList[1] == "<@593308038476201999>"):
            await message.channel.send("Ha ha ha. You're so silly :stuck_out_tongue:");
            return;

        # Loggin info.
        print(str(message.author) + " is registering an Infraction! Details:");

        # Forming the infraction description.
        infraction = "";
        for idx, i in enumerate(commandList):
            if (idx >= 2):
                infraction += i + " ";
            if (idx == commandList.__len__()):
                infraction += i;

        # Logging.
        print("- Infraction: " + infraction);
        print("- User: " + commandList[1]);
        print("- ActionTaken: " + commandList[0]);

        # Loading...
        await message.channel.send("Ok! :cowboy: lemme handle that for you...");
        res = apiHandler.addInfraction(commandList[1], infraction, commandList[0]);
        print(res);

        # Logging info to user.
        await message.channel.send(":cop: Hey, " + str(message.author) + "! Your report has been registered. Details: ");
        await message.channel.send("```- Infraction: " + infraction + "\n- "
                                   "User: " + commandList[1] + "\n- Action Taken: " + commandList[0] + "```");

client = MyClient()
client.run(str(cred["bottoken"]))

if __name__ == "__main__":
    print()