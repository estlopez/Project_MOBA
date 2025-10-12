import unreal
assets = unreal.EditorAssetLibrary.list_assets("/Game/PlaceHolders", True, False)
for asset in assets:
    unreal.log(asset)