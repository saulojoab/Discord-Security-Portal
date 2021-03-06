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
            if (words.__len__() > 2 and words[0] == "infraction"):
                if (message.author.guild_permissions.kick_members or message.author.guild_permissions.ban_members):
                    await self.Infraction(words, message);
                else:
                    await message.channel.send("You don't have permissions for that! :cop:");
            # Ban verification.
            elif (words.__len__() > 2 and words[0] == "ban"):
                if (message.author.guild_permissions.ban_members):
                    await self.Ban(words, message);
                else:
                    await message.channel.send("You don't have permissions for that! :cop:");
            # Kick verification.
            elif (words.__len__() > 2 and words[0] == "kick"):
                if (message.author.guild_permissions.kick_members):
                    await self.Kick(words, message);
                else:
                    await message.channel.send("You don't have permissions for that! :cop:");
            # Say verification.
            elif (words.__len__() > 1 and words[0] == "say"):
                await self.Say(words, message);
            # Search verification.
            elif (words.__len__() == 2 and words[0] == "search"):
                if (message.author.guild_permissions.kick_members or message.author.guild_permissions.ban_members):
                    await self.Search(words[1], message);
                else:
                    await message.channel.send("You don't have permissions for that! :cop:");
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

        try:
            apiHandler.addInfraction(commandList[1], infraction, commandList[0]);
        except:
            await message.channel.send("Yikes! :sob: Something went wrong... Maybe try again?");
            await message.channel.send("If that keeps happening, open an issue here: https://github.com/saulojoab/Discord-Security-Portal");
            return;

        # Logging info to user.
        await message.channel.send(":cop: Hey, " + str(message.author) + "! Your report has been registered. Details: ");
        await message.channel.send("```- [Infraction]: " + infraction + "\n- "
                                   "[User]: " + commandList[1] + "\n- [Action Taken]: " + commandList[0] + "```");

    async def Ban(self, commandList, message):
        """
        This method handles the ban action.
        :param commandList:
        :param message:
        :return:
        """
        # If someone tries to register an infraction against our bot.
        if (commandList[1] == "<@593308038476201999>"):
            await message.channel.send("Ha ha ha. You're so silly :stuck_out_tongue:");
            return;

        # Loggin info.
        print(str(message.author) + " is banning someone! Details:");

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

        string = self.convertUser(commandList[1])
        await message.author.guild.ban(discord.Object(id=string));

        # Loading...
        await message.channel.send("THE BAN HAMMER HAS BEEN APPLIED! :cowboy: :cop: now lemme make a report for you...");

        try:
            apiHandler.addInfraction(commandList[1], infraction, commandList[0]);
        except:
            await message.channel.send("Well, that didn't work... Maybe try again? :thinking:");
            await message.channel.send("If that keeps happening, open an issue here: https://github.com/saulojoab/Discord-Security-Portal");

        # Logging info to user.
        await message.channel.send(
            ":cop: Hey, " + str(message.author) + "! Your report has been registered. Details: ");
        await message.channel.send("```- [Infraction]: " + infraction + "\n- "
                                   "[User]: " + commandList[1] + "\n- [Action Taken]: " +
                                   commandList[0] + "```");

    async def Kick(self, commandList, message):
        """
        This method handles the kick action.
        :param commandList:
        :param message:
        :return:
        """
        # If someone tries to register an infraction against our bot.
        if (commandList[1] == "<@593308038476201999>"):
            await message.channel.send("Ha ha ha. You're so silly :stuck_out_tongue:");
            return;

        # Loggin info.
        print(str(message.author) + " is banning someone! Details:");

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

        string = self.convertUser(commandList[1])
        await message.author.guild.kick(discord.Object(id=string));

        # Loading...
        await message.channel.send("KICK KICK KICK, I'VE KICKED! :cowboy: :cop: now lemme make a report for you...");

        try:
            apiHandler.addInfraction(commandList[1], infraction, commandList[0]);
        except:
            await message.channel.send("Well, that didn't work... Maybe try again? :thinking:");
            await message.channel.send("If that keeps happening, open an issue here: https://github.com/saulojoab/Discord-Security-Portal");

        # Logging info to user.
        await message.channel.send(
            ":cop: Hey, " + str(message.author) + "! Your report has been registered. Details: ");
        await message.channel.send("```- [Infraction]: " + infraction + "\n- "
                                   "[User]: " + commandList[1] + "\n- [Action Taken]: " +
                                   commandList[0] + "```");

    async def Search(self, id, message):
        """
        This method returns all infraction history from a user.
        :param id:
        :param message:
        :return:
        """
        await message.channel.send("Searching...");
        infractions = apiHandler.searchInfractions(self.convertUser(id));

        if infractions == []:
            await message.channel.send(":cop: There are no records about that user. That's probably good.");
            return;

        await message.channel.send(":cop: Here's what I found about that user:");
        stringInfractions = ""
        for idx, i in enumerate(infractions):
            stringInfractions += str(idx + 1) + ".\n[INFRACTION]: " + i["description"] + "\n[ACTION TAKEN]: " + i["actionTaken"] + "\n\n";
        await message.channel.send("```" + stringInfractions + "```");
        await message.channel.send(":warning: This user has commited a total of " + str(infractions.__len__()) + " infractions.");

    def convertUser(self, user):
        for i in ['<', '@', '>']:
            user = user.replace(i, "");
        return user;


client = MyClient()
client.run(str(cred["bottoken"]))

if __name__ == "__main__":
    print()