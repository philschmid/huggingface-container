from __future__ import annotations
from dataclasses import dataclass, field
import jinja2
import yaml
from pathlib import Path
import shutil

DOCKER_REPOSITORY = "huggingface"


@dataclass
class ContainerTemplate:
    template_path: str
    base_image: str
    env_variables: list = field(default_factory=lambda: [])
    conda_channels: list = field(default_factory=lambda: [])
    conda_dependencies: list = field(default_factory=lambda: [])
    pip_dependencies: list = field(default_factory=lambda: [])

    def __post_init__(self):
        self.jinja = jinja2.Template(Path(self.template_path).read_text(encoding="utf-8"), keep_trailing_newline=True)
        self.content = self.jinja.render(
            base_image=self.base_image,
            env_vars={item["key"]: item["value"] for item in self.env_variables},
            pip_dependencies=self.pip_dependencies,
        )


@dataclass
class ContainerImage:
    id: str
    base_target_path: Path
    template: ContainerTemplate
    extra_tags: list = field(default_factory=lambda: [])
    deprecated: bool = False

    def __post_init__(self):
        self.tags = self.extra_tags + [self.id]
        self.target_path = self.base_target_path.joinpath(*self.id.split("-"))
        self.target_path.mkdir(parents=True, exist_ok=True)
        print(self.target_path)


def make_markdown_table(array):
    """the same input as above"""

    nl = "\n"

    markdown = nl
    markdown += f"| {' | '.join(array[0])} |"

    markdown += nl
    markdown += f"| {' | '.join(['---']*len(array[0]))} |"

    markdown += nl
    for entry in array[1:]:
        markdown += f"| {' | '.join(entry)} |{nl}"

    return markdown


def main():
    # Directory for GitHub Actions workflow configuration files.
    workflow_dir = Path(".github", "workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)

    # Delete existing build-and-push workflows.
    for old_workflow_path in workflow_dir.glob("*.yml"):
        old_workflow_path.unlink()

    # Template file for Docker build and push workflows.
    workflow_template_path = Path("templates").joinpath("github_action.yaml")
    workflow_template = jinja2.Template(workflow_template_path.read_text(encoding="utf-8"), keep_trailing_newline=True)

    # Read container image buildspecs.
    image_table = [["ID", "Framework", "Type", "Tags", "Dockerfile", "URI", "Deprecated"]]
    for buildpsec in Path("buildspec").glob("**/buildspec.yaml"):
        # creates path-to-build from buildspec/path/to/build
        updated_path_to_buildspec = Path(*buildpsec.parts[1:-1])
        container_repository = str(updated_path_to_buildspec).replace("/", "-")
        base_target_path = Path("containers").joinpath(updated_path_to_buildspec)

        # delete old container files
        shutil.rmtree(updated_path_to_buildspec, ignore_errors=True)

        yaml_file = yaml.safe_load(buildpsec.read_text(encoding="utf-8"))
        if not yaml_file:
            continue
        images = [
            ContainerImage(
                id=id,
                base_target_path=base_target_path,
                template=ContainerTemplate(**image["template"]),
                deprecated=image.get("deprecated", False),
                extra_tags=image.get("extra_tags", []),
            )
            for id, image in yaml_file.items()
        ]

        for image in images:
            if image.deprecated:
                continue

            # write dockerfile
            image.target_path.joinpath("Dockerfile").write_text(image.template.content)
            # write conda environment.yaml file
            if image.template.conda_channels:
                conda_env = {
                    "name": "base",
                    "channels": image.template.conda_channels,
                    "dependencies": image.template.conda_dependencies,
                }
                image.target_path.joinpath("environment.yaml").write_text(yaml.safe_dump(conda_env, sort_keys=False))

            # write GitHub Actions workflow file
            workflow_path = workflow_dir.joinpath(f'{"-".join(image.target_path.parts[1:])}.yml')
            workflow_content = workflow_template.render(
                image_id=f"{DOCKER_REPOSITORY}/{container_repository}:{image.id}",
                image=f"{DOCKER_REPOSITORY}/{container_repository}",
                tags=[f"{DOCKER_REPOSITORY}/{container_repository}:{tag}" for tag in image.tags],
                dockerfile_dir=str(image.target_path),
                workflow_file=str(workflow_path),
            )
            workflow_path.write_text(workflow_content, encoding="utf-8")

            # add image to table
            image_table.append(
                [
                    image.id,
                    container_repository.split("-")[0],
                    container_repository.split("-")[1],
                    ";".join(image.tags),
                    f"[dockerfile]({str(image.target_path.joinpath('Dockerfile'))})",
                    f"{DOCKER_REPOSITORY}/{container_repository}:{image.id}",
                    str(image.deprecated),
                ]
            )
        with open("available_images.md", "w") as f:
            f.write("# Available images\n")
            f.write(make_markdown_table(image_table))


if __name__ == "__main__":
    main()
