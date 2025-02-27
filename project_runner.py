import configparser
import datetime
import subprocess
import time

import click
from bdd_tags_processor.bdd_tags_expression_processor import filter_feature_and_scenarios

from libraries.logger_core import start_logger_facility
from package_installer import ensure_package_versions

logger, project_folder = start_logger_facility()


@click.group()
@click.pass_context
def main(context):
    pass


@main.command(short_help='run test scenarios ')
@click.option('--feature-dir', '-fd', 'feature_dir', type=str, default='features', show_default=True,
              help='feature directory. Default value is the folder named features')
@click.option('--tags', '-tg', default='{~@norun}', help='specify behave tags to run. Default value ~@norun signifies All')
@click.option('--forks', '-fk', type=click.IntRange(1, 10), default=1, show_default=True,
              help='number of processes. Default value is 1')
@click.option('--stage', '-sg', 'stage_name', type=click.Choice(['QA', 'SIT', 'UAT', 'PROD']), default='QA',
              help='specify the stage to run. Default value is QA')
@click.option('--platform', '-pl', 'platform_name', type=click.Choice(['API', 'WEB', 'ANDROID', 'IOS']), default='WEB',
              help='specify platform to run. Default value is WEB')
@click.option('--parallel-scheme', '-ps', 'parallel_scheme', type=click.Choice(['feature', 'scenario']),
              default='scenario', help='specify the stage to run. Default value is scenario')
@click.option('--remote', '-rm', 'is_remote', type=click.Choice(['true', 'false']),
              default='false', help='specify the remote with cross browser')
@click.option('--is_highlight', '-hl', 'is_highlight', type=click.Choice(['true', 'false']),
              default='false', help='specify the highlight for elements')
@click.option('--browser', '-br', 'browser', type=click.Choice(['chrome', 'safari', 'firefox']), default='chrome',
              help='specify browser to run. Default value is chrome')
def run(feature_dir, tags, forks, stage_name, platform_name, parallel_scheme, is_remote, is_highlight, browser):

    # ensure all the packages are installed
    ensure_package_versions()

    total_scenarios = filter_feature_and_scenarios(feature_dir, 'features/final', tags)
    params = []

    if tags:
        params.append('-t @final')
    if forks:
        params.append(f'--parallel-processes {forks}')
    if parallel_scheme:
        params.append(f'--parallel-scheme {parallel_scheme}')

    args = {
        "params": ' '.join(params)
    }

    if total_scenarios > 0:
        _run_feature(args, stage_name, platform_name, is_remote, is_highlight, browser)


def config_from_command_line(stage_name, platform_name, is_remote, is_highlight, browser):
    config = configparser.ConfigParser()
    print(stage_name, platform_name, is_remote, is_highlight, browser)
    config.read('config_env.ini')

    config.set('project_folder', 'project_folder', project_folder)
    config.set('drivers_config', 'stage', stage_name)
    config.set('drivers_config', 'platform', platform_name)
    config.set('drivers_config', 'remote-saucelabs', is_remote)
    config.set('drivers_config', 'is_highlight', is_highlight)
    config.set('drivers_config', 'browser', browser)


    # Save the changes to the config.ini file
    with open('config_env.ini', 'w') as config_file:
        config.write(config_file)
    logger.info('Config file updated based on user provided command line arguments')


def _run_feature(args, stage_name, platform_name, is_remote, is_highlight, browser):
    config_from_command_line(stage_name, platform_name, is_remote, is_highlight, browser)
    cmd = f"behavex {args['params']}"
    logger.info(f'Command prepared: {cmd}')
    # Get the start time in seconds since the epoch
    start_time = datetime.datetime.now().timestamp()
    start_time_str = datetime.datetime.now().strftime('%I:%M:%S %p')  # Format the start time as HH:MM:SS AM/PM
    logger.info(f'Start time: {start_time_str}')

    try:
        completed_process = subprocess.run(cmd, shell=True)
        # Calculate the total time taken
        end_time = datetime.datetime.now()
        duration = end_time.timestamp() - start_time
        duration_seconds = duration
        duration_minutes = duration / 60

        logger.info(f'Execution completed at: {end_time.strftime("%I:%M:%S %p")}')
        duration_time = int(time.time() - start_time)
        status = 'ok' if completed_process.returncode == 0 else 'failed'

        if status == 'failed':
            logger.error('There are FAILED Scenarios that need investigation')
            exit(1)
    except subprocess.CalledProcessError as e:
        logger.error('Executing the behaveX command failed')
        exit(1)

    logger.info(f'Total time taken: {duration_seconds:.2f} seconds ({duration_minutes:.2f} minutes)')


if __name__ == '__main__':
    # To DEBUG do the following:
    # 1. disable the @click definition mentioned above main() and run()
    # 2. disable main() below
    # 3. enabled the statement below
    # run("features/scenarios/web", "{~@norun and @function-read-javascript-2}", 1, 'QA', 'WEB','scenario', 'false', 'true', 'chrome')
    # run("features/scenarios/iPhone", "{~@norun and (@scroll_element_ios)}", 2, 'QA', 'IOS', 'scenario', 'true')
    main()