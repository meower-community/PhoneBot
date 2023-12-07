from MeowerBot import Bot, cbids
from MeowerBot.ext.help import Help 
from os import environ as env
from dotenv import load_dotenv

load_dotenv()

bot = Bot(prefix="@phone")
bridges = {}

@bot.command(name="dial", args=1)
async def dial(ctx, chat):
      if chat in bridges:
         return await ctx.send_msg(f"Uh oh, {chat} is already in a call")

      if ctx.message.chat.id in bridges:
         return await ctx.send_msg("Uh oh, looks like you are already in a call, use @phone hangup to hangup")

      message = await (bot.get_chat(chat) \
                .send_msg("Ring Ring..."))
      
      if message is None:
         return await ctx.send_msg(f"Failed to call {chat}")
 
      bridges[ctx.message.chat.id] = chat
      bridges[chat] = ctx.message.chat.id

@bot.command(name="hangup", args=0)
async def hangup(ctx, *_):
      chat = bridges.get(ctx.message.chat.id)
      if not chat:
         return await ctx.send_msg("This chat is currenly not in a call")
 
      bridges.pop(chat)
      bridges.pop(ctx.message.chat.id)
      await (bot.get_chat(chat).send_msg("BZZZz (Call ended)"))
      await ctx.send_msg("BZZZz (Call ended)")

@bot.listen(cbids.message)
async def message(message):
      if message.user.username == env["username"]:
         return 
      origin_chat = message.chat.id
      to_chat = bridges.get(origin_chat)
      if to_chat is None:
         return

      await (bot.get_chat(to_chat)
            .send_msg(f"{message.user.username}: {message.data}"))

bot.register_cog(Help(bot))
bot.run(env["username"], env["password"])
