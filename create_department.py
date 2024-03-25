from file_storage.models import Organ, OrganDepartment

all_organs = Organ.objects.all()

for organ in all_organs:
    department_name = "Văn phòng " + organ.name
    new_department = OrganDepartment(
        name=department_name,
        organ=organ,
        code="VPVPVP"
    )
    new_department.save()
    print("Created " + department_name)
