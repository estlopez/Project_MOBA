import unreal

# Use the modern Editor Actor Subsystem
actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

deleted_count = 0

# Loop through all actors in the level
for actor in actor_subsystem.get_all_level_actors():
    # Match by class name to find all BP_TurretSpawnPoint instances
    if actor.get_class().get_name().startswith("BP_TurretSpawnPoint"):
        unreal.EditorLevelLibrary.destroy_actor(actor)
        deleted_count += 1

unreal.log(f"🗑️ Deleted {deleted_count} BP_TurretSpawnPoint actor(s) from the level.")
