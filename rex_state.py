import json


class RexState():
    BOT_LOOP = True
    admins = []
    triggers = []

    @classmethod
    def set_bot_loop(cls, state: bool):
        cls.BOT_LOOP = state

    @classmethod
    def set_permissions(cls):
        with open("rex_permissions.json", "r") as bp:
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
