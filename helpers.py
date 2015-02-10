"""Helpers for Flask-Restless and Flask.

"""

from flask.ext.restless import ProcessingException
from werkzeug.exceptions import BadRequest

from postprocessors import json_serializer


class IllegalArgumentError(Exception):
    """This exception is raised when a calling function has provided illegal
    arguments to a function or method.

    """
    pass


class CreateAPIWrapper(object):
    def __init__(self, apimanager, api_version):
        self.apimanager = apimanager
        self.app = apimanager.app
        self.api_version = api_version

    def resource(self,
                 model,
                 results_per_page=25,
                 methods=None,
                 exclude_columns_in_get=None,
                 include_columns_in_get=None,
                 exclude_columns_in_put=None,
                 include_columns_in_put=None,
                 exclude_columns_in_post=None,
                 include_columns_in_post=None,
                 preprocessors=None,
                 postprocessors=None,
                 get_single_preprocessors=None,
                 get_many_preprocessors=None,
                 patch_single_preprocessors=None,
                 post_preprocessors=None,
                 delete_preprocessors=None,
                 get_single_postprocessors=None,
                 get_many_postprocessors=None,
                 patch_single_postprocessors=None,
                 post_postprocessors=None,
                 delete_postprocessors=None,
                 allow_functions=True,
                 relationname=None
                 ):
        """Creates a restful api endpoint using dnordbergs flask-restless
        branch.

        Uses some helpful conventions to set pre and post processors
        and include and exclude columns.

        :model: The database model to define the resource endpoint for
        :results_per_page: Number of paginated results for the GETMANY endpoint
        :max_results_per_page: Total results returned
        :methods: Methods available at resource endpoint
        :exclude_columns_in_get: GET columns to exclude
        :include_columns_in_get: GET columns to include
        :exclude_columns_in_put: PUT columns in exclude
        :include_columns_in_put: PUT columns in include
        :exclude_columns_in_post: POST columns in exclude
        :include_columns_in_post: POST columns in include
        :preprocessors: Global endpoint resource preprocessors
        :postprocessors: Global endpoint resource postprocessors
        :get_single_preprocessors: GETSINGLE preprocessors
        :get_many_preprocessors: GETMANY preprocessors
        :patch_single_preprocessors: PATCHSINGLE preprocessors
        :post_preprocessors: POST preprocessors
        :delete_preprocessors: DELETE preprocessors
        :get_single_postprocessors: GETSINGLE postprocessors
        :get_many_postprocessors: GETMANY postprocessors
        :patch_single_postprocessors: PATCHSINGLE postprocessors
        :post_postprocessors: POST postprocessors
        :delete_postprocessors: DELETE postprocessors
        :allow_functions: Provide endpoints to execute database functions
        :relationname: If specified, provides rest endpoints to the inner
                       resource defined by the relationname
        :returns: None
        """
        # Init params
        if methods is None:
            methods = ['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS']
        # http://docs.python-guide.org/en/latest/writing/gotchas.html
        if exclude_columns_in_get is None:
            exclude_columns_in_get = []
        if include_columns_in_get is None:
            include_columns_in_get = []
        if exclude_columns_in_put is None:
            exclude_columns_in_put = []
        if include_columns_in_put is None:
            include_columns_in_put = []
        if exclude_columns_in_post is None:
            exclude_columns_in_post = []
        if include_columns_in_post is None:
            include_columns_in_post = []
        if preprocessors is None:
            preprocessors = []
        if postprocessors is None:
            postprocessors = []
        if get_single_preprocessors is None:
            get_single_preprocessors = []
        if get_many_preprocessors is None:
            get_many_preprocessors = []
        if patch_single_preprocessors is None:
            patch_single_preprocessors = []
        if post_preprocessors is None:
            post_preprocessors = []
        if delete_preprocessors is None:
            delete_preprocessors = []
        if get_single_postprocessors is None:
            get_single_postprocessors = []
        if get_many_postprocessors is None:
            get_many_postprocessors = []
        if patch_single_postprocessors is None:
            patch_single_postprocessors = []
        if post_postprocessors is None:
            post_postprocessors = []
        if delete_postprocessors is None:
            delete_postprocessors = []

        # Exclude and include columns using the flask-restless interface
        api_opts = {}
        if exclude_columns_in_get:
            api_opts['exclude_columns'] = exclude_columns_in_get
        if include_columns_in_get:
            api_opts['include_columns'] = include_columns_in_get

        # Set other processors
        if exclude_columns_in_put and include_columns_in_put:
            msg = ('Cannot simultaneously specify both include columns and'
                   ' exclude columns (PUT).')
            raise IllegalArgumentError(msg)

        if exclude_columns_in_post and include_columns_in_post:
            msg = ('Cannot simultaneously specify both include columns and'
                   ' exclude columns (POST).')
            raise IllegalArgumentError(msg)

        preprocessors_ = {
            'GET_SINGLE': [] + preprocessors + get_single_preprocessors,
            'GET_MANY': preprocessors + get_many_preprocessors,
            'PATCH_SINGLE': preprocessors + patch_single_preprocessors,
            'POST': preprocessors + post_preprocessors,
            'DELETE': [] + preprocessors + delete_preprocessors,
        }

        postprocessors_ = {
            'GET_SINGLE': [json_serializer] + postprocessors + get_single_postprocessors,
            'GET_MANY': [json_serializer] + postprocessors + get_many_postprocessors,
            'PATCH_SINGLE': [json_serializer] + postprocessors + patch_single_postprocessors,
            'POST': [json_serializer] + postprocessors + post_postprocessors,
            'DELETE': [] + delete_postprocessors,
        }

        self.apimanager.create_api(model,
                                   methods=methods,
                                   url_prefix="/api/v{}".format(self.api_version),
                                   results_per_page=results_per_page,
                                   max_results_per_page=100000,
                                   postprocessors=postprocessors_,
                                   preprocessors=preprocessors_,
                                   allow_functions=allow_functions,
                                   relationname=relationname,
                                   validation_exceptions=[ProcessingException,
                                                          BadRequest],
                                   **api_opts
                                   )
