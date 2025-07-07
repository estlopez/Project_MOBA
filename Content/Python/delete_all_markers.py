import unreal

# Names of the placeholder Blueprint classes to delete
DUMMY_MARKER_CLASS_NAMES = [
    "BP_LaneBuilder_C",
    "BP_TurretSpawnPoint_C",
    "BP_PlayerStartMarker_C"
]

# Get all actors in the level
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()

deleted_count = 0

for actor in all_actors:
    if actor.get_class().get_name() in DUMMY_MARKER_CLASS_NAMES:
        unreal.EditorLevelLibrary.destroy_actor(actor)
        deleted_count += 1
        unreal.log(f"🗑️ Deleted dummy marker: {actor.get_name()}")

unreal.log(f"✅ Cleanup complete. Total dummy markers deleted: {deleted_count}")
