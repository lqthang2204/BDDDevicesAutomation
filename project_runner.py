import configparser
import datetime
import logging
import os
import subprocess
import time
from glob import glob
from pathlib import Path

import click

logging.basicConfig(level=logging.INFO)


def validate_tags(ctx, param, value):
    if not value.startswith('@'):
        raise click.BadParameter(f"Tags {value} should start with '@'")
    return value


def split(features_dir, result_dir, tags):
    Path(result_dir).mkdir(parents=True, exist_ok=True)
    for f in os.listdir(result_dir):
        os.remove(os.path.join(result_dir, f))

    required_tags = tags.replace(' ', '').split(',')

    total_features = 0
    total_scenarios = 0

    feature_files = [os.path.normpath(feature_path) for feature_path in glob(features_dir + '/*.feature')]

    for feature_file in feature_files:
        with open(feature_file, 'r') as f:
            feature_content = f.read().strip()
        if not any(tag in feature_content for tag in required_tags):
            continue

        filename_head = f"{result_dir}/par_{os.path.splitext(os.path.basename(feature_file))[0]}_"
        feature_blocks = feature_content.split('\n\n')

        feature_header = feature_blocks[0] + '\n\n\n'
        feature_tags = set(feature_header.split('\n')[0].strip().split())
        all_cases = [case.strip() for case in feature_blocks[1:]]
        feature_cases = [case for case in all_cases if not case.startswith('#  Scenario') or case.startswith('#  @')]
        sequence_cases = []

        sequence_cases.append(feature_header)
        found_cases = 0
        for case in feature_cases:
            if case.strip().startswith('@'):
                case_as_list = case.split('\n')
                case_tags = set(case_as_list[0].strip().split())
                buffer_tags = case_as_list[0].strip()
                buffer_case = '\n'.join(case_as_list[1:])
            else:
                case_tags = set()
                buffer_tags = ''
                buffer_case = case
            if any((feature_tags.intersection(required_tags), case_tags.intersection(required_tags))):
                sequence_cases.append(buffer_tags + ' @final\n')
                sequence_cases.append(buffer_case + ' \n\n')
                found_cases += 1

        if found_cases > 0:
            total_features += 1
            total_scenarios += found_cases
            with open(f"{filename_head}.feature", 'w', encoding='utf-8') as result:
                result.writelines(sequence_cases)

    logging.info(f'{total_scenarios} Scenarios found in {total_features} Features files')


@click.group()
@click.pass_context
def main(context):
    print(context)
    pass


@main.command(short_help='run test scenarios ')
@click.option('--feature-dir', '-fd', 'feature_dir', type=str, default='features', show_default=True,
              help='feature directory')
@click.option('--tags', '-tg', callback=validate_tags, default='@web', help='specify behave tags to run')
@click.option('--forks', '-fk', type=click.IntRange(1, 10), default=5, show_default=True,
              help='number of processes')
@click.option('--stage', '-sg', 'stage_name', type=click.Choice(['QA', 'SIT', 'UAT', 'PROD']), default='QA',
              help='specify the stage to run')
@click.option('--platform', '-pl', 'platform_name', type=click.Choice(['WEB', 'ANDROID', 'iOS', 'API']), default='WEB',
              help='specify platform to run')
@click.option('--parallel-scheme', '-ps', 'parallel_scheme', type=click.Choice(['feature', 'scenario']),
              default='scenario',
              help='specify the stage to run')
def run(feature_dir, tags, forks, stage_name, platform_name, parallel_scheme):
    params = []
    if feature_dir:
        params.append(f"-ip 'features/final'")
    if tags:
        params.append(f"-t {tags}")
    if forks:
        params.append(f'--parallel-processes {forks}')
    if parallel_scheme:
        params.append(f'--parallel-scheme {parallel_scheme}')

    args = {
        "params": ' '.join(params)
    }

    split(feature_dir, 'features/final', tags)
    _run_feature(args, stage_name, platform_name)


def config_from_command_line(stage_name, platform_name):
    config = configparser.ConfigParser()
    config.read('config_env.ini')

    # Modify the 'platform' value in the [drivers_config] section
    config.set('drivers_config', 'platform', platform_name)
    config.set('drivers_config', 'stage', stage_name)

    # Save the changes to the config.ini file
    with open('config_env.ini', 'w') as config_file:
        config.write(config_file)
    logging.info('Config file updated based on user provided command line arguments')


def _run_feature(args, stage_name, platform_name):
    config_from_command_line(stage_name, platform_name)
    cmd = f"behavex {args['params']}"
    logging.info(f'Command prepared: {cmd}')
    # Get the start time
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
            logging.error('Executing the behaveX command failed')
            exit(1)
    except subprocess.CalledProcessError as e:
        logging.error('Executing the behaveX command failed')
        exit(1)

    logging.info(f'Total time taken: {duration_seconds:.2f} seconds ({duration_minutes:.2f} minutes)')


if __name__ == '__main__':
    # To DEBUG use:
    # run("features", 2, "@test-2", 'QA', 'WEB')
    main()
    # split('features', 'features/final', "@web")
