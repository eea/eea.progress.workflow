""" GET
"""
# -*- coding: utf-8 -*-
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter, queryAdapter
from zope.interface import implementer
from zope.interface import Interface
from eea.progress.workflow.interfaces import IWorkflowProgress


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class WorkflowProgress(object):
    """ Get workflow progress
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"workflow.progress": {
            "@id": "{}/@workflow.progress".format(self.context.absolute_url())
        }}
        if not expand:
            return result

        if IPloneSiteRoot.providedBy(self.context):
            return result

        progress = queryAdapter(self.context, IWorkflowProgress)
        if progress:
            result["workflow.progress"]['steps'] = json_compatible(
                progress.steps)
            result["workflow.progress"]['done'] = json_compatible(
                progress.done)
        return result


class WorkflowProgressGet(Service):
    """Get workflow progress information"""

    def reply(self):
        """ Reply
        """
        info = WorkflowProgress(self.context, self.request)
        return info(expand=True)["workflow.progress"]
