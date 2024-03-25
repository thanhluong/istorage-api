import json

from file_storage.models import Organ, CategoryFile


all_organs = Organ.objects.all()
categories = json.load(open("category_info_each_eliminated.json"))

for organ in all_organs:
    cnt = 0

    for category_json in categories:
        order = category_json["order"]
        category_file_name = ((order - 1) * "--") + " " + category_json["name"] + " của " + organ.name
        new_category_file = CategoryFile(
            name=category_file_name,
            organ=organ,
            order=order,
            parent=None,
        )
        new_category_file.save()
        cnt += 1

    print("Created {} category files for {}".format(cnt, organ.name))
