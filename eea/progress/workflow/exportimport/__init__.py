""" GenericSetup export/import XML adapters
"""
import os
from zope.component import queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import IBody
from eea.progress.workflow.config import PROGRESSFILE


#
# Workflow progress
#
def importWorkflowProgress(context):
    """Import settings."""
    logger = context.getLogger('eea.progress.workflow')

    body = context.readDataFile(PROGRESSFILE)
    if body is None:
        logger.info("Nothing to import")
        return

    site = context.getSite()
    tool = getToolByName(site, 'portal_workflow', None)
    if not tool:
        logger.info('portal_workflows tool missing')
        return

    importer = queryMultiAdapter((tool, context), IBody, name=PROGRESSFILE)
    if importer is None:
        logger.warning("Import adapter missing.")
        return

    # set filename on importer so that syntax errors can be reported properly
    subdir = getattr(context, '_profile_path', '')
    importer.filename = os.path.join(subdir, PROGRESSFILE)

    importer.body = body
    logger.info("Imported.")


def exportWorkflowProgress(context):
    """Export settings."""
    logger = context.getLogger('eea.progress.workflow')
    site = context.getSite()
    tool = getToolByName(site, 'portal_workflow')

    if tool is None:
        logger.info("Nothing to export")
        return

    exporter = queryMultiAdapter((tool, context), IBody, name=PROGRESSFILE)
    if exporter is None:
        logger.warning("Export adapter missing.")
        return

    context.writeDataFile(PROGRESSFILE,
                          exporter.body, exporter.mime_type)
    logger.info("Exported.")
