from App.models import BuildingDetails
from App.database import db

def updateBuildingDetails(building_details_id, location_id, num_floors, faculty):
    building = BuildingDetails.query.filter_by(id=building_details_id, location_id=location_id).first()

    if building:
        building.num_floors = num_floors
        building.faculty = faculty
        db.session.commit()
        return True
    return False

def deleteBuildingDetails(building_details_id, location_id):
    building = BuildingDetails.query.filter_by(id=building_details_id, location_id=location_id).first()

    if building:
        db.session.delete(building)
        db.session.commit()
        return True
    return False