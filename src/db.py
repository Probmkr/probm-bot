import psycopg2
import psycopg2.extras
from typing import List, TypeAlias, TypedDict, Any
from datetime import datetime
from lib import Logger
from var import LT

logger = Logger()


class DiscordUser(TypedDict):
    id: str
    username: str
    discriminator: str
    avatar: str
    bot: str
    system: str
    mfa_enabled: str
    banner: str
    accent_color: str
    locale: str
    verified: str
    email: str
    flags: str
    premium_type: str
    public_flags: str


class TokenData(TypedDict):
    user_id: int
    access_token: str
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str
    last_update: datetime


class GuildRole(TypedDict):
    guild_id: int
    role: int


class DatabaseControl:
    def __init__(self, dsn: str):
        self.dsn = dsn
        if not self.check_table_exists("user_token"):
            logger.log(LT.INFO, "[!] user_token データベースがないので作ります")
            self.execute("""
create table user_token (
  user_id bigserial not null primary key,
  access_token text not null,
  expires_in serial not null,
  refresh_token text not null,
  scope text not null,
  token_type text not null,
  last_update real not null
);
""")
        if not self.check_table_exists("guild_role"):
            logger.log(LT.INFO, "[!] guild_role データベースがないので作ります")
            self.execute("""
create table guild_role (
  guild_id bigserial not null primary key,
  role bigserial not null
);
""")

    def get_dict_conn(self):
        return psycopg2.connect(self.dsn, cursor_factory=psycopg2.extras.DictCursor)

    def get_user_tokens(self) -> List[TokenData] | bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("select * from user_token")
                    res: List[TokenData] = cur.fetchall()
                    return res
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                return False

    def get_user_token(self, user_id: int) -> TokenData | None | bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "select * from user_token where user_id = %s",
                        (user_id, )
                    )
                    res: TokenData = cur.fetchall()[0]
                    return res
            except IndexError:
                return None
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                return False

    def update_user_token(self, token_data: TokenData) -> bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        update user_token set
                        access_token = %(access_token)s,
                        expires_in = %(expires_in)s,
                        refresh_token = %(refresh_token)s,
                        scope = %(scope)s,
                        token_type = %(token_type)s,
                        last_update = %(last_update)s
                        where user_id = %(user_id)s
                        """,
                        {
                            "access_token": token_data["access_token"],
                            "expires_in": token_data["expires_in"],
                            "refresh_token": token_data["refresh_token"],
                            "scope": token_data["scope"],
                            "token_type": token_data["token_type"],
                            "last_update": token_data["last_update"],
                            "user_id": token_data["user_id"]
                        }
                    )
                    return True
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                conn.rollback()
                return False

    def delete_user_token(self, user_id: int) -> TokenData | bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    token_data = self.get_user_token(user_id)
                    cur.execute(
                        "delete from user_token where user_id = %s",
                        (user_id, )
                    )
                    return token_data
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                conn.rollback()
                return False

    def add_user_token(self, token_data: TokenData) -> bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        insert into user_token values (
                            %(user_id)s,
                            %(access_token)s,
                            %(expires_in)s,
                            %(refresh_token)s,
                            %(scope)s,
                            %(token_type)s,
                            %(last_update)s
                        )
                        """,
                        {
                            "user_id": token_data["user_id"],
                            "access_token": token_data["access_token"],
                            "expires_in": token_data["expires_in"],
                            "refresh_token": token_data["refresh_token"],
                            "scope": token_data["scope"],
                            "token_type": token_data["token_type"],
                            "last_update": token_data["last_update"]
                        }
                    )
                    return True
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                conn.rollback()
                return False

    def set_user_token(self, token_data: TokenData) -> bool:
        exists = self.get_user_token(token_data["user_id"])
        if exists:
            return self.update_user_token(token_data)
        elif exists == None:
            return self.add_user_token(token_data)
        else:
            return False

    def get_guild_roles(self) -> List[GuildRole] | bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("select * from guild_role")
                    res: List[GuildRole] = cur.fetchall()
                    return res
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                return False

    def get_guild_role(self, guild_id: int) -> GuildRole | None | bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "select * from guild_role where guild_id = %s",
                        (guild_id, )
                    )
                    res: TokenData = cur.fetchall()[0]
                    return res
            except IndexError:
                return None
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                return False

    def update_guild_role(self, guild_role: GuildRole) -> bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        update guild_role set
                        role = %(role)s
                        where guild_id = %(guild_id)s
                        """,
                        {
                            "role": guild_role["role"],
                            "guild_id": guild_role["guild_id"]
                        }
                    )
                    return True
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                conn.rollback()
                return False

    def delete_guild_role(self, guild_id: int) -> GuildRole | bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    guild_role = self.get_guild_role(guild_id)
                    cur.execute(
                        "delete from guild_role where guild_id = %s",
                        (guild_id, )
                    )
                    return guild_role
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                conn.rollback()
                return False

    def add_guild_role(self, guild_role: GuildRole) -> bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        insert into guild_role values (
                            %(guild_id)s,
                            %(role)s
                        )
                        """,
                        {
                            "guild_id": guild_role["guild_id"],
                            "role": guild_role["role"]
                        }
                    )
                    return True
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                conn.rollback()
                return False

    def set_guild_role(self, guild_role: GuildRole) -> bool:
        exists = self.get_guild_role(guild_role["guild_id"])
        logger.log(LT.DEBUG, exists)
        logger.log(LT.DEBUG, bool(exists))
        if exists:
            return self.update_guild_role(guild_role)
        elif exists == None:
            return self.add_guild_role(guild_role)
        else:
            return False

    def check_table_exists(self, table_name: str) -> bool:
        with self.get_dict_conn() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "select exists (select from pg_tables where schemaname = 'public' and tablename = %s)",
                        (table_name, )
                    )
                    res = cur.fetchone()[0]
                    return res
            except Exception as e:
                logger.log(LT.ERROR, "database error:", e)
                return False

    def execute(self, sql: str) -> Any:
        with self.get_dict_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.description

    def execute_param(self, sql: str, param: dict) -> Any | Exception:
        with self.get_dict_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, param)
                return cur.description


DBC: TypeAlias = DatabaseControl
