


from sdk.eidolon_ai_sdk.builtins.logic_units.toolhouse_logic_unit import Toolhouse, tool_build


def test_tool_registration():
    config = Toolhouse()
    tool_build(config)
    
