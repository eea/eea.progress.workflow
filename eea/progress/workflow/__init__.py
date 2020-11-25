""" Main product initializer
"""
from zope.i18nmessageid.message import MessageFactory
from eea.progress.workflow import zmi

EEAMessageFactory = MessageFactory('eea')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

zmi.initialize()
