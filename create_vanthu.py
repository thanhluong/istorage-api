from file_storage.models import Organ, OrganDepartment, StorageUser

all_organs = Organ.objects.all()

for organ in all_organs:
    full_name = "Văn Thư " + organ.name
    username = "vanthu_coquan_" + organ.code[5:9] + organ.code[10].lower()
    email = username + "@quangngai.gov.vn"
    new_usr = StorageUser(
        username=username,
        full_name=full_name,
        email=email,
        department=OrganDepartment.objects.get(id=organ.id),
        is_staff=False,
    )
    new_usr.menu_permission = "1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25-26-27-28-29-30-31-32-33-34-35-36-37-38-39-40-41-42-43-44-45-46-47-48-49-50-51-52-53-54-55-56-57-58-59-60-61-62-63-64-65-66-67-68-69-70-71-72-73-74-75-76-201-202-203-204"
    new_usr.set_password("vanthu11235")
    new_usr.save()
    print("Added new user: ", new_usr.username)