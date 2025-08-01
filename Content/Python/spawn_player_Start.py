import unreal

# Paths to your Blueprint assets
placeholder_marker_path = "/Game/PlaceHolders/BP_PlayerStartMarker.BP_PlayerStartMarker"
player_start_bp_path = "/Game/Blueprints/BP_NewPlayerStartMarker.BP_NewPlayerStartMarker"

# Load the Blueprint classes
placeholder_class = unreal.EditorAssetLibrary.load_blueprint_class(placeholder_marker_path)
player_start_class = unreal.EditorAssetLibrary.load_blueprint_class(player_start_bp_path)

# Validate asset loading
if not placeholder_class:
    unreal.log_error(f"❌ Could not load placeholder marker class from: {placeholder_marker_path}")
if not player_start_class:
    unreal.log_error(f"❌ Could not load new player start class from: {player_start_bp_path}")

# Proceed only if both classes are loaded
if placeholder_class and player_start_class:
    # Get the current level world
    editor_world = unreal.EditorLevelLibrary.get_editor_world()

    # Find the first placeholder marker in the level
    placeholder_actors = unreal.GameplayStatics.get_all_actors_of_class(editor_world, placeholder_class)

    if not placeholder_actors:
        unreal.log_warning("⚠️ No BP_PlayerStartMarker actors found in the level.")
    else:
        placeholder_actor = placeholder_actors[0]
        location = placeholder_actor.get_actor_location()
        rotation = placeholder_actor.get_actor_rotation()

        # Spawn the actual player start actor at the same transform
        spawned_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(player_start_class, location, rotation)
        if spawned_actor:
            unreal.log(f"✅ Spawned BP_NewPlayerStartMarker at {location}")
        else:
            unreal.log_error("❌ Failed to spawn BP_NewPlayerStartMarker.")
