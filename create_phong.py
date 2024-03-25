from file_storage.models import Organ, Phong


all_organs = Organ.objects.all()

for organ in all_organs:
    phong_name = "Phông " + organ.name
    new_phong = Phong(
        fond_name=phong_name,
        organ=organ,
        identifier="PSNV"
    )
    new_phong.save()

    print("Created " + phong_name)
