import unreal
from math import sqrt

# ------------ CONFIG ------------
MARKER_PATH = "/Game/PlaceHolders/BP_TurretSpawnPoint.BP_TurretSpawnPoint"
TURRET_BLUEPRINT_PATH = "/Game/AutoTurretAsset/TurretAssetFiles/Blueprints/BaseTurret_perception.BaseTurret_perception"

# Add this tag to every spawned turret so we can detect duplicates later
SPAWN_TAG = "SpawnedByScript"

# How close (in cm) an existing tagged turret can be before we skip spawning another one
DUPLICATE_RADIUS = 50.0

# Lift the spawn location slightly to help with collision on uneven ground
Z_LIFT = 5.0
# --------------------------------

def v_dist(a: unreal.Vector, b: unreal.Vector) -> float:
    return sqrt((a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2)

# Load classes
marker_class = unreal.EditorAssetLibrary.load_blueprint_class(MARKER_PATH)
turret_class = unreal.EditorAssetLibrary.load_blueprint_class(TURRET_BLUEPRINT_PATH)

if not marker_class:
    unreal.log_error(f"❌ Could not load marker class: {MARKER_PATH}")
if not turret_class:
    unreal.log_error(f"❌ Could not load turret class: {TURRET_BLUEPRINT_PATH}")

if marker_class and turret_class:
    world = unreal.EditorLevelLibrary.get_editor_world()

    # Get all markers via GameplayStatics to match by class (includes child classes)
    markers = unreal.GameplayStatics.get_all_actors_of_class(world, marker_class)

    if not markers:
        unreal.log_warning("⚠️ No BP_TurretSpawnPoint markers found in the current level.")
    else:
        # Gather existing turrets we previously spawned (by tag), to avoid duplicates
        all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
        existing_spawned_turrets = [
            a for a in all_actors
            if SPAWN_TAG in [str(t) for t in a.tags]
        ]

        spawned_count = 0
        for marker in markers:
            loc = marker.get_actor_location()
            rot = marker.get_actor_rotation()

            # Optional small Z lift to reduce spawn collision
            loc = unreal.Vector(loc.x, loc.y, loc.z + Z_LIFT)

            # Skip if a tagged turret already exists at (about) this location
            if any(v_dist(a.get_actor_location(), loc) <= DUPLICATE_RADIUS for a in existing_spawned_turrets):
                unreal.log(f"ℹ️ Skipped duplicate spawn near {loc} (found existing tagged turret).")
                continue

            turret = unreal.EditorLevelLibrary.spawn_actor_from_class(
                turret_class,
                loc,
                rot
            )

            if turret:
                # Add a tag so future runs can detect duplicates
                new_tags = list(turret.tags)
                if SPAWN_TAG not in [str(t) for t in new_tags]:
                    new_tags.append(unreal.Name(SPAWN_TAG))
                    turret.tags = new_tags

                # Give a readable label in the World Outliner
                base_label = "BP_BaseTurret_perception"
                unreal.EditorLevelLibrary.set_actor_label(turret, f"{base_label}_{spawned_count:02d}", True)

                existing_spawned_turrets.append(turret)
                spawned_count += 1
                unreal.log(f"✅ Spawned turret at {loc}")
            else:
                unreal.log_warning(f"⚠️ Failed to spawn turret at marker: {marker.get_name()}")

        unreal.log(f"🎯 Done. Turrets spawned: {spawned_count}")
