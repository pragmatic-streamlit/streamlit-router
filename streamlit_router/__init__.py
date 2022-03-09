import inspect
import typing
from functools import wraps

from werkzeug.routing import Map, Rule
import streamlit as st


class StreamlitRouter:
    """ for syntax @
    https://werkzeug.palletsprojects.com/en/2.0.x/routing/
    """

    def __init__(self, default_path='/', inject_name='router'):
        self._map = Map()
        self.view_methods = {}
        self.views = {}
        self.default_path = default_path
        self.inject_name = inject_name
        self.urls = self._map.bind("", "/")

    def register(self, func: typing.Callable, path: str, methods: typing.List[str] = None, endpoint: str = None):
        return self.map(path, methods, endpoint)(func)

    def map(self, path: str, methods: typing.List[str] = None, endpoint: str = None):  # pylint: disable=unused-argument
        def _(func):
            nonlocal endpoint, methods
            if not endpoint:
                endpoint = func.__name__
            if not methods:
                methods = ['GET']
            self.views[endpoint] = func
            self._map.add(Rule(path, methods=methods, endpoint=endpoint))
            self.view_methods[endpoint] = methods

            @wraps(func)
            def wraped(*args, **kwargs):
                if args:
                    raise AssertionError(
                        'positon style args not allowed for route func')
                argspec = inspect.getfullargspec(func).args
                if self.inject_name in argspec:
                    kwargs[self.inject_name] = self
                return func(*args, **kwargs)
            return wraped
        return _

    def handle(self, path: str, method: str = None):
        endpoint, kwargs = self.urls.match(path, method) # pylint: disable=unpacking-non-sequence
        func = self.views[endpoint]
        argspec = inspect.getfullargspec(func).args
        if self.inject_name in argspec:
            kwargs[self.inject_name] = self
        return func(**kwargs)

    def redirect(self, path: str, method: str = None):
        st.session_state['request'] = (path, method)
        st.experimental_rerun()

    def build(self, endpoint: str, values: typing.Dict = None, method: str = None):
        if not method and self.view_methods[endpoint]:
            method = self.view_methods[endpoint][0]
        return self.urls.build(endpoint, values), method

    def serve(self):
        request = st.session_state.get('request')
        query_string = st.experimental_get_query_params()
        if request:
            self.handle(*request)
            path, method = request
            query_string['request'] = [f'{method}:{path}']
            st.experimental_set_query_params(**query_string)
        elif 'request' in query_string:
            method, path = query_string.get('request')[0].split(':')
            st.session_state['request'] = (path, method)
            st.experimental_rerun()
        else:
            self.handle(self.default_path)
