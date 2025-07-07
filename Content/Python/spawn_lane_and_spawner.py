import unreal

# Asset paths
lane_builder_path = "/Game/PlaceHolders/BP_LaneBuilder.BP_LaneBuilder"
lane_bp_path = "/Game/Blueprints/BP_Lane.BP_Lane"
minion_spawn_path = "/Game/Blueprints/BP_MinionSpawn.BP_MinionSpawn"

# Load classes
lane_class = unreal.EditorAssetLibrary.load_blueprint_class(lane_bp_path)
minion_spawn_class = unreal.EditorAssetLibrary.load_blueprint_class(minion_spawn_path)

# Get all actors in level
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()

for actor in all_actors:
    if actor.get_class().get_name() == "BP_LaneBuilder_C":
        location = actor.get_actor_location()
        rotation = actor.get_actor_rotation()

        # Spawn BP_Lane
        lane_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(lane_class, location, rotation)
        unreal.log(f"✅ Spawned Lane at {location}")

        # Spawn BP_MinionSpawn
        minion_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(minion_spawn_class, location, rotation)
        unreal.log(f"✅ Spawned Minion Spawn at {location}")

        # Set lane_target reference
        if minion_actor and lane_actor:
            try:
                minion_actor.set_editor_property("lane_target", lane_actor)
            except Exception as e:
                unreal.log_warning(f"⚠️ Could not set 'lane_target': {e}")

            # Optional: Set lane_selectors enum to Lane1 (adjust if needed)
            try:
                enum_asset = unreal.load_object(None, "/Game/Blueprints/ENum_LaneSelect.ENum_LaneSelect")
                if enum_asset:
                    enum_value = unreal.get_enum_value_by_name(enum_asset, "Lane1")
                    minion_actor.set_editor_property("lane_selectors", enum_value)
            except Exception as e:
                unreal.log_warning(f"⚠️ Could not set 'lane_selectors': {e}")
