import unreal

# Load Blueprint classes
lane_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Lane")
minion_spawn_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_MinionSpawn")
turret_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/AutoTurretAsset/TurretAssetFiles/Blueprints/BaseTurret_perception")

# Find BP_LevelBuilder
level_builder = None
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if actor.get_name().startswith("BP_LevelBuilder"):
        level_builder = actor
        break

if not level_builder:
    unreal.log_warning("BP_LevelBuilder not found in level.")
    quit()

origin = level_builder.get_actor_location()

# === 1. Spawn the Lane Actor ===
lane_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(lane_bp, origin)
lane_actor.set_actor_label("Generated_Lane")

# Get the spline component from the lane
spline_comp = None
for comp in lane_actor.get_components_by_class(unreal.SplineComponent):
    spline_comp = comp
    break

if not spline_comp:
    unreal.log_warning("No SplineComponent found on BP_Lane.")
    quit()

# === 2. Add Spline Points ===
spline_comp.clear_spline_points()

total_length = 7000
num_points = 4
spacing = total_length / (num_points - 1)

for i in range(num_points):
    point_location = origin + unreal.Vector(i * spacing, 0, 0)
    spline_comp.add_spline_point(point_location, unreal.SplineCoordinateSpace.WORLD)

spline_comp.update_spline()

# === 3. Spawn Minion Spawner at first spline point ===
start_location = spline_comp.get_location_at_spline_point(0, unreal.SplineCoordinateSpace.WORLD)
minion_spawn = unreal.EditorLevelLibrary.spawn_actor_from_class(minion_spawn_bp, start_location)
minion_spawn.set_actor_label("LaneSpawner")

# Set Lane reference on minion spawner
if minion_spawn.has_property("Lane"):
    minion_spawn.set_editor_property("Lane", lane_actor)
    unreal.log("Minion spawner successfully linked to lane.")
else:
    unreal.log_warning("Minion spawner does not have a 'Lane' property.")

# === 4. Spawn Turret at BP_LevelBuilder location for now ===
turret_location = origin
turret = unreal.EditorLevelLibrary.spawn_actor_from_class(turret_bp, turret_location)

if turret:
    turret.set_actor_label("LaneTurret")
    
    if turret.has_property("TeamID"):
        turret.set_editor_property("TeamID", 2)
    if turret.has_property("FireInterval_BetweenShots"):
        turret.set_editor_property("FireInterval_BetweenShots", 1.5)
    if turret.has_property("LookAtSpeed"):
        turret.set_editor_property("LookAtSpeed", 5.0)
    if turret.has_property("LaneTarget"):
        turret.set_editor_property("LaneTarget", lane_actor)

    unreal.log("Turret spawned and configured.")
else:
    unreal.log_warning("Turret could not be spawned. Check Blueprint path and class.")
