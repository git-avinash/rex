import json


class RexState:
    BOT_LOOP = True
    admins = []
    triggers = []
    chat_bot_driver = None
    clever_bot_driver = None

    @classmethod
    def set_permissions(cls):
        with open("./data/rex_permissions.json", "r") as bp:
            permission = json.load(bp)
            cls.admins = permission["admins"]
            cls.triggers = permission["triggers"]

    @classmethod
    def is_admin(cls, userid):
        for admin in cls.admins:
            if admin == userid:
                return True

        return False

    @classmethod
    def is_trigger(cls, trigger_message):
        for trigger in cls.triggers:
            if trigger == trigger_message:
                return True

        return False
