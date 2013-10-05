from __future__ import with_statement
import pytest
from Objects.params import Params
import redis

class TestPublishSubscribe(object):

    def test_physical_network_emit_to_system(self, r):
        channel = "physical.arduinos.arduino1.values"
        data = '{\"firstname\": \"damien\", \"lastname\": \"PUIG\"}'
        subscription = r.pubsub()

        assert subscription.psubscribe(Params.specific_channels["physical.arduinos"]) is None


        assert r.publish(channel, data) == 1



        # there should be now 2 messages in the buffer, a subscribe and the
        # one we just published
        assert next(subscription.listen()) == \
            {
                'type': 'psubscribe',
                'pattern': None,
                'channel': Params.specific_channels["physical.arduinos"],
                'data': 1
            }

        receive = next(subscription.listen())

        assert receive == \
            {
                'type': 'pmessage',
                'pattern': Params.specific_channels["physical.arduinos"],
                'channel': channel,
                'data': data
            }



    def test_physical_network_subscribe_to_comand(self, r):
        channel = "comands.physical"

        data = 'STOP'

        subscription = r.pubsub()

        assert subscription.subscribe(channel) is None


        assert r.publish(channel, data) == 1



        # there should be now 2 messages in the buffer, a subscribe and the
        # one we just published
        assert next(subscription.listen()) == \
            {
                'type': 'subscribe',
                'pattern': None,
                'channel': channel,
                'data': 1
            }

        receive = next(subscription.listen())

        assert receive == \
            {
                'type': 'message',
                'pattern': None,
                'channel': channel,
                'data': data
            }


    def test_system_emit_to_sinks(self, r):
        channel = "system.arduinos.arduino1.values"

        data = '{\"firstname\": \"damien\", \"lastname\": \"PUIG\"}'

        subscription = r.pubsub()

        assert subscription.psubscribe(Params.specific_channels["system.arduinos"]) is None


        assert r.publish(channel, data) == 1



        # there should be now 2 messages in the buffer, a subscribe and the
        # one we just published
        assert next(subscription.listen()) == \
            {
                'type': 'psubscribe',
                'pattern': None,
                'channel': Params.specific_channels["system.arduinos"],
                'data': 1
            }

        receive = next(subscription.listen())

        assert receive == \
            {
                'type': 'pmessage',
                'pattern': Params.specific_channels["system.arduinos"],
                'channel': channel,
                'data': data
            }



    def test_system_psubscribe_to_comand(self, r):
        channel = "comands.system"

        data = 'STOP'

        subscription = r.pubsub()

        assert subscription.subscribe(channel) is None


        assert r.publish(channel, data) == 1



        # there should be now 2 messages in the buffer, a subscribe and the
        # one we just published
        assert next(subscription.listen()) == \
            {
                'type': 'subscribe',
                'pattern': None,
                'channel': channel,
                'data': 1
            }

        receive = next(subscription.listen())

        assert receive == \
            {
                'type': 'message',
                'pattern': None,
                'channel': channel,
                'data': data
            }