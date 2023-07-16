import configparser
import subprocess
import time
import datetime

import logging
import click

logging.basicConfig(level=logging.INFO)


def validate_tags(ctx, param, value):
    if not value.startswith('@'):
        raise click.BadParameter("Tags should not start with '@'")
    return value


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
@click.option('--parallel-scheme', '-ps', 'parallel_scheme', type=click.Choice(['feature', 'scenario']),
              default='scenario',
              help='specify the stage to run')
@click.option('--stage', '-sg', 'stage_name', type=click.Choice(['QA', 'SIT', 'UAT', 'PROD']), default='QA',
              help='specify the stage to run')
@click.option('--platform', '-pl', 'platform_name', type=click.Choice(['WEB', 'ANDROID', 'iOS', 'API']), default='WEB',
              help='specify platform to run')
def run(feature_dir, forks, tags, stage_name, platform_name, parallel_scheme):
    params = []
    if feature_dir:
        params.append(f"-ip {feature_dir}")
    if tags:
        params.append(f"-t {tags}")
    if forks:
        params.append(f'--parallel-processes {forks}')
    if parallel_scheme:
        params.append(f'--parallel-scheme {parallel_scheme}')

    args = {
        "params": ' '.join(params)
    }

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
    #   run("features", 2, "@test-2", 'QA', 'WEB')
    main()
