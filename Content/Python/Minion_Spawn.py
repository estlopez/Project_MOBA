# MinionSpawn_Build_Robust.py
import unreal

# ================== CONFIG ==================
SOURCE_MODE = "LANES"  # "LANES" or "MARKERS"

LANE_BP_PATH          = "/Game/Blueprints/BP_Lane.BP_Lane"
LANE_MARKER_PATH      = "/Game/PlaceHolders/BP_LaneBuilder.BP_LaneBuilder"
MINION_SPAWN_BP_PATH  = "/Game/Blueprints/BP_MinionSpawn.BP_MinionSpawn"

SPAWN_TAG = "SpawnedByScript_Spawner"
CYCLE_LANE_ENUM_IF_UNKNOWN = True

# If SOURCE_MODE == "MARKERS"
DELETE_MARKER_AFTER = False
# ============================================

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

def get_lane_enum_from_lane(lane_actor, default_idx):
    try:
        val = lane_actor.get_editor_property("LaneNumber")
        if isinstance(val, int):
            return val
        return int(val)
    except Exception:
        return default_idx

def find_lanes_robust(world, lane_class):
    """
    Try by class first; if none found, fall back to scanning all actors and matching:
    - class name contains 'BP_Lane'
    - OR has a component named 'PathSpline'
    Returns list[Actor].
    """
    lanes = []
    if lane_class:
        lanes = unreal.GameplayStatics.get_all_actors_of_class(world, lane_class)

    if lanes:
        return lanes

    unreal.log_warning("⚠️ No lanes found by class. Falling back to name/component scan…")
    all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for a in all_actors:
        try:
            cls_name = a.get_class().get_name()  # e.g., 'BP_Lane_C'
            if "BP_Lane" in cls_name:
                lanes.append(a)
                continue

            # component-hint fallback
            comps = a.get_components_by_class(unreal.ActorComponent)
            for c in comps:
                # PathSpline is typically a USplineComponent named 'PathSpline'
                n = c.get_name()
                if n == "PathSpline":
                    lanes.append(a)
                    break
        except Exception:
            pass

    return lanes

# Load assets
lane_class    = unreal.EditorAssetLibrary.load_blueprint_class(LANE_BP_PATH)
marker_class  = unreal.EditorAssetLibrary.load_blueprint_class(LANE_MARKER_PATH)
spawner_class = unreal.EditorAssetLibrary.load_blueprint_class(MINION_SPAWN_BP_PATH)

if not spawner_class:
    unreal.log_error(f"❌ Could not load spawner class: {MINION_SPAWN_BP_PATH}")

if SOURCE_MODE == "LANES" and not lane_class:
    unreal.log_warning(f"⚠️ Could not load lane class: {LANE_BP_PATH} — will try robust fallback scan.")
if SOURCE_MODE == "MARKERS" and not marker_class:
    unreal.log_error(f"❌ Could not load marker class: {LANE_MARKER_PATH}")

editor = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
world = editor.get_editor_world()

if SOURCE_MODE == "LANES":
    sources = find_lanes_robust(world, lane_class)
else:
    sources = unreal.GameplayStatics.get_all_actors_of_class(world, marker_class) if marker_class else []

if not sources:
    unreal.log_warning(f"⚠️ No source actors found for mode '{SOURCE_MODE}'. Ensure lanes/markers are loaded.")
else:
    # Deterministic order
    sources = sorted(sources, key=lambda a: a.get_full_name())
    made = 0
    for idx, src in enumerate(sources):
        loc = src.get_actor_location()
        rot = src.get_actor_rotation()

        set_current_level(src.get_level())

        spawner = unreal.EditorLevelLibrary.spawn_actor_from_class(spawner_class, loc, rot)
        if not spawner:
            unreal.log_warning(f"⚠️ Failed to spawn BP_MinionSpawn at {src.get_name()}")
            continue

        unreal.EditorLevelLibrary.set_actor_label(spawner, f"BP_MinionSpawn_{idx:02d}", True)
        spawner.tags = list(spawner.tags) + [unreal.Name(SPAWN_TAG)]

        if SOURCE_MODE == "LANES":
            lane = src
            # Bind lane_target
            try:
                spawner.set_editor_property("lane_target", lane)
            except Exception as e:
                unreal.log_warning(f"⚠️ Could not set 'lane_target' on {spawner.get_name()}: {e}")

            # Decide lane_selectors
            fallback = (idx % 3) if CYCLE_LANE_ENUM_IF_UNKNOWN else 0
            lane_enum_value = get_lane_enum_from_lane(lane, fallback)
            try:
                spawner.set_editor_property("lane_selectors", lane_enum_value)
            except Exception as e:
                unreal.log_warning(f"⚠️ Could not set 'lane_selectors' on {spawner.get_name()}: {e}")

        else:  # MARKERS
            # Find nearest lane and bind (optional but recommended)
            try:
                lanes_for_bind = find_lanes_robust(world, lane_class)
                nearest = None
                best_d2 = 1e18
                for l in lanes_for_bind:
                    d2 = (l.get_actor_location() - loc).size_squared()
                    if d2 < best_d2:
                        best_d2, nearest = d2, l
                if nearest:
                    spawner.set_editor_property("lane_target", nearest)
                    fallback = (idx % 3) if CYCLE_LANE_ENUM_IF_UNKNOWN else 0
                    lane_enum_value = get_lane_enum_from_lane(nearest, fallback)
                    spawner.set_editor_property("lane_selectors", lane_enum_value)
            except Exception as e:
                unreal.log_warning(f"⚠️ Could not auto-bind nearest lane/enum: {e}")

            if DELETE_MARKER_AFTER:
                try:
                    unreal.EditorLevelLibrary.destroy_actor(src)
                    unreal.log(f"🧹 Deleted marker {src.get_name()}")
                except Exception as e:
                    unreal.log_warning(f"⚠️ Failed to delete marker {src.get_name()}: {e}")

        lvl = src.get_level().get_path_name() if src.get_level() else "UnknownLevel"
        unreal.log(f"✅ Spawned MinionSpawner at {loc} in [{lvl}] (mode={SOURCE_MODE})")
        made += 1

    unreal.log(f"🎯 Done. Minion Spawners spawned: {made} (mode={SOURCE_MODE})")
