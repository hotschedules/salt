# -*- coding: utf-8 -*-

# Import Python libs
from __future__ import absolute_import

# Import Salt libs
import salt.config
import salt.daemons.masterapi as masterapi

# Import Salt Testing Libs
from tests.support.unit import TestCase
from tests.support.mock import (
    patch,
    MagicMock,
)


class LocalFuncsTestCase(TestCase):
    '''
    TestCase for salt.daemons.masterapi.LocalFuncs class
    '''

    def setUp(self):
        opts = salt.config.master_config(None)
        self.local_funcs = masterapi.LocalFuncs(opts, 'test-key')

    def test_runner_token_not_authenticated(self):
        '''
        Asserts that a TokenAuthenticationError is returned when the token can't authenticate.
        '''
        mock_ret = {u'error': {u'name': u'TokenAuthenticationError',
                               u'message': u'Authentication failure of type "token" occurred.'}}
        ret = self.local_funcs.runner({u'token': u'asdfasdfasdfasdf'})
        self.assertDictEqual(mock_ret, ret)

    def test_runner_token_authorization_error(self):
        '''
        Asserts that a TokenAuthenticationError is returned when the token authenticates, but is
        not authorized.
        '''
        token = u'asdfasdfasdfasdf'
        load = {u'token': token, u'fun': u'test.arg', u'kwarg': {}}
        mock_token = {u'token': token, u'eauth': u'foo', u'name': u'test'}
        mock_ret = {u'error': {u'name': u'TokenAuthenticationError',
                               u'message': u'Authentication failure of type "token" occurred '
                                           u'for user test.'}}

        with patch('salt.auth.LoadAuth.authenticate_token', MagicMock(return_value=mock_token)), \
             patch('salt.auth.LoadAuth.get_auth_list', MagicMock(return_value=[])):
            ret = self.local_funcs.runner(load)

        self.assertDictEqual(mock_ret, ret)

    def test_runner_token_salt_invocation_error(self):
        '''
        Asserts that a SaltInvocationError is returned when the token authenticates, but the
        command is malformed.
        '''
        token = u'asdfasdfasdfasdf'
        load = {u'token': token, u'fun': u'badtestarg', u'kwarg': {}}
        mock_token = {u'token': token, u'eauth': u'foo', u'name': u'test'}
        mock_ret = {u'error': {u'name': u'SaltInvocationError',
                               u'message': u'A command invocation error occurred: Check syntax.'}}

        with patch('salt.auth.LoadAuth.authenticate_token', MagicMock(return_value=mock_token)), \
             patch('salt.auth.LoadAuth.get_auth_list', MagicMock(return_value=['testing'])):
            ret = self.local_funcs.runner(load)

        self.assertDictEqual(mock_ret, ret)

    def test_runner_eauth_not_authenticated(self):
        '''
        Asserts that an EauthAuthenticationError is returned when the user can't authenticate.
        '''
        mock_ret = {u'error': {u'name': u'EauthAuthenticationError',
                               u'message': u'Authentication failure of type "eauth" occurred for '
                                           u'user UNKNOWN.'}}
        ret = self.local_funcs.runner({u'eauth': u'foo'})
        self.assertDictEqual(mock_ret, ret)

    def test_runner_eauth_authorization_error(self):
        '''
        Asserts that an EauthAuthenticationError is returned when the user authenticates, but is
        not authorized.
        '''
        load = {u'eauth': u'foo', u'username': u'test', u'fun': u'test.arg', u'kwarg': {}}
        mock_ret = {u'error': {u'name': u'EauthAuthenticationError',
                               u'message': u'Authentication failure of type "eauth" occurred for '
                                           u'user test.'}}
        with patch('salt.auth.LoadAuth.authenticate_eauth', MagicMock(return_value=True)), \
             patch('salt.auth.LoadAuth.get_auth_list', MagicMock(return_value=[])):
            ret = self.local_funcs.runner(load)

        self.assertDictEqual(mock_ret, ret)

    def test_runner_eauth_salt_invocation_error(self):
        '''
        Asserts that an EauthAuthenticationError is returned when the user authenticates, but the
        command is malformed.
        '''
        load = {u'eauth': u'foo', u'username': u'test', u'fun': u'bad.test.arg.func', u'kwarg': {}}
        mock_ret = {u'error': {u'name': u'SaltInvocationError',
                               u'message': u'A command invocation error occurred: Check syntax.'}}
        with patch('salt.auth.LoadAuth.authenticate_eauth', MagicMock(return_value=True)), \
             patch('salt.auth.LoadAuth.get_auth_list', MagicMock(return_value=['testing'])):
            ret = self.local_funcs.runner(load)

        self.assertDictEqual(mock_ret, ret)

    def test_wheel_token_not_authenticated(self):
        '''
        Asserts that a TokenAuthenticationError is returned when the token can't authenticate.
        '''
        mock_ret = {u'error': {u'name': u'TokenAuthenticationError',
                               u'message': u'Authentication failure of type "token" occurred.'}}
        ret = self.local_funcs.wheel({u'token': u'asdfasdfasdfasdf'})
        self.assertDictEqual(mock_ret, ret)

    def test_wheel_token_authorization_error(self):
        '''
        Asserts that a TokenAuthenticationError is returned when the token authenticates, but is
        not authorized.
        '''
        token = u'asdfasdfasdfasdf'
        load = {u'token': token, u'fun': u'test.arg', u'kwarg': {}}
        mock_token = {u'token': token, u'eauth': u'foo', u'name': u'test'}
        mock_ret = {u'error': {u'name': u'TokenAuthenticationError',
                               u'message': u'Authentication failure of type "token" occurred '
                                           u'for user test.'}}

        with patch('salt.auth.LoadAuth.authenticate_token', MagicMock(return_value=mock_token)), \
             patch('salt.auth.LoadAuth.get_auth_list', MagicMock(return_value=[])):
            ret = self.local_funcs.wheel(load)

        self.assertDictEqual(mock_ret, ret)

    def test_wheel_token_salt_invocation_error(self):
        '''
        Asserts that a SaltInvocationError is returned when the token authenticates, but the
        command is malformed.
        '''
        token = u'asdfasdfasdfasdf'
        load = {u'token': token, u'fun': u'badtestarg', u'kwarg': {}}
        mock_token = {u'token': token, u'eauth': u'foo', u'name': u'test'}
        mock_ret = {u'error': {u'name': u'SaltInvocationError',
                               u'message': u'A command invocation error occurred: Check syntax.'}}

        with patch('salt.auth.LoadAuth.authenticate_token', MagicMock(return_value=mock_token)), \
             patch('salt.auth.LoadAuth.get_auth_list', MagicMock(return_value=['testing'])):
            ret = self.local_funcs.wheel(load)

        self.assertDictEqual(mock_ret, ret)

    def test_wheel_eauth_not_authenticated(self):
        '''
        Asserts that an EauthAuthenticationError is returned when the user can't authenticate.
        '''
        mock_ret = {u'error': {u'name': u'EauthAuthenticationError',
                               u'message': u'Authentication failure of type "eauth" occurred for '
                                           u'user UNKNOWN.'}}
        ret = self.local_funcs.wheel({u'eauth': u'foo'})
        self.assertDictEqual(mock_ret, ret)

    def test_wheel_eauth_authorization_error(self):
        '''
        Asserts that an EauthAuthenticationError is returned when the user authenticates, but is
        not authorized.
        '''
        load = {u'eauth': u'foo', u'username': u'test', u'fun': u'test.arg', u'kwarg': {}}
        mock_ret = {u'error': {u'name': u'EauthAuthenticationError',
                               u'message': u'Authentication failure of type "eauth" occurred for '
                                           u'user test.'}}
        with patch('salt.auth.LoadAuth.authenticate_eauth', MagicMock(return_value=True)), \
             patch('salt.auth.LoadAuth.get_auth_list', MagicMock(return_value=[])):
            ret = self.local_funcs.wheel(load)

        self.assertDictEqual(mock_ret, ret)

    def test_wheel_eauth_salt_invocation_error(self):
        '''
        Asserts that an EauthAuthenticationError is returned when the user authenticates, but the
        command is malformed.
        '''
        load = {u'eauth': u'foo', u'username': u'test', u'fun': u'bad.test.arg.func', u'kwarg': {}}
        mock_ret = {u'error': {u'name': u'SaltInvocationError',
                               u'message': u'A command invocation error occurred: Check syntax.'}}
        with patch('salt.auth.LoadAuth.authenticate_eauth', MagicMock(return_value=True)), \
             patch('salt.auth.LoadAuth.get_auth_list', MagicMock(return_value=['testing'])):
            ret = self.local_funcs.wheel(load)

        self.assertDictEqual(mock_ret, ret)

    def test_wheel_user_not_authenticated(self):
        '''
        Asserts that an UserAuthenticationError is returned when the user can't authenticate.
        '''
        mock_ret = {u'error': {u'name': u'UserAuthenticationError',
                               u'message': u'Authentication failure of type "user" occurred for '
                                           u'user UNKNOWN.'}}
        ret = self.local_funcs.wheel({})
        self.assertDictEqual(mock_ret, ret)


