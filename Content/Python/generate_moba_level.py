import unreal

# Load Blueprint classes
turret_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/AutoTurretAsset/TurretAssetFiles/Blueprints/BaseTurret_perception")
minion_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Minion")
lane_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Lane")
player_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/PlayerBlueprints/BP_TopDownCharacter")

# Get the world and locate the LevelBuilder actor
world = unreal.EditorLevelLibrary.get_editor_world()
level_builder = None
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if actor.get_name().startswith("BP_LevelBuilder"):
        level_builder = actor
        break

if not level_builder:
    unreal.log_warning("BP_LevelBuilder not found in level.")
    quit()

origin = level_builder.get_actor_location()
spawn_offset = 800  # Distance between spawns

# === Spawn Lanes ===
for i in range(3):
    lane_location = origin + unreal.Vector(0, i * spawn_offset, 0)
    lane = unreal.EditorLevelLibrary.spawn_actor_from_class(lane_bp, lane_location)
    lane.set_actor_label(f"Lane_{i}")

# === Spawn Turrets for Each Lane (Team 1 and Team 2) ===
for i in range(3):  # 3 lanes
    for team in [1, 2]:
        offset = spawn_offset * (1 if team == 1 else -1)
        turret_location = origin + unreal.Vector(offset, i * spawn_offset, 0)
        turret = unreal.EditorLevelLibrary.spawn_actor_from_class(turret_bp, turret_location)
        turret.set_actor_label(f"Turret_Team{team}_Lane{i}")
        if turret.has_property("TeamID"):
            turret.set_editor_property("TeamID", team)

# === Spawn Minions at Each Lane Start ===
for i in range(3):
    for team in [1, 2]:
        offset = spawn_offset * (1 if team == 1 else -1)
        minion_location = origin + unreal.Vector(offset * 1.5, i * spawn_offset, 0)
        minion = unreal.EditorLevelLibrary.spawn_actor_from_class(minion_bp, minion_location)
        minion.set_actor_label(f"Minion_Team{team}_Lane{i}")
        if minion.has_property("TeamID"):
            minion.set_editor_property("TeamID", team)

# === Spawn Player (Test) ===
player_location = origin + unreal.Vector(0, -spawn_offset * 2, 0)
player = unreal.EditorLevelLibrary.spawn_actor_from_class(player_bp, player_location)
player.set_actor_label("TestPlayer")

unreal.log("MOBA Level Generation Complete.")
