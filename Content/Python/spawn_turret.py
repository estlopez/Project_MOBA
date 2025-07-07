import unreal

# Blueprint asset paths
TURRET_BP_PATH = "/Game/AutoTurretAsset/TurretAssetFiles/Blueprints/BaseTurret_perception.BaseTurret_perception"
TURRET_MARKER_PATH = "/Game/PlaceHolders/BP_TurretSpawnPoint.BP_TurretSpawnPoint"

# Load the turret blueprint class
turret_class = unreal.EditorAssetLibrary.load_blueprint_class(TURRET_BP_PATH)

# Get all actors in the level
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()

# Loop through and find all turret marker actors
for actor in all_actors:
    if actor.get_class().get_name() == "BP_TurretSpawnPoint_C":
        location = actor.get_actor_location()
        rotation = actor.get_actor_rotation()

        # Spawn turret at the marker's position
        spawned_turret = unreal.EditorLevelLibrary.spawn_actor_from_class(turret_class, location, rotation)

        if spawned_turret:
            unreal.log(f"✅ Spawned Turret at {location}")
        else:
            unreal.log_warning(f"⚠️ Failed to spawn turret at {location}")