class FakeCache(object):

    def __init__(self):
        self.data = {}

    def store(self, bank, key, value):
        self.data[bank, key] = value

    def fetch(self, bank, key):
        return self.data[bank, key]


class RemoteFuncsTestCase(TestCase):
    '''
    TestCase for salt.daemons.masterapi.RemoteFuncs class
    '''

    def setUp(self):
        opts = salt.config.master_config(None)
        self.funcs = masterapi.RemoteFuncs(opts)
        self.funcs.cache = FakeCache()

    def test_mine_get(self, tgt_type_key='tgt_type'):
        '''
        Asserts that ``mine_get`` gives the expected results.

        Actually this only tests that:

        - the correct check minions method is called
        - the correct cache key is subsequently used
        '''
        self.funcs.cache.store('minions/webserver', 'mine',
                               dict(ip_addr='2001:db8::1:3'))
        with patch('salt.utils.minions.CkMinions._check_compound_minions',
                   MagicMock(return_value=(dict(
                       minions=['webserver'],
                       missing=[])))):
            ret = self.funcs._mine_get(
                {
                    'id': 'requester_minion',
                    'tgt': 'G@roles:web',
                    'fun': 'ip_addr',
                    tgt_type_key: 'compound',
                }
            )
        self.assertDictEqual(ret, dict(webserver='2001:db8::1:3'))

    def test_mine_get_pre_nitrogen_compat(self):
        '''
        Asserts that pre-Nitrogen API key ``expr_form`` is still accepted.

        This is what minions before Nitrogen would issue.
        '''
        self.test_mine_get(tgt_type_key='expr_form')
