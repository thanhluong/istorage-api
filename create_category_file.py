from file_storage.models import Organ, CategoryFile


all_organs = Organ.objects.all()

for organ in all_organs:
    category_file_name = "Hồ sơ, tài liệu công tác tổng hợp của " + organ.name
    order = 1
    new_category_file = CategoryFile(
        name=category_file_name,
        organ=organ,
        order=order,
        parent=None,
    )
    new_category_file.save()

    category_file_name = "Tài liệu về tổ chức Đoàn thể cơ quan " + organ.name
    order = 1
    new_category_file = CategoryFile(
        name=category_file_name,
        organ=organ,
        order=order,
        parent=None,
    )
    new_category_file.save()

    print("Created 2 category files for " + organ.name)
