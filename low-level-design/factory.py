
"""
    Problem: Design a Notification System

    - Design a system that can send notifications to users through multiple channels — 
    Email, SMS, and Push. Given a channel type and a message, the system should create the right notifier and send the message. 
    It should be easy to add a new channel later without modifying existing code.

"""
"""
    Questions:
        - do we need to care about checking if user exists?
        - duplicate sends?
        - how do we want to approach concurrency, multi-users, persistence?
        - do we we need to consider how to store the messsages?
        - do we need to enforce character limits based on channel? ie. emails can potentially be longer than an sms. if we allow the same size for all channels, when we send
            do we chunk the message?
                - out of scope
        - concurrency? should we have one queue for messages to send where multiple workers poll from

    - Requirements:
        - primary capabilities
            - send notifications to users through multiple channels(email, sms, push)
                - send
                - create
                - notify
                
            - message and channel type are given
            - easy to add new channel without modifying existing code

        - rules & completion
            - implement a factory design, where one class/method handles which channel to ship
            
        - error handling
            - check if user exists, if doesn't, then return error
            - let's just go with at least once delivery

        - scope boundaries
            - just handle the message creation, send, and factory implementation 

    - Entities & Responsibilities:
        - Message:
            - to: User()
            - from: User()
            - msg: string
            - channel: 
                Channel(Enum) -> 
                    - Email
                    - SMS
                    - Push

        - User:
            - name: str
            - channels: Dict: {"SMS": str, "email": str...}

        - Notifier(ABC):
            @abstractmethod
            def send(self, destination: str, content: str) -> bool


        - NotifierFactory:
            @staticmethod
            def create(channel: channel) -> Notifier()

        - NotificationService:
            - def lookup_user(User, Channel)

    - Class Design:
    - Implementation:
    - Extensibility:
 
"""

"""
    Entities

    Channel(Enum) — EMAIL, SMS, PUSH
    User — name: str, channels: Dict[Channel, str]
    Notifier(ABC) — send(destination: str, content: str) -> bool
    EmailNotifier(Notifier), SMSNotifier(Notifier) — fully implement both (stub the actual send with a print); skip PushNotifier, mention it follows the same pattern
    NotifierFactory — standalone class (not a Notifier subclass), holds a dict registry {Channel: NotifierClass}, create(channel: Channel) -> Notifier
    NotificationService — __init__(self, users: Dict[str, User]), send(user_id: str, channel: Channel, content: str) -> bool

    Cut from original plan (mention only, don't build)

    No standalone Message class — pass (user_id, channel, content) directly into NotificationService.send()
    No from_user — not doing any work in the design
    No retry/at-least-once mechanics beyond returning a bool
    No persistence, concurrency, or character-limit chunking

    NotificationService.send() logic

    Look up user = self.users.get(user_id) → raise/return error if None
    destination = user.channels[channel]
    notifier = NotifierFactory.create(channel)
    return notifier.send(destination, content)

    NotifierFactory — use a dict registry, not if/elif
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Optional


class Channel(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class User:
    def __init__(self, name: str, channels: Optional[Dict[Channel, str]] = None):
        self.name = name
        self.channels = channels if channels is not None else {}

    def out(self):
        print(f"name: {self.name} || channels: {self.channels}")


class Notifier(ABC):
    @abstractmethod
    def send(self, destination: str, content: str) -> bool:
        ...


class SMSNotifier(Notifier):
    def send(self, destination: str, content: str) -> bool:
        print(f"sending {Channel.SMS} to destination: {destination} || content: {content}")
        return True


class EmailNotifier(Notifier):
    def send(self, destination: str, content: str) -> bool:
        print(f"sending {Channel.EMAIL} to destination: {destination} || content: {content}")
        return True


class PushNotifier(Notifier):
    def send(self, destination: str, content: str) -> bool:
        print(f"sending {Channel.PUSH} to destination: {destination} || content: {content}")
        return True


_channels = {
    Channel.EMAIL: EmailNotifier,
    Channel.SMS: SMSNotifier,
    Channel.PUSH: PushNotifier,
}


class NotifierFactory:
    @staticmethod
    def create(channel: Channel) -> Optional[Notifier]:
        notifier_cls = _channels.get(channel)
        return notifier_cls() if notifier_cls else None


class NotificationService:
    def __init__(self, users: Dict[str, User]):
        self.users = users

    def send(self, user_id: str, channel: Channel, content: str) -> bool:
        user = self.users.get(user_id)
        if user is None:
            raise ValueError(f"User not found: {user_id}")

        destination = user.channels.get(channel)
        if destination is None:
            raise ValueError(f"User {user_id} has no destination for channel: {channel}")

        notifier = NotifierFactory.create(channel)
        if notifier is None:
            raise ValueError(f"No notifier registered for channel: {channel}")

        return notifier.send(destination, content)


def main():
    print("Starting\n")

    users = {
        "u1": User("michael", {Channel.SMS: "911"}),
    }
    service = NotificationService(users)

    result = service.send("u1", Channel.SMS, "hello!")
    print(f"Send result: {result}\n")

    try:
        service.send("u2", Channel.SMS, "hello!")
    except ValueError as e:
        print(f"Expected error: {e}\n")

    print("Finished")


if __name__ == "__main__":
    main()