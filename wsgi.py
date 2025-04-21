import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, BuildingDetails, Location, Room
from App.main import create_app
from App.controllers import *

#added
from flask_googlemaps import GoogleMaps

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


#added
app.config['GOOGLEMAPS_KEY'] = "8JZ7i18MjFuM35dJHq70n3Hx4"
GoogleMaps(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

'''
Admin Commands
'''
admin = AppGroup('admin', help='Admin commands') 

@admin.command("login", help="Log in admin user")
@click.argument("username", default="bob")
@click.argument("password", default="bobpass")
def login_admin(username, password):
    if login(username, password):
        print(f'{username} logged in successfully')
    else:
        print(f'Error: Admin user {username} already logged in or does not exists.')

@admin.command("logout", help="Log out admin user")
def logout_admin():
    if logout():
        print("Admin logged out successfully")
        
@admin.command("location", help= "Create location")
@click.argument("admin_id", default="1")
@click.argument("name", default="tcb3")
@click.argument("latitude", default="10.3")
@click.argument("longitude", default="40.4")
@click.argument("type", default="None")
@click.argument("image", default="None")
@click.argument("description", default="None")
def create_location(admin_id, name, latitude, longitude, type, image, description):
    if createLocation(admin_id, name, latitude, longitude, type, image, description):
        print(f'{name} location was created successfully with latitude of {latitude} and longitude of {longitude}')
    else:
        print(f'Error: {name} location already exists with latitude of {latitude} and longitude of {longitude}')


@admin.command("updateloc", help= "Update location")
@click.argument("location_id", default="1")
@click.argument("name", default="tcb3")
@click.argument("latitude", default="12.3")
@click.argument("longitude", default="32.4")
@click.argument("type", default="None")
@click.argument("image", default="None")
@click.argument("description", default="None")
def update_location(location_id, name, latitude, longitude, type, image, description):
    if updateLocation(location_id, name, latitude, longitude, type, image, description):
        print(f'{name} location was successfully updated to latitude of {latitude} and longitude of {longitude}')
    else:
        print(f'Error: {name} location already exists with latitude of {latitude} and longitude of {longitude}')

@admin.command("deleteloc", help= "Delete location")
@click.argument("location_id", default="1")
def delete_location(location_id):
    if deleteLocation(location_id):
        print(f'Location {location_id} successfully deleted')
    else:
        print(f'Location {location_id} already deleted')

@admin.command("listloc", help= "List location")
def list_locations():
    locations = Location.query.all()
    if locations:
        for loc in locations:
            print(f"ID: {loc.id}, Name: {loc.name}, Latitude: {loc.latitude}, Longitude: {loc.longitude}")
    else:
        print("No locations found.")

app.cli.add_command(admin)


@admin.command("building", help="Create building")
@click.argument("location_id", default="1")
@click.argument("num_floors", default="3")
@click.argument("faculty", default="FST")
def create_building(location_id, num_floors, faculty):
    if createBuildingDetails(location_id, num_floors, faculty):
        print(f'Building located in {location_id} was successfully created in faculty {faculty}')
    else:
        print(f'Building already exists')

@admin.command("update-building", help= "Update building")
@click.argument("building_id", default= "1")
@click.argument("location_id", default= "1")
@click.argument("num_floors", default="4")
@click.argument("faculty", default="Eng")
def update_building(building_id, location_id, num_floors, faculty):
    if updateBuildingDetails(building_id, location_id, num_floors, faculty):
        print(f'Building updated to location id: {location_id} and faculty: {faculty}')
    else:
        print(f'Building already updated/does not exists')


@admin.command("delete-building", help= "Delete building")
@click.argument("building_id", default="1")
@click.argument("location_id", default="1")
def delete_building(building_id, location_id):
    if deleteBuildingDetails(building_id, location_id):
        print(f'Building {building_id} successfully deleted')
    else:
        print(f'Building {building_id} already deleted')

@admin.command("list-buildings", help= "List building")
def list_buildings():
    buildings = BuildingDetails.query.all()
    if buildings:
        for building in buildings:
            print(f"ID: {building.id}, Location ID: {building.location_id}, Floors: {building.num_floors}, Faculty: {building.faculty}")
    else:
        print("No buildings found.")

@admin.command("create-room", help = "Create room")
@click.argument("building_id", default="1")
@click.argument("admin_id", default="1")
@click.argument("floor", default="1")
@click.argument("name", default="room101")
@click.argument("latitude", default="12.3")
@click.argument("longitude", default="32.4")
@click.argument("type", default="None")
@click.argument("image", default="None")
def create_room(building_id, admin_id, floor, name, latitude, longitude, type, image):
    if createRoom(building_id, admin_id, floor, name, latitude, longitude, type, image):
        print(f'Room {name} in building: {building_id} was successfully created on floor {floor}')
    else:
        print(f'Room already exists')

@admin.command("update-room", help = "Update room")
@click.argument("room_id", default="1")
@click.argument("building_id", default="1")
@click.argument("admin_id", default="1")
@click.argument("floor", default="3")
@click.argument("name", default="room401")
@click.argument("latitude", default="32.3")
@click.argument("longitude", default="12.4")
@click.argument("type", default="None")
@click.argument("image", default="None")
def update_room(room_id, building_id, admin_id, floor, name, latitude, longitude, type, image):
    if updateRoom(room_id, building_id, admin_id, floor, name, latitude, longitude, type, image):
        print(f'Room {name} updated to building: {building_id} was successfully created on floor {floor}')
    else:
         print(f'Room with id {room_id} and building_id {building_id} does not exist')



@admin.command("delete-room", help= "Delete room")
@click.argument("room_id", default="1")
@click.argument("building_id", default="1")
def delete_room(room_id, building_id):
    if deleteRoom(room_id, building_id):
        print(f'Room {room_id} successfully deleted')
    else:
        print(f'Room {room_id} already deleted/does not exists')

@admin.command("list-rooms", help= "List rooms")
def list_rooms():
    rooms = Room.query.all()
    if rooms:
        for room in rooms:
            print(f"ID: {room.id}, Building ID: {room.building_id}, Floor: {room.floor}, Name: {room.name}")
    else:
        print("No rooms found.")


app.cli.add_command(admin)



'''
Building Details Commands
# '''
building = AppGroup('building', help='building commands') 
@building.command("update-building", help= "Update building")
@click.argument("building_details_id", default= "1")
@click.argument("location_id", default= "1")
@click.argument("num_floors", default="3")
@click.argument("faculty", default="Eng")
def update_building(building_details_id, location_id, num_floors, faculty):
    if updateBuildingDetails(building_details_id, location_id, num_floors, faculty):
        print(f'Building updated to location id: {location_id} and faculty: {faculty}')
    else:
        print(f'Building already exists')

@building.command("delete-building", help= "Delete building")
@click.argument("building_id", default="1")
@click.argument("location_id", default="1")
def delete_building(building_id, location_id):
    if deleteBuildingDetails(building_id, location_id):
        print(f'Building {building_id} successfully deleted')
    else:
        print(f'Building {building_id} already deleted')

app.cli.add_command(building)


'''
Location Commands
'''
location= AppGroup('location', help='Location commands') 

@location.command("get-location", help= "Get location")
@click.argument("location_id", default="1")
def get_location(location_id):
    return getLocation(location_id)

@location.command("update-location", help= "Update location")
@click.argument("location_id", default="1")
@click.argument("name", default="tcb3")
@click.argument("latitude", default="12.3")
@click.argument("longitude", default="32.4")
@click.argument("type", default="None")
@click.argument("image", default="None")
def update_location(location_id, name, latitude, longitude, type, image):
    if updateLocationDetails(location_id, name, latitude, longitude, type, image):
        print(f'{name} location was successfully updated to latitude of {latitude} and longitude of {longitude}')
    else:
        print(f'Error: {name} location already exists with latitude of {latitude} and longitude of {longitude}')

@location.command("delete-location", help= "Delete location")
@click.argument("location_id", default="1")
def delete_location(location_id):
    if deleteLocation(location_id):
        print(f'Location {location_id} successfully deleted')
    else:
        print(f'Location {location_id} already deleted')


app.cli.add_command(location)


'''
Room Commands
'''
room = AppGroup('room', help='Admin commands') 

@room.command("update-room", help = "Update room")
@click.argument("room_id", default="1")
@click.argument("building_id", default="1")
@click.argument("floor", default="3")
@click.argument("name", default="room401")
@click.argument("type", default="None")
def update_room(room_id, building_id, name, floor, type):
    if updateRoomDetails(room_id, building_id, name, floor, type):
        print(f'Room {name} updated to building: {building_id} was successfully created on floor {floor}')
    else:
         print(f'Room with id {room_id} and building_id {building_id} does not exist')


@room.command("delete-room", help= "Delete room")
@click.argument("room_id", default="1")
@click.argument("building_id", default="1")
def delete_room(room_id, building_id):
    if deleteRoom(room_id, building_id):
        print(f'Room {room_id} successfully deleted')
    else:
        print(f'Room {room_id} already deleted/does not exists')

app.cli.add_command(room)


if __name__ == "__main__":
    app.run(debug=True)
