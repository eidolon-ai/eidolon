import os
import sys

import click
import dotenv
from click import Option, Context
from click.core import ParameterSource

from eidolon_ai_cli.security import security_providers
from eidolon_ai_cli.terminal2 import EidolonCLI

dotenv.load_dotenv()


def _validate_security_options(ctx: Context, param: Option, value):
    if ctx.get_parameter_source(param.name) == ParameterSource.COMMANDLINE:
        param_name = param.name.split("_")[1]
        security_provider = security_providers[param_name]
        args = security_provider["args"]
        if value is None or len(value) < len(args.keys()):
            env_vars = [os.environ.get(v['env_var']) for k, v in args.items()]
            raise click.BadParameter(f"requires [{', '.join(args.keys())}]. Alternatively, set the {env_vars} environment variables.")
        else:
            for i, (arg_name, arg) in enumerate(args.items()):
                if not value[i]:
                    raise click.BadParameter(f"requires argument {arg_name}. Alternatively, set the {arg['env_var']} environment variable.")
    return value


def add_security_options():
    def _add_security_options(func):
        for provider_name, provider in security_providers.items():
            args = provider["args"]
            env_vars = [os.environ.get(v['env_var']) for k, v in args.items()]
            if len(args.keys()) == 1:
                env_vars = env_vars[0]
            metavars = [k + "=${" + v['env_var'] + "}" for k, v in args.items()]
            func = click.option(f"--security:{provider_name}", f"security_{provider_name}",
                                nargs=len(args.keys()), help=provider["help"], callback=_validate_security_options,
                                is_flag=False, flag_value=env_vars, metavar=metavars)(func)
        return func

    return _add_security_options


@click.command()
@add_security_options()
def main(**kwargs):
    """
    Eidolon CLI: A command line interface for the Eidolon SDK
    """
    # only one of the security providers can be enabled. If more than one then throw a click.BadParameter exception
    security_providers_enabled = [(k[9:], v) for k, v in kwargs.items() if k.startswith("security_") and v]
    if len(security_providers_enabled) == 0:
        provider_instance = None
    else:
        if len(security_providers_enabled) > 1:
            raise click.BadParameter("Only one security provider can be enabled at a time.")
        else:
            security_provider = security_providers_enabled[0]

        values = security_provider[1]
        security_provider = security_providers[security_provider[0]]
        if len(security_provider["args"].keys()) == 1:
            values = [values]

        args = {arg: values[i] for i, arg in enumerate(security_provider["args"].keys())}
        provider_instance = security_provider["impl"](**args)

    app = EidolonCLI(provider_instance)
    sys.exit(app.main())


if __name__ == "__main__":
    main()
