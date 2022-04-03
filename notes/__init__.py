import warnings
import aiohttp
import asyncio
from utils.templates import *


class NotesClient:

    def __init__(self, host: str, username: str = "", password: str = "", ssl: bool = True):
        self.host = host
        self.authorize = aiohttp.BasicAuth(username, password)
        self.loop = asyncio.get_event_loop()
        self.ssl = ssl

    def get_notes(self, id_: int = None, **kwargs):
        """
        Get a list of notes with specified parameters.
        :param id_: (optional) the id of the desired note. Defaults to None.
        :param kwargs: (optional) Parameters for query. Includes 'category:str', 'exclude:str or list', 'pruneBefore:int', 'chunkSize:int', 'chunkCursor:int'
        :return: Json of notes
        """
        acceptable_params = ['category', 'exclude', 'pruneBefore', 'chunkSize', 'chunkCursor']
        params = {key:kwargs[key] for key in kwargs.keys() if key in acceptable_params}
        if id_:
            id_ = f"/{id_}"
        else:
            id_ = ""
        if not "exclude" in params:
            warnings.warn("--Not excluding content could lead to too much data returning and a gateway timeout! Please consider using 'exclude=[\'content\']'--")
        else:
            if not "content" in params['exclude']:
                warnings.warn(
                    "--Not excluding content could lead to too much data returning and a gateway timeout! Please consider using 'exclude=[\'content\']'--")
        query_string = id_ + notes_template.render(params=params)
        status, notes = self.loop.run_until_complete(self.__async_notes("GET", query_string))
        if status == 404:
            return None
        elif status == 200:
            return {"status": status, "notes":notes}


    def post_note(self, title: str, content: str, category: str = ""):
        """
        Post a note to the api
        :param title: Desired title of the note.
        :param content: Body of the note.
        :param category: Folder to post the note to. Defaults to "".
        :return: Response result.
        """
        body = {
            "title": title,
            "content": content,
            "category": category
        }
        status, notes = self.loop.run_until_complete(self.__async_notes("POST", body=body))
        return {"status": status, "notes": notes}

    def put_note(self, id_: int, **kwargs):
        """
        Update note on the server.
        :param id_: ID of the note to update
        :param kwargs: (optional) Fields to update in note. Includes 'title:str', 'content:str', 'category:str'.
        :return:
        """
        acceptable_params = ['title', 'content', 'category']
        body = {k: kwargs[k] for k in acceptable_params if k in kwargs}
        query_string = f"/{id_}"
        status, notes = self.loop.run_until_complete(self.__async_notes("PUT", query=query_string, body=body))
        return {"status": status, "notes": notes}

    def delete_note(self, id_:int):
        """
        Delete note from the server.
        :param id_: ID of the note to update
        :return:
        """
        query_string = f"/{id_}"
        status, notes = self.loop.run_until_complete(self.__async_notes("DELETE", query=query_string))
        return {"status": status, "notes": notes}

    def get_settings(self):
        status, settings = self.loop.run_until_complete(self.__async_settings("GET"))
        return {"status": status, "settings": settings}

    def put_settings(self, **kwargs):
        status, settings = self.loop.run_until_complete(self.__async_settings("PUT", kwargs))
        return {"status": status, "settings": settings}

    async def __async_notes(self, caller: str, query: str = "", body:dict = {}):
        """
        Asynchronous request to notes api.
        :param caller: Method calling the api
        :param query: Query string for api
        :param body: Dict of values for making note.
        :return: Json of notes
        """
        # ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=self.ssl)
        endpoint = f"/index.php/apps/notes/api/v1/notes{query}"
        headers = {"Accept": "application/json"}
        async with aiohttp.ClientSession(connector=conn) as session:
            if caller == "GET":
                async with session.get(self.host + endpoint,
                                       auth=self.authorize, headers=headers) as response:
                    status = response.status
                    notes = await response.json()
            elif caller == "POST":
                async with session.post(self.host + endpoint,
                                       auth=self.authorize, headers=headers, data=body) as response:
                    status = response.status
                    notes = await response.json()
            elif caller == "PUT":
                async with session.put(self.host + endpoint,
                                       auth=self.authorize, headers=headers, data=body) as response:
                    status = response.status
                    notes = await response.json()
            elif caller == "DELETE":
                async with session.delete(self.host + endpoint,
                                       auth=self.authorize, headers=headers) as response:
                    status = response.status
                    notes = await response.json()
        return status, notes

    async def __async_settings(self, caller: str, body: dict={}):
        """
        Asynchronous request to notes api.
        :param caller: function calling this method.
        :param body: Settings to be changed.
        :return: Json of notes
        """
        # ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=self.ssl)
        endpoint = f"/index.php/apps/notes/api/v1/settings"
        headers = {"Accept": "application/json"}
        async with aiohttp.ClientSession(connector=conn) as session:
            if caller == "GET":
                async with session.get(self.host + endpoint,
                                       auth=self.authorize, headers=headers) as response:
                    status = response.status
                    settings = await response.json()
            elif caller == "PUT":
                async with session.put(self.host + endpoint,
                                       auth=self.authorize, headers=headers, data=body) as response:
                    status = response.status
                    settings = await response.json()
        return status, settings
