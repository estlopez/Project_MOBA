# PlayerStart_Build.py
import unreal

# ================== CONFIG ==================
# Placeholder (marker) that indicates where to spawn the new player start
PLAYER_MARKER_PATH = "/Game/PlaceHolders/BP_PlayerStartMarker.BP_PlayerStartMarker"

# The actual player start Blueprint to spawn
PLAYER_START_BP_PATH = "/Game/Blueprints/PlayerBlueprints/BP_NewPlayerStartMarker.BP_NewPlayerStartMarker"

SPAWN_TAG = "SpawnedByScript_PlayerStart"

# Delete the old marker once we've spawned the new one?
DELETE_MARKER_AFTER = True
# ============================================


# --- Load the Blueprint classes ---
marker_class = unreal.EditorAssetLibrary.load_blueprint_class(PLAYER_MARKER_PATH)
player_start_class = unreal.EditorAssetLibrary.load_blueprint_class(PLAYER_START_BP_PATH)

if not marker_class:
    unreal.log_error(f"❌ Could not load marker class: {PLAYER_MARKER_PATH}")
if not player_start_class:
    unreal.log_error(f"❌ Could not load player start class: {PLAYER_START_BP_PATH}")

def set_current_level(level_obj):
    """Ensure we spawn in the same level as the source actor."""
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        subsys.set_current_level(level_obj)
    except Exception:
        try:
            unreal.EditorLevelUtils.set_current_level(level_obj)
        except Exception as e:
            unreal.log_warning(f"⚠️ Failed to set current level: {e}")

if marker_class and player_start_class:
    editor = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = editor.get_editor_world()

    # Find all placeholder actors in the loaded level(s)
    markers = unreal.GameplayStatics.get_all_actors_of_class(world, marker_class)
    if not markers:
        unreal.log_warning("⚠️ No BP_PlayerStartMarker actors found in the current world.")
    else:
        markers = sorted(markers, key=lambda a: a.get_full_name())
        spawned_count = 0

        for idx, marker in enumerate(markers):
            loc = marker.get_actor_location()
            rot = marker.get_actor_rotation()

            set_current_level(marker.get_level())

            # Spawn the new Player Start
            player_start = unreal.EditorLevelLibrary.spawn_actor_from_class(player_start_class, loc, rot)
            if not player_start:
                unreal.log_warning(f"⚠️ Failed to spawn PlayerStart at {marker.get_name()}")
                continue

            # Label + tag
            unreal.EditorLevelLibrary.set_actor_label(player_start, f"BP_NewPlayerStart_{idx:02d}", True)
            player_start.tags = list(player_start.tags) + [unreal.Name(SPAWN_TAG)]

            # Delete the marker afterward (optional)
            if DELETE_MARKER_AFTER:
                try:
                    unreal.EditorLevelLibrary.destroy_actor(marker)
                    unreal.log(f"🧹 Deleted placeholder {marker.get_name()}")
                except Exception as e:
                    unreal.log_warning(f"⚠️ Failed to delete placeholder {marker.get_name()}: {e}")

            unreal.log(f"✅ Spawned Player Start at {loc}")
            spawned_count += 1

        unreal.log(f"🎯 Done. Spawned {spawned_count} PlayerStart actors.")
