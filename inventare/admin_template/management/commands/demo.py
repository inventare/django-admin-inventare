from django.core.management.base import BaseCommand

import json
import logging
import os
import re
import time
from django.template.loader import get_template
from django.template.loader_tags import ExtendsNode, IncludeNode
from django.templatetags.static import StaticNode
from django.contrib.staticfiles import finders
from abc import abstractmethod
from typing import TypeVar, Generic, Callable, Any, Type

from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

import asyncio
from websockets.server import serve

T = TypeVar('T')

class NodeParserStrategyBase(Generic[T]):
    node: T
    parse_nodelist: Callable

    def __init__(self, node: T, parse_nodelist: Callable):
        self.node = node
        self.parse_nodelist = parse_nodelist

    @classmethod
    @abstractmethod
    def is_supported(cls, node: Any) -> bool:
        pass

    @abstractmethod
    def get_paths(self) -> list[str]:
        pass

class ExtendsParserStrategy(NodeParserStrategyBase[ExtendsNode]):
    @classmethod
    def is_supported(cls, node: Any) -> bool:
        return isinstance(node, ExtendsNode)
    
    def get_paths(self) -> list[str]:
        parent = self.node.parent_name.resolve({})
        extension_template = get_template(parent)
        
        self.parse_nodelist(extension_template.template.nodelist)
        return [extension_template.template.origin.name]

class IncludeParserStrategy(NodeParserStrategyBase[IncludeNode]):
    @classmethod
    def is_supported(cls, node: Any) -> bool:
        return isinstance(node, IncludeNode)

    def get_paths(self) -> list[str]:
        template = self.node.template.resolve({})
        inclusion_template = get_template(template)
        
        self.parse_nodelist(inclusion_template.template.nodelist)
        return [inclusion_template.template.origin.name]

class StaticParserStrategy(NodeParserStrategyBase[StaticNode]):
    @classmethod
    def is_supported(cls, node: Any) -> bool:
        return isinstance(node, StaticNode)

    def get_paths(self) -> list[str]:
        result = finders.find(self.node.path.resolve({}))
        if not result:
            return []
        path = str(result)
        return [path]

class HotReloadEventHandler(FileSystemEventHandler):
    def __init__(self, notify_frontend):
        self.notify_frontend = notify_frontend
        super().__init__()

    def on_moved(self, event: FileSystemEvent) -> None:
        self.notify_frontend()
    
    def on_created(self, event: FileSystemEvent) -> None:
        self.notify_frontend()
    
    def on_deleted(self, event: FileSystemEvent) -> None:
        self.notify_frontend()
    
    def on_modified(self, event: FileSystemEvent) -> None:
        self.notify_frontend()


class Command(BaseCommand):
    files: list[str] = []
    ignore_paths_regex: str = '\.venv*'
    parser_strategies: list[Type[NodeParserStrategyBase]] = [
        ExtendsParserStrategy,
        IncludeParserStrategy,
        StaticParserStrategy,
    ]

    def make_files_relative(self):
        current_path = os.getcwd()
        self.files = list(map(lambda file: os.path.relpath(file, current_path), self.files))

    def filter_ignore_paths(self):
        self.files = list(filter(lambda file: re.match(self.ignore_paths_regex, file) is None, self.files))

    def parse_node(self, node):
        for strategy in self.parser_strategies:
            if not strategy.is_supported(node):
                continue
            try:
                paths = strategy(node, self.parse_nodelist).get_paths()
                if not paths:
                    continue
            except Exception:
                continue
            self.files.append(*paths)

    def parse_nodelist(self, nodelist):
        if not nodelist:
            return
        
        for node in nodelist:
            self.parse_node(node)
            
            if hasattr(node, 'nodelist'):
                self.parse_nodelist(node.nodelist)

    def handle_initialize_view(self, path: str):
        print(f"Initialized {path}")

        print(path)

        from django.urls import resolve
        match = resolve(path)
        if not match.func:
            return
        
        print(match.func)
        print(dir(match.func))
    
    def notify_frontend(self):
        if not self.websocket:
            return
        asyncio.run(
            self.websocket.send(json.dumps({ 'event': 'reload' }))
        )

    def handle_message_receive(self, data: str):
        data = json.loads(data)
        if data.get('event') == 'initialize_view':
            self.handle_initialize_view(data.get('path'))

    async def websocket_server(self, websocket):
        self.websocket = websocket
        async for message in websocket:
            self.handle_message_receive(message)

    async def run_server(self):
        async with serve(self.websocket_server, "localhost", 9002):
            await asyncio.Future()

    def handle(self, *args, **options):
        template_name = 'admin/login.html'
        template = get_template(template_name)

        self.files.append(template.template.origin.name)
        self.parse_nodelist(template.template.nodelist)

        self.make_files_relative()
        self.filter_ignore_paths()

        event_handler = HotReloadEventHandler(self.notify_frontend)
        observer = Observer()
        for file in self.files:
            observer.schedule(event_handler, file, False)

        observer.start()
        try:
            asyncio.run(self.run_server())
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
