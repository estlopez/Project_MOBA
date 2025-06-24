import unreal

# Load Blueprint classes
turret_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/AutoTurretAsset/TurretAssetFiles/Blueprints/BaseTurret_perception")
minion_spawner_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_MinionSpawn")
lane_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Lane")
player_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/PlayerBlueprints/BP_TopDownCharacter")

# Find BP_LevelBuilder in the level
level_builder = None
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if actor.get_name().startswith("BP_LevelBuilder"):
        level_builder = actor
        break

if not level_builder:
    unreal.log_warning("BP_LevelBuilder not found in level.")
    quit()

origin = level_builder.get_actor_location()
lane_spacing = 1000  # Distance between the two lanes (Y-axis)
lane_length = 1500   # Distance from center to turrets/spawners (X-axis)

# === Generate Two Lanes ===
for i in range(2):
    lane_y_offset = (i - 0.5) * lane_spacing  # -500 and +500
    lane_location = origin + unreal.Vector(0, lane_y_offset, 0)
    
    # Spawn Lane
    lane = unreal.EditorLevelLibrary.spawn_actor_from_class(lane_bp, lane_location)
    lane.set_actor_label(f"Lane_{i}")

    # Spawn Minion Spawner (Team 1 - Player's team) on the left
    spawner_location = lane_location + unreal.Vector(-lane_length, 0, 0)
    spawner = unreal.EditorLevelLibrary.spawn_actor_from_class(minion_spawner_bp, spawner_location)
    spawner.set_actor_label(f"MinionSpawner_Team1_Lane{i}")
    if spawner.has_property("TeamID"):
        spawner.set_editor_property("TeamID", 1)

    # Spawn Turret (Team 2 - Enemy) on the right
    turret_location = lane_location + unreal.Vector(lane_length, 0, 0)
    turret = unreal.EditorLevelLibrary.spawn_actor_from_class(turret_bp, turret_location)
    turret.set_actor_label(f"Turret_Team2_Lane{i}")
    if turret.has_property("TeamID"):
        turret.set_editor_property("TeamID", 2)

# === Spawn Player Character (Team 1) slightly left of center
player_location = origin + unreal.Vector(-lane_length * 1.5, 0, 0)
player = unreal.EditorLevelLibrary.spawn_actor_from_class(player_bp, player_location)
player.set_actor_label("TestPlayer")
if player.has_property("TeamID"):
    player.set_editor_property("TeamID", 1)

unreal.log("Two-lane MOBA level generated successfully with correct actors.")
