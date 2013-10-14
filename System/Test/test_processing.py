from __future__ import with_statement
import json
from Objects.params import Params


class TestProcessing(object):
    def test_receive_information_from_physical_network(self, r):

        channel = 'foo.*'
        data = '{\"firstname\": \"damien\", \"lastname\": \"PUIG\"}'
        subscription = r.pubsub()

        assert subscription.psubscribe(channel) is None

        assert r.publish("foo.info", data) == 1



        # there should be now 2 messages in the buffer, a subscribe and the
        # one we just published
        assert next(subscription.listen()) == \
               {
                   'type': 'psubscribe',
                   'pattern': None,
                   'channel': 'foo.*',
                   'data': 1
               }

        receive = next(subscription.listen())

        assert receive == \
               {
                   'type': 'pmessage',
                   'pattern': 'foo.*',
                   'channel': 'foo.info',
                   'data': data
               }


    def test_deserialise_information_from_physical_network(self, r):

        data = '{\"firstname\": \"damien\", \"lastname\": \"PUIG\"}'
        received = \
            {
                'type': 'pmessage',
                'pattern': 'foo.*',
                'channel': 'foo.info',
                'data': data
            }

        result = json.loads(received['data'])

        assert result['firstname'] == 'damien'


    def test_qoc_incoming_message(self, r):
        data = '{\"firstname\": \"damien\", \"lastname\": \"PUIG\", \"qoc\": {\"completeness\": \"1\",  \"significance\": \"normal\"} }'
        received = \
            {
                'type': 'pmessage',
                'pattern': 'foo.*',
                'channel': 'foo.info',
                'data': data
            }

        result = json.loads(received['data'])

        assert result['qoc']['significance'] == 'normal'


    def test_if_received_information_doesnt_match_representation(self, r):

        data = 800
        received = \
            {
                'type': 'pmessage',
                'pattern': 'foo.*',
                'channel': 'foo.info',
                'data': data
            }

        try:
            result = json.loads(received['data'])
        except Exception, e:
            assert received['data'] == 800
