""" Progress adapters
"""
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import base_hasattr
from zope.interface import implementer
from eea.progress.workflow.interfaces import IWorkflowProgress


@implementer(IWorkflowProgress)
class WorkflowProgress(object):
    """
    Abstract adapter for workflow progress. This will be used as a fallback
    adapter if the API can't find a more specific adapter for your workflow

    """

    def __init__(self, context):
        self.context = context
        self._hasProgress = None
        self._progress = None
        self._done = None
        self._steps = None
        self._minProgress = None

    @property
    def minProgress(self):
        """Minimum progress to display"""
        return -1

    @property
    def hasProgress(self):
        """Is progress updated"""
        if self._hasProgress is not None:
            return self._hasProgress

        wftool = getToolByName(self.context, "portal_workflow")
        workflows = wftool.getWorkflowsFor(self.context)
        for wf in workflows:
            for state in wf.states.values():
                progress = (state.progress if
                            base_hasattr(state, "progress") else None)
                if progress:
                    self._hasProgress = True
                    return self._hasProgress

        self._hasProgress = False
        return self._hasProgress

    def guessProgress(self, state):
        """Guess progress from state"""
        if "private" in state.lower():
            return 25
        elif "pending" in state.lower():
            return 50
        elif "published" in state.lower():
            return 100
        elif "visible" in state.lower():
            return 100
        elif "internal" in state.lower():
            return 100
        elif "external" in state.lower():
            return 100
        return 75

    @property
    def progress(self):
        """Progress"""
        if self._progress is not None:
            return self._progress

        self._progress = 0
        wftool = getToolByName(self.context, "portal_workflow")
        try:
            state = wftool.getInfoFor(self.context, "review_state")
        except WorkflowException:
            state = "published"

        # No progress defined
        if not self.hasProgress:
            self._progress = self.guessProgress(state)
            return self._progress

        # Progress defined via ZMI
        workflows = wftool.getWorkflowsFor(self.context)
        for wf in workflows:
            state = wf.states.get(state)
            if not state:
                continue
            progress = (state.progress if
                        base_hasattr(state, "progress") else None)
            if progress is not None:
                self._progress = progress
                break

        return self._progress

    @property
    def done(self):
        """Done"""
        return self.progress

    @property
    def steps(self):
        """Return a SimpleVocabulary like tuple with steps and % done like:

        (
          ('private', 0, 'Private'),
          ('pending': 50, 'Pending'),
          ('visible': 50, 'Public Draft'),
          ('published', 100, 'Public')
        )

        """
        if self._steps is not None:
            return self._steps

        hasProgress = self.hasProgress

        self._steps = []
        wftool = getToolByName(self.context, "portal_workflow")
        progress_steps = {}

        for wf in wftool.getWorkflowsFor(self.context):
            for name, item in sorted(
                wf.states.items(),
                key=lambda a: (a[1].progress if
                               base_hasattr(a[1], "progress") else 0)
                if hasProgress
                else self.guessProgress(a[0]),
            ):
                title = item.title if base_hasattr(item, "title") else name
                description = (
                    item.description or title
                    if base_hasattr(item, "description")
                    else title
                )
                if hasProgress:
                    progress = (item.progress if
                                base_hasattr(item, "progress") else 0)
                else:
                    progress = self.guessProgress(name)

                if progress <= self.minProgress:
                    continue

                has_progress = progress_steps.get(progress)

                if has_progress:
                    name_list = has_progress[0]
                    title_list = has_progress[2]
                    desc_list = has_progress[3]

                    name_list.append(name)
                    title_list.append(title)
                    desc_list.append(description)
                else:
                    step = (
                        [name, ],
                        progress,
                        [title, ],
                        [description, ],
                    )
                    self._steps.append(step)
                    progress_steps[progress] = step

            break
        return self._steps
