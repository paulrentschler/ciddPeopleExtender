from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender, ISchemaModifier
from Products.Archetypes.atapi import *
from zope.interface import implements, Interface
from zope.component import adapts, provideAdapter

from Products.FacultyStaffDirectory.interfaces.person import IPerson

# Any field you tack on must have ExtensionField as its first subclass:
class _RichtextExtensionField(ExtensionField, TextField):
    pass

# Create a rich text field to contain info about publications (until FSD gets good publication support)
class biblioRefs(object):
    """Adapter that adds a rich text field to Person.
    
    You could also change or delete existing fields (though you might violate assumptions made in other code). To do that, implement ISchemaModifier instead of ISchemaExtender.
    """
    adapts(IPerson)
    implements(ISchemaExtender)
    
    _fields = [
            _RichtextExtensionField('publishedPapers',
                required=False,
                searchable=True,
                schemata="Professional Information",
                validators = ('isTidyHtmlWithCleanup',),
                default_output_type = 'text/x-html-safe',
                widget=RichWidget(
                    label=u"Selected publications",
                    description=u"Enter details of up to 6 papers you want to promote",
                ),
            ),

            _RichtextExtensionField('studySystems',
                required=False,
                searchable=True,
                schemata="Professional Information",
                validators = ('isTidyHtmlWithCleanup',),
                default_output_type = 'text/x-html-safe',
                widget=RichWidget(
                    label=u"Study systems",
                    description=u"One per line",
                ),
            ),
            
        ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self._fields

# Change the wording and order of a few fields; hide fields we're not going to use
class modifyCiddFields(object):
    adapts(IPerson)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context
        
    from Products.FacultyStaffDirectory.Person import schema

    def fiddle(object, schema):
        
        schema.moveField('studySystems', after='biography')
        schema.moveField('publishedPapers', after='studySystems')
		
        schema['classifications'].widget.label = "Choose a category that best describes you"
        schema['id'].widget.description = "Required. Example: abc123 (the part of your default Penn State email address before @psu.edu)"
        schema['image'].widget.description = "You can upload an image up to 200px wide by 250px high (make sure it's at a resolution of 72 px/inch)"

        schema['officeAddress'].widget.label = "Office (room and building)"

        schema['biography'].widget.label = "Your research interests"
        schema['specialties'].widget.description = "Browse to choose one or more areas where you have expertise or research interests. Note: some areas have sub-areas you can select (e.g. cognitive neuroscience is a sub-area of neuroscience)."
        schema['departments'].widget.label = "Your lab affiliation (if applicable)"
        schema['departments'].widget.description = "If your lab has a web presence on the CIDD site, select it from the list provided."
        schema['websites'].widget.label = "A website where people can find out more about you"
        schema['websites'].widget.description = "Example: http://www.example.com/"

        schema['officeCity'].widget.visible={'edit':'invisible','view':'invisible'}
        schema['officeState'].widget.visible={'edit':'invisible','view':'invisible'}
        schema['officePostalCode'].widget.visible={'edit':'invisible','view':'invisible'}
        schema['education'].widget.visible={'edit':'invisible','view':'invisible'}
        schema['committees'].widget.visible={'edit':'invisible','view':'invisible'}
#        schema['departments'].widget.visible={'edit':'invisible','view':'invisible'}
        schema['specialties'].widget.visible={'edit':'invisible','view':'invisible'}

        return schema

