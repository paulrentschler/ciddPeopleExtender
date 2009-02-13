from Products.FacultyStaffDirectory.extenderInstallation import declareInstallRoutines

from Products.ciddPeopleExtender.person import biblioRefs
from Products.ciddPeopleExtender.person import modifyCiddFields

# declareInstallRoutines(globals(), biblioRefs, 'ciddPeopleExtender')  # Put the name of your product here.
# If you need to do further things at installation, declare your own install() and uninstall() rather than using declareInstallRoutines(). Do what you need to, and also call extenderInstallation.installExtender() (and uninstallExtender(), respectively) if extenderInstallation.localAdaptersAreSupported is True.
# 

def install(portal):
    """Register the extender so it takes effect on this Plone site."""
    sm = portal.getSiteManager()  # Local components are not per-container; they are per-sitemanager. It just so happens that every Plone site has a sitemanager. Hooray.
    sm.registerAdapter(biblioRefs, name='ciddPeopleExtenderBiblioRefs')
    sm.registerAdapter(modifyCiddFields, name='ciddPeopleExtenderModifyCiddFields')
    
    return "Registered the extender at the root of the Plone site."

def uninstall(portal):
    """Unregister the schema extender so it no longer takes effect on this Plone site."""
    sm = portal.getSiteManager()
    sm.unregisterAdapter(biblioRefs, name='ciddPeopleExtenderBiblioRefs')
    sm.unregisterAdapter(modifyCiddFields, name='ciddPeopleExtenderModifyCiddFields')
    
    return "Removed the extender from the root of the Plone site."