from fastapi import WebSocket
from datetime import datetime, timedelta
from typing import Dict, Set, List
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._meta: dict[WebSocket, dict] = {}

    async def connect(
        self, websocket: WebSocket, user_id: str = "", username: str = "Anonym"
    ):
        await websocket.accept()
        self.active_connections.append(websocket)
        self._meta[websocket] = {"user_id": user_id, "username": username}
        logging.info(
            f"Підключено: {username} ({user_id}) [{websocket.client.host}:{websocket.client.port}]"
        )

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            meta = self._meta.pop(websocket, {})
            self.active_connections.remove(websocket)
            logging.info(
                f"Відключено: {meta.get('username', '?')} ({meta.get('user_id', '?')}) "
                f"[{websocket.client.host}:{websocket.client.port}]"
            )

    def get_username(self, websocket: WebSocket) -> str:
        return self._meta.get(websocket, {}).get("username", "Anonym")

    def get_user_id(self, websocket: WebSocket) -> str:
        return self._meta.get(websocket, {}).get("user_id", "")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, exclude: WebSocket | None = None):
        for connection in self.active_connections:
            if connection is not exclude:
                await connection.send_text(message)


class UserRole(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class ModerationManager:
    def __init__(self):
        self.users: dict = {}
        self.muted_users: dict[str, datetime] = {}
        self.banned_users: set[str] = set()
        self.audit_logger = logging.getLogger("moderation_audit")
        self.audit_logger.setLevel(logging.INFO)

    def set_users(self, users: dict):
        self.users = users

    def get_user_by_username(self, username: str):
        for user_id, user_data in self.users.items():
            if user_data["username"] == username:
                return user_id, user_data
        return None

    def audit_log(
        self, action: str, actor: str, target: str | None = None, extra: str = ""
    ):
        msg = f"[MODERATION] {action} | by={actor}"
        if target:
            msg += f" | target={target}"
        if extra:
            msg += f" | {extra}"
        self.audit_logger.info(msg)

    def get_role(self, username: str) -> UserRole:
        user = self.get_user_by_username(username)
        if not user:
            return UserRole.USER
        _, user_data = user
        role = user_data["role"]
        if isinstance(role, UserRole):
            return role
        try:
            return UserRole(role)
        except ValueError:
            return UserRole.USER

    def has_moder_permissions(self, username: str) -> bool:
        role = self.get_role(username)
        return role in [UserRole.ADMIN, UserRole.MODERATOR]

    def is_admin(self, username: str) -> bool:
        return self.get_role(username) == UserRole.ADMIN

    def mute_user(self, username: str, minutes: int):
        mute_end = datetime.now() + timedelta(minutes=minutes)
        self.muted_users[username] = mute_end
        logging.info(f"{username} muted until {mute_end}")

    def unmute_user(self, username: str):
        self.muted_users.pop(username, None)

    def is_muted(self, username: str) -> bool:
        if username not in self.muted_users:
            return False
        if datetime.now() >= self.muted_users[username]:
            del self.muted_users[username]
            return False
        return True

    def ban_user(self, username: str):
        self.banned_users.add(username)

    def unban_user(self, username: str):
        self.banned_users.discard(username)

    def is_banned(self, username: str) -> bool:
        return username in self.banned_users

    def set_moderator(self, username: str, value: bool):
        user = self.get_user_by_username(username)
        if not user:
            return False
        user_id, user_data = user
        user_data["role"] = UserRole.MODERATOR if value else UserRole.USER
        self.users[user_id] = user_data
        return True

    async def handle_command(self, sender_username: str, message: str, manager):
        parts = message.split()
        if not parts:
            return "Порожня команда"
        command = parts[0]

        if self.is_muted(sender_username):
            remaining = self.muted_users.get(sender_username)
            if remaining:
                secs = int((remaining - datetime.now()).total_seconds())
                return f"🔇 Ви замучені. Залишилось: {secs} сек."

        if command == "/mute":
            if not self.has_moder_permissions(sender_username):
                return "Недостатньо прав"
            try:
                target_username = parts[1]
                minutes = int(parts[2])
                self.mute_user(target_username, minutes)
                self.audit_log(
                    "MUTE", sender_username, target_username, f"{minutes} min"
                )
                await manager.broadcast(
                    f"🔇 {target_username} замучений на {minutes} хв"
                )
            except (IndexError, ValueError):
                return "Формат: /mute username minutes"

        elif command == "/unmute":
            if not self.has_moder_permissions(sender_username):
                return "Недостатньо прав"
            try:
                target_username = parts[1]
                self.unmute_user(target_username)
                self.audit_log("UNMUTE", sender_username, target_username)
                await manager.broadcast(f"🔊 {target_username} розмучений")
            except IndexError:
                return "Формат: /unmute username"

        elif command == "/ban":
            if not self.has_moder_permissions(sender_username):
                return "Недостатньо прав"
            try:
                target_username = parts[1]
                self.ban_user(target_username)
                self.audit_log("BAN", sender_username, target_username)

                for conn in list(manager.active_connections):
                    if manager.get_username(conn) == target_username:
                        await conn.close(code=1008)

                await manager.broadcast(f"⛔ {target_username} забанений")
            except IndexError:
                return "Формат: /ban username"

        elif command == "/unban":
            if not self.has_moder_permissions(sender_username):
                return "Недостатньо прав"
            try:
                target_username = parts[1]
                self.unban_user(target_username)
                self.audit_log("UNBAN", sender_username, target_username)
                await manager.broadcast(f"✅ {target_username} розбанений")
            except IndexError:
                return "Формат: /unban username"

        elif command == "/set_moder":
            if not self.is_admin(sender_username):
                return "Тільки admin може змінювати moderator"
            try:
                target_username = parts[1]
                value = parts[2].lower() == "true"
                success = self.set_moderator(target_username, value)
                if not success:
                    return "Користувача не знайдено"
                self.audit_log(
                    "SET_MODER", sender_username, target_username, f"value={value}"
                )
                await manager.broadcast(f"🛡️ {target_username} moderator = {value}")
            except IndexError:
                return "Формат: /set_moder username True/False"

        elif command == "/help":
            return (
                "📋 Команди:\n"
                "/mute <username> <minutes> — замутити\n"
                "/unmute <username> — розмутити\n"
                "/ban <username> — забанити\n"
                "/unban <username> — розбанити\n"
                "/set_moder <username> True/False — (admin) видати/забрати moder"
            )

        else:
            return f"Невідома команда: {command}. Введіть /help"


manager = ConnectionManager()
moderation = ModerationManager()
