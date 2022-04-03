
import aiohttp
import asyncio
from utils.templates import *


class BookmarkClient:

    def __init__(self, host: str, username: str = "", password: str = "", ssl: bool = True):
        self.host = host
        self.authorize = aiohttp.BasicAuth(username, password)
        self.loop = asyncio.get_event_loop()
        self.ssl = ssl

    def get_bookmarks(self, id_: int = None, **kwargs):
        '''
        Gets booksmarks from server
        :param id_: (optional) ID of the desired bookmark. Defaults to None.
        :param kwargs: (optional) Parameters for query. Includes tags:list, page:int, limit:int, sortby:str (one of url, title, description, public, lastmodified, clickcount), search:list (one of url, title, description, tags), conjunction:str ('and', 'or'), folder:int, url:str, unavailable, archive
        :return: Json of bookmarks
        '''
        acceptable_params = ['tags', 'page', 'limit', 'sortby', 'search', 'conjunction', 'folder', 'url', 'unavailable', 'archive']
        params = {key: kwargs[key] for key in kwargs.keys() if key in acceptable_params}
        if id_:
            id_ = f"/{id_}"
        else:
            id_ = ""
        query_string = id_ + bookmarks_template.render(params=params)
        response = self.loop.run_until_complete(self.__async_bookmarks("GET", query_string))
        try:
            return {"status":response[0], "bookmarks":response[1]['data']}
        except KeyError:
            return {"status":response[0], "bookmarks":response[1]}


    def post_bookmark(self, url: str, title: str = "", description: str = "", **kwargs):
        '''
        Posts a bookmark to the api.
        :param url: Link to the page of the bookmark
        :param title: Title of the bookmark
        :param description: Summary of the bookmarked page's content.
        :param kwargs: includes 'tags':list, 'folders':list
        :return: Json of bookmark
        '''
        params = kwargs
        query_string = bookmarks_template.render(params=params)
        body = {
            "url": url,
            "title": title,
            "description": description,
        }
        status, bookmark = self.loop.run_until_complete(self.__async_bookmarks("POST", query=query_string, body=body))
        return {"status": status, "bookmark": bookmark['item']}

    def put_bookmark(self, id_: int, **kwargs):
        """
        Update bookmark on the server.
        :param id_: ID of the bookmark to update
        :param kwargs: (optional) Fields to update in bookmark. Includes 'tags"list', 'title:str', 'description:str', 'folder:list'.
        :return: Json of new bookmark.
        """
        acceptable_params = ['tags,', 'title', 'description', 'folder']
        body = {k: kwargs[k] for k in acceptable_params if k in kwargs}
        query_string = f"/{id_}"
        status, bookmark = self.loop.run_until_complete(self.__async_bookmarks("PUT", query=query_string, body=body))
        return {"status": status, "bookmark": bookmark['item']}

    def delete_bookmark(self, id_):
        '''
        :param id_: ID of the bookmark to be deleted.
        :return: status of delete request.
        '''
        query_string = f"/{id_}"
        status, bookmarks = self.loop.run_until_complete(self.__async_bookmarks("DELETE", query=query_string))
        return {"status": status}

    def export_bookmarks(self):
        '''
        :return: Bookmarks in html format
        '''
        query_string = "/export"
        status, bookmarks = self.loop.run_until_complete(self.__async_bookmarks("EXPORT", query_string))
        return {"status":status, "bookmark":bookmarks}


    async def __async_bookmarks(self, caller: str, query: str = "", body: dict = {}):
        """
        Asynchronous request to bookmarks api.
        :param caller: Method calling the api
        :param query: Query string for api
        :param body: Dict of values for making bookmarks.
        :return: Json of bookmarks
        """
        # ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=self.ssl)
        endpoint = f"/index.php/apps/bookmarks/public/rest/v2/bookmark{query}"
        headers = {"Accept": "application/json"}
        async with aiohttp.ClientSession(connector=conn) as session:
            if caller == "GET":
                async with session.get(self.host + endpoint,
                                       auth=self.authorize, headers=headers) as response:
                    status = response.status
                    bookmarks = await response.json()
            elif caller == "POST":
                async with session.post(self.host + endpoint,
                                        auth=self.authorize, headers=headers, data=body) as response:
                    status = response.status
                    bookmarks = await response.json()
            elif caller == "PUT":
                async with session.put(self.host + endpoint,
                                       auth=self.authorize, headers=headers, data=body) as response:
                    status = response.status
                    bookmarks = await response.json()
            elif caller == "DELETE":
                async with session.delete(self.host + endpoint,
                                          auth=self.authorize, headers=headers) as response:
                    status = response.status
                    bookmarks = await response.json()
            elif caller == "EXPORT":
                async with session.get(self.host + endpoint,
                                       auth=self.authorize, headers=headers) as response:
                    status = response.status
                    bookmarks = await response.text()
        return status, bookmarks