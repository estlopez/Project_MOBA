import unreal

player_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/PlayerBlueprints/BP_TopDownCharacter")
player_marker_class = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/BP_PlayerStartMarker")

player_index = 0

for marker in unreal.EditorLevelLibrary.get_all_level_actors():
    if not marker.is_a(player_marker_class):
        continue

    location = marker.get_actor_location()
    player = unreal.EditorLevelLibrary.spawn_actor_from_class(player_bp, location)
    player.set_actor_label(f"GeneratedPlayer_{player_index}")

    if player.has_property("auto_possess_player"):
        player.set_editor_property("auto_possess_player", unreal.AutoPossessPlayer.PLAYER0)

    unreal.log(f"✅ Player #{player_index} spawned at {location}")
    player_index += 1
