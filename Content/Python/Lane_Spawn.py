# Lane_Build.py
import unreal

# ================== CONFIG ==================
LANE_MARKER_PATH = "/Game/PlaceHolders/BP_LaneBuilder.BP_LaneBuilder"
LANE_BP_PATH     = "/Game/Blueprints/BP_Lane.BP_Lane"

SPAWN_TAG = "SpawnedByScript_Lane"
DELETE_MARKER_AFTER = True
# ============================================

lane_marker_class = unreal.EditorAssetLibrary.load_blueprint_class(LANE_MARKER_PATH)
lane_class        = unreal.EditorAssetLibrary.load_blueprint_class(LANE_BP_PATH)

if not lane_marker_class:
    unreal.log_error(f"❌ Could not load marker class: {LANE_MARKER_PATH}")
if not lane_class:
    unreal.log_error(f"❌ Could not load lane class: {LANE_BP_PATH}")

def set_current_level(level_obj):
    ok = False
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        subsys.set_current_level(level_obj)
        ok = True
    except Exception:
        try:
            unreal.EditorLevelUtils.set_current_level(level_obj)
            ok = True
        except Exception as e:
            unreal.log_warning(f"⚠️ Failed to set current level: {e}")
    return ok

if lane_marker_class and lane_class:
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    markers = unreal.GameplayStatics.get_all_actors_of_class(world, lane_marker_class)

    if not markers:
        unreal.log_warning("⚠️ No BP_LaneBuilder markers found.")
    else:
        markers = sorted(markers, key=lambda a: a.get_full_name())
        count = 0
        for idx, m in enumerate(markers):
            loc = m.get_actor_location()
            rot = m.get_actor_rotation()

            # spawn into the marker's level
            set_current_level(m.get_level())

            lane = unreal.EditorLevelLibrary.spawn_actor_from_class(lane_class, loc, rot)
            if not lane:
                unreal.log_warning(f"⚠️ Failed to spawn BP_Lane at marker {m.get_name()}")
                continue

            unreal.EditorLevelLibrary.set_actor_label(lane, f"BP_Lane_{idx:02d}", True)
            lane.tags = list(lane.tags) + [unreal.Name(SPAWN_TAG)]

            if DELETE_MARKER_AFTER:
                try:
                    unreal.EditorLevelLibrary.destroy_actor(m)
                    unreal.log(f"🧹 Deleted marker {m.get_name()}")
                except Exception as e:
                    unreal.log_warning(f"⚠️ Failed to delete marker {m.get_name()}: {e}")

            unreal.log(f"✅ Spawned Lane at {loc}")
            count += 1

        unreal.log(f"🎯 Done. Lanes spawned: {count}")

