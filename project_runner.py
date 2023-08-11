import configparser
import datetime
import logging
import subprocess
import time

import click
from bdd_tags_processor.bdd_tags_expression_processor import filter_feature_and_scenarios

from package_installer import ensure_package_versions

logging.basicConfig(level=logging.INFO)
import os


@click.group()
@click.pass_context
def main(context):
    pass


@main.command(short_help='run test scenarios ')
@click.option('--feature-dir', '-fd', 'feature_dir', type=str, default='features', show_default=True,
              help='feature directory. Default value is the folder named features')
@click.option('--tags', '-tg', default='{~@norun}', help='specify behave tags to run. Default value ~@norun signifies All')
@click.option('--forks', '-fk', type=click.IntRange(1, 10), default=5, show_default=True,
              help='number of processes. Default value is 5')
@click.option('--stage', '-sg', 'stage_name', type=click.Choice(['QA', 'SIT', 'UAT', 'PROD']), default='QA',
              help='specify the stage to run. Default value is QA')
@click.option('--parallel-scheme', '-ps', 'parallel_scheme', type=click.Choice(['feature', 'scenario']),
              default='scenario', help='specify the stage to run. Default value is scenario')
def run(feature_dir, tags, forks, stage_name, parallel_scheme):
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
        _run_feature(args, stage_name)


def config_from_command_line(stage_name):
    project_folder = os.path.dirname(os.path.abspath(__file__))

    config = configparser.ConfigParser()
    config.read('config_env.ini')

    config.set('project_folder', 'project_folder', project_folder)
    config.set('drivers_config', 'stage', stage_name)

    # Save the changes to the config.ini file
    with open('config_env.ini', 'w') as config_file:
        config.write(config_file)
    logging.info('Config file updated based on user provided command line arguments')


def _run_feature(args, stage_name):
    config_from_command_line(stage_name)
    cmd = f"behavex {args['params']}"
    logging.info(f'Command prepared: {cmd}')
    # Get the start time in seconds since the epoch
    start_time = datetime.datetime.now().timestamp()
    start_time_str = datetime.datetime.now().strftime('%I:%M:%S %p')  # Format the start time as HH:MM:SS AM/PM
    logging.info(f'Start time: {start_time_str}')

    try:
        completed_process = subprocess.run(cmd, shell=True)
        # Calculate the total time taken
        end_time = datetime.datetime.now()
        duration = end_time.timestamp() - start_time
        duration_seconds = duration
        duration_minutes = duration / 60

        logging.info(f'Execution completed at: {end_time.strftime("%I:%M:%S %p")}')
        duration_time = int(time.time() - start_time)
        status = 'ok' if completed_process.returncode == 0 else 'failed'

        if status == 'failed':
            logging.error('There are FAILED Scenarios that need investigation')
            exit(1)
    except subprocess.CalledProcessError as e:
        logging.error('Executing the behaveX command failed')
        exit(1)

    logging.info(f'Total time taken: {duration_seconds:.2f} seconds ({duration_minutes:.2f} minutes)')


if __name__ == '__main__':
    # To DEBUG do the following:
    # 1. disable the @click definition mentioned above main() and run()
    # 2. disable main() below
    # 3. enabled the statement below
    # run("features/orangeHRM*.feature", "{~@norun and (@test1 or @test2)}", 2, 'QA',  'scenario')
    main()
