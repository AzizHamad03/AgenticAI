"""Run HRPipelineFlow using candidate and job-position IDs."""

import argparse
import json
import os

import django


def setup_django():

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "config.settings",
    )

    django.setup()


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Run the HR pipeline from database data"
        )
    )

    parser.add_argument(
        "candidate_id",
        type=int,
    )

    parser.add_argument(
        "job_position_id",
        type=int,
    )

    args = parser.parse_args()

    # Django must be initialized before
    # importing models / flow.
    setup_django()

    from core.flows.hr_pipeline.flow import (
        HRPipelineError,
        HRPipelineFlow,
    )

    try:

        result = HRPipelineFlow().kickoff(
            candidate_id=args.candidate_id,
            job_position_id=args.job_position_id,
        )

    except HRPipelineError as exc:

        print(
            f"Pipeline error: {exc}"
        )

        raise SystemExit(1)

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )


if __name__ == "__main__":
    main()