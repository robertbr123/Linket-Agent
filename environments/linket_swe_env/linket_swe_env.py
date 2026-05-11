"""Canonical Linket alias for ``environments.hermes_swe_env.hermes_swe_env``."""

from environments.hermes_swe_env.hermes_swe_env import *  # noqa: F401,F403


if __name__ == "__main__":
    from environments.hermes_swe_env.hermes_swe_env import HermesSweEnv

    HermesSweEnv.cli()
