"""
This module offers a command-line interface (CLI) tool for seamless interaction with the 
instabuildhub application. It empowers users to leverage Google's models and configure various 
parameters essential for generating, enhancing, or engaging with projects.

Key Features:
Initialize environment variables required for OpenAI operations.
Empower users to define parameters such as:
Project directory
Model selection (defaults to palm API)
Temperature settings
Step configurations
Code enhancement mode
Lite mode for resource-efficient operations
Azure endpoint for Azure OpenAI services
Utilization of project-specific preprompts or default ones
Logging verbosity level
Engage with AI, databases, and archival processes according to user-specified parameters.
Additional Information:

Make sure the .env file contains the GOOGLE_API_KEY or provide it in the current working directory.
The default project directory is established at projects/example.
When using Azure services, specify the Azure endpoint for the OpenAI service.
"""

import logging
import os
from pathlib import Path
# changing the openai importation
import openai

import typer
from dotenv import load_dotenv

from instabuildhub.data.file_repository import FileRepository, FileRepositories, archive
from instabuildhub.core.ai import AI
from instabuildhub.core.steps import STEPS, Config as StepsConfig
from instabuildhub.cli.collect import collect_learnings
from instabuildhub.cli.learning import check_collection_consent
from instabuildhub.data.code_vector_repository import CodeVectorRepository

app = typer.Typer()  # creates a CLI app


def load_env_if_needed():
    if os.getenv("GOOGLE_API_KEY") is None:
        load_dotenv()
    if os.getenv("GOOGLE_API_KEY") is None:
        # if there is no .env file, try to load from the current working directory
        load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
        # needs modification-----> api
    openai.api_key = os.getenv("GOOGLE_API_KEY")


def load_prompt(dbs: FileRepositories):
    if dbs.input.get("prompt"):
        return dbs.input.get("prompt")

    dbs.input["prompt"] = input(
        "\nWhat application would you like me build for you?\n"
    )
    return dbs.input.get("prompt")


def preprompts_path(use_custom_preprompts: bool, input_path: Path = None) -> Path:
    original_preprompts_path = Path(__file__).parent.parent / "preprompts"
    if not use_custom_preprompts:
        return original_preprompts_path

    custom_preprompts_path = input_path / "preprompts"
    if not custom_preprompts_path.exists():
        custom_preprompts_path.mkdir()

    for file in original_preprompts_path.glob("*"):
        if not (custom_preprompts_path / file.name).exists():
            (custom_preprompts_path / file.name).write_text(file.read_text())
    return custom_preprompts_path


@app.command()
def main(
    project_path: str = typer.Argument("projects/example", help="path"),
    model: str = typer.Argument("palm", help="model id string"),
    temperature: float = 0.1,
    steps_config: StepsConfig = typer.Option(
        StepsConfig.DEFAULT, "--steps", "-s", help="decide which steps to run"
    ),
    improve_mode: bool = typer.Option(
        False,
        "--improve",
        "-i",
        help="Improve code from existing project.",
    ),
    vector_improve_mode: bool = typer.Option(
        False,
        "--vector-improve",
        "-vi",
        help="Improve code from existing project using vector store.",
    ),
    lite_mode: bool = typer.Option(
        False,
        "--lite",
        "-l",
        help="Lite mode - run only the main prompt.",
    ),
    azure_endpoint: str = typer.Option(
        "",
        "--azure",
        "-a",
        help="""Endpoint for your Azure OpenAI Service (https://xx.openai.azure.com).
            In that case, the given model is the deployment name chosen in the Azure AI Studio.""",
    ),
    use_custom_preprompts: bool = typer.Option(
        False,
        "--use-custom-preprompts",
        help="""Use your project's custom preprompts instead of the default ones.
          Copies all original preprompts to the project's workspace if they don't exist there.""",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    if lite_mode:
        assert not improve_mode, "Lite mode cannot improve code"
        if steps_config == StepsConfig.DEFAULT:
            steps_config = StepsConfig.LITE

    if improve_mode:
        assert (
            steps_config == StepsConfig.DEFAULT
        ), "Improve mode not compatible with other step configs"
        steps_config = StepsConfig.IMPROVE_CODE

    if vector_improve_mode:
        assert (
            steps_config == StepsConfig.DEFAULT
        ), "Vector improve mode not compatible with other step configs"
        steps_config = StepsConfig.VECTOR_IMPROVE

    load_env_if_needed()

    ai = AI(
        model_name=model,
        temperature=temperature,
        azure_endpoint=azure_endpoint,
    )

    project_path = os.path.abspath(
        project_path
    )  # resolve the string to a valid path (eg "a/b/../c" to "a/c")
    path = Path(project_path).absolute()
    print("Running instabuildhub in", path, "\n")

    # testing the path size

    # print("Project Path Length:", len(project_path))
    # print("Workspace Path Length:", len(workspace_path))
    # print("Input Path Length:", len(input_path))
    # print("Memory Path Length:", len(memory_path))
    # print("Archive Path Length:", len(archive_path))
    # print("Project Metadata Path Length:", len(project_metadata_path))

    workspace_path = path
    input_path = path

    project_metadata_path = path / ".insteng"
    memory_path = project_metadata_path / "memory"
    archive_path = project_metadata_path / "archive"

    fileRepositories = FileRepositories(
        memory=FileRepository(memory_path),
        logs=FileRepository(memory_path / "logs"),
        input=FileRepository(input_path),
        workspace=FileRepository(workspace_path),
        preprompts=FileRepository(preprompts_path(use_custom_preprompts, input_path)),
        archive=FileRepository(archive_path),
        project_metadata=FileRepository(project_metadata_path),
    )

    codeVectorRepository = CodeVectorRepository()

    if steps_config not in [
        StepsConfig.EXECUTE_ONLY,
        StepsConfig.USE_FEEDBACK,
        StepsConfig.EVALUATE,
        StepsConfig.IMPROVE_CODE,
        StepsConfig.VECTOR_IMPROVE,
        StepsConfig.SELF_HEAL,
    ]:
        # archive(fileRepositories)
        load_prompt(fileRepositories)

    steps = STEPS[steps_config]
    for step in steps:
        messages = step(ai, fileRepositories)
        fileRepositories.logs[step.__name__] = AI.serialize_messages(messages)

    # print("Total api cost: $ ", ai.token_usage_log.usage_cost())

    if check_collection_consent():
        collect_learnings(model, temperature, steps, fileRepositories)

    fileRepositories.logs["token_usage"] = ai.token_usage_log.format_log()

if __name__ == "__main__":
    app()
    # main()

