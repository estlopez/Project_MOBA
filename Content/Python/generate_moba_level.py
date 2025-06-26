import unreal

# === Load the Player Character Blueprint ===
player_bp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/PlayerBlueprints/BP_TopDownCharacter")

if not player_bp:
    unreal.log_warning("❌ Could not load BP_TopDownCharacter.")
    quit()

# === Set Spawn Location ===
spawn_location = unreal.Vector(200, 200, 100)

# === Spawn the player character ===
player_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(player_bp, spawn_location)

if player_actor:
    player_actor.set_actor_label("PlayerCharacter")

    # Set Auto Possess Player to Player 0
    player_actor.set_editor_property("AutoPossessPlayer", unreal.AutoPossessPlayer.PLAYER0)

    unreal.log("✅ Player character spawned and set to Auto Possess Player 0.")
else:
    unreal.log_warning("❌ Failed to spawn player character.")