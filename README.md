# DiscordUserAPI

**About**

DiscordUserAPI allows you to automate a lot of discord actions needing only a user token. 

What you can do:

1. `validate()`
	- Validates discord token, if valid gathers all basic information about the account (id, email, phone, has nitro, gifts, game pass, payments)
2. `get_profile()`
	- Gets basic information about the discord profile
3. `get_gifts()`
	- Gets all gifts on account
4. `get_game_pass()`
	- Gets xbox game pass code if present
5. `get_nitro()`
	- Checks status of nitro on account
6. `get_user_channels()`
	- Gets all DM channels (they're formally known as user channels)
7. `get_guilds()`
	- Gets all guilds, returns json about each guild
8. `get_friends()`
	- Gets all friends
9. `get_messages(terms)`
	- Gets all messages sent through DM's (this should be changed, function is poorly written)
10. `send_messages(msg, channel_id)`
	- Sends message to channel specified by the channel_id
11. `send_mass_dms(message_list)`
	- Will dm every open user channel with list of messages (this should be changed, function is poorly written)
12. `set_typing(channel_id)`
	- Sets user typing in specefied channel
13. `delete_freinds()`
	- Removes all freinds
14. `leave_guilds()`
	- Leaves all guilds
15. `delete_channels()`
	- Deletes all open user channels
16. `get_friends_with_nitro()`
	- Gets list of all friends with nitro
17. `search(terms)`
	- Searchs all user channel messages filtered by list of terms 


Since this was written with OOP in mind, you can have multiple instances of accounts by just creating multiple Api() objects.
You can save accounts by dumping their json into an `accounts.json` file, as shown at [line 25](https://github.com/NMan1/DiscordAPI/blob/3ccbddd4dacfab0020fad9a253d488d392f13694/main.py#L25)
As well as if you have a lot of tokens, create a `token.txt` file and they'll all be loaded and then dumped to `accounts.json`
