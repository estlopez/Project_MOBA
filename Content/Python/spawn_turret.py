import unreal

turret_bp = unreal.EditorAssetLibrary.load_blueprint_class(
    "/Game/AutoTurretAsset/TurretAssetFiles/Blueprints/BaseTurret_perception")
team_enum = unreal.load_object(None, "/Game/Blueprints/ENum_TeamID.ENum_TeamID")
turret_marker_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_TurretSpawnPoint")

turret_index = 0

for marker in unreal.EditorLevelLibrary.get_all_level_actors():
    if not marker.is_a(turret_marker_class):
        continue

    location = marker.get_actor_location()
    turret = unreal.EditorLevelLibrary.spawn_actor_from_class(turret_bp, location)
    turret.set_actor_label(f"GeneratedTurret_{turret_index}")

    if turret.has_property("TeamID"):
        turret.set_editor_property("TeamID", unreal.get_enum_value_by_name(team_enum, "Team2"))
    if turret.has_property("FireInterval_BetweenShots"):
        turret.set_editor_property("FireInterval_BetweenShots", 1.0)
    if turret.has_property("LookAtSpeed"):
        turret.set_editor_property("LookAtSpeed", 5.0)

    unreal.log(f"✅ Turret #{turret_index} placed at {location}")
    turret_index += 1
