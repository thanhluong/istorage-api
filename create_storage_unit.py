from file_storage.models import Warehouse, WarehouseRoom, Shelf, Drawer
from file_storage.models import Organ

all_organs = Organ.objects.all()

for organ in all_organs:
    warehouse = Warehouse(organ=organ, name="Kho " + organ.name)
    warehouse.save()
    warehouse_room = WarehouseRoom(warehouse=warehouse, name="Phòng kho " + organ.name)
    warehouse_room.save()
    shelf = Shelf(warehouse_room=warehouse_room, name="Kệ " + organ.name)
    shelf.save()
    drawer = Drawer(shelf=shelf, name="Hộp " + organ.name)
    drawer.save()
    print('Create storage unit for organ: ', organ.name)