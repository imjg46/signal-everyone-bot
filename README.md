# signal-everyone-bot
A Bot that mention @everyone in Signal Groups

# Before you start
You'll need these files:
> signal-cli-0.14.6
> 
> OpenJDK25U 
> 
> python-3.14.6

# How to start
run the command in **signal-cli-0.14.6\bin**

> signal-cli link -n "[any name]"

 After linking, run

> signal-cli -a +[your number] listGroups

 Find Your Group
 This should look like:

> Id: qwertyqwerty Name: [Group Name] Description:  Active: true Blocked: false Members:

 Focus on the Members part, only extract the uuid using any llm you want

 Then copy it in the **bot.py** field
After that, **config.json** Put your information

# How to run 
> run the script **bot.py**

The script must be always running in order to @everyone to work.
