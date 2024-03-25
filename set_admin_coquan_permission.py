from django.contrib.auth.models import Group

from file_storage.models import StorageUser

admin_coquan = Group.objects.all()[0]
all_users = StorageUser.objects.all()

for user in all_users:
    if user.username.startswith("admin_coquan"):
        user.groups.add(admin_coquan)
    user.save()