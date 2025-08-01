import unreal

# Path to the player character blueprint
player_bp_path = "/Game/Blueprints/PlayerBlueprints/BP_TopDownCharacter.BP_TopDownCharacter"

# Load the Blueprint
player_bp = unreal.EditorAssetLibrary.load_blueprint_class(player_bp_path)

if not player_bp:
    unreal.log_error(f"❌ Could not load blueprint: {player_bp_path}")
else:
    # Get the Class Default Object (CDO)
    cdo = unreal.get_default_object(player_bp)

    # Set Auto Possess Player to Player 0
    cdo.set_editor_property("auto_possess_player", unreal.AutoPossessPlayer.PLAYER0)
    unreal.log("✅ Set Auto Possess Player to Player 0 for BP_TopDownCharacter.")
