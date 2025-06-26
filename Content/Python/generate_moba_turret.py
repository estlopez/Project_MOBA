import unreal

# Load the correct Turret Blueprint class
turret_bp = unreal.EditorAssetLibrary.load_blueprint_class(
    "/Game/AutoTurretAsset/TurretAssetFiles/Blueprints/BaseTurret_perception"
)

if not turret_bp:
    unreal.log_warning("Could not load BaseTurret_perception Blueprint class.")
    quit()

# Find the BP_LevelBuilder actor
level_builder = None
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if actor.get_name().startswith("BP_LevelBuilder"):
        level_builder = actor
        break

if not level_builder:
    unreal.log_warning("BP_LevelBuilder not found in level.")
    quit()

# Get the spawn location from LevelBuilder
spawn_location = level_builder.get_actor_location()

# Spawn the turret
turret = unreal.EditorLevelLibrary.spawn_actor_from_class(turret_bp, spawn_location)

if turret:
    turret.set_actor_label("Test_BaseTurret")
    unreal.log("✅ BaseTurret_perception successfully spawned at LevelBuilder location.")
else:
    unreal.log_warning("❌ Failed to spawn BaseTurret_perception.")
