from mongoengine import *
from Objects.value import Value

class Device(Document):
	name = StringField(max_length=60, required=True)
	description = StringField(max_length=120, required=True)
	values = ListField(ReferenceField('Value', reverse_delete_rule=NULLIFY))
	location = PointField(auto_index=False, required=True)

	@queryset_manager
	def objects(doc_cls, queryset):
		return queryset.order_by('-created_date')


	def __str__(self):
		#formatedLocation = "{0}, {1}".format(self.location.coordinates[0], self.location.coordinates[1])
		return "{{\"name\": \"{0}\", \"description\": \"{1}\", \"values\": \"{2}\"}}".format(self.name, self.description, len(self.values))