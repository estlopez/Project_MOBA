import unreal

# Load assets
lane_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_Lane")
minion_spawn_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_MinionSpawn")
lane_enum = unreal.load_object(None, "/Game/Blueprints/ENum_LaneSelect.ENum_LaneSelect")
lane_marker_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_LaneBuilder")

# Terrain projection
def get_ground_position(world_location):
    start = world_location + unreal.Vector(0, 0, 1000)
    end = world_location - unreal.Vector(0, 0, 10000)
    result = unreal.SystemLibrary.line_trace_single(
        unreal.EditorLevelLibrary.get_editor_world(),
        start, end,
        unreal.TraceTypeQuery.VISIBILITY, False, [], unreal.DrawDebugTrace.NONE, True)
    return result['Location'] if result['Hit'] else world_location

lane_index = 0

for marker in unreal.EditorLevelLibrary.get_all_level_actors():
    if not marker.is_a(lane_marker_class):
        continue

    origin = marker.get_actor_location()

    # Spawn lane
    lane_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(lane_bp, origin)
    lane_actor.set_actor_label(f"GeneratedLane_{lane_index}")

    # Add spline points
    spline = next((c for c in lane_actor.get_components_by_class(unreal.SplineComponent)), None)
    if spline:
        spline.clear_spline_points()
        spacing = 7000 / 3
        for i in range(4):
            point = origin + unreal.Vector(i * spacing, 0, 0)
            spline.add_spline_point(get_ground_position(point), unreal.SplineCoordinateSpace.WORLD)
        spline.update_spline()

    # Spawn MinionSpawner
    start_location = spline.get_location_at_spline_point(0, unreal.SplineCoordinateSpace.WORLD)
    spawner = unreal.EditorLevelLibrary.spawn_actor_from_class(minion_spawn_bp, start_location)
    spawner.set_actor_label(f"GeneratedMinionSpawner_{lane_index}")

    # Assign lane_target and enum
    if spawner.has_property("lane_target"):
        spawner.set_editor_property("lane_target", lane_actor)
    if spawner.has_property("lane_selectors"):
        enum_name = f"Lane{min(lane_index + 1, 3)}"  # Lane1, Lane2, Lane3 only
        value = unreal.get_enum_value_by_name(lane_enum, enum_name)
        spawner.set_editor_property("lane_selectors", value)

    unreal.log(f"✅ Lane + Spawner #{lane_index} placed at {origin}")
    lane_index += 1
