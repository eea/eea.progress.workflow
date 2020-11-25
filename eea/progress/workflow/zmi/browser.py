""" Browser controllers
"""
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import base_hasattr


class ZMIStateProgressEdit(BrowserView):
    """ ZMI edit for state progress monitoring
    """

    def setProperties(self, form):
        """ Update properties
        """
        progress = form.get('progress', 0)
        self.context.progress = progress

    def __call__(self, **kwargs):
        form = self.request.form
        form.update(kwargs)

        submit = form.get('submit', None)
        if not submit:
            return self.index()

        self.setProperties(form)

        redirect = form.get('redirect', self.__name__)
        self.request.response.redirect(
            redirect + '?manage_tabs_message=Changes saved')


class ZMIWorkflowProgressEdit(BrowserView):
    """ ZMI edit for workflow progress monitoring
    """
    def states(self):
        """ Defined states
        """
        items = self.context.states.items()
        items = sorted(items, key=lambda a: a[1].progress if
                       base_hasattr(a[1], 'progress') else 0)
        return items
