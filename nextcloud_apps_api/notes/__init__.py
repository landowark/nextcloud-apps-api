import warnings
import aiohttp
import asyncio
import requests
from nextcloud_apps_api.utils.templates import *
from nextcloud_apps_api.utils.custom_exceptions import *


class NotesAsyncClient:

    def __init__(self, host: str, username: str = "", password: str = "", ssl: bool = True):
        self.host = host
        self.authorize = aiohttp.BasicAuth(username, password)
        # self.loop = self.get_or_create_eventloop()
        self.loop = asyncio.get_running_loop()
        self.ssl = ssl

    def get_or_create_eventloop(self):
        try:
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()

    async def get_notes(self, id_: int = None, **kwargs):
        """
        Get a list of notes with specified parameters.
        :param id_: (optional) the id of the desired note. Defaults to None.
        :param kwargs: (optional) Parameters for query. Includes 'category:str', 'exclude:str or list', 'pruneBefore:int', 'chunkSize:int', 'chunkCursor:int'
        :return: Json of notes
        """
        acceptable_params = ['category', 'exclude', 'pruneBefore', 'chunkSize', 'chunkCursor']
        params = {key:kwargs[key] for key in kwargs.keys() if key in acceptable_params}
        if id_:
            id_ = f"/notes/{id_}"
        else:
            id_ = "/notes"
        if not "exclude" in params:
            warnings.warn("--Not excluding content could lead to too much data returning and a gateway timeout! Please consider using 'exclude=[\'content\']'--")
        else:
            if not "content" in params['exclude']:
                warnings.warn(
                    "--Not excluding content could lead to too much data returning and a gateway timeout! Please consider using 'exclude=[\'content\']'--")
        query_string = id_ + notes_template.render(params=params)
        status, notes = await self.__async_notes(caller="GET", query=query_string)
        return status, notes


    async def post_note(self, title: str, content: str, category: str = ""):
        """
        Post a note to the api
        :param title: Desired title of the note.
        :param content: Body of the note.
        :param category: Folder to post the note to. Defaults to "".
        :return: Response result.
        """
        query_string = "/notes"
        body = {
            "title": title,
            "content": content,
            "category": category
        }
        status, notes = await self.__async_notes(caller="POST", query=query_string, body=body)
        return status, notes

    async def put_note(self, id_: int, **kwargs):
        """
        Update note on the server.
        :param id_: ID of the note to update
        :param kwargs: (optional) Fields to update in note. Includes 'title:str', 'content:str', 'category:str'.
        :return:
        """
        acceptable_params = ['title', 'content', 'category']
        body = {k: kwargs[k] for k in acceptable_params if k in kwargs}
        query_string = f"/notes/{id_}"
        status, notes = await self.__async_notes(caller="PUT", query=query_string, body=body)
        return status, notes

    async def delete_note(self, id_:int):
        """
        Delete note from the server.
        :param id_: ID of the note to update
        :return:
        """
        query_string = f"/notes/{id_}"
        status, notes = await self.__async_notes(caller="DELETE", query=query_string)
        return status, notes

    async def get_settings(self):
        query_string = "/settings"
        status, settings = await self.__async_notes(caller="GET", query=query_string)
        return status, settings

    async def put_settings(self, **kwargs):
        query_string = "/settings"
        status, settings = await self.__async_notes(caller="PUT", body=kwargs, query=query_string)
        return status, settings

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
        endpoint = f"/index.php/apps/notes/api/v1{query}"
        headers = {"Accept": "application/json"}
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.request(caller, self.host + endpoint,
                                       auth=self.authorize, headers=headers, data=body) as response:
                ok = response.ok
                status = response.status
                notes = await response.json()
        if ok:
            return status, notes
        else:
            raise RequestError(f"The server returned a bad response: {status}")


class NotesClient:

    def __init__(self, host: str, username: str = "", password: str = "", ssl: bool = True):
        self.host = host
        self.authorize = requests.auth.HTTPBasicAuth(username, password)
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
            id_ = f"/notes/{id_}"
        else:
            id_ = "/notes"
        if not "exclude" in params:
            warnings.warn("--Not excluding content could lead to too much data returning and a gateway timeout! Please consider using 'exclude=[\'content\']'--")
        else:
            if not "content" in params['exclude']:
                warnings.warn(
                    "--Not excluding content could lead to too much data returning and a gateway timeout! Please consider using 'exclude=[\'content\']'--")
        query_string = id_ + notes_template.render(params=params)
        status, notes = self.__notes(caller="GET", query=query_string)
        return status, notes


    def post_note(self, title: str, content: str, category: str = ""):
        """
        Post a note to the api
        :param title: Desired title of the note.
        :param content: Body of the note.
        :param category: Folder to post the note to. Defaults to "".
        :return: Response result.
        """
        query_string = "/notes"
        body = {
            "title": title,
            "content": content,
            "category": category
        }
        status, notes = self.__notes(caller="POST", query=query_string, body=body)
        return status, notes

    def put_note(self, id_: int, **kwargs):
        """
        Update note on the server.
        :param id_: ID of the note to update
        :param kwargs: (optional) Fields to update in note. Includes 'title:str', 'content:str', 'category:str'.
        :return:
        """
        acceptable_params = ['title', 'content', 'category']
        body = {k: kwargs[k] for k in acceptable_params if k in kwargs}
        query_string = f"/notes/{id_}"
        status, notes = self.__notes(caller="PUT", query=query_string, body=body)
        return status, notes

    def delete_note(self, id_:int):
        """
        Delete note from the server.
        :param id_: ID of the note to update
        :return:
        """
        query_string = f"/notes/{id_}"
        status, notes = self.__notes(caller="DELETE", query=query_string)
        return status, notes

    def get_settings(self):
        query_string = "/settings"
        status, settings = self.__notes(caller="GET", query=query_string)
        return status, settings

    def put_settings(self, **kwargs):
        query_string = "/settings"
        status, settings = self.__notes(caller="PUT", body=kwargs, query=query_string)
        return status, settings

    def __notes(self, caller: str, query: str = "", body:dict = {}):
        """
        Request to notes api.
        :param caller: Method calling the api
        :param query: Query string for api
        :param body: Dict of values for making note.
        :return: Json of notes
        """

        endpoint = f"/index.php/apps/notes/api/v1{query}"
        print(endpoint)
        headers = {"Accept": "application/json"}
        with requests.Session() as session:
            with session.request(caller, self.host + endpoint,
                                       auth=self.authorize, headers=headers, data=body, verify=self.ssl) as response:
                ok = response.ok
                status = response.status_code
                notes = response.json()
        if ok:
            return status, notes
        else:
            raise RequestError(f"The server returned a bad response: {status}")