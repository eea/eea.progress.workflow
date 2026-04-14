"""Integration tests for eea.progress.workflow REST API views

Uses direct view instantiation to test without RelativeSession.
"""

import unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from transaction import commit
from eea.progress.workflow.tests.base import FUNCTIONAL_TESTING


class TestWorkflowProgressSetup(unittest.TestCase):
    """Test eea.progress.workflow installation"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_product_installed(self):
        """Test that eea.progress.workflow is installed"""
        from Products.CMFPlone.utils import get_installer
        installer = get_installer(self.portal, self.layer["request"])
        self.assertTrue(installer.is_product_installed("eea.progress.workflow"))

    def test_portal_exists(self):
        """Test that portal is set up"""
        self.assertIsNotNone(self.portal)


class TestWorkflowProgressView(unittest.TestCase):
    """Test workflow.progress view classes"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_workflow_progress_adapter_registered(self):
        """Test that WorkflowProgress adapter class exists"""
        from eea.progress.workflow.restapi.get import WorkflowProgress
        self.assertIsNotNone(WorkflowProgress)

    def test_workflow_progress_on_site_root(self):
        """Test WorkflowProgress on site root returns basic structure"""
        from eea.progress.workflow.restapi.get import WorkflowProgress
        wp = WorkflowProgress(self.portal, self.portal.REQUEST)
        result = wp(expand=False)
        self.assertIn("workflow.progress", result)
        self.assertIn("@id", result["workflow.progress"])

    def test_workflow_progress_get_class_exists(self):
        """Test that WorkflowProgressGet class exists"""
        from eea.progress.workflow.restapi.get import WorkflowProgressGet
        self.assertIsNotNone(WorkflowProgressGet)


class TestWorkflowProgressOnDocument(unittest.TestCase):
    """Test workflow.progress on content objects"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "test-doc", title="Test Document")
        commit()

    def test_workflow_progress_on_document(self):
        """Test WorkflowProgress on a Document"""
        from eea.progress.workflow.restapi.get import WorkflowProgress
        doc = self.portal["test-doc"]
        wp = WorkflowProgress(doc, self.portal.REQUEST)
        result = wp(expand=True)
        self.assertIn("workflow.progress", result)

    def test_workflow_progress_has_done_on_document(self):
        """Test that WorkflowProgress on Document has done field"""
        from eea.progress.workflow.restapi.get import WorkflowProgress
        doc = self.portal["test-doc"]
        wp = WorkflowProgress(doc, self.portal.REQUEST)
        result = wp(expand=True)
        self.assertIn("done", result["workflow.progress"])


if __name__ == "__main__":
    unittest.main()