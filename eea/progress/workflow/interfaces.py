""" Module where all interfaces, events and exceptions live.

    >>> portal = layer['portal']
    >>> sandbox = portal._getOb('sandbox')

"""

from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface
from eea.progress.workflow.config import EEAMessageFactory as _


class IBaseObject(Interface):
    """ Marker interface for Archetypes or Dexterity objects
    """


class IEeaProgressWorkflowLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IWorkflow(Interface):
    """ Marker interface for workflow
    """


class IWorkflowState(Interface):
    """ Marker interface for workflow state
    """


#
# Adapters
#
class IWorkflowProgress(Interface):
    """
    These adapters provides progress information for an object

    By default, if you don't manually define any progress via ZMI
    the system tries to guess the progress using a very simple algorithm:

      - private = 25%
      - pending = 50%
      - published = 100%

        >>> from eea.progress.workflow.interfaces import IWorkflowProgress
        >>> IWorkflowProgress(sandbox).hasProgress
        False

        >>> IWorkflowProgress(sandbox).progress
        25

        >>> portal.portal_workflow.doActionFor(sandbox, 'submit')
        >>> IWorkflowProgress(sandbox).progress
        50

        >>> portal.portal_workflow.doActionFor(sandbox, 'publish')
        >>> IWorkflowProgress(sandbox).progress
        100

    You can also get a list of steps and their percentage:


        >>> IWorkflowProgress(sandbox).steps
        [(['private'], 25, ['Private'], ...(['published'], 100, ['Publish...)]

    And % done (on a simple item it's the same as progress). This is useful
    within Collections

        >>> IWorkflowProgress(sandbox).done
        100

    You can always change progress values per state via ZMI:

        >>> wf = portal.portal_workflow.simple_publication_workflow
        >>> wf.states.pending.progress = 60
        >>> wf.states.published.progress = 90

        >>> IWorkflowProgress(sandbox).hasProgress
        True

        >>> IWorkflowProgress(sandbox).progress
        90

    Changing at least one state will disable the auto-detection mechanism. So
    don't forget to manually set progress for all possible states within your
    workflow:

        >>> portal.portal_workflow.doActionFor(sandbox, 'retract')
        >>> IWorkflowProgress(sandbox).progress
        0

        >>> portal.portal_workflow.doActionFor(sandbox, 'submit')
        >>> IWorkflowProgress(sandbox).progress
        60

        >>> IWorkflowProgress(sandbox).done
        60

        >>> IWorkflowProgress(sandbox).steps
        [(['private'], 0, ['Private'],...['pending'], 60, ['Pending...

    """
    progress = schema.Int(
        title=_(u"Progress"),
        description=_(u"For a folderish item, this can be the sum of all items"
                      "with progress 100% / total items possible progress"),
        readonly=True,
        default=0
    )

    done = schema.Int(
        title=_(u"% Done"),
        description=_(u"For a folderish item, this can be the sum of all items"
                      "progress / total items possible progress"),
        readonly=True,
        default=0
    )

    steps = schema.List(
        title=_(u"Steps"),
        description=_(u"A list of workflow steps with percetage"),
        readonly=True
    )
