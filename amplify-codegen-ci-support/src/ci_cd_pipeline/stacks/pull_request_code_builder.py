from aws_cdk import core
from aws_cdk.aws_codebuild import (
    BuildEnvironment,
    BuildSpec,
    ComputeType,
    EventAction,
    FilterGroup,
    LinuxBuildImage,
    Project,
    Source,
    GitHubSourceCredentials
)


class PullRequestCodeBuilder(Project):
    BUILD_IMAGE = LinuxBuildImage.AMAZON_LINUX_2_3

    def __init__(self,
                 scope: core.Construct,
                 id: str, *,
                 project_name: str,
                 github_owner,
                 github_repo,
                 buildspec_path,
                 environment_variables={},
                 base_branch: str = "master"):
        build_environment = BuildEnvironment(build_image=self.BUILD_IMAGE,
                                             privileged=True,
                                             compute_type=ComputeType.LARGE)

        trigger_on_pr = FilterGroup.in_event_of(EventAction.PULL_REQUEST_CREATED,
                                                EventAction.PULL_REQUEST_UPDATED,
                                                EventAction.PULL_REQUEST_MERGED,
                                                EventAction.PUSH,
                                                EventAction.PULL_REQUEST_REOPENED)

        pr_codebuild_project = super().__init__(scope,
                                                id,
                                                project_name=project_name,
                                                environment_variables=environment_variables,
                                                build_spec=BuildSpec.from_source_filename(buildspec_path),
                                                badge=True,
                                                source=Source.git_hub(owner=github_owner,
                                                                      report_build_status=True,
                                                                      repo=github_repo,
                                                                      webhook=True,
                                                                      webhook_filters=[trigger_on_pr]),
                                                environment=build_environment)
